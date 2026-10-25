"""Create the asset file for task U3 of the NVIDIA agent task review.

Usage: python make_u3_assets.py TARGET_FOLDER

Creates TARGET_FOLDER/mug.usda: a green cylinder 1 m tall, resting on z = 0,
Z-up, in meters, with the cylinder as the default prim. The file is written as
plain text, so its bytes are the same every time and check_u3.py can tell if
an agent changed it. Needs no packages.
"""
import sys
from pathlib import Path

ASSETS = {
    "mug.usda": """#usda 1.0
(
    defaultPrim = "Mug"
    metersPerUnit = 1
    upAxis = "Z"
)

def Cylinder "Mug"
{
    uniform token axis = "Z"
    float3[] extent = [(-0.4, -0.4, -0.5), (0.4, 0.4, 0.5)]
    double height = 1
    color3f[] primvars:displayColor = [(0, 1, 0)]
    double radius = 0.4
    double3 xformOp:translate = (0, 0, 0.5)
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
