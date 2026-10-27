# Run: 2026-10-26, Claude Code, docs+mcp

The Tier 1 tasks run again with NVIDIA's USD Code MCP server available, under method version 0.3. The agent gets the [docs+MCP standard instructions](../../tasks.md#docsmcp-standard-instructions), then each task prompt, unchanged.

## Environment

| Item | Value |
| --- | --- |
| Agent | Claude Code, VS Code extension |
| Agent version | 2.1.310, the same as the Tier 1 run |
| Model | claude-opus-5-5, the same as the Tier 1 run |
| Operating system | Ubuntu 24.04 under WSL 2 on Windows 11 |
| Python | 3.12.3 |
| usd-core | 26.11 (agent's install and the rerun) |
| Working folder | A new, empty folder per task under `~/agent-runs/nvidia/2026-10-26-claude-code-mcp/` (`U1/` to `U5/`), outside this repository; each rerun is in a `-rerun` folder beside it, such as `U1-rerun/` |
| MCP server | USD Code MCP, `NVIDIA-Omniverse/kit-usd-agents` at commit `4ce780d659078e7e7c12448778d3b05c842e6ffb`, Docker image `360aaf4962b4` (NeMo Agent Toolkit MCP 1.30.0), at `http://localhost:9903/mcp`. The same container serves every run. Its 7 tools are listed in [`usd-code-mcp-tools.json`](../../mcp/usd-code-mcp-tools.json). |
| MCP registration | Local scope, in each task folder only (`claude mcp add --transport http usd-code-mcp http://localhost:9903/mcp`). Not registered at user scope, in this repository, or in any Tier 1 folder; checked with `claude mcp list` before the runs. The Isaac Sim MCP server was set up but not registered and is not used. |
| Retrieval settings | The server's defaults, unchanged during the runs |
| User instructions | None (`~/.claude/CLAUDE.md` absent) |
| Auto memory | Off (`autoMemoryEnabled: false`) |
| claude.ai connectors | Off (`disableClaudeAiConnectors: true`) |
| Web search | On, as in the Tier 1 run |
| Permissions | Each web fetch domain, command, and MCP tool was approved at a prompt. In U1, approvals for openusd.org, docs.nvidia.com, and `get_usd_method_detail` were saved to the folder's `.claude/settings.local.json`; in U2, approvals for docs.nvidia.com, `search_usd_code_examples`, and `get_usd_method_detail`; in U3, approvals for docs.nvidia.com, openusd.org, and `search_usd_code_examples`; in U4, approvals for docs.nvidia.com, openusd.org, and `get_usd_method_detail`. Commands that read outside the folder were approved once each, not saved. |

## Entry points on the day of the run

Checked 2026-10-26, after U1: https://openusd.org/llms.txt and https://openusd.org/release/llms.txt still return 404, and https://docs.nvidia.com/learn-openusd/llms.txt still returns the 27-line course index. https://docs.nvidia.com/learn-openusd now redirects (301) to `https://docs.nvidia.com/learn-openusd/`, which still returns 404. The agent used none of them in U1 to U4.

## Notes

- U1 was restarted. The first session was stopped by the reviewer at its first permission prompts, before any page was read or package installed. Its folder was emptied, its transcript moved out of the run tree, and a new session (not a resumed one) was started with the same message. That transcript is [`U1/false-start-transcript.md`](U1/false-start-transcript.md). It isn't counted as a hint, because nothing was said to the agent about the task.
- In U1, Claude Code saved the two large MCP search results to files under `~/.claude/projects/.../tool-results/`, outside the run folder, and the agent changed into that folder to read them. This is logged as an issue in the run log and as finding F12. The same happened in U2 with its one large search result. U2 also wrote checksums of the asset files to Claude Code's session scratchpad under `/tmp/claude-1000/`, outside the run folder, which is logged as an issue too. In U3, the agent tried to read its saved search result with `jq`, which isn't installed, so nothing was read, and it dropped the result. It also read Claude Code's output file for its background pip install, under `/tmp/claude-1000/`. Both are logged as issues. The U3 export labels the `jq` attempt "Searched memories", but no memory was used, and auto memory is off.
- In U3, WebFetch's summary of the Learn OpenUSD Creating Composition Arcs index invented `nvidia-omniverse.github.io/LearnOpenUSD/` links, which it marked as assumed. The agent said that site isn't allowed, and fetched the same paths on docs.nvidia.com. The docs page has no such links. The same happened with the course index in U4.
- U4 had no reads, writes, or commands outside its folder. Its only MCP calls were two method lookups, both small enough to pass to the agent directly, and it didn't use the code search.
- Before the U2 session, [`make_u2_assets.py`](../../make_u2_assets.py) created `table.usda` and `chair.usda` in the empty folder. They matched the Tier 1 files byte for byte. The rerun created fresh copies in its own folder. U3 and U4 were set up the same way, with [`make_u3_assets.py`](../../make_u3_assets.py) for `mug.usda` and [`make_u4_assets.py`](../../make_u4_assets.py) for `crate.usda`.
- The MCP results the agent relied on were checked the same way as its cited pages: against usd-core 26.11 and the live docs. The full results come from the session's log, since `/export` collapses tool calls.
- The reviewer reran the agent's `task.py` on 2026-10-26 in a clean folder with a fresh virtual environment, Python 3.12.3, and usd-core 26.11, using the commands in [tasks.md](../../tasks.md#scoring). The rerun folders have no MCP server registered.

## Tasks

| Task | Outcome | Hints | MCP calls | Folder |
| --- | --- | --- | --- | --- |
| U1 | pass-with-issues | 0 | 3 | [U1](U1/) |
| U2 | pass-with-issues | 0 | 2 | [U2](U2/) |
| U3 | pass-with-issues | 0 | 2 | [U3](U3/) |
| U4 | pass-with-issues | 0 | 2 | [U4](U4/) |
| U5 | not yet run | | | |

Each task folder holds the agent's final `task.py`, the exported conversation `transcript.md`, `rerun-output.txt` from the reviewer's rerun, and `check-output.txt` from the task's checker on that rerun.
