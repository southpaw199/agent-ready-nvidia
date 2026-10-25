# Run: 2026-10-25, Claude Code

## Environment

| Item | Value |
| --- | --- |
| Agent | Claude Code, VS Code extension |
| Agent version | 2.1.310 |
| Model | claude-opus-5-5 |
| Operating system | Ubuntu 24.04 under WSL 2 on Windows 11 |
| Python | 3.12.3 |
| usd-core | 26.11 (agent's install and the rerun) |
| Working folder | A new, empty folder, `~/agent-runs/2026-10-25-claude-code/U1/`, outside this repository |
| User instructions | None (`~/.claude/CLAUDE.md` absent) |
| Auto memory | Off (`autoMemoryEnabled: false`) |
| claude.ai connectors | Off (`disableClaudeAiConnectors: true`) |
| Web search | On, as in the LanceDB runs. The agent limited each search to openusd.org and docs.nvidia.com itself. |
| Permissions | Each web fetch domain and command was approved at a prompt; approvals for openusd.org and docs.nvidia.com were saved to the folder's `.claude/settings.local.json` |
| Caches | pip cache already held the usd-core 26.11 wheel from the reference run |

## Entry points on the day of the run

Checked 2026-10-25: https://openusd.org/llms.txt still returned 404, and https://docs.nvidia.com/learn-openusd/llms.txt still returned the 27-line course index. The agent used neither.

## Notes

- One web search was rejected at the permission prompt with the note "Yes within the allowed domains", which the reviewer meant as approval. The agent read it as a decline and fetched pages directly instead. It isn't counted as a hint, because it said nothing about the task.
- The reviewer reran the agent's `task.py` on 2026-10-25 in a clean folder with a fresh virtual environment, Python 3.12.3, and usd-core 26.11, using the commands in [tasks.md](../../tasks.md#scoring).
- `/export` collapses shell commands and search results. The commands, search domains, and returned URLs described in the run log come from the session's full log.

## Tasks

| Task | Outcome | Hints | Folder |
| --- | --- | --- | --- |
| U1 | pass-with-issues | 0 | [U1](U1/) |

Each task folder holds the agent's final `task.py` and the exported conversation, `transcript.md`. Unlike the LanceDB runs, every task folder also holds `rerun-output.txt`, the output of the agent's `task.py` rerun in a clean folder, and `check-output.txt`, the result of [`check_u1.py`](../../check_u1.py) on the `scene.usda` that rerun saved.
