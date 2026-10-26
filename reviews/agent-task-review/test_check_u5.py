"""Test check_u5.py against the reference solution and known mistakes.

Usage: python test_check_u5.py   (in a virtual environment with usd-core)

Each case is a task.py: the reference, an edit of it, or a whole script
written by hand. It runs in an "agent" folder with the main set, then is
rerun in a clean folder with a fresh main set and in another with the holdout
set, as the reviewer does, and both are checked. The test passes if every
case fails exactly the expected criteria and raises exactly the expected
kinds of issue.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = (HERE / "reference" / "U5" / "task.py").read_text()

# A correct script that writes its own checks instead of using UsdValidation.
BY_HAND = '''import json
from pathlib import Path

from pxr import Usd, UsdGeom, UsdUtils

HERE = Path(__file__).resolve().parent


def problems(path):
    stage = Usd.Stage.Open(str(path))
    found = set()
    if not stage.HasAuthoredMetadata("upAxis"):
        found.add("missing_up_axis")
    if not stage.HasAuthoredMetadata("metersPerUnit"):
        found.add("missing_meters_per_unit")
    if not broken_refs_ok(path):
        found.add("broken_reference")
    return sorted(found)


def broken_refs_ok(path):
    layers, assets, unresolved = UsdUtils.ComputeAllDependencies(str(path))
    return not unresolved


report = {p.name: problems(p) for p in sorted(HERE.glob("*.usda"))}
(HERE / "report.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
'''
METADATA_BY_HAND = '''    if not stage.HasAuthoredMetadata("upAxis"):
        found.add("missing_up_axis")
    if not stage.HasAuthoredMetadata("metersPerUnit"):
        found.add("missing_meters_per_unit")'''
# Checks the values instead of whether they're authored, so a Y-up file in centimeters is flagged.
METADATA_BY_VALUE = '''    if UsdGeom.GetStageUpAxis(stage) != UsdGeom.Tokens.z:
        found.add("missing_up_axis")
    if UsdGeom.GetStageMetersPerUnit(stage) != 1.0:
        found.add("missing_meters_per_unit")'''
ALL_DEPENDENCIES = '''    layers, assets, unresolved = UsdUtils.ComputeAllDependencies(str(path))
    return not unresolved'''
# Looks only at direct references in the file itself: misses nested ones, payloads, and sublayers.
DIRECT_REFERENCES = '''    layer = Usd.Stage.Open(str(path)).GetRootLayer()
    ok = True

    def visit(spec):
        nonlocal ok
        for ref in spec.referenceList.GetAddedOrExplicitItems():
            if ref.assetPath and not (path.parent / ref.assetPath).exists():
                ok = False
        for child in spec.nameChildren:
            visit(child)

    for spec in layer.rootPrims:
        visit(spec)
    return ok'''
# A correct script that works on layers without composing a stage, as Codex's U5 run did.
BY_LAYER = '''import json
from pathlib import Path

from pxr import Ar, Sdf

HERE = Path(__file__).resolve().parent


def broken(layer, seen):
    if layer.identifier in seen:
        return False
    seen.add(layer.identifier)
    paths = list(layer.subLayerPaths)

    def visit(path):
        spec = layer.GetObjectAtPath(path)
        for key in ("references", "payload"):
            if spec.HasInfo(key):
                paths.extend(a.assetPath for a in spec.GetInfo(key).GetAppliedItems() if a.assetPath)

    layer.Traverse(Sdf.Path.absoluteRootPath, visit)
    for path in paths:
        if not Ar.GetResolver().Resolve(Sdf.ComputeAssetPathRelativeToLayer(layer, path)):
            return True
        child = Sdf.Layer.FindOrOpenRelativeToLayer(layer, path)
        if child is not None and broken(child, seen):
            return True
    return False


report = {}
for path in sorted(HERE.glob("*.usda")):
    layer = Sdf.Layer.FindOrOpen(str(path))
    codes = []
    if not layer.pseudoRoot.HasInfo("upAxis"):
        codes.append("missing_up_axis")
    if not layer.pseudoRoot.HasInfo("metersPerUnit"):
        codes.append("missing_meters_per_unit")
    if broken(layer, set()):
        codes.append("broken_reference")
    report[path.name] = codes
(HERE / "report.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
'''
MAIN_FILES = ('["good.usda", "y_up_centimeters.usda", "no_up_axis.usda", "no_units.usda", '
              '"broken_reference.usda", "nested_broken_reference.usda", "two_problems.usda"]')


def edit(old, new, base=None):
    def apply(src, agent_dir):
        src = base if base is not None else src
        assert old in src, f"case no longer matches its script: {old!r}"
        return src.replace(old, new.replace("{agent}", str(agent_dir)))
    return apply


# name: (task.py for the case, criteria expected to fail, kinds of issue expected)
CASES = {
    "reference (built-in validators)": (lambda s, a: s, set(), []),
    "checks written by hand": (lambda s, a: BY_HAND, set(), []),
    "checks written by hand on layers, without a stage": (lambda s, a: BY_LAYER, set(), []),
    "metadata checked by value, not by whether it's authored": (
        edit(METADATA_BY_HAND, METADATA_BY_VALUE, base=BY_HAND), {"C4"}, []),
    "only direct references checked": (
        edit(ALL_DEPENDENCIES, DIRECT_REFERENCES, base=BY_HAND), {"C5", "C6"}, []),
    "file list written into the script": (
        edit('sorted(HERE.glob("*.usda"))', f"[HERE / n for n in {MAIN_FILES}]"),
        {"C6"}, ["names main-set files"]),
    "parts folder included": (edit('HERE.glob("*.usda")', 'HERE.rglob("*.usda")'), {"C3", "C6"}, []),
    "report keyed by full path": (edit("report[path.name]", "report[str(path)]"), set(), []),
    "hardcoded folder": (
        edit("HERE = Path(__file__).resolve().parent", 'HERE = Path("{agent}")'),
        {"C1", "C3", "C4", "C5", "C6"}, ["hardcoded absolute path"]),
    "asset file edited": (
        edit('(HERE / "report.json")', '(HERE / "no_units.usda").write_text("#usda 1.0\\n")\n(HERE / "report.json")'),
        {"C2"}, ["names main-set files"]),
}
# The route each case's NOTE line should report.
ROUTES = {
    "reference (built-in validators)": "built-in UsdValidation validators",
    "checks written by hand": "checks written by hand",
    "checks written by hand on layers, without a stage": "checks written by hand",
}


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def run_case(name, change, root):
    folders = {"agent": [], "rerun": [], "rerun-holdout": ["--holdout"]}
    for folder, flag in folders.items():
        (root / folder).mkdir(parents=True)
        run([sys.executable, str(HERE / "make_u5_assets.py"), "."] + flag, root / folder)
    script = change(REFERENCE, root / "agent")
    outs, failed, issues = [], set(), set()
    for folder in folders:
        (root / folder / "task.py").write_text(script)
        task = run([sys.executable, "task.py"], root / folder)
        if folder == "agent":
            continue
        out = run([sys.executable, str(HERE / "check_u5.py"), "."], root / folder).stdout
        if task.returncode:
            out = f"task.py exited with {task.returncode}:\n{task.stderr[-2000:]}\n{out}"
        outs.append(f"--- {folder}\n{out}")
        failed |= set(re.findall(r"^FAIL  (C\d)", out, re.M))
        issues |= set(re.findall(r"^ISSUE (.*)$", out, re.M))
    return failed, sorted(issues), "\n".join(outs)


def main():
    problems = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, (name, (change, want_failed, want_issues)) in enumerate(CASES.items()):
            failed, issues, out = run_case(name, change, Path(tmp) / str(i))
            issues_ok = len(issues) == len(want_issues) and all(
                any(w in i for i in issues) for w in want_issues)
            notes = re.findall(r"^NOTE  how task.py finds the problems: (.*)$", out, re.M)
            route_ok = name not in ROUTES or (notes and all(n == ROUTES[name] for n in notes))
            ok = failed == want_failed and issues_ok and route_ok
            problems += not ok
            print(f"{'ok  ' if ok else 'BAD '} {name}: fails {sorted(failed) or 'nothing'}, "
                  f"{len(issues)} kind(s) of issue" + (f", route: {notes[0]}" if name in ROUTES and notes else ""))
            if not ok:
                print(f"     expected fails {sorted(want_failed) or 'nothing'}, issues {want_issues}, "
                      f"route {ROUTES.get(name, 'any')}\n{out}")
    print(f"\n{len(CASES) - problems} of {len(CASES)} cases behaved as expected")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
