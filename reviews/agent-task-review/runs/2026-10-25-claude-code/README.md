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
| Working folder | A new, empty folder per task under `~/agent-runs/nvidia/2026-10-25-claude-code/` (`U1/` to `U5/`), outside this repository; each rerun was in a `-rerun` folder beside it, such as `U1-rerun/` |
| User instructions | None (`~/.claude/CLAUDE.md` absent) |
| Auto memory | Off (`autoMemoryEnabled: false`) |
| claude.ai connectors | Off (`disableClaudeAiConnectors: true`) |
| Web search | On, as in the LanceDB runs. The agent limited each search to openusd.org and docs.nvidia.com itself. |
| Permissions | Each web fetch domain and command was approved at a prompt; approvals for openusd.org and docs.nvidia.com were saved to the folder's `.claude/settings.local.json` |
| Caches | pip cache already held the usd-core 26.11 wheel from the reference run |

## Entry points on the day of the run

Checked 2026-10-25: https://openusd.org/llms.txt still returned 404, and https://docs.nvidia.com/learn-openusd/llms.txt still returned the 27-line course index. Rechecked before U2 and after U3, U4, and U5 the same day, with the same results. The agent used neither in any task.

## Notes

- U2 was run as a pilot, before U3 to U5 were written, to test the task design. Nothing in the run called for a change to U2. Before the session, [`make_u2_assets.py`](../../make_u2_assets.py) created `table.usda` and `chair.usda` in the empty folder, and the rerun created fresh copies in its own folder.
- In U4, the agent's `which python3` printed `~/agent-runs/nvidia/2026-10-25-claude-code/U3-rerun/.venv/bin/python3`: VS Code had been launched from a terminal with the reviewer's U3 rerun environment still active, and the session inherited it. The agent read nothing in `U3-rerun/` and built its own environment from `/usr/bin/python3`, so the result isn't affected, but it saw a sibling folder's path. From U5 on, each session is launched from a terminal with no virtual environment active. Each agent's `.venv/pyvenv.cfg` records the Python that created it, which shows the same happened in two earlier runs: U1's session started inside the LanceDB Codex T4 environment, and U3's inside the reviewer's Codex U1 rerun environment. U2 and U5 started clean. Every one of these environments is built on the same `/usr/bin/python3.12`, and the outside-folder checks found no reads of other run folders, so no result is affected; the agents saw other folders' paths, nothing more.
- In U1, one web search was rejected at the permission prompt with the note "Yes within the allowed domains", which the reviewer meant as approval. The agent read it as a decline and fetched pages directly instead. It isn't counted as a hint, because it said nothing about the task.
- The reviewer reran the agent's `task.py` on 2026-10-25 in a clean folder with a fresh virtual environment, Python 3.12.3, and usd-core 26.11, using the commands in [tasks.md](../../tasks.md#scoring).
- `/export` collapses shell commands and search results. The commands, search domains, and returned URLs described in the run log come from the session's full log.

## Tasks

| Task | Outcome | Hints | Folder |
| --- | --- | --- | --- |
| U1 | pass-with-issues | 0 | [U1](U1/) |
| U2 | pass-with-issues | 0 | [U2](U2/) |
| U3 | pass-with-issues | 0 | [U3](U3/) |
| U4 | pass-with-issues | 0 | [U4](U4/) |
| U5 | pass-with-issues | 0 | [U5](U5/) |

Each task folder holds the agent's final `task.py` and the exported conversation, `transcript.md`. U5's also holds the agent's `report.json`, and a `holdout/` folder with the rerun on the holdout set. Unlike the LanceDB runs, every task folder also holds `rerun-output.txt`, the output of the agent's `task.py` rerun in a clean folder, and `check-output.txt`, the result of [`check_u1.py`](../../check_u1.py) on the `scene.usda` that rerun saved.
