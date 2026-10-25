# Case study: NVIDIA OpenUSD, Omniverse, and Isaac Sim

**Status: in progress.**

This case study applies the [agent task review](../../methods/agent-task-review/method.md) to three related doc sets: [OpenUSD](https://openusd.org) with NVIDIA's [Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/) course, [Omniverse](https://docs.omniverse.nvidia.com), and [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com). It runs in three tiers:

| Tier | What the agents do | Docs |
| --- | --- | --- |
| 1 | Hands-on OpenUSD tasks U1 to U5, run on a CPU with the `usd-core` package from PyPI | openusd.org and Learn OpenUSD |
| 2 | Answer a set of 20 questions from the docs, with citations. Omniverse and Isaac Sim need an RTX GPU to run, so this tier is questions only. | Omniverse and Isaac Sim |
| 3 | Answer the Isaac Sim setup questions from Tier 2 again with NVIDIA's `install-isaacsim` agent skill loaded, for comparison | Isaac Sim |

| Folder | What it holds |
| --- | --- |
| [`reviews/agent-task-review/`](reviews/agent-task-review/) | Tasks, success criteria, reference results, the run log, and findings. |

Results will be added here as each tier is finished.
