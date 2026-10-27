# NVIDIA OpenUSD: docs only against docs plus USD Code MCP, Tier 1

**Draft for Alan.** Not yet part of the [Tier 1 report](report.md).

- **Method:** [agent task review](../../../../methods/agent-task-review/method.md): version 0.2 for the docs-only runs, 0.3 for the docs+mcp runs
- **Agents:** Claude Code 2.1.310 (claude-opus-5-5) and Codex CLI 0.164.0 (GPT-6.1-Sol, reasoning "low"), the same in both conditions
- **Runs:** docs only on October 25, 2026, and docs+mcp on October 26, 2026. Both used the same five tasks, prompts, and checkers, with usd-core 26.11 on Python 3.12.3.
- **MCP server:** NVIDIA's USD Code MCP, `NVIDIA-Omniverse/kit-usd-agents` at commit `4ce780d`, Docker image `360aaf4962b4`, with its default retrieval settings. It was registered only in each docs+mcp run folder.
- **Sources:** [run log](run-log.csv), [findings log](findings.md), and the transcripts and session logs under [runs/](runs/). MCP results were checked against usd-core 26.11 and the live docs on October 26, 2026.

## Results by task and agent

Each cell gives docs only first, then docs+mcp.

| Task | Agent | Outcome | Time (min) | Errors recovered | MCP calls, by tool | Tier 1 issue avoided? | New issue from an MCP result? | Pages cited / MCP results cited |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U1 | Claude Code | pass-with-issues / pass-with-issues | 6 / 8 | 1 / 2 | 3: code examples ×2, method detail ×1 | **No** for F2: Python names from memory, disclosed both times. **Yes** for F1: the docs+mcp run didn't repeat Tier 1's claim that the install steps aren't in the docs. Extent and stage metadata were right both times. | **Yes:** it read the two oversized results that Claude Code had saved outside the run folder (F12) | 15 / 11 pages; 0 / 3 MCP |
| U1 | Codex | pass-with-issues / pass-with-issues | 3 / 2 | 4 / 2 | 1: knowledge search | **No** for F2: undisclosed both times. Tier 1's wrong citation for reading the default prim didn't recur. Extent and stage metadata were right both times. | No | 10 / 9 pages; 0 / 0 MCP. It named the search as "initial discovery" only. |
| U2 | Claude Code | pass-with-issues / pass-with-issues | 4 / 5 | 2 / 1 | 2: code examples ×1, method detail ×1 | **Partly** for F2: `GetPropertyStack`, from memory in Tier 1, came from the MCP method lookup. Other names were still from memory, disclosed. | **Yes:** it read the saved oversized result outside the run folder (F12) | 11 / 6 pages; 0 / 2 MCP |
| U2 | Codex | pass-with-issues / pass-with-issues | 5 / 2.5 | 2 / 2 | 2: knowledge search ×1, code examples ×1 | **No** for F2: undisclosed both times, including `subLayerPaths` both times | No | 7 / 8 pages; 0 / 1 MCP |
| U3 | Claude Code | pass-with-issues / pass-with-issues | 5 / 6 | 0 / 3 | 2: code examples ×1, method detail ×1 | **No** for F2: `UsdGeom.Gprim(mug)` came from memory both times. Tier 1 disclosed it, and the docs+mcp run didn't. | **Yes:** it tried to read the saved oversized result outside the run folder, failed, and dropped it (F12) | 11 / 7 pages; 0 / 1 MCP |
| U3 | Codex | pass-with-issues / **pass** | 3 / 1.5 | 2 / 2 | 2: knowledge search ×1, method detail ×1 | **Yes** for F2: every name came from the three tutorials it read, which show Python, or from the method lookup it cited | No | 7 / 3 pages; 0 / 1 MCP |
| U4 | Claude Code | pass-with-issues / pass-with-issues | 5 / 3 | 0 / 1 | 2: method detail ×2 | **No** for F2: disclosed both times | No | 12 / 8 pages; 0 / 2 MCP |
| U4 | Codex | pass-with-issues / pass-with-issues | 6 / 1.5 | 3 / 2 | 1: knowledge search | **No** for F2: undisclosed both times, including the units functions both times. It timed each open in a fresh process, which no Tier 1 run did. | No | 7 / 6 pages; 0 / 0 MCP |
| U5 | Claude Code | pass-with-issues / pass-with-issues | 4 / 3.5 | 0 / 1 | 5: knowledge search ×2, method detail ×3 | **No** for F2: disclosed both times. **No** for F3: hand-written checks both times, and the server never mentioned `UsdValidation`. | No. The server didn't point to the removed `ComplianceChecker`. | 8 / 7 pages; 0 / 3 MCP |
| U5 | Codex | pass-with-issues / pass-with-issues | 4 / 1.5 | 4 / 2 | 1: knowledge search | **No** for F2: undisclosed both times, with the same four names. **No** for F3: as for Claude Code. | No. Again, no `ComplianceChecker`. | 7 / 6 pages; 0 / 0 MCP |

**How the columns were filled**
- **Time** comes from the run log. Docs+mcp times run from the prompt to the agent's final answer in the session log.
- **Errors recovered** counts commands or fetches that failed and were then retried or worked around. Most Codex errors in both conditions came from its sandbox blocking network access until a command was approved.
- **MCP results cited** counts results an agent named as the source of a step. Results it read and set aside aren't counted.
- **Pages cited** counts distinct docs URLs given as sources in the final answer, not 404s or pages it only mentioned.
- **Issues that didn't occur in either condition:**
  - deprecated APIs;
  - warnings the agent didn't report;
  - missing stage metadata in U1;
  - a missing extent in U1.

## What the MCP server did well

- **Both agents used it unprompted in all ten runs**, 21 calls in all, even though the instructions only said it was available.
- **Its method lookups were accurate and small.** Every `get_usd_method_detail` result an agent relied on matched usd-core 26.11, and each was small enough to pass to the agent whole. Two examples:
  - In Claude Code U2, `GetPropertyStack` came from a lookup, where Tier 1 had used it from memory.
  - In Codex U3, lookups filled the only gap left by the tutorials it read, giving the review's one clean pass.
- **It didn't push old APIs.** In the U5 runs, no result pointed to `UsdUtils.ComplianceChecker`, which usd-core 26.11 no longer has. That was the version risk your brief flagged.
- **Every MCP result an agent cited held up** against usd-core 26.11 or the live docs, in all ten runs.

## Where it fell short

- **Oversized search results (F12).** Every `search_usd_code_examples` and `search_usd_knowledge` result was too large to pass whole: 45,000 to 66,000 tokens, or 70 to 120 KB.
  - **Claude Code** saved them to files outside the run folder, and read or tried to read them there in three of its five runs.
  - **Codex** cut them short and saw only the start.
- **Wrong examples, none relied on.**
  - **F9:** a world bounding-box example that ignores the transform.
  - **F11:** displayColor examples that author the wrong attribute.
  - **F13:** a sublayer example that adds a missing `C:/usd/` path.
  - **F10:** method lookups that returned the wrong methods.
- **Sources from other sites (F14).** Knowledge results mixed openusd.org with GitHub repositories and Remedy Entertainment's *USD Book*, even when the query asked for the two allowed sites. All five Codex sessions noticed and excluded them.
- **No route to the validators (F3).** For U5, the server's validation content pointed only to `usdchecker`, as the docs do.

## Conclusions

Over ten runs per condition, adding the MCP server didn't change whether the agents completed the tasks. Every run in both conditions met every success criterion with no hints, and the one difference in outcome is Codex U3's clean pass. The server's method lookups were its most useful part: accurate, small, and the source of the only run that relied on no Python names from memory. They didn't fix F2 generally, though, which recurred in nine of the ten docs+mcp runs. Its search tools returned results too large to use whole, and some were wrong or came from other sites. The agents relied on none of those, but the size led Claude Code to work outside its folder in three runs.

## Limitations

- **One run per task per agent.** That's ten runs per condition, and agents aren't deterministic. Read each row as a signal, not a verdict. Codex U3's clean pass in particular is a single run.
- **Different days, same everything else.** The two conditions ran a day apart, with the same agent versions, models, settings, tasks, and checkers. The live docs could have changed in between. Entry points were rechecked and hadn't, but pages weren't compared in full.
- **Order effects.** Each docs+mcp run came after its agent's docs-only run of the same task, in separate fresh sessions with memory off. No session could see another's files or history.
- **Times aren't comparable across agents.** They're session durations, affected by approval prompts and the reviewer's response time. Codex's docs+mcp times are measured from the prompt. Treat them as rough.
- **Server settings.** The server ran with its default retrieval settings. Result sizes, and so F12, may depend on settings that weren't tested.
- **Prior knowledge.** Both models know OpenUSD from training. F2 measures that knowledge, and the MCP server only partly replaces it.
- **AI assistance.** Claude ran the operator session that checked these runs and drafted this comparison. Claude is the same model family as one of the subject agents. Every MCP result an agent relied on was checked against usd-core 26.11 or the live docs, and every agent's final code was rerun by the reviewer.

## Files

- [run-log.csv](run-log.csv) has a row per run, with the `condition` and `mcp_calls` columns.
- [findings.md](findings.md) has F1 to F6 from Tier 1, F7 and F8 from the server's setup, and F9 to F14 from the docs+mcp runs.
- The run notes are in [runs/2026-10-26-claude-code-mcp/](runs/2026-10-26-claude-code-mcp/) and [runs/2026-10-26-codex-mcp/](runs/2026-10-26-codex-mcp/).
- The server's tool list is in [mcp/usd-code-mcp-tools.json](mcp/usd-code-mcp-tools.json).
