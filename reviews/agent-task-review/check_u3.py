"""Check an agent's U3 output against the success criteria.

Usage:  python check_u3.py <folder>

The folder must hold the agent's saved scene.usda, plus the mug.usda that
make_u3_assets.py created. Run it in the rerun folder's virtual environment
(it needs usd-core). It reads the saved files, and the agent's task.py and
rerun-output.txt if they're there; it does not run the agent's script. Rerun
the agent's task.py yourself first, from a clean folder, saving its output to
rerun-output.txt. C7, the switch in code, is scored by reading task.py and
rerun-output.txt; this script only flags it.

ISSUE lines flag things for the reviewer to read and confirm: a hardcoded
absolute path in task.py, or a rerun output that doesn't show both colors.
They don't fail a check.
"""
import ast
import re
import sys
from pathlib import Path

from pxr import Pcp, Usd, UsdGeom

from make_u3_assets import ASSETS

TOL = 1e-6
RED, BLUE = (1, 0, 0), (0, 0, 1)
# A color written as (1, 0, 0), (1.0, 0.0, 0.0), [1. 0. 0.], and so on.
NUM = r"\s*{}(?:\.0*)?\s*"
COLOR_TEXT = {name: re.compile(r"[(\[]" + r"[,\s]".join(NUM.format(v) for v in rgb) + r"[)\]]")
              for name, rgb in (("red", RED), ("blue", BLUE))}


def close(a, b):
    return a is not None and all(abs(x - y) <= TOL for x, y in zip(a, b))


def color_of(prim):
    value = UsdGeom.Gprim(prim).GetDisplayColorAttr().Get()
    return tuple(value[0]) if value is not None and len(value) else None


def source_issues(folder):
    """Read the agent's task.py and output for things the saved file can't show."""
    issues, notes = [], []
    script = folder / "task.py"
    if script.exists():
        tree = ast.parse(script.read_text())
        strings = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        hardcoded = [s for s in strings if s.startswith(("/", "~")) and ".usd" in s]
        if hardcoded:
            issues.append(f"hardcoded absolute path(s) in task.py: {hardcoded}. They break when the "
                          "code moves; build paths at run time, for example from __file__")
        notes.append(f"task.py switches in the session layer: {'GetSessionLayer' in names}")
    else:
        notes.append("task.py not found; source checks skipped")
    output = folder / "rerun-output.txt"
    if output.exists():
        text = output.read_text(errors="replace")
        missing = [name for name, pattern in COLOR_TEXT.items() if not pattern.search(text)]
        if missing:
            issues.append(f"rerun-output.txt shows no {' or '.join(missing)} color; read task.py "
                          "and the output to confirm C7, the switch in code")
    else:
        notes.append("rerun-output.txt not found; output check skipped")
    return issues, notes


def main(folder):
    d = Path(folder)
    results = []  # (criterion id, passed, detail)
    notes = []

    def check(cid, ok, detail):
        results.append((cid, bool(ok), detail))

    p = d / "scene.usda"
    first = p.read_text(errors="replace").splitlines()[0] if p.exists() and p.stat().st_size else ""
    check("C1", first.startswith("#usda"), f"scene.usda: first line {first!r} (text .usda expected)")

    for name, text in ASSETS.items():
        a = d / name
        check("C2", a.exists() and a.read_text() == text, f"{name} unchanged from make_u3_assets.py")

    if not p.exists():
        return report(results, notes)
    stage = Usd.Stage.Open(str(p))
    check("C3", stage is not None, "scene.usda opens with Usd.Stage.Open")
    dp = stage.GetDefaultPrim()
    check("C3", dp and dp.GetPath() == "/World" and dp.GetTypeName() == "Xform",
          f"default prim: {dp.GetPath() if dp else None} ({dp.GetTypeName() if dp else None})")

    mug = stage.GetPrimAtPath("/World/Mug")
    arcs = Usd.PrimCompositionQuery(mug).GetCompositionArcs() if mug else []
    targets = [Path(a.GetTargetLayer().realPath) for a in arcs
               if a.GetArcType() == Pcp.ArcTypeReference and a.GetTargetLayer()]
    local = (d.resolve() / "mug.usda") in [t.resolve() for t in targets]
    check("C4", local and mug.GetTypeName() == "Cylinder",
          f"/World/Mug: reference arcs to {[str(t) for t in targets] or 'none'}; "
          f"composed type {mug.GetTypeName() if mug else None} (expected mug.usda in this folder)")

    root = stage.GetRootLayer()
    spec = root.GetPrimAtPath("/World/Mug")
    vset = mug.GetVariantSets().GetVariantSet("color") if mug else None
    names = sorted(vset.GetVariantNames()) if mug and mug.GetVariantSets().HasVariantSet("color") else []
    in_scene = bool(spec) and "color" in spec.variantSets
    check("C5", in_scene and names == ["blue", "red"],
          f"variant set 'color' authored in scene.usda: {in_scene}; variants: {names} (expected ['blue', 'red'])")
    saved = vset.GetVariantSelection() if names else None
    check("C5", saved == "blue", f"saved selection: {saved!r} (expected 'blue')")

    check("C6", close(color_of(mug) if mug else None, BLUE),
          f"composed color as saved: {color_of(mug) if mug else None} (expected {BLUE})")
    direct = root.GetAttributeAtPath("/World/Mug.primvars:displayColor")
    check("C6", direct is None, "no display color authored on /World/Mug outside the variants: "
          f"{direct is None}")
    for choice, rgb in (("red", RED), ("blue", BLUE)):
        if not names:
            check("C6", False, f"selecting {choice!r}: no 'color' variant set to select from")
            continue
        with Usd.EditContext(stage, stage.GetSessionLayer()):
            vset.SetVariantSelection(choice)
        stack = UsdGeom.Gprim(mug).GetDisplayColorAttr().GetPropertyStack(Usd.TimeCode.Default())
        strongest = stack[0].path if stack else None
        from_variant = strongest is not None and strongest.ContainsPrimVariantSelection()
        check("C6", close(color_of(mug), rgb) and from_variant,
              f"selecting {choice!r}: color {color_of(mug)} (expected {rgb}); "
              f"strongest opinion at {strongest}, from a variant: {from_variant}")
    stage.GetSessionLayer().Clear()

    # Observations: recorded, not scored.
    notes.append(f"/World/Mug references as authored: "
                 f"{[(r.assetPath, str(r.primPath)) for r in spec.referenceList.GetAddedOrExplicitItems()] if spec else []}")
    notes.append(f"scene.usda upAxis authored: {stage.HasAuthoredMetadata('upAxis')}; "
                 f"metersPerUnit authored: {stage.HasAuthoredMetadata('metersPerUnit')}")
    others = [str(q.GetPath()) for q in stage.Traverse() if str(q.GetPath()) not in ("/World", "/World/Mug")]
    notes.append(f"other prims: {others or 'none'}")
    issues, source_notes = source_issues(d)
    return report(results, notes + source_notes, issues)


def report(results, notes, issues=()):
    for cid, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {cid}  {detail}")
    for n in notes:
        print(f"NOTE  {n}")
    for i in issues:
        print(f"ISSUE {i}")
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)} of {len(results)} checks passed; {len(issues)} issue(s) to review")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
