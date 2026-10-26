
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

● I'll start by looking at the folder and the asset, and loading the web fetch
  tool.

  Ran 1 shell command (ctrl+o to expand)

● The Crate asset is a Z-up, meters-scale Xform containing a Cube. Since python3
  currently resolves to a venv from another folder, I'll set up this folder's
  venv using the system interpreter, then check the docs next.

● Fetch(https://docs.nvidia.com/learn-openusd/latest/index.html)
  ⎿  Received 45.4KB (200 OK)

● Fetch(https://openusd.org/release/api/_usd__page__scenegraph_instancing.html)
  ⎿  Received 55.4KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing
       /authoring-scenegraph-instancing/exercise-authoring-scenegraph-instancing
       .html)
  ⎿  Received 63.9KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/r
       eferences-payloads/working-with-references.html)
  ⎿  Received 60.5KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/usdview-install-instruction
       s.html)
  ⎿  Received 60.4KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-
       prim.html)
  ⎿  Received 61.6KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/stage-travers
       al.html)
  ⎿  Received 71.3KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html)
  ⎿  Received 119.2KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprint
       s/xformcommonapi.html)
  ⎿  Received 70.3KB (200 OK)

● Now the remaining openusd.org pages: the UsdStage API (Open, Traverse,
  GetPrototypes), the glossary entry on instancing, and where openusd.org points
  to usd-core.

● Fetch(https://openusd.org/release/api/class_usd_stage.html)
  ⎿  Received 304.6KB (200 OK)

● Fetch(https://openusd.org/release/glossary.html)
  ⎿  Received 452.8KB (200 OK)

● Fetch(https://openusd.org/release/index.html)
  ⎿  Received 119.7KB (200 OK)

● Fetch(https://openusd.org/release/glossary.html)
  ⎿  Received 452.8KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing
       /authoring-scenegraph-instancing/scenegraph-instancing-intro.html)
  ⎿  Received 65KB (200 OK)

● I have enough from the docs. Creating the venv and installing usd-core:

  Ran 1 shell command (ctrl+o to expand)

● usd-core 26.11 is installed (the BrokenPipe message came from piping pip show
  into head, not from the install). Now the script:

● Write(task.py)
  ⎿  Wrote 69 lines to task.py
       1 """Build 1,000 referenced crates two ways (plain references vs.
         scenegraph
       2 instancing), then reopen each file from disk and compare."""
       4 import time
       5 from pathlib import Path
       6
       7 from pxr import Gf, Sdf, Usd, UsdGeom
       9 HERE = Path(__file__).resolve().parent
      10 CRATE_ASSET = "./crate.usda"  # relative to the layer that refer
         ences it
     … +66 lines (ctrl+o to expand)
  Ran 1 shell command (ctrl+o to expand)

● The script ran cleanly with no changes to crate.usda, though the instanced
  file took longer to open than expected. I'll check where the last crate landed
  and re-run a few times to confirm that timing pattern.

  Ran 1 shell command (ctrl+o to expand)

● Placement is confirmed correct for Crate_999, and open times aren't
  consistently faster for either file. I'll remove an unused Sdf import I
  spotted in task.py and do the final run.

● Update(task.py)
  ⎿  Added 1 line, removed 1 line
       4  import time
       5  from pathlib import Path
       6  
       7 -from pxr import Gf, Sdf, Usd, UsdGeom                          
       7 +from pxr import Gf, Usd, UsdGeom                               
       8  
       9  HERE = Path(__file__).resolve().parent
      10  CRATE_ASSET = "./crate.usda"  # relative to the layer that refe
          rences it

  Ran 1 shell command (ctrl+o to expand)

● I built a .venv in this folder with usd-core 26.11 from PyPI and wrote
  task.py. It ran cleanly and crate.usda is unchanged (its checksum matches the
  one I took before running).

  Complete output of the final run

  USD version: 0.26.11
  references.usda
    open time:          16.72 ms
    prims traversed:    2001
    prototypes:         0
  instanced.usda
    open time:          16.77 ms
    prims traversed:    1001
    prototypes:         1 ['/__Prototype_1']
  There were no warnings or errors, and the exit code was 0.

  Checks: I opened instanced.usda again separately. Crate_999 is at (78, 48, 0),
  which matches x = 2 × 39 and y = 2 × 24. It is an instance, and
  /World/Crate_999/Body is an instance proxy. A traversal that includes instance
  proxies visits 2,001 prims, the same as references.usda.

  Open times: These are too noisy to compare. Over five runs each file took
  13–19 ms, and neither was faster every time.

  What instancing saved, and what you give up

  What it saved: With plain references, each of the 1,000 crates has its own
  copy of its contents (the Body cube), so the stage has 2,001 prims: World,
  1,000 crates and 1,000 Bodies. With instancing, all 1,000 crates have the same
  composition arcs, so they share one prototype (/__Prototype_1) that holds a
  single Body. Traversal then visits only 1,001 prims. The OpenUSD glossary says
  prim count is "one of the primary factors that governs how USD scales." The
  saving here is small because each crate has only one child. In NVIDIA's
  exercise scene, the prim count fell from 44,408 to 1,711. Load time didn't
  improve measurably at this size.

  What you give up:
  - You can't override anything beneath an individual crate, such as giving one
    Body a different color. The docs say such edits "will result in coding
    errors" or are "silently ignored."
  - Instances have no children you can author under them.
  - The default Traverse() no longer visits the crate contents. Code has to opt
    in with Usd.TraverseInstanceProxies() or walk the prototype.
  - Prototype names aren't stable between runs.
  - You can still edit the instance prim itself, which is why each crate's
    position works. To change one crate's contents, you have to set it back to
    non-instanceable.

  Docs behind each step

  Step: Venv + pip install usd-core, version check
  Pages:
  https://docs.nvidia.com/learn-openusd/latest/usdview-install-instructions.html
  (openusd.org's https://openusd.org/release/index.html only covers building
  from source)
  ────────────────────────────────────────
  Step: CreateNew, Save, Open, Traverse, GetPrototypes
  Pages: https://openusd.org/release/api/class_usd_stage.html
  ────────────────────────────────────────
  Step: World Xform as default prim (SetDefaultPrim)
  Pages: https://docs.nvidia.com/learn-openusd/latest/composition-basics/default
  -prim.html
  ────────────────────────────────────────
  Step: Referencing crate.usda by its default prim (AddReference with no prim
  path)
  Pages: https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/
  references-payloads/working-with-references.html
  and the default-prim page above
  ────────────────────────────────────────
  Step: Placing crates with XformCommonAPI.SetTranslate(Gf.Vec3d(...))
  Pages: https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprin
  ts/xformcommonapi.html
  ────────────────────────────────────────
  Step: Meters and Z-up (SetStageMetersPerUnit, SetStageUpAxis); without them
  the
  stage falls back to cm and Y-up
  Pages: https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html
  ────────────────────────────────────────
  Step: SetInstanceable(True), sharing one prototype, proxies, restrictions
  Pages: https://openusd.org/release/api/_usd__page__scenegraph_instancing.html,

  https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/autho
  ring-scenegraph-instancing/scenegraph-instancing-intro.html,
  https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/autho
  ring-scenegraph-instancing/exercise-authoring-scenegraph-instancing.html
  ────────────────────────────────────────
  Step: What Traverse() visits by default
  Pages: https://docs.nvidia.com/learn-openusd/latest/beyond-basics/stage-traver
  sal.html
  and the scenegraph-instancing page
  ────────────────────────────────────────
  Step: Benefits and costs of instancing
  Pages: https://openusd.org/release/glossary.html (Instancing and Instanceable
  entries)

  Things that came from memory, not from these docs:
  - Building the stages in a function: I did this so each stage is released
    before the file is reopened, which makes Open() actually read from disk. The
    fact that USD keeps opened layers in memory while they're in use comes from
    memory; I didn't find it in these pages.
  - Plain Python: Timing with time.perf_counter and checking that crate.usda was
    unchanged with sha256sum are general Python and Linux knowledge.
  - Usd.PrimRange.Stage(...): My extra check that counted proxies used this call
    form from memory. The scenegraph-instancing page names
    Usd.TraverseInstanceProxies() but not this exact call.

  Other things to know:
  - python3 on your PATH points to a venv in a different folder (U3-rerun), so I
    built .venv with /usr/bin/python3.
  - A .claude/ folder showed up in this folder during the session. I didn't
    create it; Claude Code most likely did.