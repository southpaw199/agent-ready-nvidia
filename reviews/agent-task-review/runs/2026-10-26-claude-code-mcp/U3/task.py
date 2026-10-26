"""Reference mug.usda into scene.usda and give it a "color" variant set."""
import os

from pxr import Gf, Sdf, Usd, UsdGeom, Vt

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE_PATH = os.path.join(HERE, "scene.usda")
MUG_PATH = "/World/Mug"
COLORS = {"red": Gf.Vec3f(1, 0, 0), "blue": Gf.Vec3f(0, 0, 1)}


def build_scene():
    # Step 1: new stage, /World Xform as default prim, mug referenced at /World/Mug.
    stage = Usd.Stage.CreateNew(SCENE_PATH)
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    # Typeless def, so the prim type (Cylinder) comes from the referenced asset.
    mug = stage.DefinePrim(MUG_PATH)
    mug.GetReferences().AddReference("./mug.usda")

    # Step 2: "color" variant set; displayColor is authored only inside each variant.
    vset = mug.GetVariantSets().AddVariantSet("color")
    gprim = UsdGeom.Gprim(mug)
    for name, color in COLORS.items():
        vset.AddVariant(name)
        vset.SetVariantSelection(name)
        with vset.GetVariantEditContext():
            gprim.CreateDisplayColorAttr(Vt.Vec3fArray([color]))

    # Step 3: select blue and save.
    vset.SetVariantSelection("blue")
    stage.GetRootLayer().Save()


def report(stage, label):
    mug = stage.GetPrimAtPath(MUG_PATH)
    vset = mug.GetVariantSets().GetVariantSet("color")
    color = UsdGeom.Gprim(mug).GetDisplayColorAttr().Get()
    print(f"[{label}]")
    print(f"  variants:  {vset.GetVariantNames()}")
    print(f"  selection: {vset.GetVariantSelection()}")
    print(f"  color:     {list(color)}")


def inspect_scene():
    # Step 4: reopen from disk and report, then switch to red in memory only.
    stage = Usd.Stage.Open(SCENE_PATH)
    report(stage, "reopened from disk")

    # Author the red selection in the session layer, which Save() never writes,
    # so scene.usda on disk keeps selecting blue.
    vset = stage.GetPrimAtPath(MUG_PATH).GetVariantSets().GetVariantSet("color")
    with Usd.EditContext(stage, Usd.EditTarget(stage.GetSessionLayer())):
        vset.SetVariantSelection("red")
    report(stage, "after switching to red in code")


def verify_on_disk():
    layer = Sdf.Layer.OpenAsAnonymous(SCENE_PATH)
    selection = layer.GetPrimAtPath(MUG_PATH).variantSelections.get("color")
    print(f"[scene.usda on disk] color selection: {selection}")


if __name__ == "__main__":
    build_scene()
    inspect_scene()
    verify_on_disk()
