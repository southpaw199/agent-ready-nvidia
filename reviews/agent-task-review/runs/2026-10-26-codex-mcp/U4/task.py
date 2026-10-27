"""Author reference/instance scenes, then measure fresh-process disk opens.

OpenUSD sources:
https://openusd.org/release/tut_referencing_layers.html
https://openusd.org/release/api/class_usd_stage.html
https://openusd.org/release/api/class_usd_geom_xformable.html
https://openusd.org/release/api/group___usd_geom_linear_units__group.html
https://openusd.org/release/api/_usd__page__scenegraph_instancing.html
"""

from pathlib import Path
import subprocess
import sys
from time import perf_counter

from pxr import Usd, UsdGeom


HERE = Path(__file__).resolve().parent


def create_scene(filename, instanceable):
    stage = Usd.Stage.CreateNew(str(HERE / filename))
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    stage.SetMetadata("upAxis", "Z")
    for i in range(1000):
        crate = UsdGeom.Xform.Define(stage, f"/World/Crate_{i:04d}")
        prim = crate.GetPrim()
        prim.GetReferences().AddReference("./crate.usda")
        prim.SetInstanceable(instanceable)
        crate.AddTranslateOp().Set((2.0 * (i % 40), 2.0 * (i // 40), 0.0))
    stage.GetRootLayer().Save()


def measure(filename):
    start = perf_counter()
    stage = Usd.Stage.Open(str(HERE / filename))
    elapsed = perf_counter() - start
    if not stage:
        raise RuntimeError(f"Could not open {filename}")
    prim_count = sum(1 for _ in stage.Traverse())
    prototypes = stage.GetPrototypes()
    print(f"{filename}: open_seconds={elapsed:.6f}, "
          f"traversed_prims={prim_count}, prototypes={len(prototypes)}")

    # Verify every placement and that all instances share one prototype.
    assert stage.GetDefaultPrim().GetPath() == "/World"
    assert UsdGeom.GetStageMetersPerUnit(stage) == 1.0
    assert len(stage.GetPrimAtPath("/World").GetChildren()) == 1000
    instanced = filename == "instanced.usda"
    assert prim_count == (1001 if instanced else 2001)
    assert len(prototypes) == (1 if instanced else 0)
    for i in range(1000):
        prim = stage.GetPrimAtPath(f"/World/Crate_{i:04d}")
        position = prim.GetAttribute("xformOp:translate").Get()
        assert tuple(position) == (2.0 * (i % 40), 2.0 * (i // 40), 0.0)
        assert prim.IsInstance() == instanced
        assert stage.GetPrimAtPath(f"{prim.GetPath()}/Body")
        if instanced:
            assert prim.GetPrototype() == prototypes[0]


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--measure":
        measure(sys.argv[2])
    else:
        create_scene("references.usda", False)
        create_scene("instanced.usda", True)
        for filename in ("references.usda", "instanced.usda"):
            subprocess.run(
                [sys.executable, str(HERE / "task.py"), "--measure", filename],
                cwd=HERE,
                check=True,
            )
