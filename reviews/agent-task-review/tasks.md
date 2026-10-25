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

U2 needs its asset files in the folder first:

```bash
mkdir -p ~/agent-runs/nvidia/reference/U2 && cd ~/agent-runs/nvidia/reference/U2
python3 -m venv .venv && source .venv/bin/activate
pip install usd-core
R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
python $R/make_u2_assets.py .
cp $R/reference/U2/task.py .
python task.py
python $R/check_u2.py .
```

If a reference result differs from the success criteria below, update the criteria before running any agent. Never show the agent these files.

### Reference results

| Task | Reference result |
| --- | --- |
| U1 | Up axis Z, 1.0 meters per unit, default prim `/World`, `/World` (Xform) and `/World/Box` (Cube), size 4.0, world bounding box (-2, -2, 0) to (2, 2, 4). `check_u1.py`: 11 of 11 checks pass. |
| U2 | Table blue (0, 0, 1), chair green (0, 1, 0). Opinions on the table's color, strongest first: `overrides.usda` (blue), then `table.usda` (red). `check_u2.py`: 12 of 12 checks pass. |

U1 was run on October 23, 2026, with usd-core 26.11, under Python 3.12.3 and Python 3.13, with identical results. U2 was run on October 25, 2026, with usd-core 26.11 under Python 3.12.3. Each task's output, saved files, and check output are in its folder under [`reference/`](reference/).

## Scoring

- **Outcome** and **root cause** use the categories in the [rubric](../../../../methods/agent-task-review/rubric.md), as of method version 0.2.
- A task passes only if you rerun the agent's final `task.py` yourself in a clean folder and every success criterion is met. Copy only `task.py` into a new folder beside the agent's, for example `~/agent-runs/nvidia/2026-10-25-codex/U1-rerun/`, then run the commands for that task. For U1:
  ```bash
  python3 --version                # expect 3.12.3
  python3 -m venv .venv && . .venv/bin/activate
  pip install usd-core
  python task.py > rerun-output.txt 2>&1
  python ~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review/check_u1.py scene.usda > check-output.txt
  pip show usd-core | grep -E '^(Name|Version):'
  ```
  For U2, create fresh asset files in the rerun folder first, so the rerun can't use the agent's copies:
  ```bash
  python3 --version                # expect 3.12.3
  python3 -m venv .venv && . .venv/bin/activate
  pip install usd-core
  R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
  python $R/make_u2_assets.py .
  python task.py > rerun-output.txt 2>&1
  python $R/check_u2.py . > check-output.txt
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

---

## Task U2: Reference two assets and override one in a stronger layer

**Prompt given to the agent:**
> This folder has two USD asset files, table.usda and chair.usda. Don't change them. Write a Python script named task.py that does the following:
>
> 1. Creates a new USD stage and saves it as scene.usda in this folder, with a root transform prim named World as its default prim.
> 2. Adds the table and the chair to the scene by referencing the two asset files, at /World/Table and /World/Chair.
> 3. Changes the table's display color to blue (0, 0, 1) in a second layer, overrides.usda, in this folder. scene.usda should bring in overrides.usda so that its opinion is stronger than the asset's. Don't set the color anywhere else.
> 4. Saves the stage and the new layer, then reopens scene.usda from disk and prints: the table's and the chair's display colors as composed, and each layer that has an opinion about the table's display color, strongest first.
>
> Then explain in a few sentences which opinion about the table's color wins, and why, in terms of OpenUSD's strength ordering.

**Docs area exercised:** layers and sublayers, references, default prims, edit targets, composition and LIVERPS strength ordering

**Success criteria:** C1 to C6 must hold when you rerun the agent's final `task.py` in a clean folder with fresh asset files; [`check_u2.py`](check_u2.py) tests them on the saved files. C7 is scored by reading the agent's answer, and a wrong or missing explanation makes the run `pass-with-issues` rather than `fail`.

| ID | Criterion | How it's checked |
| --- | --- | --- |
| C1 | `scene.usda` and `overrides.usda` are saved as text USD files | Both exist; each first line starts with `#usda` |
| C2 | The asset files are unchanged | `table.usda` and `chair.usda` match what `make_u2_assets.py` wrote, byte for byte |
| C3 | `scene.usda` opens, and `/World` is an Xform and the default prim | `Usd.Stage.Open`, prim type, and `GetDefaultPrim()` |
| C4 | `/World/Table` and `/World/Chair` reference `table.usda` and `chair.usda` in the same folder | A reference arc to each asset, found with `Usd.PrimCompositionQuery`, resolving to the file in the folder being checked; composed type Cube |
| C5 | `overrides.usda` is composed into `scene.usda` | `overrides.usda` is among the stage's used layers, by any arc. How it was brought in is recorded, not scored |
| C6 | The table is blue, the chair is still green, and the table's color comes from `overrides.usda` | Composed `primvars:displayColor`; the attribute's property stack has `overrides.usda` first and no opinion in `scene.usda` |
| C7 | The explanation is correct for how the agent brought in `overrides.usda` | **As a sublayer** (the expected route): the override wins because a sublayer of the scene's root layer holds local opinions (the L in LIVERPS), which are stronger than opinions from references (the R). **As a second reference on the table:** both opinions come through references (the R), and the earlier reference in the list is stronger. Either way, it says the red in `table.usda` is still there, only weaker. A wrong or missing explanation scores `pass-with-issues`. |

The agent must also run the script itself, report its output, and cite a page for each step.

**What this tests:** whether the docs lead an agent to sublayers, the usual way to layer a change over a scene, when the prompt describes only the outcome and never names them; whether they explain references and editing a specific layer well enough to change a scene without touching its assets; and whether they explain strength ordering clearly enough for the agent to say why the override wins. An agent that edits `table.usda`, or sets the color in `scene.usda`, gets a blue table but fails C2 or C6: that isn't a layered change, and in a pipeline it would overwrite someone else's asset or bury the change where no one expects it.

**Expected behavior to understand before scoring:** opinions authored in `scene.usda` itself are stronger than those in its sublayers. If an agent sets the color in both, the table takes the `scene.usda` value, and C6 fails even though `overrides.usda` is correct. An agent that brings in `overrides.usda` as a second reference passes C1 to C6 if that reference comes first in the list, and fails C6 if it comes after the asset's, because a later reference is weaker.

**Issues `check_u2.py` flags in `task.py`:** it reads the agent's script and prints an `ISSUE` line for the reviewer to confirm by reading the code. Issues don't fail a check on their own.
- **Hardcoded absolute path.** Paths must be built at run time, for example from `__file__`, or be relative. A hardcoded path to the agent's own folder also fails C4 in the rerun, because the references point back at the agent's folder instead of the rerun's.
- **Layer list possibly typed by hand.** The script calls nothing that can list opinions, such as `GetPropertyStack` or `PrimCompositionQuery`. If reading `task.py` confirms the list is typed in rather than computed, score `pass-with-issues`, even when C1 to C7 hold.

[`test_check_u2.py`](test_check_u2.py) runs the checker against the reference and eight other cases: both issues above, five known mistakes, and the override brought in as a reference ahead of the asset, which passes. It confirms each case fails exactly the expected criteria. Run it after any change to `check_u2.py`.

**Recorded, not scored:**
- **How it brought in `overrides.usda`. The main observation for this task.** A sublayer, a second reference, or something else, and which page led it there. `check_u2.py` prints it as a NOTE, with the table's composition arcs in strength order.
- **How it referenced the assets.** Relative paths, or absolute ones built at run time; the asset's default prim or an explicit prim path. `check_u2.py` prints both as NOTEs.
- **If it used a sublayer, how it added it.** `subLayerPaths.append` or `insert`, or another API.
- **How it wrote the override.** An edit target (`Usd.EditContext` or `stage.SetEditTarget`), Sdf specs written directly, or text. Any of these passes.
- **How it found the layers to print.** Which API it used, and which page led to it.
- **Stage metadata.** Whether it set `upAxis` and `metersPerUnit` on `scene.usda`, as in U1. Not required here.
- **Strength ordering source.** Which page it cited for LIVERPS, and whether it says LIVERPS or LIVRPS.
- **Navigation.** Where it started, and whether it looked for an `llms.txt`.
- **Summary versus output.** Anything the script printed that the agent's summary left out or described differently.

**Starting state:** empty folder plus the asset files. Before the session, create them in the run folder with [`make_u2_assets.py`](make_u2_assets.py), then start the agent. Don't show the agent the script.

```bash
python ~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review/make_u2_assets.py .
```

That creates `table.usda` (a red 2 m cube) and `chair.usda` (a green 1 m cube, 3 m along x), each with its cube as the default prim.

**Out of scope:** variant sets, payloads, inherits, and other arcs (later tasks); Omniverse and Isaac Sim
