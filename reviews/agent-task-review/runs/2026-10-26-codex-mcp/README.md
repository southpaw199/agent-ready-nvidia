# Run: 2026-10-26, Codex, docs+mcp

The Tier 1 tasks run again with NVIDIA's USD Code MCP server available, under method version 0.3, after the [Claude Code docs+mcp run](../2026-10-26-claude-code-mcp/). The agent gets the [docs+MCP standard instructions](../../tasks.md#docsmcp-standard-instructions), then each task prompt, unchanged. Settings are otherwise the same as the [Tier 1 Codex run](../2026-10-25-codex/).

## Environment

| Item | Value |
| --- | --- |
| Agent | Codex CLI, in a WSL terminal, with its local background server |
| Agent version | 0.164.0, the same as the Tier 1 run |
| Model | GPT-6.1-Sol, reasoning "low", the same as the Tier 1 run. Choosing it with `/model` saved it as the default in `~/.codex/config.toml` (`model` and `model_reasoning_effort`). |
| Operating system | Ubuntu 24.04 under WSL 2 on Windows 11 |
| Python | 3.12.3 |
| usd-core | 26.11 (agent's install and the reviewer's rerun) |
| Working folder | A new, empty folder per task under `~/agent-runs/nvidia/2026-10-26-codex-mcp/` (`U1/` to `U5/`), outside this repository; each rerun is in a `-rerun` folder beside it |
| MCP server | USD Code MCP, `NVIDIA-Omniverse/kit-usd-agents` at commit `4ce780d659078e7e7c12448778d3b05c842e6ffb`, Docker image `360aaf4962b4` (NeMo Agent Toolkit MCP 1.30.0), at `http://localhost:9903/mcp`. The same container served the Claude Code runs. Its 7 tools are listed in [`usd-code-mcp-tools.json`](../../mcp/usd-code-mcp-tools.json). |
| MCP registration | In each task folder's `.codex/config.toml` only (`[mcp_servers.usd-code-mcp]`, `url = "http://localhost:9903/mcp"`). Codex loads a folder's config only once the folder is trusted, so each folder was trusted at the start of its session, which adds a `[projects."<folder>"]` entry with `trust_level = "trusted"` to `~/.codex/config.toml`. Not registered in `~/.codex/config.toml` itself; `codex mcp list` in a Tier 1 Codex folder shows no servers. |
| Retrieval settings | The server's defaults, unchanged during the runs |
| User instructions | None (`AGENTS.md` absent) |
| Approvals | `approval_policy = "on-request"`, workspace sandbox: every command needing the network asked for approval |
| Web search | Off (`web_search = "disabled"`) |
| ChatGPT connectors | Off (`features.apps = false`) |
| Memories | Off (`features.memories = false`) |

## Entry points on the day of the run

Checked 2026-10-26, for the Claude Code docs+mcp run: https://openusd.org/llms.txt and https://openusd.org/release/llms.txt return 404, https://docs.nvidia.com/learn-openusd/llms.txt returns the 27-line course index, and https://docs.nvidia.com/learn-openusd redirects (301) to `https://docs.nvidia.com/learn-openusd/`, which returns 404. The agent used none of them in U1 to U3.

## Notes

- No Codex processes were running before U1, so the session started its own 0.164.0 background server. The U1 server was still running when U2 started, so the reviewer stopped it and restarted the U2 session before giving it the prompt; U2 started its own server. Each later session does the same. Each session was launched from a terminal with no virtual environment active, and each agent's `.venv/pyvenv.cfg` confirms its environment was created by `/usr/bin/python3`.
- Before the U2 session, [`make_u2_assets.py`](../../make_u2_assets.py) created `table.usda` and `chair.usda` in the empty folder. They matched the Tier 1 files byte for byte. The rerun created fresh copies in its own folder. U3 was set up the same way with [`make_u3_assets.py`](../../make_u3_assets.py) and `mug.usda`.
- As in Tier 1, the sandbox blocked network access until a command was approved, so the first page fetch and the first `pip install` failed, then succeeded once approved. In U1, the first fetch tried to save the page to `/tmp`, outside the folder, which is logged as an issue under method 0.3.
- Codex passes an oversized MCP result to the agent truncated, instead of saving it to a file as Claude Code does. In U1, the agent saw part of a result of about 45,100 tokens, and in U2, parts of two results of about 45,100 and 49,000 tokens (finding F12). U2 had no reads, writes, or commands outside its folder.
- U3 is the first clean `pass` in the NVIDIA review. It read only three openusd.org tutorials, all with Python examples, and one `get_usd_method_detail` lookup supplied the remaining Python names. So, unlike every earlier run, it relied on no OpenUSD knowledge from memory (finding F2). It also did nothing outside its folder. Its `scene.usda` authors `/World/Mug` as `over "Mug"`, following the Referencing Layers tutorial's `OverridePrim`; the Cylinder type comes from the reference.
- Codex saved each docs page it downloaded in its folder (`docs-*.html`). The saved pages aren't kept here. The transcripts keep the commands and the agent's messages; page text and MCP result text that the commands printed are replaced with a line naming the page or the tool, as in the Tier 1 Codex transcripts. The full output is in the session log.
- The MCP results the agent relied on were checked the same way as its cited pages: against usd-core 26.11 and the live docs.
- The reviewer reran the agent's `task.py` on 2026-10-26 in a clean folder with a fresh virtual environment, Python 3.12.3, and usd-core 26.11, using the commands in [tasks.md](../../tasks.md#scoring). The rerun folders have no MCP server registered.

## Tasks

| Task | Outcome | Hints | MCP calls | Folder |
| --- | --- | --- | --- | --- |
| U1 | pass-with-issues | 0 | 1 | [U1](U1/) |
| U2 | pass-with-issues | 0 | 2 | [U2](U2/) |
| U3 | pass | 0 | 2 | [U3](U3/) |
| U4 | not yet run | | | |
| U5 | not yet run | | | |

Each task folder holds the agent's final `task.py`, the exported conversation `transcript.md`, `rerun-output.txt` from the reviewer's rerun, and `check-output.txt` from the task's checker on that rerun.
