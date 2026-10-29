# Case study: NVIDIA OpenUSD

**Status: complete.** The review, including a rerun with NVIDIA's USD Code MCP server, is done, and its report is published.

**[Download the report (PDF)](https://github.com/southpaw199/agent-ready-nvidia/releases/latest/download/Alan-Sloan_NVIDIA-OpenUSD-Agent-Task-Review.pdf)** · [Read it online](reviews/agent-task-review/report.md)

## About this review

This case study is part of [agent-ready-docs](https://github.com/southpaw199/agent-ready-docs), a project that tests whether documentation works for AI agents as well as for people.

More and more developers meet a product through an AI coding agent: they ask Claude Code or Codex to set something up, and the agent reads the docs for them. When the docs leave out a prerequisite, show an example that doesn't run, or document an API in only one language, the agent either gets stuck or fills the gap from memory. The developer may never know which happened.

An [agent task review](https://github.com/southpaw199/agent-ready-docs/blob/main/methods/agent-task-review/method.md) tests docs the way agents use them:

1. **Choose real tasks.** Four to six tasks a new developer would attempt, from first install to a production concern.
2. **Limit the agent to the docs.** Each attempt starts in a clean environment, and the agent must cite every page it relies on.
3. **Verify independently.** The reviewer reruns the agent's code and checks the result against written success criteria. An agent saying it succeeded isn't evidence that it did.
4. **Check the sources.** Cited pages must say what the agent claims, and anything it used that isn't in the docs is recorded.
5. **Use two agents.** A gap that two different agents hit is stronger evidence than one.
6. **Report by root cause.** Each finding is traced to a cause, such as a missing prerequisite, an incomplete example, or a page the agent couldn't find, and comes with a specific fix. The report also credits what the docs do well.

Each run is scored pass, pass with issues, pass with hints, or fail, and each finding is rated High, Medium, or Low severity, using a shared [rubric](https://github.com/southpaw199/agent-ready-docs/blob/main/methods/agent-task-review/rubric.md) so results can be compared across case studies.

## This case study

This case study applies the agent task review to the [OpenUSD](https://openusd.org) docs and NVIDIA's [Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/) course: five hands-on tasks, U1 to U5, run on a CPU with the `usd-core` package from PyPI. The agents then ran the same tasks again with NVIDIA's USD Code MCP server available.

| Folder | What it holds |
| --- | --- |
| [`reviews/agent-task-review/`](reviews/agent-task-review/) | Tasks, success criteria, reference results, the run log, findings, and the report. |

## Results in brief

Two AI coding agents, Claude Code and Codex, each attempted five OpenUSD tasks using only openusd.org and Learn OpenUSD. **Both completed all five correctly, with no hints**, and the reviewer's own reruns of their code passed every check. All ten runs are scored pass with issues, mainly because both agents used Python API names that appear on none of the pages they read.

Both agents then ran the same tasks again with NVIDIA's [USD Code MCP](https://github.com/NVIDIA-Omniverse/kit-usd-agents/tree/4ce780d659078e7e7c12448778d3b05c842e6ffb/source/mcp/usd_code_mcp) server available, without being told to use it. Both used it in all ten runs, and the outcomes barely changed. One run, Codex on U3, passed cleanly, the only clean pass in the review.

| Task | What the agent had to do |
| --- | --- |
| U1 | Set the stage's units and up axis, define a default prim, and place a red cube on the ground; save, reopen, and report the bounds |
| U2 | Reference two assets, override one's color in a separate, stronger layer, and explain which opinion wins |
| U3 | Give a referenced asset a color variant set, and switch to red in code without changing the saved file |
| U4 | Place 1,000 crates by plain reference and with instancing, compare them, and explain the tradeoff |
| U5 | Write a script that flags missing stage metadata and broken references in any folder of .usda files |

| Agent | Docs given | U1 | U2 | U3 | U4 | U5 |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Code | Docs only | With issues | With issues | With issues | With issues | With issues |
| Claude Code | Docs and MCP server | With issues | With issues | With issues | With issues | With issues |
| Codex | Docs only | With issues | With issues | With issues | With issues | With issues |
| Codex | Docs and MCP server | With issues | With issues | **Pass** | With issues | With issues |

"With issues" means pass with issues: every success criterion was met with no hints, but the run relied on knowledge not in the docs, or had a similar gap.

The docs-only runs were on October 25, 2026, under [method version 0.2](https://github.com/southpaw199/agent-ready-docs/blob/v0.2/methods/agent-task-review/method.md), and the reruns with the MCP server on October 26, under [version 0.3](https://github.com/southpaw199/agent-ready-docs/blob/v0.3/methods/agent-task-review/method.md). Agents: Claude Code 2.1.310 (claude-opus-5-5) and Codex CLI 0.164.0 (GPT-6.1-Sol, reasoning "low"), with usd-core 26.11.

## Findings

### The docs

No finding about the docs is High.

| ID | Finding | Severity |
| --- | --- | --- |
| F2 | The API reference doesn't show Python names | Medium |
| F3 | usd-core's built-in validators are off the path | Medium |
| F1 | The usd-core install steps live inside the usdview page | Low |
| F4 | No `llms.txt` at openusd.org | Low |
| F5 | API pages don't say which version they describe | Low |
| F6 | No documented way to tell whether an up axis is authored | Low |

### NVIDIA's USD Code MCP server

These are candidates, about the MCP server rather than the docs.

| ID | Finding | Severity |
| --- | --- | --- |
| F9 | A world bounding-box example ignores the transform | High |
| F11 | displayColor examples author the wrong attribute | High |
| F7 | The README's quickstart fails on a stock Ubuntu 24.04 system | Medium |
| F13 | Examples from Windows test code | Medium |
| F8 | The README gives two tool counts | Low |
| F10 | Method lookups can return the wrong methods | Low |
| F12 | Search results are too large to use | Low |
| F14 | Sources beyond the official docs | Low |

**[Read the report](reviews/agent-task-review/report.md)** (or [download it as a PDF](https://github.com/southpaw199/agent-ready-nvidia/releases/latest/download/Alan-Sloan_NVIDIA-OpenUSD-Agent-Task-Review.pdf)) for each finding's evidence and suggested fix, what the docs do well, the full comparison with the MCP server, how the two agents compared, and the limitations. The [findings log](reviews/agent-task-review/findings.md) has the evidence for each finding, the [run log](reviews/agent-task-review/run-log.csv) has a row per run, and the [runs](reviews/agent-task-review/runs/) folder has each agent's code and transcript.

## A related case study: Omniverse and Isaac Sim

NVIDIA's [Omniverse](https://docs.omniverse.nvidia.com) and [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com) are built on OpenUSD: Omniverse describes its scenes in OpenUSD, and Isaac Sim is built on Omniverse. A separate case study could review their docs the same way. It's a possible future project, not work in progress.

Both need an RTX GPU to run, so that case study would ask agents questions rather than give them tasks:

- **Questions from the docs.** A set of 20 questions about Omniverse and Isaac Sim, answered from the docs, with citations.
- **With NVIDIA's agent skill.** The Isaac Sim setup questions again, with NVIDIA's `install-isaacsim` agent skill loaded, for comparison.

This review would be its starting point. Omniverse code calls the same OpenUSD Python API, so it could test, for example, whether Omniverse's docs show the Python names that openusd.org's API reference leaves out (F2).

## Use of AI tools

AI coding assistants helped draft code and content in this repo. I ran, tested, and verified every example and every finding myself. Agent outputs are evidence to check, not results to trust.

## License

Created by Alan Sloan ([LinkedIn](https://www.linkedin.com/in/alansloan)).

- **Code** (Python files, notebooks, and workflows) is licensed under the [MIT License](LICENSE).
- **Written content** (methods, reports, findings, task definitions, and READMEs) is © 2026 Alan Sloan. All rights reserved: you may read and link to it, but not copy, republish, or adapt it without permission. See [COPYRIGHT.md](COPYRIGHT.md).
- **Agent transcripts** in the `runs/` folders are records of each agent's output, included as evidence.
