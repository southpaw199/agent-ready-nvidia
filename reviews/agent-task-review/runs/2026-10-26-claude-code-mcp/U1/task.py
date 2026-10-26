"""Create scene.usda (Z-up, meters) with a red 4 m cube resting on z = 0, then reopen and inspect it."""
from pathlib import Path

from pxr import Gf, Sdf, Usd, UsdGeom

SCENE_PATH = str(Path(__file__).resolve().parent / "scene.usda")
CUBE_SIZE = 4.0  # edge length in meters

# 1. New stage on disk; units are meters, Z is up.
stage = Usd.Stage.CreateNew(SCENE_PATH)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.meters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

# 2. Root transform prim /World, used as the default prim.
world = UsdGeom.Xform.Define(stage, Sdf.Path("/World"))
stage.SetDefaultPrim(world.GetPrim())

# 3. Red cube /World/Box. A Cube is centered on its origin, so lifting it by
#    half its size puts its bottom face on z = 0.
box = UsdGeom.Cube.Define(stage, world.GetPath().AppendChild("Box"))
box.GetSizeAttr().Set(CUBE_SIZE)
half = CUBE_SIZE / 2.0
# The Cube schema says: "If you author size you must also author extent."
box.GetExtentAttr().Set([Gf.Vec3f(-half, -half, -half), Gf.Vec3f(half, half, half)])
box.CreateDisplayColorAttr([Gf.Vec3f(1.0, 0.0, 0.0)])
UsdGeom.XformCommonAPI(box).SetTranslate(Gf.Vec3d(0.0, 0.0, half))

# 4. Save, then reopen from disk and report.
stage.Save()
del stage

stage = Usd.Stage.Open(SCENE_PATH)
print(f"Opened:          {stage.GetRootLayer().realPath}")
print(f"Up axis:         {UsdGeom.GetStageUpAxis(stage)}")
print(f"Meters per unit: {UsdGeom.GetStageMetersPerUnit(stage)}")
print(f"Default prim:    {stage.GetDefaultPrim().GetPath()}")

print("Prims:")
for prim in stage.Traverse():
    print(f"  {prim.GetPath()}  ({prim.GetTypeName()})")

cube = UsdGeom.Cube(stage.GetPrimAtPath("/World/Box"))
print(f"Cube size:       {cube.GetSizeAttr().Get()}")
print(f"Cube color:      {list(cube.GetDisplayColorAttr().Get())}")

bbox_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), includedPurposes=[UsdGeom.Tokens.default_])
world_range = bbox_cache.ComputeWorldBound(cube.GetPrim()).ComputeAlignedRange()
print("Cube world-space bounding box:")
print(f"  min: {world_range.GetMin()}")
print(f"  max: {world_range.GetMax()}")
