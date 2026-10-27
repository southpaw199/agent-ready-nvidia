# NVIDIA OpenUSD: agent task review report, Tier 1

**Author:** Alan Sloan · [linkedin.com/in/alansloan](https://www.linkedin.com/in/alansloan) · [github.com/southpaw199](https://github.com/southpaw199)

- **Method:** [agent task review](../../../../methods/agent-task-review/method.md), version 0.2 for the docs-only runs, and 0.3 for the reruns with NVIDIA's MCP server
- **Agents:** Claude Code 2.1.310 (claude-opus-5-5) and Codex CLI 0.164.0 (GPT-6.1-Sol, reasoning "low")
- **Runs:** October 25, 2026, against the live docs at [openusd.org](https://openusd.org) and NVIDIA's [Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/), with usd-core 26.11 from PyPI on Python 3.12.3. Rerun on October 26, 2026, with NVIDIA's [USD Code MCP](https://github.com/NVIDIA-Omniverse/kit-usd-agents/tree/4ce780d659078e7e7c12448778d3b05c842e6ffb/source/mcp/usd_code_mcp) server also available (commit `4ce780d`, Docker image `360aaf4962b4`).
- **Findings checked against the live docs:** October 25, 2026; the MCP server's results, against usd-core 26.11 and the live docs, on October 26, 2026
- **Scope:** Tier 1, five hands-on OpenUSD tasks that run on a CPU. Omniverse and Isaac Sim, which need an RTX GPU, are covered by the question set in Tiers 2 and 3.

## Summary

Two AI coding agents from different companies each attempted the same five OpenUSD tasks, using only openusd.org and Learn OpenUSD. **Both completed all five correctly, with no hints.** The tasks ran from a first stage to composition, variant sets, instancing, and a script that validates files. Every result was confirmed by rerunning the agent's final code in a clean folder, not by trusting its summary. For the last task, that included a rerun on a second set of files the agent never saw.

The docs carried the agents a long way. Neither agent was told to use sublayers, the session layer, or instancing, and both found them. The problems showed up in *how* they got there. **The openusd.org API reference shows C++ only, so in nine of the ten runs the agents wrote Python names that appear on no page they read.** Their guesses were right, but one agent said so each time and the other said everything came from the docs. And **neither agent found the validators that usd-core ships** for exactly the checks the last task asked for.

| Task | What the agent had to do | Claude Code | Codex |
| --- | --- | --- | --- |
| U1 | Set the stage's units and up axis, define a default prim, and place a red cube on the ground; save, reopen, and report the bounds | Pass with issues | Pass with issues |
| U2 | Reference two assets, override one's color in a separate, stronger layer, and explain which opinion wins | Pass with issues | Pass with issues |
| U3 | Give a referenced asset a color variant set, and switch to red in code without changing the saved file | Pass with issues | Pass with issues |
| U4 | Place 1,000 crates by plain reference and with instancing, compare them, and explain the tradeoff | Pass with issues | Pass with issues |
| U5 | Write a script that flags missing stage metadata and broken references in any folder of .usda files | Pass with issues | Pass with issues |

"Pass with issues" means every success criterion was met, but the run relied on knowledge that isn't in the docs, or had a similar gap; see the [rubric](../../../../methods/agent-task-review/rubric.md). In this tier, that knowledge was almost always the Python spelling of an API the docs show only in C++.

**With NVIDIA's USD Code MCP server added**, the same agents ran the same tasks a second time. Both used the server without being told to, in all ten runs. The outcomes barely changed: nine runs passed with issues, and one, Codex on U3, passed cleanly. The server's method lookups were accurate and filled some of the Python gaps, but they didn't close finding 1, which recurred in nine of the ten runs. Its search tools returned results too large to use whole, and some were wrong or came from other sites, though no agent relied on those. See [With NVIDIA's USD Code MCP server](#with-nvidias-usd-code-mcp-server).

## What the docs do well

- **Composition, without being named.** U2 asked only for "a second layer … so that its opinion is stronger than the asset's", and both agents found sublayers on their own: Claude Code from Learn OpenUSD's [Working with Sublayers](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/sublayers/working-with-sublayers.html) exercise ("The first appended sublayer will have the highest opinion"), Codex from the SdfLayer reference and Learn OpenUSD's strength ordering lesson.
- **Strength ordering.** Learn OpenUSD's [LIVERPS page](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/strength-ordering/what-is-liverps.html), its strength ordering lesson, and the openusd.org [glossary](https://openusd.org/release/glossary.html) state the order plainly. Both agents explained correctly why the override wins in U2 and why variant opinions beat the referenced asset in U3.
- **Changing a stage without saving it.** U3 asked for a switch to red that leaves the saved file selecting blue. Claude Code found the session layer on Learn OpenUSD's [edit targets page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/edit-targets-layer-muting.html), which says `Usd.Stage.Save()` "deliberately does not write it to disk". Codex reached the same result another way. Neither saved red by mistake.
- **Instancing, with its costs.** openusd.org's [Scenegraph Instancing](https://openusd.org/release/api/_usd__page__scenegraph_instancing.html) page explains both the saving ("This reduces the size of the scenegraph") and the limits (overrides beneath an instance "will be silently ignored"). Both agents' U4 explanations were right, and neither claimed a speedup its own timings didn't show: Claude Code called them "too noisy to compare", Codex "single measurements, not a benchmark". That matches the reference run, where the two files opened in about the same time at this scale.
- **Fallbacks that would hide a mistake.** The Learn OpenUSD [units page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html) and the openusd.org [up axis page](https://openusd.org/release/api/group___usd_geom_up_axis__group.html) say what an unauthored up axis or unit falls back to. Both agents authored the metadata in U1, and in U5 both checked whether it was authored rather than what value it had, so a Y-up file in centimeters wasn't flagged by mistake.
- **Learn OpenUSD's Python examples.** Where an agent reached a Learn OpenUSD page, it found working Python: units, default prims, references, sublayers, edit targets, variant sets. The Python gaps in finding 1 come from the openusd.org API reference, not from the course.
- **Precise API notes.** The [Cube page](https://openusd.org/release/api/class_usd_geom_cube.html) says "If you author size you must also author extent", and both agents did. The release [Hello World tutorial](https://openusd.org/release/tut_helloworld.html) says "Tested with USD 26.11", the version pip installed.

## Main findings

Severity: **High** means an agent following the docs would fail or get a wrong result; **Medium**, the task succeeds, but only with knowledge the docs don't give or by a route they don't point to; **Low**, friction or polish. No finding about the docs is High. Two of the MCP server's candidate findings are, in [Server findings](#server-findings).

### 1. The API reference doesn't show Python names (F2)

**Medium. Seen with both agents, in nine of the ten runs.**

The openusd.org API reference is generated from the C++ source, so it shows C++ signatures only. Agents writing Python have to translate the names themselves, and the patterns aren't uniform:

| C++, on the API page | Python, in the agents' code |
| --- | --- |
| `UsdTimeCode::Default()` | `Usd.TimeCode.Default()` |
| `UsdGeomTokens->default_` | `UsdGeom.Tokens.default_` |
| `UsdGeomSetStageUpAxis()` | `UsdGeom.SetStageUpAxis()` |
| `SdfLayer::GetSubLayerPaths()` | `layer.subLayerPaths` |
| `SdfLayer::GetPseudoRoot()` | `layer.pseudoRoot` |
| `ArGetResolver()` | `Ar.GetResolver()` |
| `UsdGeomGprim(const UsdPrim&)` | `UsdGeom.Gprim(prim)` |

**What happened:** every translation was right, and the code ran. Claude Code listed which names came from memory, and in U5 wrote that it "assumed the Python names … from the usual naming pattern". Codex said in all five tasks that all OpenUSD behavior came from the docs, while using names that appear on none of the pages it downloaded. Learn OpenUSD's Python examples cover some of these names, but the agents reached the API reference for most of their work. An agent with weaker prior knowledge would find nothing on those pages to check its guesses against.

**Suggested fix:** add a short page to the openusd.org [Developer Guides](https://openusd.org/dev/api/_developer__guides.html) on how C++ names map to Python, covering library prefixes, free functions, tokens, and properties, and link it from the API reference's front page and from the Learn OpenUSD Python examples. *We haven't found such a page; the Developer Guides and Coding Guidelines don't cover Python.*

### 2. usd-core's built-in validators are off the path (F3)

**Medium. Seen with both agents.**

usd-core 26.11 includes the `UsdValidation` framework, with built-in validators for exactly what U5 asked for: `usdGeomValidators:StageMetadataChecker` reports a missing up axis or units, and `usdUtilsValidators:MissingReferenceValidator` reports unresolvable references, payloads, and sublayers. The older `UsdUtils.ComplianceChecker` is gone from the library, and its page returns 404. But nothing either agent read led to the validators:

- Learn OpenUSD's [validation exercise](https://docs.nvidia.com/learn-openusd/latest/data-exchange/asset-validation/exercise-asset-validation-testing.html) uses the `usdchecker` command-line tool, which the usd-core pip package doesn't install.
- openusd.org's `UsdValidation` pages, such as [UsdValidationRegistry](https://openusd.org/release/api/class_usd_validation_registry.html), are C++ only, with no Python example.
- None of the API pages the agents used for U5, on stage metadata, layers, and dependencies, mentions the validators.

**What happened:** both agents wrote correct checks of their own instead: Claude Code with `HasAuthoredMetadata` and `UsdUtils.ComputeAllDependencies`, Codex by walking the layers' sublayers, references, and payloads and resolving each path. Both passed on a holdout set of files neither had seen. Neither agent searched for a validation tool, so this shows that the validators weren't on their path, not that an agent looked and failed. Codex read a Learn OpenUSD page whose navigation links to the Asset Validation section, but that section leads to `usdchecker`.

**Suggested fix:** link the validators from the up axis, units, and dependency pages, and add a Python example to Learn OpenUSD's validation exercise that runs on usd-core alone, for example `UsdValidation.ValidationRegistry().GetOrLoadValidatorByName("usdGeomValidators:StageMetadataChecker").Validate(stage)`.

## Minor findings

- **F1. The usd-core install steps live inside the usdview page.** Learn OpenUSD's only `pip install usd-core` instructions are part of [Installing usdview and Setting Up Python](https://docs.nvidia.com/learn-openusd/latest/usdview-install-instructions.html), after downloading NVIDIA's prebuilt binaries. Neither agent needed them, because the task told them to install usd-core, and in U2 search found the page. *Fix:* a short standalone section for installing usd-core with pip.
- **F4. No `llms.txt` at openusd.org.** It returns 404, and so does Learn OpenUSD's address without `/latest/`, although Learn OpenUSD's own [`llms.txt`](https://docs.nvidia.com/learn-openusd/llms.txt) works. Neither agent looked for one in any run, so this cost them nothing here. *Fix:* publish an `llms.txt` at openusd.org, and redirect `docs.nvidia.com/learn-openusd` to `/latest/`.
- **F5. API pages don't say which version they describe.** The openusd.org API reference under `/dev/` and `/release/` shows only a generation date, and searches also return older sets such as `/22.08/`. Claude Code cited `/dev/` pages for usd-core 26.11 in two tasks. Nothing went wrong, but a reader can't tell. *Fix:* show the release number in the API page header, as the tutorials already do.
- **F6. No documented way to tell whether an up axis is authored.** There's `UsdGeomStageHasAuthoredMetersPerUnit()` but no up axis equivalent, and the up axis page only says an unauthored axis returns the fallback. Both agents found another way in U5. *Fix:* one line on the up axis page pointing to `stage.HasAuthoredMetadata("upAxis")`.

The full evidence for each finding, with run references, is in the [findings log](findings.md).

## How the two agents differed

| | Claude Code | Codex |
| --- | --- | --- |
| Tasks passed, hints needed | 5 of 5, none | 5 of 5, none |
| Errors recovered from | 3 | 15, mostly its sandbox blocking the network until approved |
| Said which knowledge wasn't from the docs | In every task | In no task; said all OpenUSD behavior came from the docs |
| How it found pages | Web search limited to the two sites (U1, U2), then URLs it knew | URLs it typed itself, fetched with `curl` (web search was off) |
| Pages read per task | 8 to 15 | 7 to 11 |
| U3: switching without saving | The session layer | A freshly reopened stage, not saved |
| U5: route | Its own checks on a composed stage | Its own checks on raw layers |
| Typical time per task | 4 to 6 minutes | 3 to 6 minutes |

Both agents checked their own work beyond what was asked, such as checksums of the asset files and extra test cases. Claude Code explained more, including what it wasn't sure of; twice, though, it said something wasn't in the docs when a page it had read covered it (the install steps in U1, how relative paths resolve in U2). Codex never flagged its own guesses. The subject here is the docs, not the agents: the same gaps appear with both.

## With NVIDIA's USD Code MCP server

NVIDIA publishes MCP servers for its documentation, and [USD Code MCP](https://github.com/NVIDIA-Omniverse/kit-usd-agents/tree/4ce780d659078e7e7c12448778d3b05c842e6ffb/source/mcp/usd_code_mcp) answers questions about the OpenUSD API and finds code examples. Its 7 tools search a knowledge base and a code-example base, and look up modules, classes, and methods. To see whether it helps, both agents ran all five tasks again with the server available. The tasks, prompts, checkers, and scoring were unchanged. The only addition to the agent's instructions was one paragraph saying the server was available, and asking the agent to name the tool and query behind any step that relied on it. The agent wasn't told to use it. The server ran locally with its default settings, and was registered only in each run's folder. The [task file](tasks.md#docsmcp-standard-instructions) has the exact wording.

### Results

Each cell gives the docs-only run first, then the run with the server.

| Task | Agent | Outcome | Time (min) | Errors recovered | MCP calls | Pages cited / MCP results cited |
| --- | --- | --- | --- | --- | --- | --- |
| U1 | Claude Code | with issues / with issues | 6 / 8 | 1 / 2 | 3: code examples ×2, method lookup | 15 / 11, and 0 / 3 |
| U1 | Codex | with issues / with issues | 3 / 2 | 4 / 2 | 1: knowledge search | 10 / 9, and 0 / 0 |
| U2 | Claude Code | with issues / with issues | 4 / 5 | 2 / 1 | 2: code examples, method lookup | 11 / 6, and 0 / 2 |
| U2 | Codex | with issues / with issues | 5 / 2.5 | 2 / 2 | 2: knowledge search, code examples | 7 / 8, and 0 / 1 |
| U3 | Claude Code | with issues / with issues | 5 / 6 | 0 / 3 | 2: code examples, method lookup | 11 / 7, and 0 / 1 |
| U3 | Codex | with issues / **pass** | 3 / 1.5 | 2 / 2 | 2: knowledge search, method lookup | 7 / 3, and 0 / 1 |
| U4 | Claude Code | with issues / with issues | 5 / 3 | 0 / 1 | 2: method lookup ×2 | 12 / 8, and 0 / 2 |
| U4 | Codex | with issues / with issues | 6 / 1.5 | 3 / 2 | 1: knowledge search | 7 / 6, and 0 / 0 |
| U5 | Claude Code | with issues / with issues | 4 / 3.5 | 0 / 1 | 5: knowledge search ×2, method lookup ×3 | 8 / 7, and 0 / 3 |
| U5 | Codex | with issues / with issues | 4 / 1.5 | 4 / 2 | 1: knowledge search | 7 / 6, and 0 / 0 |

**Reading the table**
- **Outcome** uses the [rubric](../../../../methods/agent-task-review/rubric.md): "with issues" means pass-with-issues.
- **Time** is the session's length, from the prompt to the final answer. It includes the time spent waiting at approval prompts, so treat it as rough.
- **Errors recovered** counts commands or fetches that failed and were then retried or worked around. Most of Codex's errors came from its sandbox blocking the network until a command was approved.
- **MCP results cited** counts results an agent named as the source of a step.

**Tier 1 issues avoided, and new issues**
- **Finding 1, Python names from memory, recurred in nine of the ten runs.**
  - **Avoided once:** in Codex U3, every name came from the three openusd.org tutorials it read, which show the Python API, or from a method lookup it cited. That run is the only clean pass in the review.
  - **Partly avoided:** in Claude Code U2, `GetPropertyStack`, which Tier 1 had used from memory, came from a method lookup. Other names were still from memory.
  - **Undisclosed with Codex:** in four of its five runs, Codex again said nothing came from memory.
- **Finding 2, the validators, held with the server too.** Neither agent's U5 run reached `UsdValidation`, and the server's validation content pointed only to `usdchecker`, as the docs do. It never pointed to the removed `UsdUtils.ComplianceChecker`, which was the main version risk.
- **The issues that didn't occur in either condition still didn't occur:**
  - deprecated APIs and warnings the agent didn't report;
  - missing stage metadata or extent in U1.
- **One new issue came from the server.** Its search results were too large for Claude Code to pass to the agent, so Claude Code saved them to files outside the run folder. In U1 to U3, the agent read or tried to read them there, against its instructions (F12). Codex cut the same results short instead, and stayed in its folder.
- **No wrong result was relied on.** Every MCP result an agent cited held up against usd-core 26.11 or the live docs.

### What the server does well

- **Accurate method lookups.** Every `get_usd_method_detail` result an agent relied on matched usd-core 26.11, gave the Python name and signature, and was small enough to pass to the agent whole. That's what the API reference lacks (finding 1).
- **Used without prompting.** Both agents chose to use it in every task, 21 calls in all. Codex's queries even asked for the two allowed sites.
- **No outdated API.** In U5, it didn't suggest `ComplianceChecker`, which the server's older glossaries might have.

### Server findings

These are candidates, found while setting up the server or in the reruns. They're about the server, not the docs. The full evidence is in the [findings log](findings.md).

- **F12. Search results are too large to use.** Every `search_usd_code_examples` and `search_usd_knowledge` result was 45,000 to 66,000 tokens, or 70 to 120 KB, and up to 90 examples. Claude Code saved them outside the run folder and twice gave up on them. Codex passed the agent only the start. **Low.** *Fix:* return fewer examples by default, with a way to ask for more.
- **F9. A world bounding-box example ignores the transform.** The top result for a bounding-box query prints `GetRange()`, not `ComputeAlignedRange()`. On U1's scene, that puts the cube half below the ground. Claude Code noticed and didn't use it. **High, candidate:** an agent that copied it would report the wrong box.
- **F11. displayColor examples author the wrong attribute.** 8 of 35 examples in one result create a plain `displayColor` attribute, so the object isn't colored. **High, candidate:** copying one would fail U1's color check.
- **F13. Examples from Windows test code.** 57 of 88 examples in one result build paths under `C:/usd/`. The top sublayer example adds a missing path instead of the layer it created. **Medium, candidate.**
- **F14. Sources beyond the official docs.** Knowledge results mix openusd.org with GitHub repositories, including the third-party *VFX-UsdSurvivalGuide*, and Remedy Entertainment's *USD Book*. That held even when the query asked for the two allowed sites only. All five Codex sessions noticed and excluded them. **Low.**
- **F10. Method lookups can return the wrong methods.** In one call, two of three names returned other classes' methods. **Low.**
- **F7 and F8. Setup.** The README's quickstart fails four ways on a stock Ubuntu 24.04 system:
  - its scripts aren't executable;
  - Poetry is missing from the prerequisites;
  - `pip install --user` is blocked;
  - the health check needs `aiohttp`.

  The README also says both 7 and 34 tools; the server has 7. **Medium and Low.**

### Conclusions

Over ten runs per condition, adding the server didn't change whether the agents completed the tasks: every run in both conditions met every success criterion with no hints. Its method lookups were the most useful part, and gave the one clean pass, but they didn't close the Python gap in the docs, which recurred in nine of ten runs. Its search tools need work: their results were too large to use whole, and some were wrong or from other sites, though the agents relied on none of them. For the docs, the better fix is still finding 1's: a page on how C++ names map to Python.

## Limitations

- **Prior knowledge.** OpenUSD is old and widely used, so both models know it from training data, and each run tests the docs plus that knowledge. Requiring page citations reduces the effect, and checking every name against the pages cited is how finding 1 surfaced, but it doesn't remove it.
- **One run per agent per task.** Agents are non-deterministic. Treat each result as a signal, not a verdict.
- **Settings.** Codex ran at its default "low" reasoning setting and with web search off, because its search tool doesn't ask before each search. Claude Code could search, limited to the two sites. Different settings could change how each found pages.
- **Shared environment.** Three Claude Code sessions (U1, U3, U4) started from a terminal where another run's Python environment was still active. The session logs show no agent read anything in another run's folder, and every agent built its own environment, so no result is affected; the agents could see another folder's path, nothing more. The method now says to start each session from a clean terminal.
- **A repeated run.** Codex's first U3 attempt was discarded, because its session wasn't exported with the commands; its rerun had passed 11 of 11. U3 was run again from scratch, and the results here are the second attempt's. The [Codex run notes](runs/2026-10-25-codex/README.md) record it.
- **Caches.** The usd-core wheel was in the pip cache from earlier runs, so installs were faster than for a new user.
- **The MCP rerun.**
  - **Timing and order:** it ran a day later, with the same agent versions, models, settings, tasks, and checkers. Each rerun came after the same agent's docs-only run of that task, in a fresh session with memory off. The docs' entry points were rechecked that day and hadn't changed, but the pages weren't compared in full.
  - **One restart:** Claude Code's first U1 session was stopped before it read any page, and started again.
  - **Settings:** the server ran with its default settings, and result sizes may depend on settings that weren't tested.
- **Hardware.** Tier 1 covers only what runs on a CPU. Omniverse and Isaac Sim come in Tiers 2 and 3, as questions answered from the docs.
- **AI assistance.** Claude helped design the tasks, wrote the reference solutions and checkers, and helped draft this report. Claude is the same model family as one of the subject agents. The subject sessions saw only each task's prompt, never its success criteria, reference solution, checker, or this repository, and the session logs confirm they read nothing outside their own folders. The reviewer ran every reference solution and every checker test, and reran every agent's final code; every finding was checked against the live docs. Claude also ran the operator session for the MCP rerun, which checked every MCP result an agent relied on against usd-core 26.11 or the live docs.

## Files

- [Tasks, success criteria, and reference results](tasks.md), with the [reference solutions](reference/) and a checker and tests for each task
- [Run log](run-log.csv): one row per attempt
- [Findings log](findings.md): evidence, status, and severity for each finding
- Runs: [Claude Code](runs/2026-10-25-claude-code/) and [Codex](runs/2026-10-25-codex/), with each task's code, transcript, and the reviewer's rerun output and check results
- MCP reruns: [Claude Code](runs/2026-10-26-claude-code-mcp/) and [Codex](runs/2026-10-26-codex-mcp/), laid out the same way, and the server's [tool list](mcp/usd-code-mcp-tools.json)

---

© 2026 Alan Sloan. All rights reserved. You may read and link to this report; you may not copy, republish, or adapt it without permission. See [COPYRIGHT.md](../../../../COPYRIGHT.md).
