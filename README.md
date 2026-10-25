# Case study: NVIDIA OpenUSD, Omniverse, and Isaac Sim

**Status: in progress.** Tier 1 task U1 is done; U2 to U5, then Tiers 2 and 3, are next.

This case study applies the [agent task review](../../methods/agent-task-review/method.md) to three related doc sets: [OpenUSD](https://openusd.org) with NVIDIA's [Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/) course, [Omniverse](https://docs.omniverse.nvidia.com), and [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com). It runs in three tiers:

| Tier | What the agents do | Docs |
| --- | --- | --- |
| 1 | Hands-on OpenUSD tasks U1 to U5, run on a CPU with the `usd-core` package from PyPI | openusd.org and Learn OpenUSD |
| 2 | Answer a set of 20 questions from the docs, with citations. Omniverse and Isaac Sim need an RTX GPU to run, so this tier is questions only. | Omniverse and Isaac Sim |
| 3 | Answer the Isaac Sim setup questions from Tier 2 again with NVIDIA's `install-isaacsim` agent skill loaded, for comparison | Isaac Sim |

| Folder | What it holds |
| --- | --- |
| [`reviews/agent-task-review/`](reviews/agent-task-review/) | Tasks, success criteria, reference results, the run log, and findings. |

## Results so far: Tier 1, task U1

Two AI coding agents, Claude Code and Codex, each built the same small OpenUSD scene using only openusd.org and Learn OpenUSD: a Z-up stage in meters, with a red 4-meter cube resting on the ground, saved and read back from disk. **Both got it right, with no hints**, and the reviewer's own reruns of their code passed every check. Both are scored "pass with issues", because each used Python API names that appear on none of the pages it read.

| Task | What the agent had to do | Claude Code | Codex |
| --- | --- | --- | --- |
| U1 | Set the stage's units and up axis, define a default prim, and place a red cube on the ground; save, reopen, and report the bounds | Pass with issues | Pass with issues |

Agents: Claude Code 2.1.310 (claude-opus-5-5) and Codex CLI 0.164.0 (GPT-6.1-Sol, reasoning "low"), run on October 25, 2026, with usd-core 26.11, under [method](../../methods/agent-task-review/method.md) version 0.2.

### What the docs do well

- **Stage units and up axis.** The Learn OpenUSD [units page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html) shows the Python calls and states the fallbacks if they're left out: Y-up and centimeters. Both agents set both values from that page, so neither produced a scene lying on the wrong axis.
- **Extent.** The [Cube API page](https://openusd.org/release/api/class_usd_geom_cube.html) says "If you author size you must also author extent." Both agents cited it and authored a matching extent, so anything that reads the extent attribute sees a 4-meter cube, not the 2-meter default.
- **Placing the cube.** The same page says the cube is "centered at the origin". Both agents worked out from that that the cube must be raised 2 meters to rest on the ground.
- **Versioned tutorials.** The release [Hello World tutorial](https://openusd.org/release/tut_helloworld.html) says "Tested with USD 26.11", the version pip installed.

### Main finding so far: Python names aren't documented

The openusd.org API reference shows C++ only, so both agents had to translate it into Python themselves: `UsdTimeCode::Default()` into `Usd.TimeCode.Default()`, for example, and `UsdGeomTokens->default_` into `UsdGeom.Tokens.default_`. Their translations were right, and the code ran. But Claude Code flagged these names as "from what I already knew", while Codex said all OpenUSD behavior came from the docs. An agent with weaker prior knowledge would find nothing on those pages to check its guesses against.

**Suggested fix:** add a short page to the openusd.org [Developer Guides](https://openusd.org/dev/api/_developer__guides.html) on how C++ names map to Python, and link it from the API reference and the Learn OpenUSD Python examples. *We haven't found such a page yet, so this is still being verified.*

### Observations to watch in later tasks

- **Finding the docs.** openusd.org has no `llms.txt` (404), and `docs.nvidia.com/learn-openusd` without `/latest/` returns 404. Learn OpenUSD does have an [`llms.txt`](https://docs.nvidia.com/learn-openusd/llms.txt), but neither agent looked for one.
- **Which version of the API reference.** Claude Code, finding pages by search, cited openusd.org's `/dev/` API pages; Codex, typing URLs itself, cited `/release/`. The API pages under both show no version number, so an agent can't tell which release a page describes.

These results come from one run per agent and are a signal, not a verdict. The [run log](reviews/agent-task-review/run-log.csv) has a row per run, the [findings log](reviews/agent-task-review/findings.md) has the evidence for each finding, and the [runs](reviews/agent-task-review/runs/) folder has each agent's code and transcript. A full report will follow when Tier 1 is complete.
