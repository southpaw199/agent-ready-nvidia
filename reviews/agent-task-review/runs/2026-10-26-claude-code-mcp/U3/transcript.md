
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

  This folder has a USD asset file, mug.usda. Don't change it. Write a Python
  script named task.py that does the following:

  1. Creates a new USD stage and saves it as scene.usda in this folder, with a
  root transform prim named World as its default prim, and adds the mug by
  referencing mug.usda at /World/Mug.
  2. In scene.usda, gives /World/Mug a variant set named color with two
  variants, red and blue, that set the mug's display color to (1, 0, 0) and (0,
  0, 1). Don't set the display color anywhere else in scene.usda.
  3. Selects the blue variant and saves the stage.
  4. Reopens scene.usda from disk and prints the variant set's variants, the
  current selection, and the mug's display color. Then switches the selection
  to red in code and prints the selection and color again. When the script
  finishes, scene.usda on disk should still select blue.

● I'll start by looking at the folder and the mug asset, and loading the
  doc-fetching and MCP tools.

  Ran 1 shell command (ctrl+o to expand)

● Kicking off the venv install while I read the docs.

  Ran 1 shell command (ctrl+o to expand)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/v
       ariant-sets/index.html)
  ⎿  Received 42.3KB (200 OK)

● Fetch(https://openusd.org/release/api/class_usd_variant_set.html)
  ⎿  Received 39.7KB (200 OK)

● Background command "Create venv and install usd-core" completed (exit code 0)

  Read 1 file (ctrl+o to expand)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/v
       ariant-sets/working-with-variant-sets.html)
  ⎿  Received 55KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/s
       trength-ordering/liverps.html)
  ⎿  Received 0 bytes (404 Not Found)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/i
       ndex.html)
  ⎿  Received 48.2KB (200 OK)

● Fetch(https://openusd.org/release/glossary.html)
  ⎿  Received 452.8KB (200 OK)

● Those guessed github.io URLs aren't one of the allowed sites, so I'll use the
  same paths on docs.nvidia.com.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/s
       trength-ordering/what-is-liverps.html)
  ⎿  Received 49.5KB (200 OK)

● Fetch(https://openusd.org/release/glossary.html)
  ⎿  Received 452.8KB (200 OK)

● Variant opinions override the reference's green color, so I'll author color
  only within the variants. Next I'll check the session layer, references, and
  default prim.

● Fetch(https://openusd.org/release/glossary.html)
  ⎿  Received 452.8KB (200 OK)

  Called usd-code-mcp (ctrl+o to expand)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/r
       eferences-payloads/working-with-references.html)
  ⎿  Received 60.5KB (200 OK)

  Searched memories (ctrl+o to expand)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beginner/stage.html)
  ⎿  Received 0 bytes (404 Not Found)

  Called usd-code-mcp (ctrl+o to expand)

● I have what I need on default prims and the session layer. Two more lookups:
  display color, and the edit-context form that writes to the session layer.

● Fetch(https://openusd.org/release/api/class_usd_edit_context.html)
  ⎿  Received 19.6KB (200 OK)

● Fetch(https://openusd.org/release/api/class_usd_geom_gprim.html)  ⎿  Received 205.9KB (200 OK)

● I'll write the script now, applying three key choices: defining /World/Mug
  without a type so it inherits Cylinder from the reference, setting colors
  inside each variant via GetVariantEditContext() so they override the
  reference's green, and switching to red in the session layer so Save() won't
  persist it to disk.

● Write(task.py)
  ⎿  Wrote 68 lines to task.py
      1 """Reference mug.usda into scene.usda and give it a "color" varia
        nt set."""
      2 import os
      3
      4 from pxr import Gf, Sdf, Usd, UsdGeom, Vt
      5
      6 HERE = os.path.dirname(os.path.abspath(__file__))
      7 SCENE_PATH = os.path.join(HERE, "scene.usda")
      8 MUG_PATH = "/World/Mug"
      9 COLORS = {"red": Gf.Vec3f(1, 0, 0), "blue": Gf.Vec3f(0, 0, 1)}
     … +67 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● I wrote task.py and ran it with usd-core 26.11, installed from PyPI into .venv
  in this folder. It ran without warnings or errors and exited with code 0.
  scene.usda on disk still selects blue, and mug.usda is unchanged (still 387
  bytes, timestamp 19:36:00).

  Complete output of .venv/bin/python task.py

  [reopened from disk]
    variants:  ['blue', 'red']
    selection: blue
    color:     [Gf.Vec3f(0.0, 0.0, 1.0)]
  [after switching to red in code]
    variants:  ['blue', 'red']
    selection: red
    color:     [Gf.Vec3f(1.0, 0.0, 0.0)]
  [scene.usda on disk] color selection: blue

  The last line is an extra check I added. After the switch to red, it reads
  scene.usda from disk and confirms it still says blue. I also printed the file:
  primvars:displayColor appears only inside the blue and red variants and
  nowhere else.

  Two decisions in task.py

  - The mug prim has no type. mug.usda defines the mug as a Cylinder. If
    /World/Mug were defined as an Xform, that type would override the Cylinder.
    Leaving it typeless lets the type come from mug.usda.
  - Red is selected in the session layer. The session layer holds in-memory
    changes, and Save() never writes it to disk. That's why the file still
    selects blue.

  The mug's own green color in mug.usda doesn't win because a variant's settings
  take priority over anything a reference brings in.

  Sources behind each step

  Step: Venv and pip install usd-core
  Source: No docs page; standard Python commands I already knew.
  ────────────────────────────────────────
  Step: 1. Create the stage, set World as the default prim, reference the mug
  Source: https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs
  /references-payloads/working-with-references.html
  (UsdGeom.Xform.Define, GetReferences().AddReference). MCP tool
  get_usd_method_detail, query
  ["SetDefaultPrim","GetSessionLayer","SetEditTarget","DefinePrim"] on class
  UsdStage: SetDefaultPrim writes to the root layer, and DefinePrim with no
  type name creates a typeless prim. Usd.Stage.CreateNew and Usd.Stage.Open are
   from memory: the page I tried for them returned 404.
  ────────────────────────────────────────
  Step: 2. Variant set and authoring inside each variant
  Source: https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs
  /variant-sets/working-with-variant-sets.html
  (AddVariantSet, AddVariant, SetVariantSelection, with
  vset.GetVariantEditContext():) and
  https://openusd.org/release/api/class_usd_variant_set.html
  ────────────────────────────────────────
  Step: 2. Why variant colors beat the mug's green
  Source: https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs
  /strength-ordering/what-is-liverps.html
  and https://openusd.org/release/glossary.html (LIVERPS: variant sets are
  stronger than references)
  ────────────────────────────────────────
  Step: 2. Display color
  Source: https://openusd.org/release/api/class_usd_geom_gprim.html (color3f[]
  primvars:displayColor is an array). Building it with
  Vt.Vec3fArray([Gf.Vec3f(...)]) is from memory.
  ────────────────────────────────────────
  Step: 3. Select blue and save
  Source: Same variant-set pages as step 2. Calling GetRootLayer().Save() is
  from
  memory.
  ────────────────────────────────────────
  Step: 4. Switch to red without changing the file
  Source: https://openusd.org/release/glossary.html (session layer:
  "UsdStage::Save does not save its stage's session layer(s)"; usdview writes
  its variant selections there) and
  https://openusd.org/release/api/class_usd_edit_context.html (session-layer
  example in C++). The Python form with Usd.EditContext(stage,
  Usd.EditTarget(layer)): is from memory, since that page only shows C++.
  ────────────────────────────────────────
  Step: Check of the file on disk
  Source: From memory: Sdf.Layer.OpenAsAnonymous and variantSelections.

  Other notes:
  - A page I fetched suggested nvidia-omniverse.github.io links. I didn't use
    them because that site isn't one of the two you allowed.
  - I also ran the MCP tool search_usd_code_examples with "set edit target to
    session layer and change variant selection without modifying root layer".
    The result was too large to read, so nothing in the script relies on it.

  Files are in this folder:
  - task.py
  - scene.usda
  - .venv/