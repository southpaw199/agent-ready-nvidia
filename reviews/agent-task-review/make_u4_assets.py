"""Create the asset file for task U4 of the NVIDIA agent task review.

Usage: python make_u4_assets.py TARGET_FOLDER

Creates TARGET_FOLDER/crate.usda: a brown 1 m crate resting on z = 0, Z-up,
in meters. The default prim is an Xform, Crate, with the cube as its child,
Body, because instancing shares a prim's descendants, not the prim itself.
The file is written as plain text, so its bytes are the same every time and
check_u4.py can tell if an agent changed it. Needs no packages.
"""
import sys
from pathlib import Path

ASSETS = {
    "crate.usda": """#usda 1.0
(
    defaultPrim = "Crate"
    metersPerUnit = 1
    upAxis = "Z"
)

def Xform "Crate"
{
    def Cube "Body"
    {
        float3[] extent = [(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)]
        color3f[] primvars:displayColor = [(0.55, 0.35, 0.15)]
        double size = 1
        double3 xformOp:translate = (0, 0, 0.5)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }
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
