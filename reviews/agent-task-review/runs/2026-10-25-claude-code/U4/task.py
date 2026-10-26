"""Build 1,000 referenced crates two ways (plain references vs. scenegraph
instancing), then reopen each file from disk and compare."""

import time
from pathlib import Path

from pxr import Gf, Usd, UsdGeom

HERE = Path(__file__).resolve().parent
CRATE_ASSET = "./crate.usda"  # relative to the layer that references it
NUM_CRATES = 1000
COLUMNS = 40
SPACING = 2.0  # meters (stage is authored with metersPerUnit = 1)


def build_stage(path: Path, instanceable: bool) -> None:
    stage = Usd.Stage.CreateNew(str(path))
    # Match crate.usda: Z-up, 1 unit = 1 meter.
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)

    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    for i in range(NUM_CRATES):
        crate = UsdGeom.Xform.Define(stage, f"/World/Crate_{i:03d}")
        prim = crate.GetPrim()
        # No prim path given, so the reference targets crate.usda's default prim.
        prim.GetReferences().AddReference(CRATE_ASSET)
        x = SPACING * (i % COLUMNS)
        y = SPACING * (i // COLUMNS)
        UsdGeom.XformCommonAPI(crate).SetTranslate(Gf.Vec3d(x, y, 0.0))
        if instanceable:
            prim.SetInstanceable(True)

    stage.Save()


def report(path: Path) -> None:
    start = time.perf_counter()
    stage = Usd.Stage.Open(str(path))
    elapsed = time.perf_counter() - start

    prim_count = sum(1 for _ in stage.Traverse())
    prototypes = stage.GetPrototypes()

    print(f"{path.name}")
    print(f"  open time:          {elapsed * 1000:.2f} ms")
    print(f"  prims traversed:    {prim_count}")
    print(f"  prototypes:         {len(prototypes)}"
          + (f" {[str(p.GetPath()) for p in prototypes]}" if prototypes else ""))


def main() -> None:
    print(f"USD version: {'.'.join(map(str, Usd.GetVersion()))}")
    references_path = HERE / "references.usda"
    instanced_path = HERE / "instanced.usda"

    build_stage(references_path, instanceable=False)
    build_stage(instanced_path, instanceable=True)

    # build_stage() lets its stage go out of scope, so the layers are no longer
    # held in memory and Open() below has to read each file back from disk.
    for path in (references_path, instanced_path):
        report(path)


if __name__ == "__main__":
    main()
