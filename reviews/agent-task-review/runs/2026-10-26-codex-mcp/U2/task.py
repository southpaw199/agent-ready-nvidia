"""Assemble the supplied assets and author a separate blue color override.

Run with: .venv/bin/python task.py
"""

from pathlib import Path
import hashlib
import subprocess
import sys

from pxr import Sdf, Usd, UsdGeom


HERE = Path(__file__).resolve().parent


def inspect_saved_scene():
    # Open in a fresh process so no authored layers remain in the layer registry.
    # https://openusd.org/release/api/class_usd_stage.html
    stage = Usd.Stage.Open(str(HERE / "scene.usda"))
    for name in ("Table", "Chair"):
        attr = stage.GetPrimAtPath(f"/World/{name}").GetAttribute(
            "primvars:displayColor"
        )
        print(f"/World/{name} composed displayColor: {attr.Get()}")

    # https://openusd.org/release/api/class_usd_property.html
    table_color = stage.GetPrimAtPath("/World/Table").GetAttribute(
        "primvars:displayColor"
    )
    print("Table displayColor opinions (strongest first):")
    for spec in table_color.GetPropertyStack():
        if spec.HasInfo("default"):
            print(f"  {Path(spec.layer.identifier).name}: {spec.path} = {spec.default}")


def main():
    assets = [HERE / "table.usda", HERE / "chair.usda"]
    before = [hashlib.sha256(path.read_bytes()).digest() for path in assets]

    # https://openusd.org/release/api/class_usd_stage.html
    stage = Usd.Stage.CreateNew(str(HERE / "scene.usda"))
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    # https://openusd.org/release/tut_referencing_layers.html
    for name, asset in zip(("Table", "Chair"), assets):
        prim = stage.DefinePrim(f"/World/{name}")
        prim.GetReferences().AddReference(f"./{asset.name}")

    # https://openusd.org/release/api/class_sdf_layer.html
    overrides = Sdf.Layer.CreateNew(str(HERE / "overrides.usda"))
    stage.GetRootLayer().subLayerPaths.append("./overrides.usda")

    # https://openusd.org/release/api/class_usd_edit_context.html
    # https://openusd.org/release/api/class_usd_attribute.html
    with Usd.EditContext(stage, overrides):
        stage.GetPrimAtPath("/World/Table").GetAttribute(
            "primvars:displayColor"
        ).Set([(0, 0, 1)])

    # Save only the two layers this script authors.
    # https://docs.nvidia.com/learn-openusd/latest/composition-basics/layers.html
    overrides.Save()
    stage.GetRootLayer().Save()
    assert before == [hashlib.sha256(path.read_bytes()).digest() for path in assets]
    subprocess.run([sys.executable, str(HERE / "task.py"), "--inspect"], check=True,
                   cwd=HERE)


if __name__ == "__main__":
    if sys.argv[1:] == ["--inspect"]:
        inspect_saved_scene()
    else:
        main()
