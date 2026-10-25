"""Check an agent's U4 output against the success criteria.

Usage:  python check_u4.py <folder>

The folder must hold the agent's saved references.usda and instanced.usda,
plus the crate.usda that make_u4_assets.py created. Run it in the rerun
folder's virtual environment (it needs usd-core). It reads the saved files,
and the agent's task.py if it's there; it does not run the agent's script.
Rerun the agent's task.py yourself first, from a clean folder, and save its
output. C7, the printed comparison, and C8, the explanation, are scored by
reading the agent's output and answer; NOTE lines give the checker's own
counts to compare with.

Either kind of instancing passes C5: scenegraph instancing (instanceable
prims sharing a prototype) or point instancing (a PointInstancer). A NOTE
says which one the agent used.

ISSUE lines flag things in task.py for the reviewer to read and confirm:
a hardcoded absolute path, or no call that could count prims or prototypes
(so the printed counts may be typed by hand). They don't fail a check.
"""
import ast
import sys
import time
from pathlib import Path

from pxr import Gf, Pcp, Usd, UsdGeom

from make_u4_assets import ASSETS

COUNT, COLUMNS, SPACING = 1000, 40, 2.0
EXPECTED = {(SPACING * (i % COLUMNS), SPACING * (i // COLUMNS), 0.0) for i in range(COUNT)}
BOUNDS = ((-0.5, -0.5, 0.0), (78.5, 48.5, 1.0))
TOL = 1e-4

# Calls that can count prims or prototypes.
COUNT_APIS = ("Traverse", "TraverseAll", "PrimRange", "GetPrototypes", "GetAllDescendants",
              "GetChildren", "GetDescendants")


def key(v):
    return tuple(round(float(x) / TOL) * TOL for x in v)


def references_crate(prim, folder):
    arcs = Usd.PrimCompositionQuery(prim).GetCompositionArcs()
    return any(a.GetArcType() == Pcp.ArcTypeReference and a.GetTargetLayer()
               and Path(a.GetTargetLayer().realPath).resolve() == folder.resolve() / "crate.usda"
               for a in arcs)


def crates(stage, folder):
    """Prims that reference crate.usda, outside any PointInstancer's prototypes."""
    found = []
    it = iter(Usd.PrimRange(stage.GetPseudoRoot()))
    for prim in it:
        if prim.IsA(UsdGeom.PointInstancer):
            it.PruneChildren()
        elif references_crate(prim, folder):
            found.append(prim)
            it.PruneChildren()
    return found


def positions(prims):
    cache = UsdGeom.XformCache()
    return {key(cache.GetLocalToWorldTransform(p).ExtractTranslation()) for p in prims}


def bounds_ok(stage):
    world = stage.GetPrimAtPath("/World")
    if not world:
        return False, None
    rng = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_]).ComputeWorldBound(
        world).ComputeAlignedRange()
    ok = key(rng.GetMin()) == key(BOUNDS[0]) and key(rng.GetMax()) == key(BOUNDS[1])
    return ok, rng


def point_instancing(stage, folder):
    """(ok, detail) for a PointInstancer that places the 1,000 crates."""
    instancers = [UsdGeom.PointInstancer(p) for p in stage.Traverse() if p.IsA(UsdGeom.PointInstancer)]
    if len(instancers) != 1:
        return False, f"{len(instancers)} PointInstancer(s)"
    pi = instancers[0]
    targets = [stage.GetPrimAtPath(t) for t in pi.GetPrototypesRel().GetTargets()]
    protos_ok = bool(targets) and all(t and references_crate(t, folder) for t in targets)
    xforms = pi.ComputeInstanceTransformsAtTime(Usd.TimeCode.Default(), Usd.TimeCode.Default())
    world = UsdGeom.XformCache().GetLocalToWorldTransform(pi.GetPrim())
    placed = {key((m * world).ExtractTranslation()) for m in xforms}
    ok = protos_ok and len(xforms) == COUNT and placed == {key(e) for e in EXPECTED}
    return ok, (f"PointInstancer {pi.GetPath()}: {len(xforms)} instances, positions match: "
                f"{placed == {key(e) for e in EXPECTED}}, prototypes reference crate.usda: {protos_ok}")


def source_issues(script):
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
    if not names & set(COUNT_APIS):
        issues.append(f"task.py calls nothing that counts prims or prototypes ({', '.join(COUNT_APIS[:4])}, ...), "
                      "so its printed counts may be typed by hand; read task.py to confirm")
    return issues, []


def main(folder):
    d = Path(folder)
    results = []  # (criterion id, passed, detail)
    notes = []

    def check(cid, ok, detail):
        results.append((cid, bool(ok), detail))

    for name in ("references.usda", "instanced.usda"):
        p = d / name
        first = p.read_text(errors="replace").splitlines()[0] if p.exists() and p.stat().st_size else ""
        check("C1", first.startswith("#usda"), f"{name}: first line {first!r} (text .usda expected)")

    for name, text in ASSETS.items():
        a = d / name
        check("C2", a.exists() and a.read_text() == text, f"{name} unchanged from make_u4_assets.py")

    stages = {}
    for name in ("references.usda", "instanced.usda"):
        if not (d / name).exists():
            continue
        start = time.perf_counter()
        stage = Usd.Stage.Open(str(d / name))
        notes.append(f"{name}: opened in {(time.perf_counter() - start) * 1000:.1f} ms by the checker; "
                     f"{sum(1 for _ in stage.Traverse())} prims traversed "
                     f"({sum(1 for _ in stage.Traverse(Usd.TraverseInstanceProxies()))} counting instance proxies); "
                     f"{len(stage.GetPrototypes())} prototype(s)")
        stages[name] = stage
        dp = stage.GetDefaultPrim()
        check("C3", dp and dp.GetPath() == "/World" and dp.GetTypeName() == "Xform",
              f"{name}: default prim {dp.GetPath() if dp else None} ({dp.GetTypeName() if dp else None})")
    if len(stages) < 2:
        return report(results, notes)

    refs = stages["references.usda"]
    plain = crates(refs, d)
    instancers = [p for p in refs.Traverse() if p.IsA(UsdGeom.PointInstancer)]
    check("C4", len(plain) == COUNT and not any(p.IsInstanceable() for p in plain) and not instancers,
          f"references.usda: {len(plain)} prims reference crate.usda in this folder (expected {COUNT}); "
          f"instanceable: {sum(p.IsInstanceable() for p in plain)}; PointInstancers: {len(instancers)}")
    check("C4", positions(plain) == {key(e) for e in EXPECTED},
          "references.usda: crate positions match x = 2 * (i mod 40), y = 2 * (i div 40), z = 0")

    inst = stages["instanced.usda"]
    shared = crates(inst, d)
    scenegraph_ok = (len(shared) == COUNT and all(p.IsInstance() for p in shared)
                     and len(inst.GetPrototypes()) == 1 and positions(shared) == {key(e) for e in EXPECTED})
    point_ok, point_detail = point_instancing(inst, d)
    kind = "scenegraph instancing" if scenegraph_ok else "point instancing" if point_ok else "none found"
    check("C5", scenegraph_ok or point_ok,
          f"instanced.usda shares one copy of the crate: {kind}. Scenegraph: {len(shared)} referencing prims, "
          f"{sum(p.IsInstance() for p in shared)} instances, {len(inst.GetPrototypes())} prototype(s). "
          f"Point: {point_detail}")
    notes.append(f"instancing used in instanced.usda: {kind}")

    for name, stage in stages.items():
        ok, rng = bounds_ok(stage)
        check("C6", ok, f"{name}: world bounds {rng} (expected {BOUNDS[0]} to {BOUNDS[1]})")

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
