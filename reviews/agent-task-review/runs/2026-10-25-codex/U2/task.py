"""Compose two assets and author a color override in a separate local layer.

Documentation:
https://openusd.org/release/api/class_usd_stage.html
https://openusd.org/release/api/class_usd_geom_xform.html
https://openusd.org/release/tut_referencing_layers.html
https://openusd.org/release/api/class_sdf_layer.html
https://openusd.org/release/api/class_usd_geom_gprim.html
https://openusd.org/release/api/class_usd_attribute.html
https://docs.nvidia.com/learn-openusd/latest/composition-basics/strength-ordering.html
"""

from pathlib import Path

from pxr import Sdf, Usd, UsdGeom


FOLDER = Path(__file__).resolve().parent


def create_scene():
    stage = Usd.Stage.CreateNew(str(FOLDER / "scene.usda"))
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    # Asset defaultPrim metadata selects the prim brought in by each reference.
    for name, filename in (("Table", "table.usda"), ("Chair", "chair.usda")):
        prim = stage.OverridePrim(f"/World/{name}")
        if not prim.GetReferences().AddReference(f"./{filename}"):
            raise RuntimeError(f"Could not reference {filename}")

    overrides = Sdf.Layer.CreateNew(str(FOLDER / "overrides.usda"))
    stage.GetRootLayer().subLayerPaths.append("./overrides.usda")
    stage.SetEditTarget(overrides)
    table = UsdGeom.Gprim(stage.GetPrimAtPath("/World/Table"))
    # This is the only color authoring operation in this script.
    table.CreateDisplayColorAttr([(0, 0, 1)])

    overrides.Save()
    stage.GetRootLayer().Save()
    # No stage or layer handles escape this function, so reopening reads disk.


def format_colors(colors):
    return "[" + ", ".join(
        "(" + ", ".join(f"{component:g}" for component in color) + ")"
        for color in colors
    ) + "]"


def inspect_saved_scene():
    stage = Usd.Stage.Open(str(FOLDER / "scene.usda"))
    if not stage:
        raise RuntimeError("Could not reopen scene.usda")

    for name in ("Table", "Chair"):
        color = UsdGeom.Gprim(stage.GetPrimAtPath(f"/World/{name}"))
        print(f"/World/{name} composed displayColor: "
              f"{format_colors(color.GetDisplayColorAttr().Get())}")

    table_color = UsdGeom.Gprim(
        stage.GetPrimAtPath("/World/Table")
    ).GetDisplayColorAttr()
    print("Table displayColor opinions (strongest first):")
    # GetPropertyStack is diagnostic; Get above resolves the composed values.
    for spec in table_color.GetPropertyStack():
        print(f"  {Path(spec.layer.realPath).name}: {spec.path}")


if __name__ == "__main__":
    create_scene()
    inspect_saved_scene()
