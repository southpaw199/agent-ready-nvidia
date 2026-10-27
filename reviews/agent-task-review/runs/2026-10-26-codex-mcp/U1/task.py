"""Create scene.usda, reopen it, and report its scene data.

Sources:
https://openusd.org/release/tut_helloworld.html
https://openusd.org/release/api/group___usd_geom_linear_units__group.html
https://openusd.org/release/api/group___usd_geom_up_axis__group.html
https://openusd.org/release/tut_referencing_layers.html
https://openusd.org/release/api/class_usd_geom_cube.html
https://openusd.org/release/tut_inspect_and_author_props.html
https://docs.nvidia.com/learn-openusd/latest/beyond-basics/stage-traversal.html
https://openusd.org/release/api/class_usd_geom_b_box_cache.html
https://openusd.org/release/api/class_gf_b_box3d.html
"""

from pxr import Usd, UsdGeom


def create_scene():
    stage = Usd.Stage.CreateNew("scene.usda")
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    box = UsdGeom.Cube.Define(stage, "/World/Box")
    box.CreateSizeAttr(4.0)
    # Cube.size requires a matching local-space extent.
    box.CreateExtentAttr([(-2.0, -2.0, -2.0), (2.0, 2.0, 2.0)])
    box.GetDisplayColorAttr().Set([(1.0, 0.0, 0.0)])
    UsdGeom.XformCommonAPI(box).SetTranslate((0.0, 0.0, 2.0))
    stage.GetRootLayer().Save()


def inspect_scene():
    # The authoring stage has gone out of scope before opening the saved file.
    stage = Usd.Stage.Open("scene.usda")
    print(f"Up axis: {UsdGeom.GetStageUpAxis(stage)}")
    print(f"Meters per unit: {UsdGeom.GetStageMetersPerUnit(stage)}")
    print(f"Default prim: {stage.GetDefaultPrim().GetPath()}")
    print("Prims:")
    for prim in stage.Traverse():
        print(f"  {prim.GetPath()} ({prim.GetTypeName()})")

    box = UsdGeom.Cube.Get(stage, "/World/Box")
    print(f"Cube size: {box.GetSizeAttr().Get()} meters")
    cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
    bounds = cache.ComputeWorldBound(box.GetPrim()).ComputeAlignedRange()
    print("Cube world-space bounding box (meters):")
    print(f"  min: {tuple(bounds.GetMin())}")
    print(f"  max: {tuple(bounds.GetMax())}")


if __name__ == "__main__":
    create_scene()
    inspect_scene()
