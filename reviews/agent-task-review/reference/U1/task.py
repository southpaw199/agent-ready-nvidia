"""U1 reference solution: OpenUSD first stage.

Creates scene.usda with Z-up, meters, a default prim /World (Xform), and
/World/Box (Cube, 4 m edges, red) resting on the ground plane, then reopens
the file from disk and prints what it contains.
"""
from pathlib import Path

from pxr import Gf, Sdf, Usd, UsdGeom, Vt

HERE = Path(__file__).resolve().parent
OUT = HERE / "scene.usda"

SIZE = 4.0
HALF = SIZE / 2.0

# 1. Create the stage and set stage metadata.
stage = Usd.Stage.CreateNew(str(OUT))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.meters)

# 2. Root transform and default prim.
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# 3. The cube. Cube geometry is centered on its origin, so lifting it by
#    half its size puts its bottom face on z = 0.
box = UsdGeom.Cube.Define(stage, "/World/Box")
box.CreateSizeAttr(SIZE)
box.CreateExtentAttr(Vt.Vec3fArray([Gf.Vec3f(-HALF), Gf.Vec3f(HALF)]))
box.CreateDisplayColorAttr(Vt.Vec3fArray([Gf.Vec3f(1.0, 0.0, 0.0)]))
UsdGeom.XformCommonAPI(box).SetTranslate(Gf.Vec3d(0.0, 0.0, HALF))

stage.Save()

# 4. Reopen from disk and report.
reopened = Usd.Stage.Open(str(OUT))
print(f"Up axis: {UsdGeom.GetStageUpAxis(reopened)}")
print(f"Meters per unit: {UsdGeom.GetStageMetersPerUnit(reopened)}")
print(f"Default prim: {reopened.GetDefaultPrim().GetPath()}")
for prim in reopened.Traverse():
    print(f"Prim: {prim.GetPath()} ({prim.GetTypeName()})")

cube = UsdGeom.Cube(reopened.GetPrimAtPath("/World/Box"))
print(f"Cube size: {cube.GetSizeAttr().Get()}")
bbox = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
rng = bbox.ComputeWorldBound(cube.GetPrim()).ComputeAlignedRange()
print(f"World bounding box: min {rng.GetMin()}, max {rng.GetMax()}")
