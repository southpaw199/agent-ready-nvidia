"""Build 1,000 crates two ways (plain references vs. scenegraph instancing) and compare them."""
import statistics
import time
from pathlib import Path

from pxr import Gf, Sdf, Usd, UsdGeom

HERE = Path(__file__).resolve().parent
CRATE_ASSET = "./crate.usda"  # relative to the layer that references it
NUM_CRATES = 1000
COLUMNS = 40
SPACING = 2.0  # meters
OPEN_RUNS = 5


def build_stage(path: Path, instanced: bool) -> None:
    stage = Usd.Stage.CreateNew(str(path))
    # Match crate.usda: meters, Z-up, so the positions below are in meters.
    UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.meters)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

    world = UsdGeom.Xform.Define(stage, Sdf.Path("/World"))
    stage.SetDefaultPrim(world.GetPrim())

    for i in range(NUM_CRATES):
        crate = UsdGeom.Xform.Define(stage, world.GetPath().AppendChild(f"Crate_{i:04d}"))
        prim = crate.GetPrim()
        # No prim path given: the reference targets crate.usda's defaultPrim (/Crate).
        prim.GetReferences().AddReference(CRATE_ASSET)
        if instanced:
            prim.SetInstanceable(True)
        x = SPACING * (i % COLUMNS)
        y = SPACING * (i // COLUMNS)
        UsdGeom.XformCommonAPI(prim).SetTranslate(Gf.Vec3d(x, y, 0.0))

    stage.GetRootLayer().Save()


def measure(path: Path) -> None:
    open_times = []
    for _ in range(OPEN_RUNS):
        start = time.perf_counter()
        stage = Usd.Stage.Open(str(path))
        open_times.append(time.perf_counter() - start)
        del stage  # release layers so the next open starts cold

    stage = Usd.Stage.Open(str(path))
    traversed = sum(1 for _ in stage.Traverse())
    with_proxies = sum(1 for _ in stage.Traverse(Usd.TraverseInstanceProxies(Usd.PrimDefaultPredicate)))
    prototypes = stage.GetPrototypes()

    print(f"{path.name}")
    print(f"  open time (median of {OPEN_RUNS}): {statistics.median(open_times) * 1000:.2f} ms"
          f"  [runs: {', '.join(f'{t * 1000:.2f}' for t in open_times)} ms]")
    print(f"  prims visited by stage.Traverse(): {traversed}")
    print(f"  prims visited incl. instance proxies: {with_proxies}")
    print(f"  prototypes: {len(prototypes)} {[str(p.GetPath()) for p in prototypes]}")


def main() -> None:
    references_path = HERE / "references.usda"
    instanced_path = HERE / "instanced.usda"
    build_stage(references_path, instanced=False)
    build_stage(instanced_path, instanced=True)

    print(f"usd-core / USD version: {Usd.GetVersion()}")
    measure(references_path)
    measure(instanced_path)


if __name__ == "__main__":
    main()
