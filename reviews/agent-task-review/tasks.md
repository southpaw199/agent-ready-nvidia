# NVIDIA: agent task review tasks

- **Method:** [agent task review](../../../../methods/agent-task-review/method.md), version 0.2
- **Docs given to the agent, Tier 1:** openusd.org and docs.nvidia.com/learn-openusd, with no entry page named
- **Environment for every run:** Ubuntu 24.04 under WSL 2, Python 3.12.3, a new empty folder outside this repository (`~/agent-runs/nvidia/<run_id>/<task>/`, for example `~/agent-runs/nvidia/2026-10-25-codex/U1/`), and a fresh agent session with no project instructions or memory

## Tier 1 standard instructions

Give the agent these instructions first in every Tier 1 session (U1 to U5), then the task prompt. Use the same wording every time, so runs can be compared.

> I'm learning OpenUSD, an open-source framework for describing 3D scenes. Use only these two documentation sites to do this task: the OpenUSD documentation at openusd.org, and NVIDIA's Learn OpenUSD course at docs.nvidia.com/learn-openusd. Don't rely on what you remember about OpenUSD, and don't use other websites. If you use something you already knew rather than something you read in these docs, say so. Each time you rely on a docs page, tell me its URL.
>
> Work only in the current folder. Create a Python virtual environment here and install the usd-core package from PyPI into it. When you're done, run your final script and show me its complete output, including any warnings. Then list the docs page, with its URL, behind each step.

Unlike LanceDB's, these instructions don't name a page to start from. How each agent finds its way into the docs is recorded, not steered.

### Entry points, checked on 2026-10-23

| URL | Result |
| --- | --- |
| https://openusd.org/llms.txt | 404 |
| https://openusd.org/release/llms.txt | 404 |
| https://docs.nvidia.com/learn-openusd/llms.txt | 200: a 27-line index of the course's main sections |
| https://docs.nvidia.com/learn-openusd | 404. The course is at https://docs.nvidia.com/learn-openusd/latest/ |

Check these again on the day of each run, and note any change in the run's README.

## Before the first run: confirm the expected answers

The [`reference/`](reference/) folder has a working solution for each task. Run it in its own folder and virtual environment, outside any agent's folder. The script writes `scene.usda` next to itself, so copy it rather than running it in place:

```bash
mkdir -p ~/agent-runs/nvidia/reference/U1 && cd ~/agent-runs/nvidia/reference/U1
python3 --version                # expect 3.12.3
python3 -m venv .venv && source .venv/bin/activate
pip install usd-core
R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
cp $R/reference/U1/task.py .
python task.py
python $R/check_u1.py scene.usda
```

If a reference result differs from the success criteria below, update the criteria before running any agent. Never show the agent these files.

### Reference results

| Task | Reference result |
| --- | --- |
| U1 | Up axis Z, 1.0 meters per unit, default prim `/World`, `/World` (Xform) and `/World/Box` (Cube), size 4.0, world bounding box (-2, -2, 0) to (2, 2, 4). `check_u1.py`: 11 of 11 checks pass. |

Run on October 23, 2026, with usd-core 26.11, under Python 3.12.3 and Python 3.13, with identical results. The output, the saved file, and the check output are in [`reference/U1/`](reference/U1/).

## Scoring

- **Outcome** and **root cause** use the categories in the [rubric](../../../../methods/agent-task-review/rubric.md), as of method version 0.2.
- A task passes only if you rerun the agent's final `task.py` yourself in a clean folder and every success criterion is met. Copy only `task.py` into a new folder beside the agent's, for example `~/agent-runs/nvidia/2026-10-25-codex/U1-rerun/`, then:
  ```bash
  python3 --version                # expect 3.12.3
  python3 -m venv .venv && . .venv/bin/activate
  pip install usd-core
  python task.py > rerun-output.txt 2>&1
  python ~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review/check_u1.py scene.usda > check-output.txt
  pip show usd-core | grep -E '^(Name|Version):'
  ```
- Score `pass-with-issues` when every success criterion holds but the agent printed warnings it didn't report, relied on knowledge not from the docs, or cited a page that doesn't say what it claims. Open every page the agent cites to check.
- Deprecation warnings don't fail a task, but log each one with root cause `outdated-content` if the docs page the agent cited showed the deprecated form.
- When the agent stalls, give the smallest hint that lets it continue, and log the hint word for word.

---

## Task U1: First stage, units, and a cube on the ground

**Prompt given to the agent:**
> Write a Python script named task.py that does the following:
>
> 1. Creates a new USD stage and saves it as scene.usda in this folder. The scene's units are meters, and the Z axis points up.
> 2. Adds a root transform prim named World and makes it the stage's default prim.
> 3. Under World, adds a cube named Box. Its edges are 4 meters long, it is red, and it rests on the ground plane (z = 0), centered on the origin in x and y.
> 4. Saves the stage, then reopens scene.usda from disk and prints: the stage's up axis and meters per unit, the default prim, each prim's path and type, the cube's size, and the cube's world-space bounding box.

**Docs area exercised:** installation, stages, stage metadata (up axis and units), prims and default prim, UsdGeom Cube, transforms, primvars, bounding boxes

**Success criteria:** all six must hold when you rerun the agent's final `task.py` in a clean folder. [`check_u1.py`](check_u1.py) tests C1 to C6 on the saved `scene.usda`.

| ID | Criterion | How it's checked |
| --- | --- | --- |
| C1 | `scene.usda` is saved as a text USD file | File exists; first line starts with `#usda` |
| C2 | The file opens cleanly | `Usd.Stage.Open` succeeds |
| C3 | Up axis is Z and meters per unit is 1.0, **both authored** in the file | `stage.HasAuthoredMetadata` for `upAxis` and `metersPerUnit`. If either is left out, OpenUSD falls back to Y-up and centimeters (0.01) |
| C4 | `/World` is an Xform and is the default prim | Prim type and `GetDefaultPrim()` |
| C5 | `/World/Box` is a Cube with size 4 and display color red (1, 0, 0) | `size` and `primvars:displayColor` |
| C6 | The cube rests on z = 0, centered in x and y | World bounding box from `UsdGeom.BBoxCache` is (-2, -2, 0) to (2, 2, 4) |

The agent must also run the script itself, report its output, and cite a page for each step.

**What this tests:** the setup and first-success path. Can an agent install OpenUSD's Python bindings, author stage metadata, define prims, and place geometry correctly, using only the docs? A cube is centered on its origin, so the agent must lift it by half its size to rest it on the ground. An agent that skips the stage metadata gets a Y-up stage in centimeters, with the cube on the wrong axis.

**Recorded, not scored:** log these in the run's `notes`; any of them may become a finding.
- **Extent.** Was `extent` authored to match size 4? The cube's fallback extent is size 2: (-1, -1, -1) to (1, 1, 1). `BBoxCache` still computes the right bounds without an authored extent, but anything that reads the `extent` attribute directly sees a 2-meter cube. `check_u1.py` prints a NOTE for this. Before calling it a finding, check what the Cube and Boundable docs say about authoring extent after changing size.
- **How it placed the cube.** Did it reason from the cube being centered on its origin (translate z = 2), or get there by trial?
- **How it set metadata.** `UsdGeom.SetStageUpAxis` and `SetStageMetersPerUnit`, or raw `stage.SetMetadata`? Either passes; note which page led to it.
- **Install path.** Plain `pip install usd-core`, or something else? Any Python version issues?
- **Navigation.** Where did it start? Did it look for an `llms.txt` on either site, or use Markdown versions of pages? See [entry points](#entry-points-checked-on-2026-10-23).
- **Summary versus output.** Anything the script printed that the agent's summary left out or described differently.

**Starting state:** empty folder; fresh virtual environment

**Out of scope:** Omniverse, Isaac Sim, and any RTX GPU; NVIDIA accounts; building OpenUSD from source
