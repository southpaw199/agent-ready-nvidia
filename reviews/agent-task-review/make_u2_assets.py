"""Create the two asset files for task U2 of the NVIDIA agent task review.

Usage: python make_u2_assets.py TARGET_FOLDER

Creates TARGET_FOLDER/table.usda (a red 2 m cube) and TARGET_FOLDER/chair.usda
(a green 1 m cube, 3 m along x), each resting on z = 0, Z-up, in meters, with
its cube as the default prim. The files are written as plain text, so their
bytes are the same every time and check_u2.py can tell if an agent changed
them. Needs no packages.
"""
import sys
from pathlib import Path

ASSETS = {
    "table.usda": """#usda 1.0
(
    defaultPrim = "Table"
    metersPerUnit = 1
    upAxis = "Z"
)

def Cube "Table"
{
    float3[] extent = [(-1, -1, -1), (1, 1, 1)]
    color3f[] primvars:displayColor = [(1, 0, 0)]
    double size = 2
    double3 xformOp:translate = (0, 0, 1)
    uniform token[] xformOpOrder = ["xformOp:translate"]
}
""",
    "chair.usda": """#usda 1.0
(
    defaultPrim = "Chair"
    metersPerUnit = 1
    upAxis = "Z"
)

def Cube "Chair"
{
    float3[] extent = [(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)]
    color3f[] primvars:displayColor = [(0, 1, 0)]
    double size = 1
    double3 xformOp:translate = (3, 0, 0.5)
    uniform token[] xformOpOrder = ["xformOp:translate"]
}
""",
}


def main(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name, text in ASSETS.items():
        (target / name).write_text(text)
    print(f"Created {', '.join(ASSETS)} in {target}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
