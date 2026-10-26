"""Create referenced and scenegraph-instanced crate grids, then measure them.

OpenUSD sources:
https://openusd.org/release/tut_helloworld.html
https://openusd.org/release/tut_referencing_layers.html
https://openusd.org/release/api/group___usd_geom_linear_units__group.html
https://openusd.org/release/api/group___usd_geom_up_axis__group.html
https://openusd.org/release/api/class_usd_stage.html
https://openusd.org/release/api/_usd__page__scenegraph_instancing.html
"""

from pathlib import Path
import subprocess
import sys
from time import perf_counter

from pxr import Usd, UsdGeom


FOLDER = Path(__file__).resolve().parent


def create_scene(filename, instanceable):
    stage = Usd.Stage.CreateNew(str(FOLDER / filename))
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())
    for i in range(1000):
        crate = UsdGeom.Xform.Define(stage, f"/World/Crate_{i:04d}")
        prim = crate.GetPrim()
        prim.GetReferences().AddReference("./crate.usda")
        prim.SetInstanceable(instanceable)
        UsdGeom.XformCommonAPI(crate).SetTranslate(
            (2.0 * (i % 40), 2.0 * (i // 40), 0.0)
        )
    stage.GetRootLayer().Save()


def measure(filename):
    start = perf_counter()
    stage = Usd.Stage.Open(str(FOLDER / filename))
    elapsed = perf_counter() - start
    if not stage:
        raise RuntimeError(f"Could not open {filename}")
    print(f"{filename}:")
    print(f"  Open time: {elapsed:.6f} seconds")
    print(f"  Prims visited by stage.Traverse(): {sum(1 for _ in stage.Traverse())}")
    print(f"  Prototypes: {len(stage.GetPrototypes())}")


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--measure":
        measure(sys.argv[2])
        return
    create_scene("references.usda", False)
    create_scene("instanced.usda", True)
    # Both files are saved before either measurement. Fresh processes ensure
    # that Stage.Open reads the layers from disk rather than reusing our layers.
    for filename in ("references.usda", "instanced.usda"):
        subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--measure", filename],
            cwd=FOLDER,
            check=True,
        )


if __name__ == "__main__":
    main()
