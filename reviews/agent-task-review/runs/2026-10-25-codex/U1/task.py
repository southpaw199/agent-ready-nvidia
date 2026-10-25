"""Create scene.usda, then reopen it and report its scene data.

OpenUSD documentation sources for each operation are listed in SOURCES.md.
Run from this folder with: .venv/bin/python task.py
"""

from pxr import Usd, UsdGeom


def create_scene():
    # https://openusd.org/release/tut_helloworld.html
    stage = Usd.Stage.CreateNew("scene.usda")

    # https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

    # https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-prim.html
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    # https://openusd.org/release/api/class_usd_geom_cube.html
    box = UsdGeom.Cube.Define(stage, "/World/Box")
    box.GetSizeAttr().Set(4.0)
    box.GetExtentAttr().Set([(-2.0, -2.0, -2.0), (2.0, 2.0, 2.0)])

    # https://openusd.org/release/api/class_usd_geom_gprim.html
    box.GetDisplayColorAttr().Set([(1.0, 0.0, 0.0)])

    # https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/xformcommonapi.html
    UsdGeom.XformCommonAPI(box).SetTranslate((0.0, 0.0, 2.0))
    stage.GetRootLayer().Save()


def inspect_scene():
    # https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html
    stage = Usd.Stage.Open("scene.usda")
    print(f"Up axis: {UsdGeom.GetStageUpAxis(stage)}")
    print(f"Meters per unit: {UsdGeom.GetStageMetersPerUnit(stage)}")
    print(f"Default prim: {stage.GetDefaultPrim().GetPath()}")

    # https://docs.nvidia.com/learn-openusd/latest/beyond-basics/stage-traversal.html
    # https://openusd.org/release/tut_helloworld.html (GetTypeName)
    print("Prims:")
    for prim in stage.Traverse():
        print(f"  {prim.GetPath()} ({prim.GetTypeName()})")

    box = UsdGeom.Cube.Get(stage, "/World/Box")
    print(f"Cube size: {box.GetSizeAttr().Get()} meters")

    # https://openusd.org/release/api/class_usd_geom_b_box_cache.html
    # https://openusd.org/release/api/class_gf_b_box3d.html
    cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
    bounds = cache.ComputeWorldBound(box.GetPrim()).ComputeAlignedRange()
    print(f"Cube world-space bounding box (meters): {bounds}")


if __name__ == "__main__":
    # Let authoring handles leave scope before opening the saved file.
    create_scene()
    inspect_scene()
