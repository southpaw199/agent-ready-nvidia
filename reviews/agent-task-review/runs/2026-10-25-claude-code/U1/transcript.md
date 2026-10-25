
❯ I'm learning OpenUSD, an open-source framework for describing 3D scenes. Use
  only these two documentation sites to do this task: the OpenUSD documentation
  at openusd.org, and NVIDIA's Learn OpenUSD course at
  docs.nvidia.com/learn-openusd. Don't rely on what you remember about OpenUSD,
  and don't use other websites. If you use something you already knew rather
  than something you read in these docs, say so. Each time you rely on a docs
  page, tell me its URL.

  Work only in the current folder. Create a Python virtual environment here and
  install the usd-core package from PyPI into it. When you're done, run your
  final script and show me its complete output, including any warnings. Then
  list the docs page, with its URL, behind each step.

  Write a Python script named task.py that does the following:

  1. Creates a new USD stage and saves it as scene.usda in this folder. The
  scene's units are meters, and the Z axis points up.
  2. Adds a root transform prim named World and makes it the stage's default
  prim.
  3. Under World, adds a cube named Box. Its edges are 4 meters long, it is
  red, and it rests on the ground plane (z = 0), centered on the origin in x
  and y.
  4. Saves the stage, then reopens scene.usda from disk and prints: the stage's
  up axis and meters per unit, the default prim, each prim's path and type,
  the cube's size, and the cube's world-space bounding box.

● I'll start by loading the web fetch tool so I can read the two documentation
  sites, and set up the environment in parallel.

  Ran 1 shell command (ctrl+o to expand)

● The venv is ready (usd-core 26.11). Now I'll find the relevant doc pages on
  the two allowed sites.

● Web Search("OpenUSD stage up axis meters per unit SetStageUpAxis
            SetStageMetersPerUnit")
  ⎿  Did 1 search in 5s

● Web Search("learn-openusd python CreateNew stage define Xform default prim
            cube displayColor")
  ⎿  Did 1 search in 6s

● Web Search("OpenUSD BBoxCache ComputeWorldBound UsdGeom python")
  ⎿  Did 1 search in 6s

● The search summaries are secondhand, so I'll read the key pages directly.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html)
  ⎿  Received 119.2KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-
       prim.html)
  ⎿  Received 61.6KB (200 OK)

● Fetch(https://openusd.org/dev/api/class_usd_geom_cube.html)
  ⎿  Received 206.2KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprint
       s/xformcommonapi.html)
  ⎿  Received 70.3KB (200 OK)

● Next: display color, the linear-units constants, and the bounding-box API.

● Fetch(https://openusd.org/dev/api/group___usd_geom_linear_units__group.html)
  ⎿  Received 18.7KB (200 OK)

● Fetch(https://openusd.org/dev/api/class_usd_geom_b_box_cache.html)
  ⎿  Received 78.3KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/stage-setting/timecodes-tim
       esamples.html)
  ⎿  Received 106.2KB (200 OK)

● Fetch(https://openusd.org/dev/api/class_usd_geom_gprim.html)
  ⎿  Received 205.9KB (200 OK)

● A few gaps remain: the LinearUnits.meters constant, purpose tokens for the
  bbox cache, and reading a range out of a GfBBox3d.

● Fetch(https://openusd.org/dev/api/class_usd_geom_linear_units.html)
  ⎿  Received 23.4KB (200 OK)

● Fetch(https://openusd.org/dev/api/class_gf_b_box3d.html)
  ⎿  Received 48.7KB (200 OK)

● Fetch(https://openusd.org/dev/api/class_usd_geom_imageable.html)
  ⎿  Received 139.1KB (200 OK)

● Fetch(https://openusd.org/dev/api/class_usd_geom_boundable.html)
  ⎿  Received 183.1KB (200 OK)

● I have most of what I need. One more pass to confirm the getters and the
  traversal/type-name calls in the docs, so less of this rests on memory.
● Fetch(https://openusd.org/dev/api/usd_geom_2metrics_8h.html)
  ⎿  Received 40.2KB (200 OK)

● Web Search("Learn OpenUSD python stage.Traverse prim GetTypeName
            Usd.Stage.Open")
  ⎿  Error: The user doesn't want to proceed with this tool use. The tool use
     was rejected (eg. if it was a file edit, the new_string was NOT written to
     the file). The user provided the following reason for the rejection:  Yes
     within the allowed domains

● That search was declined (your note said "Yes within the allowed domains").
  Rather than retry the search, I'll fetch the Learn OpenUSD stage and prim
  pages directly.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/stage-setting/usd-stage.htm
       l)
  ⎿  Received 0 bytes (404 Not Found)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/stage-setting/prims.html)
  ⎿  Received 94.1KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/stage-travers
       al.html)
  ⎿  Received 71.3KB (200 OK)

● I now have doc backing for nearly every call. Writing the script:

● Write(task.py)
  ⎿  Wrote 46 lines to task.py
       1 """Build a Z-up, meters-based USD scene with a red 4 m cube rest
         ing on the ground, then read it back."""
       2
       3 from pathlib import Path
       4
       6
       7 SCENE_PATH = str(Path(__file__).resolve().parent / "scene.usda")
       8 CUBE_SIZE = 4.0  # edge length in stage units (meters)
       9
      10 # 1. New stage on disk; units are meters and Z is up.
     … +43 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● I set up a virtual environment in .venv with usd-core 26.11 from PyPI, wrote
  task.py, and ran it. It saved scene.usda correctly and printed no warnings or
  errors. I ran it a second time with scene.usda already there and got the same
  result.

  Complete output of .venv/bin/python task.py

  Up axis:          Z
  Meters per unit:  1.0
  Default prim:     /World
  Prims:
    /World  (Xform)
    /World/Box  (Cube)
  Cube size:        4.0
  Cube world bbox:  min (-2, -2, 0)  max (2, 2, 4)

  The bounding box shows the cube spans 4 m on each axis, is centered on x = 0
  and y = 0, and sits on z = 0. The saved scene.usda:

  #usda 1.0
  (
      defaultPrim = "World"
      metersPerUnit = 1
      upAxis = "Z"
  )

  def Xform "World"
  {
      def Cube "Box"
      {
          float3[] extent = [(-2, -2, -2), (2, 2, 2)]
          color3f[] primvars:displayColor = [(1, 0, 0)]
          double size = 4
          double3 xformOp:translate = (0, 0, 2)
          uniform token[] xformOpOrder = ["xformOp:translate"]
      }
  }

  Docs behind each step

  Step 1: create the stage, meters, Z up
  - I took Usd.Stage.CreateNew(path) from the Python example at
    https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/xf
    ormcommonapi.html
  - The setter calls and their examples (SetStageUpAxis(stage,
    UsdGeom.Tokens.z), SetStageMetersPerUnit) came from
    https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html. That
    page also says the defaults are Y up and 0.01 (centimeters) when nothing is
    set, so both values must be set explicitly.
  - The function signatures, including the getters used in step 4, are at
    https://openusd.org/dev/api/usd_geom_2metrics_8h.html
  - I confirmed LinearUnits.meters = 1.0 at
    https://openusd.org/dev/api/class_usd_geom_linear_units.html. The page
    explaining that units are stored as "meters per unit" is
    https://openusd.org/dev/api/group___usd_geom_linear_units__group.html

  Step 2: the /World transform as the default prim
  - UsdGeom.Xform.Define(stage, Sdf.Path("/World")) and
    stage.SetDefaultPrim(...) come from https://docs.nvidia.com/learn-openusd/la
    test/composition-basics/default-prim.html. It also says the default prim
    must be a top-level prim.

  Step 3: the red 4 m cube on the ground
  - From https://openusd.org/dev/api/class_usd_geom_cube.html:
    - The cube is "centered at the origin".
    - size is "the length of each edge" (default 2).
    - "If you author size you must also author extent." So I set the extent to
      ±2.
  - UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Box")) and
    GetDisplayColorAttr().Set([(r, g, b)]) follow https://docs.nvidia.com/learn-
    openusd/latest/stage-setting/timecodes-timesamples.html. The display color's
    type (color3f[] primvars:displayColor) is at
    https://openusd.org/dev/api/class_usd_geom_gprim.html
  - XformCommonAPI(...).SetTranslate(Gf.Vec3d(...)) comes from
    https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/xf
    ormcommonapi.html. Because the cube is centered on its own origin, moving it
    up 2 m puts its bottom face on z = 0. I worked that out from the Cube page;
    no page says it directly.
  - On authoring extent,
    https://openusd.org/dev/api/class_usd_geom_boundable.html says the docs
    "strongly encourage" it.

  Step 4: save, reopen and print
  - stage.Save() comes from https://docs.nvidia.com/learn-openusd/latest/composi
    tion-basics/default-prim.html
  - Usd.Stage.Open, GetPrimAtPath and prim.GetTypeName() come from
    https://docs.nvidia.com/learn-openusd/latest/stage-setting/prims.html
  - for prim in stage.Traverse(): print(prim.GetPath()) comes from https://docs.
    nvidia.com/learn-openusd/latest/beyond-basics/stage-traversal.html
  - UsdGeom.BBoxCache(time, includedPurposes) and ComputeWorldBound come from
    https://openusd.org/dev/api/class_usd_geom_b_box_cache.html
  - The purpose value "default" is listed at
    https://openusd.org/dev/api/class_usd_geom_imageable.html
  - ComputeAlignedRange() on the result is at
    https://openusd.org/dev/api/class_gf_b_box3d.html

  Parts that came from what I already knew, not from these docs

  - Python names that differ from the C++ docs:
    - UsdGeom.Tokens.default_: the docs list the token "default", but the
      trailing underscore in Python is from memory.
    - Usd.TimeCode.Default(): the docs show the C++ form UsdTimeCode::Default().
    - GfRange3d.GetMin() / GetMax(): I didn't open the Range3d page.
  - Passing Python lists and tuples where the API expects arrays or vectors.
    This includes the extent list and the color tuple.
  - The venv commands (python3 -m venv, pip install usd-core). These are
    standard Python tools and aren't in either docs site.

  All of these ran without error, which shows they work, but I didn't check them
  against a docs page.

  One search I tried was declined, so I fetched the Learn OpenUSD pages directly
  instead. I visited only the two allowed sites.