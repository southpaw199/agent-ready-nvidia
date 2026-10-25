"""U2 reference solution: references, a sublayer override, and strength ordering.

Expects table.usda and chair.usda (from make_u2_assets.py) in the same folder.
Creates scene.usda, which references both assets under /World, and
overrides.usda, a sublayer of scene.usda that changes the table's display
color to blue. Then reopens scene.usda and prints the composed colors and
the layers that hold an opinion about the table's color, strongest first.
"""
from pathlib import Path

from pxr import Gf, Sdf, Usd, UsdGeom, Vt

HERE = Path(__file__).resolve().parent
SCENE = HERE / "scene.usda"
OVERRIDES = HERE / "overrides.usda"

# 1. The scene, with /World as its default prim.
stage = Usd.Stage.CreateNew(str(SCENE))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.meters)
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# 2. Reference each asset's default prim, with paths relative to scene.usda.
table = stage.DefinePrim("/World/Table")
table.GetReferences().AddReference("./table.usda")
chair = stage.DefinePrim("/World/Chair")
chair.GetReferences().AddReference("./chair.usda")

# 3. A sublayer holds the override. Opinions in the root layer's sublayers
#    are local opinions, which are stronger than opinions from references.
overrides = Sdf.Layer.CreateNew(str(OVERRIDES))
stage.GetRootLayer().subLayerPaths.append("./overrides.usda")
with Usd.EditContext(stage, overrides):
    UsdGeom.Gprim(table).GetDisplayColorAttr().Set(Vt.Vec3fArray([Gf.Vec3f(0.0, 0.0, 1.0)]))

stage.Save()

# 4. Reopen from disk and report.
reopened = Usd.Stage.Open(str(SCENE))
table_color = UsdGeom.Gprim(reopened.GetPrimAtPath("/World/Table")).GetDisplayColorAttr()
chair_color = UsdGeom.Gprim(reopened.GetPrimAtPath("/World/Chair")).GetDisplayColorAttr()
print(f"Table display color: {list(table_color.Get())}")
print(f"Chair display color: {list(chair_color.Get())}")
print("Opinions about the table's display color, strongest first:")
for spec in table_color.GetPropertyStack(Usd.TimeCode.Default()):
    print(f"  {Path(spec.layer.identifier).name}: {list(spec.default)}")
