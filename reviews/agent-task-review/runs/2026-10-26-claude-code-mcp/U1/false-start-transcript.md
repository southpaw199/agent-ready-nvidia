
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

● I'll start by loading the web fetch and USD MCP tools.

  Ran 1 shell command (ctrl+o to expand)

● I'll create the venv and install usd-core while I read the docs.

  Ran 1 shell command (ctrl+o to expand)
  ⎿  Interrupted · What should Claude do instead?

● Fetch(https://docs.nvidia.com/learn-openusd/latest/stage-setting/units-scale-u
       p-axis.html)
  ⎿  Interrupted · What should Claude do instead?

● Fetch(https://openusd.org/release/api/class_usd_geom_cube.html)
  ⎿  Interrupted · What should Claude do instead?