"""Reference a mug and author color variants without modifying the asset.

Sources:
https://openusd.org/release/tut_helloworld.html
https://openusd.org/release/tut_referencing_layers.html
https://openusd.org/release/tut_authoring_variants.html
MCP get_usd_method_detail: UsdVariantSet.GetVariantNames/GetVariantSelection.
"""

from pathlib import Path

from pxr import Usd, UsdGeom


FOLDER = Path(__file__).resolve().parent
SCENE = FOLDER / "scene.usda"


def create_scene():
    stage = Usd.Stage.CreateNew(str(SCENE))
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())
    mug = stage.OverridePrim("/World/Mug")
    mug.GetReferences().AddReference("./mug.usda")

    variants = mug.GetVariantSets().AddVariantSet("color")
    color = UsdGeom.Gprim.Get(stage, "/World/Mug").GetDisplayColorAttr()
    for name, value in (("red", (1, 0, 0)), ("blue", (0, 0, 1))):
        variants.AddVariant(name)
        variants.SetVariantSelection(name)
        # This is the only displayColor authoring in scene.usda.
        with variants.GetVariantEditContext():
            color.Set([value])

    variants.SetVariantSelection("blue")
    stage.GetRootLayer().Save()
    # No stage or prim handles escape this function before reopening.


def inspect_scene():
    stage = Usd.Stage.Open(str(SCENE))
    mug = stage.GetPrimAtPath("/World/Mug")
    variants = mug.GetVariantSet("color")
    color = UsdGeom.Gprim.Get(stage, "/World/Mug").GetDisplayColorAttr()
    print("Variants:", variants.GetVariantNames())
    print("Selection:", variants.GetVariantSelection())
    print("Display color:", color.Get())

    variants.SetVariantSelection("red")
    print("Selection:", variants.GetVariantSelection())
    print("Display color:", color.Get())
    # Deliberately do not save: the file on disk must keep blue selected.


if __name__ == "__main__":
    create_scene()
    inspect_scene()
