"""Check an agent's U2 output against the success criteria.

Usage:  python check_u2.py <folder>

The folder must hold the agent's saved scene.usda and overrides.usda, plus the
table.usda and chair.usda that make_u2_assets.py created. Run it in the rerun
folder's virtual environment (it needs usd-core). It reads the saved files,
and the agent's task.py if it's there; it does not run the agent's script.
Rerun the agent's task.py yourself first, from a clean folder, and save its
output. C7, the explanation, is scored by reading the agent's answer; this
script doesn't check it.

ISSUE lines flag things in task.py for the reviewer to read and confirm:
a hardcoded absolute path, or no API call that could list the opinions
(so the printed layer list may be typed by hand). They don't fail a check.
"""
import ast
import sys
from pathlib import Path

from pxr import Pcp, Sdf, Usd, UsdGeom

from make_u2_assets import ASSETS

TOL = 1e-6
BLUE, RED, GREEN = (0, 0, 1), (1, 0, 0), (0, 1, 0)


def close(a, b):
    return all(abs(x - y) <= TOL for x, y in zip(a, b))


def color_of(prim):
    value = UsdGeom.Gprim(prim).GetDisplayColorAttr().Get()
    return tuple(value[0]) if value is not None and len(value) else None


# Calls that can tell a script which layers hold an opinion.
OPINION_APIS = ("GetPropertyStack", "GetPrimStack", "PrimCompositionQuery", "GetResolveInfo",
                "GetLayerStack", "GetUsedLayers", "GetPrimIndex", "GetAttributeAtPath",
                "GetPropertyAtPath")


def source_issues(script):
    """Read the agent's task.py for things the saved files can't show."""
    if not script.exists():
        return [], [f"{script.name} not found; source checks skipped"]
    tree = ast.parse(script.read_text())
    strings = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    issues = []
    hardcoded = [s for s in strings if s.startswith(("/", "~")) and ".usd" in s]
    if hardcoded:
        issues.append(f"hardcoded absolute path(s) in task.py: {hardcoded}. They break when the "
                      "code moves; build paths at run time, for example from __file__")
    if not names & set(OPINION_APIS):
        issues.append("task.py calls nothing that lists opinions "
                      f"({', '.join(OPINION_APIS[:3])}, ...), so its printed layer list may be "
                      "typed by hand; read task.py to confirm")
    return issues, []


def main(folder):
    d = Path(folder)
    results = []  # (criterion id, passed, detail)
    notes = []

    def check(cid, ok, detail):
        results.append((cid, bool(ok), detail))

    for name in ("scene.usda", "overrides.usda"):
        p = d / name
        first = p.read_text(errors="replace").splitlines()[0] if p.exists() and p.stat().st_size else ""
        check("C1", first.startswith("#usda"), f"{name}: first line {first!r} (text .usda expected)")

    for name, text in ASSETS.items():
        p = d / name
        check("C2", p.exists() and p.read_text() == text, f"{name} unchanged from make_u2_assets.py")

    if not (d / "scene.usda").exists():
        return report(results, notes)
    stage = Usd.Stage.Open(str(d / "scene.usda"))
    check("C3", stage is not None, "scene.usda opens with Usd.Stage.Open")
    dp = stage.GetDefaultPrim()
    check("C3", dp and dp.GetPath() == "/World" and dp.GetTypeName() == "Xform",
          f"default prim: {dp.GetPath() if dp else None} ({dp.GetTypeName() if dp else None})")

    prims = {}
    for path, asset in (("/World/Table", "table.usda"), ("/World/Chair", "chair.usda")):
        prim = stage.GetPrimAtPath(path)
        prims[path] = prim
        arcs = Usd.PrimCompositionQuery(prim).GetCompositionArcs() if prim else []
        targets = [Path(a.GetTargetLayer().realPath) for a in arcs
                   if a.GetArcType() == Pcp.ArcTypeReference and a.GetTargetLayer()]
        # The reference must resolve to the asset in this folder, so a rerun can't
        # pass by pointing back at the agent's original folder.
        local = (d.resolve() / asset) in [t.resolve() for t in targets]
        check("C4", local and prim.GetTypeName() == "Cube",
              f"{path}: reference arcs to {[str(t) for t in targets] or 'none'}; "
              f"composed type {prim.GetTypeName() if prim else None} (expected {asset} in this folder)")

    root = stage.GetRootLayer()
    used = [Path(layer.realPath).resolve() for layer in stage.GetUsedLayers() if layer.realPath]
    check("C5", (d.resolve() / "overrides.usda") in used,
          f"overrides.usda composed into scene.usda: layers used by the stage: {sorted(p.name for p in used)}")

    table, chair = prims["/World/Table"], prims["/World/Chair"]
    tc = color_of(table) if table else None
    cc = color_of(chair) if chair else None
    check("C6", tc is not None and close(tc, BLUE), f"table composed color: {tc} (expected {BLUE})")
    check("C6", cc is not None and close(cc, GREEN), f"chair composed color: {cc} (expected {GREEN})")

    stack = UsdGeom.Gprim(table).GetDisplayColorAttr().GetPropertyStack(Usd.TimeCode.Default()) if table else []
    layers = [Path(s.layer.realPath).name for s in stack]
    check("C6", layers[:1] == ["overrides.usda"] and "scene.usda" not in layers,
          f"layers with an opinion on the table's color, strongest first: {layers} "
          "(expected overrides.usda first, none in scene.usda)")

    # Observations: recorded, not scored. How overrides.usda was brought in is the
    # main one: the prompt doesn't say, so this shows where the docs led the agent.
    subs = [Path(root.ComputeAbsolutePath(s)).name for s in root.subLayerPaths]
    arcs = Usd.PrimCompositionQuery(table).GetCompositionArcs() if table else []
    arc_list = [(str(a.GetArcType()).replace("Pcp.ArcType", ""), Path(a.GetTargetLayer().realPath).name)
                for a in arcs if a.GetTargetLayer()]
    if "overrides.usda" in subs:
        how = "a sublayer of scene.usda"
    elif ("Reference", "overrides.usda") in arc_list:
        how = "a reference on /World/Table"
    else:
        how = "not found as a sublayer or a reference"
    notes.append(f"overrides.usda brought in as: {how}")
    notes.append(f"composition arcs on /World/Table, strongest first: {arc_list}")
    for path in ("/World/Table", "/World/Chair"):
        spec = root.GetPrimAtPath(path)
        refs = list(spec.referenceList.GetAddedOrExplicitItems()) if spec else []
        notes.append(f"{path} references as authored: {[(r.assetPath, str(r.primPath)) for r in refs]}"
                     " (empty prim path means the asset's default prim)")
    notes.append(f"sublayer paths as authored: {list(root.subLayerPaths)}")
    notes.append(f"scene.usda upAxis authored: {stage.HasAuthoredMetadata('upAxis')}; "
                 f"metersPerUnit authored: {stage.HasAuthoredMetadata('metersPerUnit')}")
    others = [str(p.GetPath()) for p in stage.Traverse()
              if str(p.GetPath()) not in ("/World", "/World/Table", "/World/Chair")]
    notes.append(f"other prims: {others or 'none'}")
    issues, skipped = source_issues(d / "task.py")
    return report(results, notes + skipped, issues)


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
