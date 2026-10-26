import os

from pxr import Sdf, Usd, UsdGeom

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE_PATH = os.path.join(HERE, "scene.usda")


def print_state(stage, label):
    mug = stage.GetPrimAtPath("/World/Mug")
    vset = mug.GetVariantSets().GetVariantSet("color")
    color = UsdGeom.Gprim(mug).GetDisplayColorAttr().Get()
    print(f"[{label}]")
    print("  variants: ", vset.GetVariantNames())
    print("  selection:", vset.GetVariantSelection())
    print("  displayColor:", color)


# 1. New stage with /World as the default prim, and the mug referenced at /World/Mug.
stage = Usd.Stage.CreateNew(SCENE_PATH)
world = UsdGeom.Xform.Define(stage, "/World").GetPrim()
stage.SetDefaultPrim(world)
mug = stage.DefinePrim("/World/Mug")
mug.GetReferences().AddReference("./mug.usda")

# 2. "color" variant set. The display color is authored only inside the variants.
# Variant opinions are stronger than reference opinions, so they override the
# green color that comes from mug.usda.
vset = mug.GetVariantSets().AddVariantSet("color")
vset.AddVariant("red")
vset.AddVariant("blue")
color_attr = UsdGeom.Gprim(mug).GetDisplayColorAttr()

vset.SetVariantSelection("red")
with vset.GetVariantEditContext():
    color_attr.Set([(1, 0, 0)])

vset.SetVariantSelection("blue")
with vset.GetVariantEditContext():
    color_attr.Set([(0, 0, 1)])

# 3. Select blue and save.
vset.SetVariantSelection("blue")
stage.Save()

# Drop the stage so the reopen below reads scene.usda from disk
# rather than reusing the layer that is still in memory.
del stage, world, mug, vset, color_attr
print("scene.usda layer still in memory:", Sdf.Layer.Find(SCENE_PATH) is not None)

# 4. Reopen from disk and inspect.
stage = Usd.Stage.Open(SCENE_PATH)
print_state(stage, "reopened from disk")

# Switch to red in the session layer, which Stage.Save() never writes,
# so scene.usda on disk keeps selecting blue.
mug = stage.GetPrimAtPath("/World/Mug")
with Usd.EditContext(stage, stage.GetSessionLayer()):
    mug.GetVariantSets().GetVariantSet("color").SetVariantSelection("red")
print_state(stage, "after switching to red in code")
