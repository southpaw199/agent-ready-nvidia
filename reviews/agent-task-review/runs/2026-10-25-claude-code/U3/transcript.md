
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

● I'll start by looking at the folder and the mug asset, and loading the web
  fetch tool.

  Ran 1 shell command (ctrl+o to expand)

● Next I'll read the docs pages for each step: install, creating a stage,
  references, variants, and the display color primvar.

● Fetch(https://openusd.org/release/tut_authoring_variants.html)
  ⎿  Received 151.4KB (200 OK)

● Fetch(https://openusd.org/release/tut_referencing_layers.html)
  ⎿  Received 143.2KB (200 OK)

● Fetch(https://openusd.org/release/tut_helloworld.html)
  ⎿  Received 122.6KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/index.html)
  ⎿  Received 45.4KB (200 OK)

● Since the mug's green color comes from a referenced file rather than a local
  opinion, I need to check how references rank against variants in strength
  order—looking that up now along with the install steps and other APIs.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/usdview-install-instruction
       s.html)
  ⎿  Received 60.4KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/s
       trength-ordering/what-is-liverps.html)
  ⎿  Received 49.5KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/v
       ariant-sets/working-with-variant-sets.html)
  ⎿  Received 55KB (200 OK)

● Fetch(https://openusd.org/release/api/class_usd_variant_set.html)
  ⎿  Received 39.7KB (200 OK)

● Since variant opinions outrank reference opinions, the variant colors will
  override the mug's own green without needing to clear anything. Next I'll
  check the edit targets, default prim, and display color to switch to red
  without modifying the file on disk.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/edit-targets-
       layer-muting.html)
  ⎿  Received 80.8KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-
       prim.html)
  ⎿  Received 61.6KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/primvars.html
       )
  ⎿  Received 85.3KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/composition-basics/variant-
       sets.html)
  ⎿  Received 47.4KB (200 OK)

● I'll confirm two more APIs: getting an existing variant set by name, and
  Usd.Stage.GetSessionLayer / Save.

● Fetch(https://openusd.org/release/api/class_usd_variant_sets.html)
  ⎿  Received 26.1KB (200 OK)

● Fetch(https://openusd.org/release/api/class_usd_stage.html)
  ⎿  Received 304.6KB (200 OK)

● I'll create a virtual environment using the system's Python 3.12 and install
  usd-core from PyPI, rather than using the Python bundled with NVIDIA's
  prebuilt binaries as the guide suggests.

  Ran 1 shell command (ctrl+o to expand)

● Write(task.py)  ⎿  Wrote 60 lines to task.py
       1 import os
       2
       3 from pxr import Sdf, Usd, UsdGeom
       4
       5 HERE = os.path.dirname(os.path.abspath(__file__))
       6 SCENE_PATH = os.path.join(HERE, "scene.usda")
       7
       8
       9 def print_state(stage, label):
      10     mug = stage.GetPrimAtPath("/World/Mug")
     … +56 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● I wrote task.py and ran it in a .venv virtual environment inside this folder,
  with usd-core 26.11 installed from PyPI. It did all four steps and printed no
  warnings. scene.usda on disk still selects blue, and mug.usda is unchanged: I
  checked its checksum before and after the run.

  Complete output of .venv/bin/python task.py

  scene.usda layer still in memory: False
  [reopened from disk]
    variants:  ['blue', 'red']
    selection: blue
    displayColor: [(0, 0, 1)]
  [after switching to red in code]
    variants:  ['blue', 'red']
    selection: red
    displayColor: [(1, 0, 0)]

  The script exited with code 0. Here is the scene.usda it saved. The display
  color appears only inside the two variants:

  usda
  #usda 1.0
  (
      defaultPrim = "World"
  )

  def Xform "World"
  {
      def "Mug" (
          prepend references = @./mug.usda@
          variants = {
              string color = "blue"
          }
          prepend variantSets = "color"
      )
      {
          variantSet "color" = {
              "blue" {
                  color3f[] primvars:displayColor = [(0, 0, 1)]

              }
              "red" {
                  color3f[] primvars:displayColor = [(1, 0, 0)]

              }
          }
      }
  }

  Docs behind each step

  Setup: virtual environment and usd-core
  - https://docs.nvidia.com/learn-openusd/latest/usdview-install-instructions.ht
    ml gave me python -m venv, pip install usd-core, and the Usd.GetVersion()
    check. That guide makes the venv from Python bundled with prebuilt USD
    binaries. I used the system's Python 3.12 instead, which is my own choice.

  Step 1: new stage, /World as default prim, reference to the mug
  - https://openusd.org/release/tut_helloworld.html: Usd.Stage.CreateNew and
    UsdGeom.Xform.Define.
  - https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-prim
    .html: stage.SetDefaultPrim(...) and stage.DefinePrim(...). It also says a
    reference to a file with a default prim needs no prim path, which is why
    mug.usda can be referenced by file name alone.
  - https://openusd.org/release/tut_referencing_layers.html:
    GetReferences().AddReference('./file.usda').

  Step 2: the color variant set
  - https://openusd.org/release/tut_authoring_variants.html: AddVariantSet,
    AddVariant, SetVariantSelection, and setting the color inside with
    vset.GetVariantEditContext(): through GetDisplayColorAttr(). It warns that a
    color set outside the edit context goes on the prim directly and overrides
    the variants. That's why the script sets the color only inside the variants.
  - That tutorial had to clear an existing color first, because a color set
    directly on a prim beats any variant. I didn't need to: mug.usda's green
    comes in through the reference, and this page lists variant set opinions as
    stronger than reference opinions: https://docs.nvidia.com/learn-openusd/late
    st/creating-composition-arcs/strength-ordering/what-is-liverps.html. The
    output confirms it, since blue and red both win over green.

  Step 3: select blue and save
  - https://openusd.org/release/api/class_usd_stage.html: Save() saves all
    changed layers except session layers.

  Step 4: reopen, print, switch to red in code
  - https://docs.nvidia.com/learn-openusd/latest/composition-basics/variant-sets
    .html and https://openusd.org/release/api/class_usd_variant_set.html:
    GetVariantNames() and GetVariantSelection().
  - https://openusd.org/release/api/class_usd_variant_sets.html:
    GetVariantSet(name), to get the existing set.
  - https://docs.nvidia.com/learn-openusd/latest/beyond-basics/edit-targets-laye
    r-muting.html: Usd.EditContext(stage, layer). It also says the session layer
    suits temporary changes and that Save() doesn't write it. So I made the red
    selection in the session layer, leaving scene.usda on disk at blue.

  What came from memory, not the docs

  - Releasing the stage before reopening: if the first stage stays alive,
    Usd.Stage.Open may reuse its layer already in memory instead of reading the
    file again. So the script deletes those references, then uses Sdf.Layer.Find
    to confirm the layer is gone. That's the "still in memory: False" line.
    Neither the warning nor Sdf.Layer.Find came from the docs pages I read.
  - UsdGeom.Gprim(prim): the docs only show UsdGeom.Gprim.Get(stage, path). I
    used the direct constructor from memory.
  - The mug's prim type: I created /World/Mug with no type, expecting it to take
    the Cylinder type from the reference. The docs didn't cover that.
  - Plain Python and checks: the os.path handling of file locations, the
    f-strings, and the checksum check on mug.usda are general Python and shell
    knowledge.