"""Create the files for task U5 of the NVIDIA agent task review.

Usage: python make_u5_assets.py TARGET_FOLDER [--holdout]

Creates a set of .usda files with known problems in TARGET_FOLDER, plus a
parts/ folder they use. The main set is what the agent works on. The holdout
set, with --holdout, has different names and structure; the reviewer reruns
the agent's script on it, so a script that only handles the files it was
shown fails C6. EXPECTED gives the problem codes each top-level file should
get. The files are written as plain text, so their bytes are the same every
time and check_u5.py can tell if an agent changed them. Needs no packages.
"""
import sys
from pathlib import Path

def scene(up="Z", mpu=1, child="", sublayers=""):
    """A top-level file. up or mpu set to None leaves that metadata out."""
    lines = []
    if mpu is not None:
        lines.append(f"    metersPerUnit = {mpu}")
    if up is not None:
        lines.append(f'    upAxis = "{up}"')
    if sublayers:
        lines.append(f"    subLayers = [\n        @{sublayers}@\n    ]")
    header = "#usda 1.0\n(\n    defaultPrim = \"World\"\n" + "".join(f"{line}\n" for line in lines) + ")\n\n"
    return header + f'def Xform "World"\n{{\n{child}}}\n'


def child(name, arc, path):
    """A child prim under /World that brings in another file by reference or payload."""
    return (f'    def "{name}" (\n        prepend {arc} = @{path}@\n    )\n    {{\n    }}\n')


def part(name, body=""):
    return (f'#usda 1.0\n(\n    defaultPrim = "{name}"\n    metersPerUnit = 1\n    upAxis = "Z"\n)\n\n'
            f'def Xform "{name}"{body}\n{{\n}}\n')


MAIN = {
    "good.usda": scene(child=child("Lamp", "references", "./parts/lamp.usda")),
    "y_up_centimeters.usda": scene(up="Y", mpu=0.01),
    "no_up_axis.usda": scene(up=None),
    "no_units.usda": scene(mpu=None),
    "broken_reference.usda": scene(child=child("Chair", "references", "./parts/missing_chair.usda")),
    "nested_broken_reference.usda": scene(child=child("Shelf", "references", "./parts/shelf.usda")),
    "two_problems.usda": scene(up=None, mpu=None, child=child("Rug", "payload", "./parts/missing_rug.usda")),
    "parts/lamp.usda": part("Lamp"),
    "parts/shelf.usda": part("Shelf", " (\n    prepend references = @./missing_books.usda@\n)"),
}
MAIN_EXPECTED = {
    "good.usda": [],
    "y_up_centimeters.usda": [],
    "no_up_axis.usda": ["missing_up_axis"],
    "no_units.usda": ["missing_meters_per_unit"],
    "broken_reference.usda": ["broken_reference"],
    "nested_broken_reference.usda": ["broken_reference"],
    "two_problems.usda": ["broken_reference", "missing_meters_per_unit", "missing_up_axis"],
}

HOLDOUT = {
    "kitchen.usda": scene(sublayers="./parts/kitchen_props.usda"),
    "garage.usda": scene(up=None, mpu=None),
    "attic.usda": scene(sublayers="./parts/missing_attic_layer.usda"),
    "cellar.usda": scene(up=None, child=child("Barrel", "payload", "./parts/missing_barrel.usda")),
    "parts/kitchen_props.usda": part("Props"),
}
HOLDOUT_EXPECTED = {
    "kitchen.usda": [],
    "garage.usda": ["missing_meters_per_unit", "missing_up_axis"],
    "attic.usda": ["broken_reference"],
    "cellar.usda": ["broken_reference", "missing_up_axis"],
}

SETS = {"main": (MAIN, MAIN_EXPECTED), "holdout": (HOLDOUT, HOLDOUT_EXPECTED)}


def main(target: Path, which: str) -> None:
    files, _ = SETS[which]
    for name, text in files.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    print(f"Created the {which} set ({len(files)} files) in {target}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--holdout"]
    main(Path(args[0] if args else "."), "holdout" if "--holdout" in sys.argv else "main")
