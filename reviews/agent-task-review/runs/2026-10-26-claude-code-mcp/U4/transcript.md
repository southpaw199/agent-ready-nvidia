
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

  This folder has a USD asset file, crate.usda. Don't change it. Write a Python
  script named task.py that does the following:

  1. Creates references.usda in this folder: a stage with a root transform prim
  named World as its default prim, and 1,000 crates under World, each one a
  prim that references crate.usda. Place crate i, for i from 0 to 999, at x = 2
  × (i mod 40), y = 2 × floor(i / 40), z = 0, in meters.
  2. Creates instanced.usda in this folder with the same 1,000 crates in the
  same places, but using OpenUSD's instancing, so the crates share one copy of
  the crate's data instead of each having its own.
  3. Saves both files, then opens each from disk and prints, for each one: how
  long it took to open, how many prims a traversal of the stage visits, and how
  many prototypes the stage has.

  Then explain in a few sentences what instancing saved in this scene, and what
  you give up by using it.

● I'll start by looking at the folder and the crate asset, and loading the
  doc-fetching and MCP tools.

  Ran 1 shell command (ctrl+o to expand)

● Tools loaded. I'll start the venv install and read the docs at the same time.

  Ran 1 shell command (ctrl+o to expand)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/scenegraph-in
       stancing.html)
  ⎿  Received 0 bytes (404 Not Found)

● Fetch(https://openusd.org/release/api/_usd__page__scenegraph_instancing.html)
  ⎿  Received 55.4KB (200 OK)

● The OpenUSD instancing page loaded. The NVIDIA URL I guessed returned a 404,
  so I'll find the right page from the course index.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/index.html)
  ⎿  Received 45.4KB (200 OK)

● Fetch(https://openusd.org/release/api/class_usd_references.html)
  ⎿  Received 46.6KB (200 OK)

● The course index didn't show its hostname, and the user limited me to
  docs.nvidia.com/learn-openusd. So I'll try those relative paths on that host.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing
       /authoring-scenegraph-instancing/scenegraph-instancing-intro.html)
  ⎿  Received 65KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/stage-travers
       al.html)
  ⎿  Received 71.3KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/r
       eferences-payloads/working-with-references.html)
  ⎿  Received 60.5KB (200 OK)

● Next: the default prim, units, and the API for instanceable and prototypes.
  I'll query the docs and the MCP in parallel.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-
       prim.html)
  ⎿  Received 61.6KB (200 OK)

● Fetch(https://openusd.org/release/api/group___usd_geom_linear_units__group.htm
       l)
  ⎿  Received 18.7KB (200 OK)

  Called usd-code-mcp (ctrl+o to expand)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprint
       s/xformcommonapi.html)
  ⎿  Received 70.3KB (200 OK)

● The MCP confirmed SetInstanceable and GetPrototypes. I'll check the Python
  names for setting stage units and up axis.

  Called usd-code-mcp (ctrl+o to expand)

● I have what I need. Now I'll write task.py.

● Write(task.py)
  ⎿  Wrote 72 lines to task.py
       1 """Build 1,000 crates two ways (plain references vs. scenegraph
         instancing) and compare them."""
       2 import statistics
       4 from pathlib import Path
       5
       6 from pxr import Gf, Sdf, Usd, UsdGeom
       7
       9 CRATE_ASSET = "./crate.usda"  # relative to the layer that refer
         ences it
      10 NUM_CRATES = 1000
     … +72 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● The script ran with no warnings. I'll spot-check the last crate's world
  position.

  Ran 1 shell command (ctrl+o to expand)

● I wrote task.py and it runs cleanly. It created references.usda and
  instanced.usda with all 1,000 crates in the right places; I checked crates 0,
  41 and 999, which sit at (0,0,0), (2,2,0) and (78,48,0) in both files.
  crate.usda was not changed. The virtual environment is in .venv/, with
  usd-core 26.11 from PyPI.

  Complete output of .venv/bin/python task.py

  usd-core / USD version: (0, 26, 11)
  references.usda
    open time (median of 5): 13.85 ms  [runs: 13.74, 14.39, 13.83, 13.85, 15.69
  ms]
    prims visited by stage.Traverse(): 2001
    prims visited incl. instance proxies: 2001
    prototypes: 0 []
  instanced.usda
    open time (median of 5): 15.15 ms  [runs: 15.25, 14.91, 15.01, 15.15, 15.64
  ms]
    prims visited by stage.Traverse(): 1001
    prims visited incl. instance proxies: 2001
    prototypes: 1 ['/__Prototype_1']

  There were no warnings or errors, and the exit code was 0.

  What instancing saved, and what you give up

  What it saved: without instancing, each of the 1,000 crates gets its own copy
  of the crate's contents, so a traversal visits 2,001 prims: World, 1,000
  crates and 1,000 Body cubes. With instancing, all 1,000 crates share one
  prototype (/__Prototype_1). The stage then has only 1,001 prims to traverse,
  because the shared Body is stored once in the prototype and not under each
  crate. Turning on instance proxies gives 2,001 again: the content is all still
  there, just shared.

  It didn't make opening faster here. The instanced file actually opened about 1
  ms slower. This crate is a single cube, so there's very little to share, and
  setting up the prototype costs about what it saves. The savings grow with the
  size of the asset.

  What you give up: you can still edit the instanced prim itself; that's how
  each crate has its own position. But you can't change anything underneath it.
  For example, you can't recolor the Body of one crate, and any such edits
  already in the files are silently ignored. To change one crate, you have to
  turn instancing off for that crate. Tools also have to deal with instances: by
  default, traversal stops at each instance, and prototype paths like
  /__Prototype_1 can change from run to run, so you shouldn't hard-code them.

  Sources behind each step

  Setup: venv and usd-core. I used standard Python and pip from my own
  knowledge; no docs page.

  Step 1: references.usda
  - World as the default prim (stage.SetDefaultPrim, a root-level Xform): https:
    //docs.nvidia.com/learn-openusd/latest/composition-basics/default-prim.html
  - Referencing crate.usda with GetReferences().AddReference(path):
    https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/refer
    ences-payloads/working-with-references.html
  - Leaving out the prim path (the reference then targets crate.usda's default
    prim, /Crate): https://openusd.org/release/api/class_usd_references.html
  - Positioning each crate with XformCommonAPI(...).SetTranslate(Gf.Vec3d(...)):
    https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/x
    formcommonapi.html
  - Units in meters:
    - The default is centimeters (0.01) unless metersPerUnit is set:
      https://openusd.org/release/api/group___usd_geom_linear_units__group.html
    - Python names UsdGeom.SetStageMetersPerUnit and UsdGeom.SetStageUpAxis: MCP
      tool get_usd_method_detail, query
      ["SetStageMetersPerUnit","SetStageUpAxis"], class UsdGeom.
    - The constants UsdGeom.LinearUnits.meters and UsdGeom.Tokens.z are spelled
      from my own knowledge. The page and the MCP only show the C++ names.

  Step 2: instanced.usda
  - How instancing works (instanceable = true on a prim that has a reference;
    instances share a prototype only when they use the same composition arcs):
    https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/aut
    horing-scenegraph-instancing/scenegraph-instancing-intro.html and
    https://openusd.org/release/api/_usd__page__scenegraph_instancing.html
  - The Python call Usd.Prim.SetInstanceable(True): MCP tool
    get_usd_method_detail, query
    ["SetInstanceable","GetPrototypes","IsInstance"].

  Step 3: open, traverse, count prototypes
  - stage.Traverse() and what it visits by default: https://docs.nvidia.com/lear
    n-openusd/latest/beyond-basics/stage-traversal.html
  - Traversal skips prototypes and instance children; instance proxies; you
    can't edit inside instances; prototype names aren't stable:
    https://openusd.org/release/api/_usd__page__scenegraph_instancing.html
  - Usd.Stage.GetPrototypes(): the same MCP query as in step 2.
  - From my own knowledge, not the docs:
    - The Python spelling Usd.TraverseInstanceProxies(Usd.PrimDefaultPredicate).
      The OpenUSD page only names the C++ UsdTraverseInstanceProxies.
    - Timing with time.perf_counter, and reporting the median of 5 opens.
    - del stage between opens so that each open starts cold.
    - Usd.GetVersion().
    - UsdGeom.XformCache for the one-off position check, which isn't part of
      task.py.

  Notes on sources:
  - One URL I guessed returned a 404: docs.nvidia.com/learn-openusd/latest/beyon
    d-basics/scenegraph-instancing.html.
  - The course index page didn't state its hostname, so I didn't use the
    GitHub-hosted URLs it listed. All the NVIDIA pages cited above loaded from
    docs.nvidia.com/learn-openusd.