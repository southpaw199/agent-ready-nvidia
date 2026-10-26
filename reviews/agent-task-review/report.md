# NVIDIA OpenUSD: agent task review report, Tier 1

**Author:** Alan Sloan · [linkedin.com/in/alansloan](https://www.linkedin.com/in/alansloan) · [github.com/southpaw199](https://github.com/southpaw199)

- **Method:** [agent task review](../../../../methods/agent-task-review/method.md), version 0.2
- **Agents:** Claude Code 2.1.310 (claude-opus-5-5) and Codex CLI 0.164.0 (GPT-6.1-Sol, reasoning "low")
- **Runs:** October 25, 2026, against the live docs at [openusd.org](https://openusd.org) and NVIDIA's [Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/), with usd-core 26.11 from PyPI on Python 3.12.3
- **Findings checked against the live docs:** October 25, 2026
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

## What the docs do well

- **Composition, without being named.** U2 asked only for "a second layer … so that its opinion is stronger than the asset's", and both agents found sublayers on their own: Claude Code from Learn OpenUSD's [Working with Sublayers](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/sublayers/working-with-sublayers.html) exercise ("The first appended sublayer will have the highest opinion"), Codex from the SdfLayer reference and Learn OpenUSD's strength ordering lesson.
- **Strength ordering.** Learn OpenUSD's [LIVERPS page](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/strength-ordering/what-is-liverps.html), its strength ordering lesson, and the openusd.org [glossary](https://openusd.org/release/glossary.html) state the order plainly. Both agents explained correctly why the override wins in U2 and why variant opinions beat the referenced asset in U3.
- **Changing a stage without saving it.** U3 asked for a switch to red that leaves the saved file selecting blue. Claude Code found the session layer on Learn OpenUSD's [edit targets page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/edit-targets-layer-muting.html), which says `Usd.Stage.Save()` "deliberately does not write it to disk". Codex reached the same result another way. Neither saved red by mistake.
- **Instancing, with its costs.** openusd.org's [Scenegraph Instancing](https://openusd.org/release/api/_usd__page__scenegraph_instancing.html) page explains both the saving ("This reduces the size of the scenegraph") and the limits (overrides beneath an instance "will be silently ignored"). Both agents' U4 explanations were right, and neither claimed a speedup its own timings didn't show: Claude Code called them "too noisy to compare", Codex "single measurements, not a benchmark". That matches the reference run, where the two files opened in about the same time at this scale.
- **Fallbacks that would hide a mistake.** The Learn OpenUSD [units page](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html) and the openusd.org [up axis page](https://openusd.org/release/api/group___usd_geom_up_axis__group.html) say what an unauthored up axis or unit falls back to. Both agents authored the metadata in U1, and in U5 both checked whether it was authored rather than what value it had, so a Y-up file in centimeters wasn't flagged by mistake.
- **Learn OpenUSD's Python examples.** Where an agent reached a Learn OpenUSD page, it found working Python: units, default prims, references, sublayers, edit targets, variant sets. The Python gaps in finding 1 come from the openusd.org API reference, not from the course.
- **Precise API notes.** The [Cube page](https://openusd.org/release/api/class_usd_geom_cube.html) says "If you author size you must also author extent", and both agents did. The release [Hello World tutorial](https://openusd.org/release/tut_helloworld.html) says "Tested with USD 26.11", the version pip installed.

## Main findings

Severity: **High** means an agent following the docs would fail or get a wrong result; **Medium**, the task succeeds, but only with knowledge the docs don't give or by a route they don't point to; **Low**, friction or polish. No Tier 1 finding is High.

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

## Limitations

- **Prior knowledge.** OpenUSD is old and widely used, so both models know it from training data, and each run tests the docs plus that knowledge. Requiring page citations reduces the effect, and checking every name against the pages cited is how finding 1 surfaced, but it doesn't remove it.
- **One run per agent per task.** Agents are non-deterministic. Treat each result as a signal, not a verdict.
- **Settings.** Codex ran at its default "low" reasoning setting and with web search off, because its search tool doesn't ask before each search. Claude Code could search, limited to the two sites. Different settings could change how each found pages.
- **Shared environment.** Three Claude Code sessions (U1, U3, U4) started from a terminal where another run's Python environment was still active. The session logs show no agent read anything in another run's folder, and every agent built its own environment, so no result is affected; the agents could see another folder's path, nothing more. The method now says to start each session from a clean terminal.
- **A repeated run.** Codex's first U3 attempt was discarded, because its session wasn't exported with the commands; its rerun had passed 11 of 11. U3 was run again from scratch, and the results here are the second attempt's. The [Codex run notes](runs/2026-10-25-codex/README.md) record it.
- **Caches.** The usd-core wheel was in the pip cache from earlier runs, so installs were faster than for a new user.
- **Hardware.** Tier 1 covers only what runs on a CPU. Omniverse and Isaac Sim come in Tiers 2 and 3, as questions answered from the docs.
- **AI assistance.** Claude helped design the tasks, wrote the reference solutions and checkers, and helped draft this report. Claude is the same model family as one of the subject agents. The subject sessions saw only each task's prompt, never its success criteria, reference solution, checker, or this repository, and the session logs confirm they read nothing outside their own folders. The reviewer ran every reference solution and every checker test, and reran every agent's final code; every finding was checked against the live docs.

## Files

- [Tasks, success criteria, and reference results](tasks.md), with the [reference solutions](reference/) and a checker and tests for each task
- [Run log](run-log.csv): one row per attempt
- [Findings log](findings.md): evidence, status, and severity for each finding
- Runs: [Claude Code](runs/2026-10-25-claude-code/) and [Codex](runs/2026-10-25-codex/), with each task's code, transcript, and the reviewer's rerun output and check results

---

© 2026 Alan Sloan. All rights reserved. You may read and link to this report; you may not copy, republish, or adapt it without permission. See [COPYRIGHT.md](../../../../COPYRIGHT.md).
