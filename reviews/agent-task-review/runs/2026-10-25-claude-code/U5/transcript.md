
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

  This folder has several USD files at the top level, and a parts folder that
  some of them use. Don't change any of them. Write a Python script named
  task.py that checks every .usda file at the top level of this folder (not the
  parts folder) for these problems:

  - missing_up_axis: the file doesn't specify the stage's up axis (upAxis).
  - missing_meters_per_unit: the file doesn't specify the stage's units
  (metersPerUnit).
  - broken_reference: the file refers to another file that can't be found,
  through a reference, a payload, or a sublayer, either directly or through a
  file it brings in.

  The script should write report.json in this folder, mapping each file's name
  to a list of the codes for the problems found in it, with an empty list for a
  file that has none, and print the report. It should work on any folder of
  .usda files, not only these.

  Then tell me how the script detects each problem.

● I'll start by looking at the folder and loading the web fetch tool.

  Ran 1 shell command (ctrl+o to expand)

● Now let me read the relevant docs pages in parallel.

● Fetch(https://openusd.org/release/api/group___usd_geom_up_axis__group.html)
  ⎿  Received 17.3KB (200 OK)

● Fetch(https://openusd.org/release/api/group___usd_geom_linear_units__group.htm
       l)
  ⎿  Received 18.7KB (200 OK)

● Fetch(https://openusd.org/release/api/dependencies_8h.html)
  ⎿  Received 65.7KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/index.html)
  ⎿  Received 45.4KB (200 OK)

● Fetch(https://openusd.org/release/api/class_usd_stage.html)
  ⎿  Received 304.6KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html)
  ⎿  Received 119.2KB (200 OK)

● Fetch(https://docs.nvidia.com/learn-openusd/latest/usdview-install-instruction
       s.html)
  ⎿  Received 60.4KB (200 OK)

● Fetch(https://openusd.org/release/api/usd_utils_page_front.html)
  ⎿  Received 20.8KB (200 OK)

● Docs gathered. Now the venv and package install.

  Ran 2 shell commands (ctrl+o to expand)

● ComputeAllDependencies returns (layers, assets, unresolvedPaths) in Python and
  follows nested references. Now I'll write the script.

● Write(task.py)
  ⎿  Wrote 48 lines to task.py
       1 """Check every top-level .usda file in a folder for missing stag
         e metrics and
         report.json.
       3
       4 Usage: python task.py [folder]   (defaults to the folder contain
       5 """
       6 import json
       7 import sys
       9
      10 from pxr import Sdf, Usd, UsdGeom, UsdUtils
     … +48 lines (ctrl+o to expand)

● Before the final run, I'll test it on a scratch folder that has a sublayer
  chain (the real files don't), so I can confirm sublayers are followed.

  Ran 1 shell command (ctrl+o to expand)

● A missing sublayer inside a nested file was caught. Now the final run on this
  folder:

  Ran 1 shell command (ctrl+o to expand)

● I made task.py, ran it, and it wrote report.json in this folder. The results
  match what's in the files: good.usda and y_up_centimeters.usda have no
  problems, and the other five each show the problems they were built to have.

  Setup

  - I created a virtual environment in .venv with python3 -m venv .venv and ran
    pip install usd-core. It installed USD version 0.26.11.
  - I didn't change any of your USD files. The only new files in this folder are
    task.py, report.json and .venv/.
  - To check sublayers, I also tested on a separate scratch folder, because none
    of your files use one. A sublayer missing two files deep was reported as
    broken_reference.

  Complete output of the final run (.venv/bin/python task.py)

  Warning: in _ReportErrors at line 3326 of /opt/USD/pxr/usd/usd/stage.cpp -- In
  </World/Chair>: Could not open asset @/home/southpaw199/agent-runs/nvidia/202
  6-10-25-claude-code/U5/parts/missing_chair.usda@ for reference introduced by
  @/home/southpaw199/agent-runs/nvidia/2026-10-25-claude-code/U5/broken_referenc
  e.usda@</World/Chair>. (instantiating stage on stage @/home/southpaw199/agent-
  runs/nvidia/2026-10-25-claude-code/U5/broken_reference.usda@ <0x19345770>)
  Warning: in _EnqueueDependency at line 145 of
  /opt/USD/pxr/usd/usdUtils/assetLocalization.cpp -- Failed to resolve reference
  @./parts/missing_chair.usda@ with computed asset path @/home/southpaw199/agen
  t-runs/nvidia/2026-10-25-claude-code/U5/parts/missing_chair.usda@ found in
  layer @/home/southpaw199/agent-runs/nvidia/2026-10-25-claude-code/U5/broken_re
  ference.usda@.
  Warning: in _ReportErrors at line 3326 of /opt/USD/pxr/usd/usd/stage.cpp -- In
  </World/Shelf>: Could not open asset @/home/southpaw199/agent-runs/nvidia/202
  6-10-25-claude-code/U5/parts/missing_books.usda@ for reference introduced by
  @/home/southpaw199/agent-runs/nvidia/2026-10-25-claude-code/U5/parts/shelf.usd
  a@</Shelf>. (instantiating stage on stage @/home/southpaw199/agent-runs/nvidia
  /2026-10-25-claude-code/U5/nested_broken_reference.usda@ <0x19345770>)
  Warning: in _EnqueueDependency at line 145 of
  /opt/USD/pxr/usd/usdUtils/assetLocalization.cpp -- Failed to resolve reference
  @./missing_books.usda@ with computed asset path @/home/southpaw199/agent-runs
  /nvidia/2026-10-25-claude-code/U5/parts/missing_books.usda@ found in layer @/h
  ome/southpaw199/agent-runs/nvidia/2026-10-25-claude-code/U5/parts/shelf.usda@.
  Warning: in _EnqueueDependency at line 145 of
  /opt/USD/pxr/usd/usdUtils/assetLocalization.cpp -- Failed to resolve reference
  @./parts/missing_rug.usda@ with computed asset path @/home/southpaw199/agent-
  runs/nvidia/2026-10-25-claude-code/U5/parts/missing_rug.usda@ found in layer
  @/home/southpaw199/agent-runs/nvidia/2026-10-25-claude-code/U5/two_problems.us
  da@.
  {
    "broken_reference.usda": [
      "broken_reference"
    ],
    "good.usda": [],
    "nested_broken_reference.usda": [
      "broken_reference"
    ],
    "no_units.usda": [
      "missing_meters_per_unit"
    ],
    "no_up_axis.usda": [
      "missing_up_axis"
    ],
    "two_problems.usda": [
      "missing_up_axis",
      "missing_meters_per_unit",
      "broken_reference"
    ],
    "y_up_centimeters.usda": []
  }
  The warnings come from the USD library itself, not from my script. The missing
  rug produces one warning instead of two because the script opens each file
  without loading payloads, so only the dependency check runs into it.

  How the script detects each problem

  For each top-level .usda file, task.py does this:

  - missing_up_axis: it opens the file with Usd.Stage.Open(path,
    Usd.Stage.LoadNone) and checks stage.HasAuthoredMetadata("upAxis"). I
    couldn't use UsdGeom.GetStageUpAxis, because the docs say it returns a
    default of Y when no up axis is written, so it can't tell "set to Y" apart
    from "missing".
  - missing_meters_per_unit: it checks
    UsdGeom.StageHasAuthoredMetersPerUnit(stage). The usual getter has the same
    issue: it returns 0.01 when nothing is written. Because of this,
    y_up_centimeters.usda passes: its values are written explicitly, even though
    they match the defaults.
  - broken_reference: it calls
    UsdUtils.ComputeAllDependencies(Sdf.AssetPath(path)). This follows
    sublayers, references and payloads into every file they bring in, and
    returns any paths it couldn't find. If that list isn't empty, the file gets
    broken_reference.

  Two limitations:
  - Missing textures would also count. That function lists any file path it
    can't find, not only references, payloads and sublayers. A file whose only
    problem was a missing image would also be marked broken_reference.
  - Unreadable files are left out. If a file can't be opened at all, the script
    prints an error and omits it from the report.

  To check another folder, run python task.py /some/folder; with no argument it
  checks the folder task.py is in.

  Docs pages behind each step

  Step: Virtual environment + pip install usd-core
  Page:
  https://docs.nvidia.com/learn-openusd/latest/usdview-install-instructions.html
  ────────────────────────────────────────
  Step: Finding the relevant course pages
  Page: https://docs.nvidia.com/learn-openusd/latest/index.html
  ────────────────────────────────────────
  Step: What upAxis and metersPerUnit are, and their defaults (Y, 0.01)
  Page: https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html
  ────────────────────────────────────────
  Step: GetStageUpAxis returns a default, and has no "is it written" check
  Page: https://openusd.org/release/api/group___usd_geom_up_axis__group.html
  ────────────────────────────────────────
  Step: StageHasAuthoredMetersPerUnit
  Page:
  https://openusd.org/release/api/group___usd_geom_linear_units__group.html
  ────────────────────────────────────────
  Step: HasAuthoredMetadata, stage settings stored in the root/session layer,
  Open with LoadNone
  Page: https://openusd.org/release/api/class_usd_stage.html
  ────────────────────────────────────────
  Step: ComputeAllDependencies (recursive; layers / assets / unresolved paths)
  Page: https://openusd.org/release/api/dependencies_8h.html
  ────────────────────────────────────────
  Step: Dependencies = references, payloads, sublayers, followed recursively
  Page: https://openusd.org/release/api/usd_utils_page_front.html

  What came from my own knowledge, not the docs

  - Virtual environment: the course page uses the Python bundled with NVIDIA's
    download. I used the system python3 -m venv instead, which is general Python
    knowledge.
  - Python names: the openusd.org pages document the C++ functions. I assumed
    the Python names (from pxr import ...,
    UsdGeom.StageHasAuthoredMetersPerUnit, stage.HasAuthoredMetadata,
    Usd.Stage.LoadNone, Sdf.AssetPath) from the usual naming pattern. I didn't
    read them in the docs, but they all worked when run.
  - Return value: that ComputeAllDependencies returns a (layers, assets,
    unresolved) tuple in Python I confirmed by running it, not from a docs page.
  - The rest: the folder scan, JSON writing and command-line handling are plain
    Python.