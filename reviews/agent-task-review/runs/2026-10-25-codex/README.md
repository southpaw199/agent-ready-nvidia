# Run: 2026-10-25, Codex

A second agent on the same tasks, so findings can be compared across model families. The tasks, standard instructions, and scoring are identical to the [Claude Code run](../2026-10-25-claude-code/). Codex ran U1 first, then U2 to U5 as a batch after Claude Code had finished all five.

## Environment

| Item | Value |
| --- | --- |
| Agent | Codex CLI, in a WSL terminal |
| Agent version | 0.164.0, for both the CLI and its local background server. The CLI was updated from 0.163.0 just before the run. |
| Model | GPT-6.1-Sol, reasoning "low", as in the LanceDB runs |
| Operating system | Ubuntu 24.04 under WSL 2 on Windows 11 |
| Python | 3.12.3 |
| usd-core | 26.11 (agent's install and the reviewer's rerun) |
| Working folder | A new, empty folder per task under `~/agent-runs/nvidia/2026-10-25-codex/` (`U1/`, `U2/`), outside this repository; each rerun was in a `-rerun` folder beside it |
| User instructions | None (`AGENTS.md` absent) |
| Approvals | `approval_policy = "on-request"`, workspace sandbox: every command needing the network asked for approval |
| Web search | Off (`web_search = "disabled"`), because Codex's search tool doesn't ask before each search |
| ChatGPT connectors | Off (`features.apps = false`) |
| Memories | Off (`features.memories = false`) |
| MCP servers | None configured (`codex mcp list`). `/mcp` shows only `codex_tui`, which Codex provides itself, for its own tools such as worktree management; it was also present in every LanceDB Codex session |

## Entry points on the day of the run

Checked 2026-10-25: https://openusd.org/llms.txt still returned 404, and https://docs.nvidia.com/learn-openusd/llms.txt still returned the 27-line course index. The agent used neither. In U1 it started from https://openusd.org/release/tut_helloworld.html and https://docs.nvidia.com/learn-openusd/latest/index.html, URLs it typed itself; in U2, from https://openusd.org/release/tut_referencing_layers.html. Rechecked before the U2 to U5 batch the same day, with the same results.

## Notes

- Codex app-server processes started during the LanceDB runs were still running before this run. Codex's scheduled updater had updated them in place from 0.163.0 to 0.164.0 on 2026-10-23, after the LanceDB runs finished. They were stopped first, so this session started its own server. The session log confirms 0.164.0 for this run.
- Before the U2 to U5 batch, the background server left from the U1 session (started while the CLI was still 0.163.0) was stopped, so each session started its own 0.164.0 server. Each session was launched from a terminal with no virtual environment active, and each agent's `.venv/pyvenv.cfg` confirms its environment was created by `/usr/bin/python3`; U1's was too.
- The sandbox blocked network access until a command was approved, so the first page fetch and the first `pip install` failed, then succeeded once approved, as in the LanceDB runs. In each task, the first fetch tried to save the page to `/tmp`, outside the folder, and failed for the same reason.
- Codex saved each docs page it downloaded in its folder (`docs_*` or `docs-*`, `.html` and `.txt`). The saved pages aren't kept here. In U1 it also wrote its citations to `SOURCES.md`, which is kept.
- The reviewer reran the agent's `task.py` on 2026-10-25 in a clean folder with a fresh virtual environment, Python 3.12.3, and usd-core 26.11, using the commands in [tasks.md](../../tasks.md#scoring).

## How Codex differs from the Claude Code run

- Codex has no page-reading tool, so it read docs pages with `curl` and parsed them with short Python scripts and `rg`. The page text those commands printed is left out of the transcripts here, which keep the commands and the agent's messages.
- With web search off, Codex had to find pages from URLs it already knew or links on pages it had downloaded. It cited openusd.org's `/release/` pages; Claude Code, which found pages by search, cited `/dev/`.

## Tasks

| Task | Outcome | Hints | Folder |
| --- | --- | --- | --- |
| U1 | pass-with-issues | 0 | [U1](U1/) |
| U2 | pass-with-issues | 0 | [U2](U2/) |

Each task folder holds the agent's final `task.py` and its exported conversation, `transcript.md` (and, in U1, its `SOURCES.md`), plus the reviewer's `rerun-output.txt` and `check-output.txt`, as in the [Claude Code run](../2026-10-25-claude-code/).
