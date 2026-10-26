# NVIDIA: agent task review tasks

- **Method:** [agent task review](../../../../methods/agent-task-review/method.md), version 0.2
- **Docs given to the agent, Tier 1:** openusd.org and docs.nvidia.com/learn-openusd, with no entry page named
- **Environment for every run:** Ubuntu 24.04 under WSL 2, Python 3.12.3, a new empty folder outside this repository (`~/agent-runs/nvidia/<run_id>/<task>/`, for example `~/agent-runs/nvidia/2026-10-25-codex/U1/`), and a fresh agent session with no project instructions or memory, started from a terminal with no virtual environment active (run `deactivate` first), so the agent doesn't inherit a rerun's Python

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

U3 works the same way, with its own asset file:

```bash
mkdir -p ~/agent-runs/nvidia/reference/U3 && cd ~/agent-runs/nvidia/reference/U3
python3 -m venv .venv && source .venv/bin/activate
pip install usd-core
R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
python $R/make_u3_assets.py .
cp $R/reference/U3/task.py .
python task.py > rerun-output.txt 2>&1
python $R/check_u3.py .
```

U4 the same way:

```bash
mkdir -p ~/agent-runs/nvidia/reference/U4 && cd ~/agent-runs/nvidia/reference/U4
python3 -m venv .venv && source .venv/bin/activate
pip install usd-core
R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
python $R/make_u4_assets.py .
cp $R/reference/U4/task.py .
python task.py
python $R/check_u4.py .
```

U5 runs on two sets of files, the main set and the holdout set:

```bash
R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
mkdir -p ~/agent-runs/nvidia/reference/U5 && cd ~/agent-runs/nvidia/reference/U5
python3 -m venv .venv && source .venv/bin/activate
pip install usd-core
for s in main holdout; do
  mkdir -p $s && cd $s
  python $R/make_u5_assets.py . $([ $s = holdout ] && echo --holdout)
  cp $R/reference/U5/task.py .
  python task.py > output.txt 2>&1
  python $R/check_u5.py .
  cd ..
done
```

If a reference result differs from the success criteria below, update the criteria before running any agent. Never show the agent these files.

### Reference results

| Task | Reference result |
| --- | --- |
| U1 | Up axis Z, 1.0 meters per unit, default prim `/World`, `/World` (Xform) and `/World/Box` (Cube), size 4.0, world bounding box (-2, -2, 0) to (2, 2, 4). `check_u1.py`: 11 of 11 checks pass. |
| U2 | Table blue (0, 0, 1), chair green (0, 1, 0). Opinions on the table's color, strongest first: `overrides.usda` (blue), then `table.usda` (red). `check_u2.py`: 12 of 12 checks pass. |
| U3 | Variants `blue` and `red`. As saved: selection `blue`, mug blue (0, 0, 1). After switching in code: selection `red`, mug red (1, 0, 0); the saved file still selects `blue`. `check_u3.py`: 11 of 11 checks pass. |
| U4 | Scenegraph instancing. `references.usda`: 2,001 prims traversed, 0 prototypes. `instanced.usda`: 1,001 prims traversed, 1 prototype. Both open in about 16 to 24 ms, and both compose to bounds (-0.5, -0.5, 0) to (78.5, 48.5, 1). `check_u4.py`: 10 of 10 checks pass. |
| U5 | Built-in `UsdValidation` validators. Main set: `good.usda` and `y_up_centimeters.usda` clean; `no_up_axis.usda`, `no_units.usda`, `broken_reference.usda`, and `nested_broken_reference.usda` one code each; `two_problems.usda` all three. Holdout set: `kitchen.usda` clean, `attic.usda` broken reference (a missing sublayer), `garage.usda` both metadata codes, `cellar.usda` missing up axis and a broken reference (a missing payload). `check_u5.py`: 13 of 13 on the main set and 9 of 9 on the holdout set. |

U1 was run on October 23, 2026, with usd-core 26.11, under Python 3.12.3 and Python 3.13, with identical results. U2 to U5 were run on October 25, 2026, with usd-core 26.11 under Python 3.12.3. Open times vary from run to run; compare an agent's times with each other, not with these.

The reviewer confirmed the U2 to U4 references independently the same day, in `~/agent-runs/nvidia/reference/`, with Python 3.12.3 and usd-core 26.11. Every check passed, and the outputs matched the ones recorded here: identical for U2 and U3, and the same counts for U4, which opened in 13.8 and 15.1 ms. The reviewer also ran the three checker tests, `test_check_u2.py`, `test_check_u3.py`, and `test_check_u4.py`: 9 of 9, 9 of 9, and 10 of 10 cases behaved as expected. The reviewer confirmed the U5 reference the same way, after it was written: 13 of 13 checks on the main set and 9 of 9 on the holdout set, with both reports identical to the ones recorded here, and `test_check_u5.py` 9 of 9. Each task's output, saved files, and check output are in its folder under [`reference/`](reference/).

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
  For U3, the same, with its own asset script and checker. The checker also reads `rerun-output.txt`, so keep that name:
  ```bash
  python3 --version                # expect 3.12.3
  python3 -m venv .venv && . .venv/bin/activate
  pip install usd-core
  R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
  python $R/make_u3_assets.py .
  python task.py > rerun-output.txt 2>&1
  python $R/check_u3.py . > check-output.txt
  pip show usd-core | grep -E '^(Name|Version):'
  ```
  For U4:
  ```bash
  python3 --version                # expect 3.12.3
  python3 -m venv .venv && . .venv/bin/activate
  pip install usd-core
  R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
  python $R/make_u4_assets.py .
  python task.py > rerun-output.txt 2>&1
  python $R/check_u4.py . > check-output.txt
  pip show usd-core | grep -E '^(Name|Version):'
  ```
  For U5, rerun twice, on the main set in `U5-rerun/` and on the holdout set in `U5-rerun-holdout/`, copying only `task.py` into each. The holdout rerun shows whether the script works on files it hasn't seen (C6).
  ```bash
  python3 --version                # expect 3.12.3
  R=~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review
  cd ~/agent-runs/nvidia/<run_id>/U5-rerun
  python3 -m venv .venv && . .venv/bin/activate
  pip install usd-core
  python $R/make_u5_assets.py .
  python task.py > rerun-output.txt 2>&1
  python $R/check_u5.py . > check-output.txt
  cd ../U5-rerun-holdout
  python $R/make_u5_assets.py . --holdout
  python task.py > rerun-output.txt 2>&1
  python $R/check_u5.py . > check-output.txt
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

---

## Task U3: Add a variant set and switch between its variants in code

**Prompt given to the agent:**
> This folder has a USD asset file, mug.usda. Don't change it. Write a Python script named task.py that does the following:
>
> 1. Creates a new USD stage and saves it as scene.usda in this folder, with a root transform prim named World as its default prim, and adds the mug by referencing mug.usda at /World/Mug.
> 2. In scene.usda, gives /World/Mug a variant set named color with two variants, red and blue, that set the mug's display color to (1, 0, 0) and (0, 0, 1). Don't set the display color anywhere else in scene.usda.
> 3. Selects the blue variant and saves the stage.
> 4. Reopens scene.usda from disk and prints the variant set's variants, the current selection, and the mug's display color. Then switches the selection to red in code and prints the selection and color again. When the script finishes, scene.usda on disk should still select blue.

**Docs area exercised:** variant sets and variants, variant edit contexts, variant selections, references, edit targets and the session layer

**Success criteria:** C1 to C7 must hold when you rerun the agent's final `task.py` in a clean folder with a fresh asset file. [`check_u3.py`](check_u3.py) tests C1 to C6 on the saved file; C7 is scored by reading `task.py` and `rerun-output.txt`, with help from the checker's `ISSUE` lines.

| ID | Criterion | How it's checked |
| --- | --- | --- |
| C1 | `scene.usda` is saved as a text USD file | First line starts with `#usda` |
| C2 | The asset file is unchanged | `mug.usda` matches what `make_u3_assets.py` wrote, byte for byte |
| C3 | `scene.usda` opens, and `/World` is an Xform and the default prim | `Usd.Stage.Open`, prim type, and `GetDefaultPrim()` |
| C4 | `/World/Mug` references `mug.usda` in the same folder | A reference arc, found with `Usd.PrimCompositionQuery`, resolving to the file in the folder being checked; composed type Cylinder |
| C5 | `scene.usda` gives `/World/Mug` a variant set `color` with exactly the variants `red` and `blue`, and the saved selection is `blue` | The root layer's prim spec lists the variant set; `GetVariantNames()` and `GetVariantSelection()` on the reopened stage |
| C6 | Each variant carries its color, and nothing else sets it in `scene.usda` | As saved, the mug is blue. The checker selects each variant in the session layer: red gives (1, 0, 0) and blue gives (0, 0, 1), with the strongest opinion inside that variant. No display color is authored on `/World/Mug` outside the variants. |
| C7 | The script switches to red in code and prints the selection and color both before and after | `check_u3.py` flags an output that doesn't show both colors. Confirm by reading `task.py`: the switch must happen in the script, not by reopening a file the script saved with red. If reading confirms the switch is missing or broken, C7 fails, and so does the run. |

The agent must also run the script itself, report its output, and cite a page for each step.

**What this tests:** whether the docs explain how to author a variant set on a prim that references an asset, put opinions inside each variant, and switch between variants in code without changing the saved file. That last part is where the docs on edit targets and the session layer come in, though the prompt doesn't name either.

**Expected behavior to understand before scoring:**
- **Switching on the stage is fine if it isn't saved.** `SetVariantSelection` on the reopened stage edits the root layer in memory. That passes, as long as the script doesn't save afterward. Switching in the session layer passes too, and leaves nothing to save by accident. The checker notes which one the agent used.
- **Saving after the switch is the trap.** A script that switches to red and then calls `Save()` leaves `scene.usda` selecting red, and fails C5 and C6.
- **A color set directly on `/World/Mug` wins over the variants.** A local opinion outside the variants is stronger than one inside them (L before V in LIVERPS), so switching variants no longer changes the color. C6 fails, and the output shows no red.

**Issues `check_u3.py` flags:** it prints an `ISSUE` line for the reviewer to confirm. Issues don't fail a check on their own.
- **Hardcoded absolute path** in `task.py`, as in U2. It also fails C4 in the rerun.
- **No red or blue in `rerun-output.txt`.** The output doesn't show both colors, so the switch may be missing or broken. Read `task.py` to confirm. If it is, C7 fails. If `task.py` does switch and only prints the colors in a form the checker didn't recognize, C7 holds; note the false alarm in `notes`.

[`test_check_u3.py`](test_check_u3.py) runs the checker against the reference and eight other cases: both kinds of issue, switching without the session layer (passes), switching and then saving, a color set outside the variants, variants named `Red` and `Blue`, and an edited asset file. Run it after any change to `check_u3.py`.

**Recorded, not scored:**
- **How it switched.** In the session layer, on the stage without saving, or something else, and which page led to it. `check_u3.py` notes whether `task.py` uses the session layer.
- **How it authored the variants.** `GetVariantEditContext()`, an edit target, or Sdf specs written directly, and which page.
- **Whether it noticed the save trap.** Did it explain why the saved file still selects blue, or just get there?
- **How it referenced the asset.** Relative or run-time paths; default prim or explicit prim path.
- **Stage metadata.** Whether it set `upAxis` and `metersPerUnit` on `scene.usda`. Not required here.
- **Navigation.** Where it started, and whether it looked for an `llms.txt`.
- **Summary versus output.** Anything the script printed that the agent's summary left out or described differently.

**Starting state:** empty folder plus the asset file. Before the session, create it in the run folder with [`make_u3_assets.py`](make_u3_assets.py), then start the agent. Don't show the agent the script.

```bash
python ~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review/make_u3_assets.py .
```

That creates `mug.usda`, a green cylinder 1 m tall, with the cylinder as its default prim.

**Out of scope:** variant sets inside the asset file, nested variant sets, payloads, and instancing (U4); Omniverse and Isaac Sim

---

## Task U4: Place 1,000 copies by reference and with instancing, and explain the tradeoff

**Prompt given to the agent:**
> This folder has a USD asset file, crate.usda. Don't change it. Write a Python script named task.py that does the following:
>
> 1. Creates references.usda in this folder: a stage with a root transform prim named World as its default prim, and 1,000 crates under World, each one a prim that references crate.usda. Place crate i, for i from 0 to 999, at x = 2 × (i mod 40), y = 2 × floor(i / 40), z = 0, in meters.
> 2. Creates instanced.usda in this folder with the same 1,000 crates in the same places, but using OpenUSD's instancing, so the crates share one copy of the crate's data instead of each having its own.
> 3. Saves both files, then opens each from disk and prints, for each one: how long it took to open, how many prims a traversal of the stage visits, and how many prototypes the stage has.
>
> Then explain in a few sentences what instancing saved in this scene, and what you give up by using it.

**Docs area exercised:** scenegraph instancing, instanceable metadata, prototypes and instance proxies, point instancing, references, stage traversal

**Success criteria:** C1 to C7 must hold when you rerun the agent's final `task.py` in a clean folder with a fresh asset file; [`check_u4.py`](check_u4.py) tests C1 to C6 on the saved files. C7 is scored by reading `task.py` and `rerun-output.txt`. C8, the explanation, is scored by reading the agent's answer, and a wrong or missing explanation makes the run `pass-with-issues` rather than `fail`, as in U2.

| ID | Criterion | How it's checked |
| --- | --- | --- |
| C1 | `references.usda` and `instanced.usda` are saved as text USD files | Both exist; each first line starts with `#usda` |
| C2 | The asset file is unchanged | `crate.usda` matches what `make_u4_assets.py` wrote, byte for byte |
| C3 | Both files open, and `/World` is an Xform and the default prim in each | `Usd.Stage.Open`, prim type, and `GetDefaultPrim()` |
| C4 | `references.usda` has 1,000 plain references to `crate.usda` in the right places | 1,000 prims with a reference arc resolving to `crate.usda` in the folder being checked, none instanceable, no PointInstancer; their world positions match the grid |
| C5 | `instanced.usda` places the same 1,000 crates sharing one copy of the crate | Either scenegraph instancing (1,000 instanceable prims referencing `crate.usda`, one prototype) or point instancing (one PointInstancer with 1,000 instances of a prototype that references `crate.usda`); positions match the grid either way |
| C6 | Both files compose to the same scene | World bounds of `/World` in each are (-0.5, -0.5, 0) to (78.5, 48.5, 1) |
| C7 | The script prints the open time, the prims traversed, and the prototype count for both files, all measured by the script | Read `task.py` and `rerun-output.txt`; compare the counts with the checker's NOTE lines, which give its own counts. If a measurement is missing or made up, C7 fails, and so does the run. |
| C8 | The explanation is correct | Says instancing cut the number of prims the stage holds, giving its numbers (2,001 to 1,001 with scenegraph instancing, or a handful with point instancing), which saves memory and composition work as scenes grow. Says what you give up: with scenegraph instancing, the prims inside each instance are read-only instance proxies, so one crate's contents can't be edited without breaking instancing for it, and every instance shares the same composed data; with point instancing, the instances aren't prims at all and their differences live in arrays. Doesn't claim a time saving that its own numbers don't show. A wrong or missing explanation scores `pass-with-issues`. |

The agent must also run the script itself, report its output, and cite a page for each step.

**What this tests:** whether the docs explain instancing well enough for an agent to set it up, measure what it changes, and explain the tradeoff. The prompt says "OpenUSD's instancing" without saying which kind, so the run also shows which kind the docs lead to. This is the closest match to LanceDB's T5, which asked the same of a vector index.

**Expected behavior to understand before scoring:**
- **The prim counts are the signal, not the times.** At 1,000 small crates, both files open in tens of milliseconds, and the times vary from run to run. Scenegraph instancing roughly halves the prims a traversal visits. Point instancing cuts them to a handful, and its file opens noticeably faster.
- **The first open in a process is slower.** It pays one-time startup costs, so whichever file a script times first can look slower for reasons that have nothing to do with instancing. The reference opens the asset once before timing. Record whether the agent noticed.
- **Counting instance proxies gives 2,001 for both files.** A traversal that includes instance proxies, for example with `Usd.TraverseInstanceProxies()`, visits every crate's contents. If the agent counted that way and said so, C7 holds; record it.
- **Point instancing passes.** It shares the crate as a prototype too. The checker accepts either kind and notes which one.

**Issues `check_u4.py` flags in `task.py`:** it prints an `ISSUE` line for the reviewer to confirm by reading the code. Issues don't fail a check on their own.
- **Hardcoded absolute path,** as in U2 and U3. It also fails C4 and C5 in the rerun.
- **Counts possibly typed by hand.** The script calls nothing that can count prims or prototypes, such as `Traverse` or `GetPrototypes`. If reading `task.py` confirms the counts are typed in, C7 fails.

[`test_check_u4.py`](test_check_u4.py) runs the checker against the reference and nine other cases: both kinds of issue, point instancing (passes), crates never marked instanceable, both files instanceable, the wrong grid, copies instead of references, and an edited asset file. Run it after any change to `check_u4.py`.

**Recorded, not scored:**
- **Which instancing it used,** and which page led there. `check_u4.py` prints it as a NOTE.
- **How it counted and timed.** Default traversal or instance proxies; one timed open or several; whether it allowed for the slower first open.
- **What its explanation covers.** Instance proxies, de-instancing a crate to edit it, point instancing as the alternative for very many simple copies, and memory as the main saving.
- **How it referenced the asset.** Relative or run-time paths; default prim or explicit prim path.
- **Navigation.** Where it started, and whether it looked for an `llms.txt`.
- **Summary versus output.** Anything the script printed that the agent's summary left out or described differently.

**Starting state:** empty folder plus the asset file. Before the session, create it in the run folder with [`make_u4_assets.py`](make_u4_assets.py), then start the agent. Don't show the agent the script.

```bash
python ~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review/make_u4_assets.py .
```

That creates `crate.usda`, a brown 1 m crate: an Xform with the cube as its child, so there's something below the instance for instancing to share.

**Out of scope:** payloads and load rules, nested instancing, refining individual instances, and GPU rendering; Omniverse and Isaac Sim

---

## Task U5: Write a script that flags problems in .usda files

**Prompt given to the agent:**
> This folder has several USD files at the top level, and a parts folder that some of them use. Don't change any of them. Write a Python script named task.py that checks every .usda file at the top level of this folder (not the parts folder) for these problems:
>
> - missing_up_axis: the file doesn't specify the stage's up axis (upAxis).
> - missing_meters_per_unit: the file doesn't specify the stage's units (metersPerUnit).
> - broken_reference: the file refers to another file that can't be found, through a reference, a payload, or a sublayer, either directly or through a file it brings in.
>
> The script should write report.json in this folder, mapping each file's name to a list of the codes for the problems found in it, with an empty list for a file that has none, and print the report. It should work on any folder of .usda files, not only these.
>
> Then tell me how the script detects each problem.

**Docs area exercised:** asset validation, the `UsdValidation` framework and its built-in validators, `usdchecker`, stage metadata, layer dependencies

**Success criteria:** C1 to C6 must hold when you rerun the agent's final `task.py` in two clean folders: one with a fresh main set, and one with the holdout set, which the agent never sees. [`check_u5.py`](check_u5.py) tests all six; it scores C1 to C5 on the main set, and the same checks on the holdout set count as C6.

| ID | Criterion | How it's checked |
| --- | --- | --- |
| C1 | `report.json` is written, as a JSON object mapping each file to a list of codes | It parses, and every value is a list of strings |
| C2 | The files are unchanged | Every file `make_u5_assets.py` wrote, including `parts/`, matches byte for byte |
| C3 | The report covers exactly the top-level `.usda` files | No file missing, and nothing from `parts/`. Keys are compared by file name, so full paths are fine |
| C4 | `missing_up_axis` and `missing_meters_per_unit` are right for every file | Including `y_up_centimeters.usda`, which authors a Y up axis and centimeters and so has neither problem |
| C5 | `broken_reference` is right for every file, and no other codes appear | Including a broken reference inside `parts/shelf.usda`, and a missing payload |
| C6 | The same holds on the holdout set | C1 to C5 again, on different files: a missing sublayer, a missing payload, and different names |

The agent must also run the script itself, report its output, and cite a page for each step. The explanation of how the script detects each problem is recorded, not scored.

**What this tests:** where the docs lead an agent that has to validate files. usd-core 26.11 includes the `UsdValidation` framework, with built-in validators for exactly these problems: `usdGeomValidators:StageMetadataChecker` and `usdUtilsValidators:MissingReferenceValidator`. The older `UsdUtils.ComplianceChecker` is gone from this build. Learn OpenUSD's validation exercise uses the `usdchecker` command-line tool, which the usd-core pip package doesn't install, and openusd.org documents `UsdValidation` in C++ only. So an agent can use the built-in validators by working out their Python names, try `usdchecker` and find it missing, or write its own checks. Any route passes if the report is right; which one it takes is the main observation.

**Expected behavior to understand before scoring:**
- **USD prints warnings when it opens these files.** Opening a file with a broken reference, payload, or sublayer prints warnings such as "Could not open asset". With the built-in validators, `MissingReferenceValidator` also prints "Ill-formed SdfPath" for each missing file. That one looks like a quirk of the validator itself; it appears even when the report is right, and it's logged as a possible `product-defect` to verify, not a docs finding. These warnings are expected. An agent that reports them hasn't done anything wrong; one that leaves them out of its summary is scored as with any unreported warning.
- **Authored, not the right value.** `y_up_centimeters.usda` authors both settings, just not Z-up meters. A script that tests the values instead of whether they're authored flags it and fails C4.
- **Following every dependency.** A broken reference can hide inside a file that's brought in (`nested_broken_reference.usda`), or come through a payload or a sublayer. A script that checks only direct references in the top-level file misses these and fails C5 and C6. `UsdUtils.ComputeAllDependencies` and the built-in validator both follow them. A script that opens stages without loading payloads, then checks composition errors, misses the missing payloads.

**Issues `check_u5.py` flags in `task.py`:** it prints an `ISSUE` line for the reviewer to confirm by reading the code. Issues don't fail a check on their own.
- **Hardcoded absolute path or folder.** The script must find its files at run time. A hardcoded folder also fails C1 to C6 in the reruns, because the script reads and writes the agent's folder instead.
- **Main-set file names written into the script.** It may only handle the files it was shown. The holdout rerun, C6, settles it.

[`test_check_u5.py`](test_check_u5.py) runs the checker against the reference and eight other cases: correct checks written by hand (passes), metadata checked by value, only direct references checked, a file list written into the script, the `parts/` folder included, a report keyed by full paths (passes), a hardcoded folder, and an edited file. Each case is checked on both sets. Run it after any change to `check_u5.py`.

**Recorded, not scored:**
- **Which route it took,** and which pages led there: built-in validators, `usdchecker`, or its own checks. `check_u5.py` prints it as a NOTE. Did it look for `usdchecker` or `ComplianceChecker` and find them missing?
- **Whether its explanation matches its code.** For example, an agent that says it uses OpenUSD's validators but checks by hand.
- **Python names.** If it used `UsdValidation`, whether it worked out the Python names from the C++ pages (see F2) and said so.
- **Warnings.** Which USD warnings it reported, including "Ill-formed SdfPath".
- **Navigation.** Where it started, and whether it looked for an `llms.txt`.
- **Summary versus output.** Anything the script printed that the agent's summary left out or described differently.

**Starting state:** empty folder plus the main set. Before the session, create it in the run folder with [`make_u5_assets.py`](make_u5_assets.py), then start the agent. Don't show the agent the script, and don't create the holdout set in the agent's folder; it's only for the reruns.

```bash
python ~/projects/agent-ready-docs/case-studies/nvidia/reviews/agent-task-review/make_u5_assets.py .
```

That creates seven top-level files and a `parts/` folder with two more.

**Out of scope:** fixing the problems, validators beyond these three problems, usdz packages, and writing custom `UsdValidation` validators; Omniverse and Isaac Sim
