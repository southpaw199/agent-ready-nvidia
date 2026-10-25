"""U3 reference solution: a variant set, and switching between its variants in code.

Expects mug.usda (from make_u3_assets.py) in the same folder. Creates
scene.usda, which references the mug at /World/Mug and adds a "color" variant
set there with "red" and "blue" variants, selects blue, and saves. Then
reopens scene.usda, prints the variants and the composed color, switches to
red in the session layer so the saved file still selects blue, and prints the
color again.
"""
from pathlib import Path

from pxr import Gf, Usd, UsdGeom, Vt

HERE = Path(__file__).resolve().parent
SCENE = HERE / "scene.usda"
COLORS = {"red": (1.0, 0.0, 0.0), "blue": (0.0, 0.0, 1.0)}

# 1. The scene, with /World as its default prim, and the mug by reference.
stage = Usd.Stage.CreateNew(str(SCENE))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.meters)
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
mug = stage.DefinePrim("/World/Mug")
mug.GetReferences().AddReference("./mug.usda")

# 2. A variant set on the referencing prim. Each variant's opinions are
#    authored inside its edit context, so they apply only when it's selected.
vset = mug.GetVariantSets().AddVariantSet("color")
for name, rgb in COLORS.items():
    vset.AddVariant(name)
    vset.SetVariantSelection(name)
    with vset.GetVariantEditContext():
        UsdGeom.Gprim(mug).GetDisplayColorAttr().Set(Vt.Vec3fArray([Gf.Vec3f(*rgb)]))

# 3. Select blue and save.
vset.SetVariantSelection("blue")
stage.Save()


def show(stage, label):
    prim = stage.GetPrimAtPath("/World/Mug")
    color = UsdGeom.Gprim(prim).GetDisplayColorAttr().Get()
    selection = prim.GetVariantSets().GetVariantSet("color").GetVariantSelection()
    print(f"{label}: selection {selection!r}, display color {list(color)}")


# 4. Reopen from disk, then switch in the session layer, which isn't saved.
reopened = Usd.Stage.Open(str(SCENE))
names = reopened.GetPrimAtPath("/World/Mug").GetVariantSets().GetVariantSet("color").GetVariantNames()
print(f"Variants in 'color': {names}")
show(reopened, "As saved")
with Usd.EditContext(reopened, reopened.GetSessionLayer()):
    reopened.GetPrimAtPath("/World/Mug").GetVariantSets().GetVariantSet("color").SetVariantSelection("red")
show(reopened, "After switching")
