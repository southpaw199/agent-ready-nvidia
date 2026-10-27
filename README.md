# Case study: NVIDIA OpenUSD, Omniverse, and Isaac Sim

**Status: in progress.** Tier 1 is done, including a rerun with NVIDIA's USD Code MCP server, and its report is published; Tiers 2 and 3 are next.

Part of [agent-ready-docs](https://github.com/southpaw199/agent-ready-docs), which tests whether documentation works for AI agents as well as for people.

This case study applies the [agent task review](https://github.com/southpaw199/agent-ready-docs/blob/main/methods/agent-task-review/method.md) to three related doc sets: [OpenUSD](https://openusd.org) with NVIDIA's [Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/) course, [Omniverse](https://docs.omniverse.nvidia.com), and [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com). It runs in three tiers:

| Tier | What the agents do | Docs |
| --- | --- | --- |
| 1 | Hands-on OpenUSD tasks U1 to U5, run on a CPU with the `usd-core` package from PyPI, then run again with NVIDIA's USD Code MCP server available | openusd.org and Learn OpenUSD |
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

Agents: Claude Code 2.1.310 (claude-opus-5-5) and Codex CLI 0.164.0 (GPT-6.1-Sol, reasoning "low"), run on October 25, 2026, with usd-core 26.11, under [method](https://github.com/southpaw199/agent-ready-docs/blob/v0.2/methods/agent-task-review/method.md) version 0.2.

### What the docs do well

- **Composition, without being named.** U2's prompt asked only for "a second layer … so that its opinion is stronger", and both agents found sublayers on their own: Claude Code from Learn OpenUSD's [Working with Sublayers](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/sublayers/working-with-sublayers.html) exercise, Codex from the SdfLayer reference and Learn OpenUSD's strength ordering lesson. Both then explained correctly why the override wins.
- **Strength ordering.** Learn OpenUSD's [LIVERPS page](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/strength-ordering/what-is-liverps.html), its strength ordering lesson, and the openusd.org [glossary](https://openusd.org/release/glossary.html) all state the order plainly. The agents cited them in U2 and U3 to explain which opinion wins, and both explanations were right each time.
- **Changing a stage without saving it.** For U3, Claude Code found the session layer on Learn OpenUSD's [edit targets page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/edit-targets-layer-muting.html), which says `Usd.Stage.Save()` "deliberately does not write it to disk". Codex reached the same result another way. Neither saved red by mistake.
- **Instancing and its costs.** openusd.org's [Scenegraph Instancing](https://openusd.org/release/api/_usd__page__scenegraph_instancing.html) page explains both the saving and the limits, such as overrides beneath an instance being "silently ignored". Both agents' U4 explanations drew on it, and neither claimed a speedup its own timings didn't show.
- **Fallbacks that would hide a mistake.** The Learn OpenUSD [units page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html) and the openusd.org [up axis page](https://openusd.org/release/api/group___usd_geom_up_axis__group.html) state what an unauthored up axis or unit falls back to. Both agents set the metadata in U1 and, in U5, checked whether it was authored rather than what value it had.
- **Exact API notes.** The [Cube page](https://openusd.org/release/api/class_usd_geom_cube.html) says "If you author size you must also author extent", and both agents did. The release [Hello World tutorial](https://openusd.org/release/tut_helloworld.html) says "Tested with USD 26.11", the version pip installed.

### Main findings

Severity uses the scale defined in the [report](reviews/agent-task-review/report.md#main-findings). No finding about the docs is High.

#### 1. The API reference doesn't show Python names

| ID | Severity | Seen with |
| --- | --- | --- |
| F2 | Medium | Both agents, in nine of the ten runs |

The openusd.org API reference shows C++ only, so again and again both agents translated it into Python themselves: `UsdTimeCode::Default()` into `Usd.TimeCode.Default()`, `GetSubLayerPaths()` into `subLayerPaths`, `ArGetResolver()` into `Ar.GetResolver()`, and so on. Their translations were right, and the code ran. Claude Code said which names came from memory; Codex said, in all five tasks, that everything came from the docs. An agent with weaker prior knowledge would find nothing on those pages to check its guesses against.

**Suggested fix:** add a short page to the openusd.org [Developer Guides](https://openusd.org/dev/api/_developer__guides.html) on how C++ names map to Python, and link it from the API reference and the Learn OpenUSD Python examples. *We haven't found such a page; the Developer Guides and Coding Guidelines don't cover Python.*

#### 2. usd-core's built-in validators are off the path

| ID | Severity | Seen with |
| --- | --- | --- |
| F3 | Medium | Both agents |

usd-core 26.11 ships validators for exactly U5's checks (`usdGeomValidators:StageMetadataChecker` and `usdUtilsValidators:MissingReferenceValidator`), but neither agent found them. Both wrote correct checks of their own instead. Learn OpenUSD's validation exercise uses the `usdchecker` command-line tool, which the usd-core pip package doesn't install, and openusd.org documents `UsdValidation` in C++ only.

**Suggested fix:** link the validators from the stage metadata pages and from Learn OpenUSD's validation exercise, with a Python example that runs on usd-core alone.

### Minor findings

| ID | Finding | Severity | Suggested fix |
| --- | --- | --- | --- |
| F1 | **The usd-core install steps live inside the usdview page.** Learn OpenUSD's only `pip install usd-core` instructions come after downloading NVIDIA's prebuilt binaries. | Low | A short standalone section for installing usd-core with pip. |
| F4 | **No `llms.txt` at openusd.org.** It returns 404, and so does `docs.nvidia.com/learn-openusd` without `/latest/`. Learn OpenUSD does have an [`llms.txt`](https://docs.nvidia.com/learn-openusd/llms.txt), but neither agent looked for one in any task. | Low | Publish an `llms.txt` at openusd.org, and redirect `docs.nvidia.com/learn-openusd` to `/latest/`. |
| F5 | **API pages don't say which version they describe.** Pages under `/dev/` and `/release/` show no version number, and searches also turn up older sets such as `/22.08/`. Claude Code cited `/dev/` pages in U1 and U2. | Low | Show the release number in the API page header, as the tutorials already do. |
| F6 | **No documented way to tell whether an up axis is authored.** The units API has a function for this, but the up axis API doesn't. Both agents found another way in U5. | Low | One line on the up axis page pointing to `stage.HasAuthoredMetadata("upAxis")`. |

### How the two agents differed

Claude Code explained more, including what it wasn't sure of, but twice said something wasn't documented when a page it had read covered it: the usd-core install steps (U1) and how relative paths resolve (U2). Codex never flagged its own guesses.

## Results: Tier 1 with NVIDIA's USD Code MCP server

NVIDIA's [USD Code MCP](https://github.com/NVIDIA-Omniverse/kit-usd-agents/tree/4ce780d659078e7e7c12448778d3b05c842e6ffb/source/mcp/usd_code_mcp) server answers questions about the OpenUSD API and finds code examples. To see whether it helps, both agents ran the same five tasks again with the server available. The tasks, prompts, checkers, and scoring were unchanged. The agents were told the server was available, but not told to use it.

**Both used it in all ten runs, and the outcomes barely changed.** Nine runs passed with issues, and one, Codex on U3, passed cleanly, the only clean pass in the review. The server's method lookups were accurate and filled some of the Python gaps, but finding 1 still recurred in nine of the ten runs. Its search tools returned results too large to use whole, and some were wrong or came from other sites, though no agent relied on those.

| Task | Claude Code, docs only / with MCP | Codex, docs only / with MCP |
| --- | --- | --- |
| U1 | Pass with issues / Pass with issues | Pass with issues / Pass with issues |
| U2 | Pass with issues / Pass with issues | Pass with issues / Pass with issues |
| U3 | Pass with issues / Pass with issues | Pass with issues / **Pass** |
| U4 | Pass with issues / Pass with issues | Pass with issues / Pass with issues |
| U5 | Pass with issues / Pass with issues | Pass with issues / Pass with issues |

Rerun on October 26, 2026, with the same agents and usd-core version, under [method](https://github.com/southpaw199/agent-ready-docs/blob/v0.3/methods/agent-task-review/method.md) version 0.3, with the server at commit `4ce780d`.

### Server findings

These are candidates, about the server rather than the docs, sorted by severity.

| ID | Finding | Severity | Suggested fix |
| --- | --- | --- | --- |
| F9 | **A world bounding-box example ignores the transform.** An agent that copied the top result would report the wrong box. | High | Print `ComputeAlignedRange()`, which applies the transform, as other examples in the same result already do. |
| F11 | **displayColor examples author the wrong attribute.** 8 of 35 examples in one result leave the object uncolored. | High | Correct or remove those examples, so every displayColor example authors the `primvars:displayColor` primvar. |
| F7 | **The README's quickstart fails on a stock Ubuntu 24.04 system**, in four separate ways. | Medium | Fix the scripts' permissions and the build, and list every prerequisite, including Poetry. |
| F13 | **Examples from Windows test code.** Most examples in one result build paths under `C:/usd/`, and the top sublayer example adds the wrong layer. | Medium | Use relative or temporary paths, and fix the top sublayer example. |
| F8 | **The README gives two tool counts**, 7 and 34; the server has 7. | Low | Give one count. |
| F10 | **Method lookups can return the wrong methods.** | Low | Match method names exactly within the requested class, and label each result with its class. |
| F12 | **Search results are too large to use**, at 45,000 to 66,000 tokens each. | Low | Return fewer examples by default, with a way to ask for more. |
| F14 | **Sources beyond the official docs.** Knowledge results mix openusd.org with third-party sites, even when asked not to. | Low | Label each entry's source, and offer a way to limit results to official docs. |

## Read more

These results come from one run per agent per task, in each condition, and are a signal, not a verdict. **[Read the Tier 1 report](reviews/agent-task-review/report.md)** for the full findings, suggested fixes, the MCP comparison, how the two agents compared, and the limitations. The [run log](reviews/agent-task-review/run-log.csv) has a row per run, the [findings log](reviews/agent-task-review/findings.md) has the evidence for each finding, and the [runs](reviews/agent-task-review/runs/) folder has each agent's code and transcript.

## Use of AI tools

AI coding assistants helped draft code and content in this repo. I ran, tested, and verified every example and every finding myself. Agent outputs are evidence to check, not results to trust.

## License

Created by Alan Sloan ([LinkedIn](https://www.linkedin.com/in/alansloan)).

- **Code** (Python files, notebooks, and workflows) is licensed under the [MIT License](LICENSE).
- **Written content** (methods, reports, findings, task definitions, and READMEs) is © 2026 Alan Sloan. All rights reserved: you may read and link to it, but not copy, republish, or adapt it without permission. See [COPYRIGHT.md](COPYRIGHT.md).
- **Agent transcripts** in the `runs/` folders are records of each agent's output, included as evidence.
