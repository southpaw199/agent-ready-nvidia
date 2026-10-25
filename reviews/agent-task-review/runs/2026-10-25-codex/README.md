# Run: 2026-10-25, Codex

A second agent on the same task, so findings can be compared across model families. The task, standard instructions, and scoring are identical to the [Claude Code run](../2026-10-25-claude-code/).

## Environment

| Item | Value |
| --- | --- |
| Agent | Codex CLI, in a WSL terminal |
| Agent version | 0.164.0, for both the CLI and its local background server. The CLI was updated from 0.163.0 just before the run. |
| Model | GPT-6.1-Sol, reasoning "low", as in the LanceDB runs |
| Operating system | Ubuntu 24.04 under WSL 2 on Windows 11 |
| Python | 3.12.3 |
| usd-core | 26.11 (agent's install and the reviewer's rerun) |
| Working folder | A new, empty folder, `~/agent-runs/nvidia/2026-10-25-codex/U1/`, outside this repository; the rerun was in `U1-rerun/` beside it |
| User instructions | None (`AGENTS.md` absent) |
| Approvals | `approval_policy = "on-request"`, workspace sandbox: every command needing the network asked for approval |
| Web search | Off (`web_search = "disabled"`), because Codex's search tool doesn't ask before each search |
| ChatGPT connectors | Off (`features.apps = false`) |
| Memories | Off (`features.memories = false`) |

## Entry points on the day of the run

Checked 2026-10-25: https://openusd.org/llms.txt still returned 404, and https://docs.nvidia.com/learn-openusd/llms.txt still returned the 27-line course index. The agent used neither. It started from https://openusd.org/release/tut_helloworld.html and https://docs.nvidia.com/learn-openusd/latest/index.html, URLs it typed itself.

## Notes

- Old Codex app-server processes from the LanceDB runs, version 0.164.0, were still running before this run. They were stopped first, so this session started its own server.
- The sandbox blocked network access until a command was approved, so the first page fetch and the first `pip install` failed, then succeeded once approved, as in the LanceDB runs.
- Codex saved each docs page it downloaded in its folder (`docs_*.html` and `.txt`) and wrote its citations to `SOURCES.md`. The saved pages aren't kept here; `SOURCES.md` is.
- The reviewer reran the agent's `task.py` on 2026-10-25 in a clean folder with a fresh virtual environment, Python 3.12.3, and usd-core 26.11, using the commands in [tasks.md](../../tasks.md#scoring).

## How Codex differs from the Claude Code run

- Codex has no page-reading tool, so it read docs pages with `curl` and parsed them with short Python scripts. The page text those scripts printed is left out of the transcript here, which keeps the commands and the agent's messages.
- With web search off, Codex had to find pages from URLs it already knew or links on pages it had downloaded. It cited openusd.org's `/release/` pages; Claude Code, which found pages by search, cited `/dev/`.

## Tasks

| Task | Outcome | Hints | Folder |
| --- | --- | --- | --- |
| U1 | pass-with-issues | 0 | [U1](U1/) |

Each task folder holds the agent's final `task.py`, its `SOURCES.md`, and its exported conversation, `transcript.md`, plus the reviewer's `rerun-output.txt` and `check-output.txt`, as in the [Claude Code run](../2026-10-25-claude-code/).
