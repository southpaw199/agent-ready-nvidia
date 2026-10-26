"""Build scene.usda from table.usda and chair.usda, override the table's
color in overrides.usda, then reopen the scene and report the result."""
import os

from pxr import Gf, Sdf, Usd, UsdGeom

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE_PATH = os.path.join(HERE, "scene.usda")
OVERRIDES_PATH = os.path.join(HERE, "overrides.usda")

# 1. New stage with a root Xform "World" as its default prim.
stage = Usd.Stage.CreateNew(SCENE_PATH)
world = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()
stage.SetDefaultPrim(world)

# 2. Reference the assets. No prim path is given, so each reference
#    brings in the asset file's defaultPrim (Table / Chair).
table = stage.DefinePrim("/World/Table")
table.GetReferences().AddReference("./table.usda")
chair = stage.DefinePrim("/World/Chair")
chair.GetReferences().AddReference("./chair.usda")

# 3. Create overrides.usda and add it as a sublayer of scene.usda, so it is
#    part of the scene's local layer stack (stronger than the reference).
overrides = Sdf.Layer.CreateNew(OVERRIDES_PATH)
stage.GetRootLayer().subLayerPaths.append("./overrides.usda")

# Author the blue color only in overrides.usda by switching the edit target.
with Usd.EditContext(stage, stage.GetEditTargetForLocalLayer(overrides)):
    UsdGeom.Gprim(table).GetDisplayColorAttr().Set([Gf.Vec3f(0, 0, 1)])

# 4. Save both layers, then reopen the scene from disk.
overrides.Save()
stage.GetRootLayer().Save()

reopened = Usd.Stage.Open(SCENE_PATH)
for path in ("/World/Table", "/World/Chair"):
    attr = UsdGeom.Gprim(reopened.GetPrimAtPath(path)).GetDisplayColorAttr()
    print(f"{path} displayColor (composed): {attr.Get()}")

print("Layers with an opinion on /World/Table displayColor (strongest first):")
table_color = UsdGeom.Gprim(reopened.GetPrimAtPath("/World/Table")).GetDisplayColorAttr()
for i, spec in enumerate(table_color.GetPropertyStack(), 1):
    print(f"  {i}. {spec.layer.identifier}  (spec {spec.path}) = {spec.default}")
