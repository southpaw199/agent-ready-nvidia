"""Check an agent's U1 output against the success criteria.

Usage:  python check_u1.py <path-to-scene.usda>

Run it in the rerun folder's virtual environment (it needs usd-core). It
reads the saved file only; it does not run the agent's script. Rerun the
agent's task.py yourself first, from a clean folder, and save its output.
"""
import sys
from pathlib import Path

from pxr import Gf, Usd, UsdGeom

TOL = 1e-6


def close(a, b):
    return all(abs(x - y) <= TOL for x, y in zip(a, b))


def main(path):
    p = Path(path)
    results = []  # (criterion id, passed, detail)

    def check(cid, ok, detail):
        results.append((cid, bool(ok), detail))

    check("C1", p.exists() and p.suffix == ".usda", f"file: {p}")
    if not p.exists():
        return report(results, [])
    first = p.read_text(errors="replace").splitlines()[0] if p.stat().st_size else ""
    check("C1", first.startswith("#usda"), f"first line: {first!r} (text .usda expected)")

    stage = Usd.Stage.Open(str(p))
    check("C2", stage is not None, "opens with Usd.Stage.Open")

    up = UsdGeom.GetStageUpAxis(stage)
    mpu = UsdGeom.GetStageMetersPerUnit(stage)
    check("C3", up == "Z" and stage.HasAuthoredMetadata("upAxis"), f"upAxis authored: {stage.HasAuthoredMetadata('upAxis')}, value: {up}")
    check("C3", abs(mpu - 1.0) <= TOL and stage.HasAuthoredMetadata("metersPerUnit"),
          f"metersPerUnit authored: {stage.HasAuthoredMetadata('metersPerUnit')}, value: {mpu}")

    dp = stage.GetDefaultPrim()
    check("C4", dp and dp.GetPath() == "/World", f"defaultPrim: {dp.GetPath() if dp else None}")
    world = stage.GetPrimAtPath("/World")
    check("C4", world and world.GetTypeName() == "Xform", f"/World type: {world.GetTypeName() if world else None}")

    box = stage.GetPrimAtPath("/World/Box")
    check("C5", box and box.GetTypeName() == "Cube", f"/World/Box type: {box.GetTypeName() if box else None}")
    if not (box and box.GetTypeName() == "Cube"):
        return report(results, [])
    cube = UsdGeom.Cube(box)
    size = cube.GetSizeAttr().Get()
    check("C5", abs(size - 4.0) <= TOL, f"size: {size}")
    color = cube.GetDisplayColorAttr().Get()
    check("C5", color is not None and len(color) >= 1 and close(color[0], (1, 0, 0)),
          f"displayColor: {list(color) if color is not None else None}")

    bbox = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
    rng = bbox.ComputeWorldBound(box).ComputeAlignedRange()
    check("C6", close(rng.GetMin(), (-2, -2, 0)) and close(rng.GetMax(), (2, 2, 4)),
          f"world bound: min {rng.GetMin()}, max {rng.GetMax()} (expected (-2,-2,0) to (2,2,4))")

    # Observations: recorded, not scored.
    notes = []
    ext_auth = cube.GetExtentAttr().HasAuthoredValue()
    ext = cube.GetExtentAttr().Get()
    notes.append(f"extent authored: {ext_auth}; extent attribute returns {list(ext) if ext is not None else None}"
                 + ("" if ext_auth else "  <-- stale fallback: tools that read extent directly see a 2 m cube"))
    notes.append(f"xformOpOrder: {list(UsdGeom.Xformable(box).GetXformOpOrderAttr().Get() or [])}")
    others = [str(pr.GetPath()) for pr in stage.Traverse() if str(pr.GetPath()) not in ("/World", "/World/Box")]
    notes.append(f"other prims: {others or 'none'}")
    return report(results, notes)


def report(results, notes):
    for cid, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {cid}  {detail}")
    for n in notes:
        print(f"NOTE  {n}")
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)} of {len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
