"""U4 reference solution: 1,000 plain references compared with scenegraph instancing.

Expects crate.usda (from make_u4_assets.py) in the same folder. Creates
references.usda, with 1,000 crates that each reference crate.usda, and
instanced.usda, with the same crates marked instanceable so they share one
prototype. Then opens each from disk and prints the time to open, the number
of prims a default traversal visits, and the number of prototypes.
"""
import time
from pathlib import Path

from pxr import Gf, Usd, UsdGeom

HERE = Path(__file__).resolve().parent
COUNT, COLUMNS, SPACING = 1000, 40, 2.0


def build(path, instanceable):
    stage = Usd.Stage.CreateNew(str(path))
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.meters)
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())
    for i in range(COUNT):
        crate = UsdGeom.Xform.Define(stage, f"/World/Crate_{i:04d}")
        crate.GetPrim().GetReferences().AddReference("./crate.usda")
        crate.AddTranslateOp().Set(Gf.Vec3d(SPACING * (i % COLUMNS), SPACING * (i // COLUMNS), 0.0))
        # Instancing: the crate's descendants come from one shared prototype.
        crate.GetPrim().SetInstanceable(instanceable)
    stage.Save()


build(HERE / "references.usda", instanceable=False)
build(HERE / "instanced.usda", instanceable=True)

# The first stage opened in a process pays one-time startup costs, so open one
# before timing; otherwise whichever file is timed first looks slower.
Usd.Stage.Open(str(HERE / "crate.usda"))

for name in ("references.usda", "instanced.usda"):
    start = time.perf_counter()
    stage = Usd.Stage.Open(str(HERE / name))
    seconds = time.perf_counter() - start
    prims = sum(1 for _ in stage.Traverse())
    print(f"{name}: opened in {seconds * 1000:.1f} ms; {prims} prims traversed; "
          f"{len(stage.GetPrototypes())} prototype(s)")
