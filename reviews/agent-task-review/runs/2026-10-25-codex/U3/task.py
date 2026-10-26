"""Create color variants, save blue, and inspect a temporary red selection.

Documentation:
https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html
https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-prim.html
https://openusd.org/release/tut_referencing_layers.html
https://openusd.org/release/tut_authoring_variants.html
https://openusd.org/release/api/class_usd_variant_set.html
https://openusd.org/release/tut_inspect_and_author_props.html
"""

from pathlib import Path
import subprocess
import sys

from pxr import Usd, UsdGeom


FOLDER = Path(__file__).resolve().parent
SCENE = FOLDER / "scene.usda"


def inspect_saved_stage():
    """Run in a fresh process so the stage is read from disk."""
    stage = Usd.Stage.Open(str(SCENE))
    mug = stage.GetPrimAtPath("/World/Mug")
    variants = mug.GetVariantSets().GetVariantSet("color")
    color = UsdGeom.Gprim(mug).GetDisplayColorAttr()
    print("Variants:", variants.GetVariantNames())
    print("Current selection:", variants.GetVariantSelection())
    print("Display color:", color.Get())

    variants.SetVariantSelection("red")
    print("Selection after switching:", variants.GetVariantSelection())
    print("Display color after switching:", color.Get())
    # Deliberately do not save: the selection on disk must remain blue.


def main():
    stage = Usd.Stage.CreateNew(str(SCENE))
    world = stage.DefinePrim("/World", "Xform")
    stage.SetDefaultPrim(world)
    mug = stage.OverridePrim("/World/Mug")
    mug.GetReferences().AddReference("./mug.usda")

    variants = mug.GetVariantSets().AddVariantSet("color")
    for name, rgb in (("red", (1, 0, 0)), ("blue", (0, 0, 1))):
        variants.AddVariant(name)
        variants.SetVariantSelection(name)
        with variants.GetVariantEditContext():
            UsdGeom.Gprim(mug).GetDisplayColorAttr().Set([rgb])

    variants.SetVariantSelection("blue")
    stage.GetRootLayer().Save()

    # The child uses the same virtual-environment interpreter. Its stdout and
    # stderr are inherited, including any USD warnings.
    subprocess.run([sys.executable, str(Path(__file__).resolve()), "--inspect"],
                   cwd=FOLDER, check=True)


if __name__ == "__main__":
    if sys.argv[1:] == ["--inspect"]:
        inspect_saved_stage()
    else:
        main()
