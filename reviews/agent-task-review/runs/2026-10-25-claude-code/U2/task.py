"""Build scene.usda from table.usda and chair.usda, and override the table's
display color to blue in a separate layer, overrides.usda."""

import os

from pxr import Gf, Sdf, Usd, UsdGeom

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE_PATH = os.path.join(HERE, "scene.usda")
OVERRIDES_PATH = os.path.join(HERE, "overrides.usda")

# 1. New stage with a root Xform /World as the default prim.
stage = Usd.Stage.CreateNew(SCENE_PATH)
world = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()
stage.SetDefaultPrim(world)

# 2. Reference the assets. Each asset file has a default prim, so no prim
#    path is needed. Asset paths are relative to scene.usda.
table = stage.DefinePrim("/World/Table")
table.GetReferences().AddReference("./table.usda")
chair = stage.DefinePrim("/World/Chair")
chair.GetReferences().AddReference("./chair.usda")

# 3. Sublayer overrides.usda into scene.usda, then author the color there.
#    Opinions in the root layer stack (local) beat opinions from references.
overrides = Sdf.Layer.CreateNew(OVERRIDES_PATH)
stage.GetRootLayer().subLayerPaths.append("./overrides.usda")
with Usd.EditContext(stage, overrides):
    UsdGeom.Gprim(table).GetDisplayColorPrimvar().Set([Gf.Vec3f(0, 0, 1)])

# 4. Save both layers, reopen from disk and report.
stage.Save()
overrides.Save()

stage = Usd.Stage.Open(SCENE_PATH)
for path in ("/World/Table", "/World/Chair"):
    gprim = UsdGeom.Gprim(stage.GetPrimAtPath(path))
    print(f"{path} displayColor: {gprim.GetDisplayColorPrimvar().Get()}")

print("Layers with an opinion on /World/Table displayColor (strongest first):")
attr = UsdGeom.Gprim(stage.GetPrimAtPath("/World/Table")).GetDisplayColorAttr()
for i, spec in enumerate(attr.GetPropertyStack(), 1):
    print(f"  {i}. {spec.layer.identifier}  value={spec.default}")
