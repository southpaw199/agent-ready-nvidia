# Case study: NVIDIA OpenUSD, Omniverse, and Isaac Sim

**Status: in progress.** Tier 1 is done, and its report is published; Tiers 2 and 3 are next.

This case study applies the [agent task review](../../methods/agent-task-review/method.md) to three related doc sets: [OpenUSD](https://openusd.org) with NVIDIA's [Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/) course, [Omniverse](https://docs.omniverse.nvidia.com), and [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com). It runs in three tiers:

| Tier | What the agents do | Docs |
| --- | --- | --- |
| 1 | Hands-on OpenUSD tasks U1 to U5, run on a CPU with the `usd-core` package from PyPI | openusd.org and Learn OpenUSD |
| 2 | Answer a set of 20 questions from the docs, with citations. Omniverse and Isaac Sim need an RTX GPU to run, so this tier is questions only. | Omniverse and Isaac Sim |
| 3 | Answer the Isaac Sim setup questions from Tier 2 again with NVIDIA's `install-isaacsim` agent skill loaded, for comparison | Isaac Sim |

| Folder | What it holds |
| --- | --- |
| [`reviews/agent-task-review/`](reviews/agent-task-review/) | Tasks, success criteria, reference results, the run log, and findings. |

## Results: Tier 1

Two AI coding agents, Claude Code and Codex, each attempted five OpenUSD tasks using only openusd.org and Learn OpenUSD. **Both completed all five correctly, with no hints**, and the reviewer's own reruns of their code passed every check, including a rerun of each agent's U5 validator on files it had never seen. All ten runs are scored "pass with issues", mainly because both agents used Python API names that appear on none of the pages they read.

| Task | What the agent had to do | Claude Code | Codex |
| --- | --- | --- | --- |
| U1 | Set the stage's units and up axis, define a default prim, and place a red cube on the ground; save, reopen, and report the bounds | Pass with issues | Pass with issues |
| U2 | Reference two assets, override one's color in a separate, stronger layer, and explain which opinion wins | Pass with issues | Pass with issues |
| U3 | Give a referenced asset a color variant set, and switch to red in code without changing the saved file | Pass with issues | Pass with issues |
| U4 | Place 1,000 crates by plain reference and with instancing, compare them, and explain the tradeoff | Pass with issues | Pass with issues |
| U5 | Write a script that flags missing stage metadata and broken references in any folder of .usda files | Pass with issues | Pass with issues |

Agents: Claude Code 2.1.310 (claude-opus-5-5) and Codex CLI 0.164.0 (GPT-6.1-Sol, reasoning "low"), run on October 25, 2026, with usd-core 26.11, under [method](../../methods/agent-task-review/method.md) version 0.2.

### What the docs do well

- **Composition, without being named.** U2's prompt asked only for "a second layer … so that its opinion is stronger", and both agents found sublayers on their own: Claude Code from Learn OpenUSD's [Working with Sublayers](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/sublayers/working-with-sublayers.html) exercise, Codex from the SdfLayer reference and Learn OpenUSD's strength ordering lesson. Both then explained correctly why the override wins.
- **Strength ordering.** Learn OpenUSD's [LIVERPS page](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/strength-ordering/what-is-liverps.html), its strength ordering lesson, and the openusd.org [glossary](https://openusd.org/release/glossary.html) all state the order plainly. The agents cited them in U2 and U3 to explain which opinion wins, and both explanations were right each time.
- **Changing a stage without saving it.** For U3, Claude Code found the session layer on Learn OpenUSD's [edit targets page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/edit-targets-layer-muting.html), which says `Usd.Stage.Save()` "deliberately does not write it to disk". Codex reached the same result another way. Neither saved red by mistake.
- **Instancing and its costs.** openusd.org's [Scenegraph Instancing](https://openusd.org/release/api/_usd__page__scenegraph_instancing.html) page explains both the saving and the limits, such as overrides beneath an instance being "silently ignored". Both agents' U4 explanations drew on it, and neither claimed a speedup its own timings didn't show.
- **Fallbacks that would hide a mistake.** The Learn OpenUSD [units page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html) and the openusd.org [up axis page](https://openusd.org/release/api/group___usd_geom_up_axis__group.html) state what an unauthored up axis or unit falls back to. Both agents set the metadata in U1 and, in U5, checked whether it was authored rather than what value it had.
- **Exact API notes.** The [Cube page](https://openusd.org/release/api/class_usd_geom_cube.html) says "If you author size you must also author extent", and both agents did. The release [Hello World tutorial](https://openusd.org/release/tut_helloworld.html) says "Tested with USD 26.11", the version pip installed.

### Main findings

**1. Python names aren't documented.** The openusd.org API reference shows C++ only, so again and again both agents translated it into Python themselves: `UsdTimeCode::Default()` into `Usd.TimeCode.Default()`, `GetSubLayerPaths()` into `subLayerPaths`, `ArGetResolver()` into `Ar.GetResolver()`, and so on. Their translations were right, and the code ran. Claude Code said which names came from memory; Codex said, in all five tasks, that everything came from the docs. An agent with weaker prior knowledge would find nothing on those pages to check its guesses against. **Suggested fix:** add a short page to the openusd.org [Developer Guides](https://openusd.org/dev/api/_developer__guides.html) on how C++ names map to Python, and link it from the API reference and the Learn OpenUSD Python examples. *No such page has been found; this is still being verified.*

**2. usd-core's built-in validators are off the path.** usd-core 26.11 ships validators for exactly U5's checks (`usdGeomValidators:StageMetadataChecker` and `usdUtilsValidators:MissingReferenceValidator`), but neither agent found them. Both wrote correct checks of their own instead. Learn OpenUSD's validation exercise uses the `usdchecker` command-line tool, which the usd-core pip package doesn't install, and openusd.org documents `UsdValidation` in C++ only. **Suggested fix:** link the validators from the stage metadata pages and from Learn OpenUSD's validation exercise, with a Python example that runs on usd-core alone.

### Observations

- **Finding the docs.** openusd.org has no `llms.txt` (404), and `docs.nvidia.com/learn-openusd` without `/latest/` returns 404. Learn OpenUSD does have an [`llms.txt`](https://docs.nvidia.com/learn-openusd/llms.txt), but neither agent looked for one in any task.
- **Which version of the docs.** openusd.org's API pages under `/dev/` and `/release/` show no version number, and searches also turn up older sets such as `/22.08/` and `/25.11/`. Claude Code cited `/dev/` API pages in U1 and U2 and `/release/` pages after that; Codex cited `/release/` throughout. None of them cited an older set.
- **An agent's "it's not in the docs" needs checking too.** Twice, Claude Code said something wasn't documented when a page it had read covered it: the usd-core install steps (U1) and how relative paths resolve (U2).

These results come from one run per agent per task and are a signal, not a verdict. **[Read the Tier 1 report](reviews/agent-task-review/report.md)** for the findings, including four minor ones, suggested fixes, how the two agents compared, and the limitations. The [run log](reviews/agent-task-review/run-log.csv) has a row per run, the [findings log](reviews/agent-task-review/findings.md) has the evidence for each finding, and the [runs](reviews/agent-task-review/runs/) folder has each agent's code and transcript.
