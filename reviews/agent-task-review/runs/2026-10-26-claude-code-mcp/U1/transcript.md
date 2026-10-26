
❯ I'm learning OpenUSD, an open-source framework for describing 3D scenes. Use
  only these two documentation sites to do this task: the OpenUSD documentation
  at openusd.org, and NVIDIA's Learn OpenUSD course at
  docs.nvidia.com/learn-openusd. Don't rely on what you remember about OpenUSD,
  and don't use other websites. If you use something you already knew rather
  than something you read in these docs, say so. Each time you rely on a docs
  page, tell me its URL.

  You also have the usd-code-mcp server, which answers questions about the
  OpenUSD API and finds code examples. You can use it alongside the two
  documentation sites. When a step relies on an MCP result rather than a page,
  name the tool and the query you sent.

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

● I'll start by setting up the venv and loading the doc-fetching and MCP tools.

  Ran 1 shell command (ctrl+o to expand)

● Venv is ready (usd-core 0.26.11). Now reading the docs for each step.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/stage-setting/units-scale-a
       nd-up-axis.html)
  ⎿  Received 0 bytes (404 Not Found)

● Fetch(https://openusd.org/release/api/class_usd_geom_cube.html)
  ⎿  Received 206.2KB (200 OK)

● Fetch(https://openusd.org/release/api/group___usd_geom_up_axis__group.html)
  ⎿  Received 17.3KB (200 OK)

● Fetch(https://openusd.org/release/api/group___usd_geom_linear_units__group.htm
       l)
  ⎿  Received 18.7KB (200 OK)

● The cube docs confirm two things: the cube is centered at the origin, and if
  you set size you must also set extent. Next I'll check the Learn OpenUSD pages
  and the MCP.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/index.html)
  ⎿  Received 45.4KB (200 OK)

  Called usd-code-mcp 2 times, ran 3 shell commands (ctrl+o to expand)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html)
  ⎿  Received 119.2KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-
       prim.html)
  ⎿  Received 61.6KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/primvars.html
       )
  ⎿  Received 85.3KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprint
       s/xformcommonapi.html)
  ⎿  Received 70.3KB (200 OK)

● The XformCommonAPI result was a reconstructed script rather than a verbatim
  quote, so I'll verify SetTranslate against the API reference while also
  checking the stage, traversal, and bounding-box pages.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html)
  ⎿  Received 66.1KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/stage-travers
       al.html)
  ⎿  Received 71.3KB (200 OK)

● Fetch(https://openusd.org/release/api/class_usd_geom_b_box_cache.html)
  ⎿  Received 78.3KB (200 OK)

● Fetch(https://openusd.org/release/api/class_usd_geom_xform_common_a_p_i.html)
  ⎿  Received 105.2KB (200 OK)

  Called usd-code-mcp (ctrl+o to expand)

● I have docs for every step. Writing task.py.

● Write(task.py)
  ⎿  Wrote 50 lines to task.py
       1 """Create scene.usda (Z-up, meters) with a red 4 m cube resting
         on z = 0, then reopen and inspect it."""
       2 from pathlib import Path
       3
       4 from pxr import Gf, Sdf, Usd, UsdGeom
       6 SCENE_PATH = str(Path(__file__).resolve().parent / "scene.usda")
       7 CUBE_SIZE = 4.0  # edge length in meters
       8
       9 # 1. New stage on disk; units are meters, Z is up.
      10 stage = Usd.Stage.CreateNew(SCENE_PATH)
     … +46 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)
● I created task.py and the .venv virtual environment, with usd-core 0.26.11
  installed from PyPI. The script ran with exit code 0 and printed no warnings
  or errors. The output also shows the cube's color, which you didn't ask for.
  This is the complete output (stdout and stderr combined):

  Opened:
  /home/southpaw199/agent-runs/nvidia/2026-10-26-claude-code-mcp/U1/scene.usda
  Up axis:         Z
  Meters per unit: 1.0
  Default prim:    /World
  Prims:
    /World  (Xform)
    /World/Box  (Cube)
  Cube size:       4.0
  Cube color:      [Gf.Vec3f(1.0, 0.0, 0.0)]
  Cube world-space bounding box:
    min: (-2, -2, 0)
    max: (2, 2, 4)

  The bounding box runs from z = 0 to z = 4, so the box sits on the ground plane
  and is centered on x/y = 0. This is the scene.usda that was written:

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

  Sources behind each step

  Venv and install: python3 -m venv and pip install usd-core came from what I
  already knew, not from these docs.

  1. Create the stage, meters, Z up
  - Usd.Stage.CreateNew(path) and stage.Save():
    https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html
  - UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z) and SetStageMetersPerUnit:
    https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html
  - The up axis can only be "Y" or "Z":
    https://openusd.org/release/api/group___usd_geom_up_axis__group.html
  - UsdGeom.LinearUnits.meters:
    https://openusd.org/release/api/group___usd_geom_linear_units__group.html.
    That page shows only the C++ name (UsdGeomLinearUnits::meters) and doesn't
    give its value. The Python spelling came from what I already knew; the
    output above confirms the value is 1.0.

  2. World Xform as the default prim
  - UsdGeom.Xform.Define(stage, Sdf.Path("/World")) and
    stage.SetDefaultPrim(...): https://docs.nvidia.com/learn-openusd/latest/comp
    osition-basics/default-prim.html

  3. Red 4 m cube resting on z = 0
  - The cube is "centered at the origin" with a default size of 2, and "If you
    author size you must also author extent":
    https://openusd.org/release/api/class_usd_geom_cube.html. Because the cube
    is centered, I moved it up by half its size (2 m) so its bottom face sits on
    z = 0.
  - UsdGeom.Cube.Define(...) and GetSizeAttr().Set(...): MCP tool
    search_usd_code_examples, query "set displayColor on a cube and set default
    prim". The result included the example "How to set the size of a cube
    primitive using pxr.UsdGeom.Cube?".
  - Setting the extent: the same MCP result's example "How to set the extent of
    a cube prim?".
  - CreateDisplayColorAttr(defaultValue): MCP tool get_usd_method_detail, query
    method_names="ComputeExtent,GetDisplayColorPrimvar,CreateDisplayColorAttr",
    class_name="UsdGeom.Cube". That result also gives the type as color3f[], a
    list of Gf.Vec3f values.
  - displayColor is a primvar of type Color3fArray, set with Gf.Vec3f values:
    https://docs.nvidia.com/learn-openusd/latest/beyond-basics/primvars.html
  - UsdGeom.XformCommonAPI(prim).SetTranslate(Gf.Vec3d(...)): https://docs.nvidi
    a.com/learn-openusd/latest/scene-description-blueprints/xformcommonapi.html,
    plus the signature in
    https://openusd.org/release/api/class_usd_geom_xform_common_a_p_i.html.
    - The tool I used to read the Learn OpenUSD page returned a rebuilt example
      rather than a verbatim quote, so I confirmed the method against the
      openusd.org reference.
    - Applying it directly to the Cube, rather than an Xform, relies on what I
      already knew: a Cube can take transforms.

  4. Reopen and print
  - Usd.Stage.Open(path):
    https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html
  - UsdGeom.GetStageUpAxis and GetStageMetersPerUnit:
    https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html
  - stage.GetDefaultPrim(): https://docs.nvidia.com/learn-openusd/latest/composi
    tion-basics/default-prim.html
  - stage.Traverse() and prim.GetPath(): https://docs.nvidia.com/learn-openusd/l
    atest/beyond-basics/stage-traversal.html. That page doesn't use
    GetTypeName(); it came from what I already knew.
  - The world-space bounding box:
    - UsdGeom.BBoxCache(Usd.TimeCode.Default(),
      includedPurposes=[UsdGeom.Tokens.default_]) and ComputeWorldBound(prim):
      MCP tool search_usd_code_examples, query "compute world bounding box of a
      prim with BBoxCache".
    - What the constructor arguments mean:
      https://openusd.org/release/api/class_usd_geom_b_box_cache.html
    - ComputeAlignedRange() came from what I already knew. The MCP example used
      GetRange(). I used ComputeAlignedRange() because it applies the transform,
      so the result is in world space.

  These other small pieces in task.py also came from what I already knew, not
  from the docs:
  - GetExtentAttr() and GetDisplayColorAttr().Get()
  - Sdf.Path.AppendChild
  - GetRootLayer().realPath
  - del stage before reopening the file

  The first Learn OpenUSD page I tried for units and up axis returned 404 Not
  Found: https://docs.nvidia.com/learn-openusd/latest/stage-setting/units-scale-
  and-up-axis.html. I found the units lesson through the course index instead.