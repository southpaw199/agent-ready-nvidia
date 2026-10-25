"""Test check_u2.py against the reference solution and known mistakes.

Usage: python test_check_u2.py   (in a virtual environment with usd-core)

Each case edits the reference task.py, runs it in an "agent" folder, then
reruns it in a clean "rerun" folder with fresh asset files, as the reviewer
does, and checks the rerun folder. The test passes if every case fails
exactly the expected criteria and raises exactly the expected issues.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = (HERE / "reference" / "U2" / "task.py").read_text()

OVERRIDE = "with Usd.EditContext(stage, overrides):"
SUBLAYER_OVERRIDE = """stage.GetRootLayer().subLayerPaths.append("./overrides.usda")
with Usd.EditContext(stage, overrides):
    UsdGeom.Gprim(table).GetDisplayColorAttr().Set(Vt.Vec3fArray([Gf.Vec3f(0.0, 0.0, 1.0)]))"""
# The same override, brought in as a second reference on the table instead of a sublayer.
REFERENCE_OVERRIDE = """spec = Sdf.CreatePrimInLayer(overrides, "/TableOverride")
color = Sdf.AttributeSpec(spec, "primvars:displayColor", Sdf.ValueTypeNames.Color3fArray)
color.default = Vt.Vec3fArray([Gf.Vec3f(0.0, 0.0, 1.0)])
overrides.Save()
table.GetReferences().AddReference("./overrides.usda", "/TableOverride",
                                   position=Usd.ListPosition{position})"""
STACK_LOOP = """for spec in table_color.GetPropertyStack(Usd.TimeCode.Default()):
    print(f"  {Path(spec.layer.identifier).name}: {list(spec.default)}")"""


def edit(old, new):
    def apply(src, agent_dir):
        assert old in src, f"case no longer matches the reference: {old!r}"
        return src.replace(old, new.replace("{agent}", str(agent_dir)))
    return apply


def edits(*fns):
    def apply(src, agent_dir):
        for fn in fns:
            src = fn(src, agent_dir)
        return src
    return apply


# name: (change to the reference, criteria expected to fail, issue text expected)
CASES = {
    "reference": (lambda s, a: s, set(), []),
    "absolute paths built at run time": (
        edits(edit('"./table.usda"', 'str(HERE / "table.usda")'),
              edit('"./chair.usda"', 'str(HERE / "chair.usda")')),
        set(), []),
    "hardcoded absolute paths": (
        edits(edit('"./table.usda"', '"{agent}/table.usda"'),
              edit('"./chair.usda"', '"{agent}/chair.usda"')),
        {"C4"}, ["hardcoded absolute path"]),
    "layer list typed by hand": (
        edit(STACK_LOOP, 'print("  overrides.usda: [Gf.Vec3f(0.0, 0.0, 1.0)]")\n'
                         'print("  table.usda: [Gf.Vec3f(1.0, 0.0, 0.0)]")'),
        set(), ["typed by hand"]),
    "color set in scene.usda": (edit(OVERRIDE, "if True:"), {"C6"}, []),
    "asset file edited": (
        edits(edit(OVERRIDE, "if False:"),
              edit("stage.Save()\n", 'stage.Save()\n(HERE / "table.usda").write_text('
                   '(HERE / "table.usda").read_text().replace("(1, 0, 0)", "(0, 0, 1)"))\n')),
        {"C2", "C6"}, []),
    "override layer never brought into the scene": (
        edits(edit('stage.GetRootLayer().subLayerPaths.append("./overrides.usda")\n', ""),
              edit(OVERRIDE, "if False:")),
        {"C5", "C6"}, []),
    "override layer referenced ahead of the asset": (
        edit(SUBLAYER_OVERRIDE, REFERENCE_OVERRIDE.replace("{position}", "FrontOfPrependList")),
        set(), []),
    "override layer referenced behind the asset (weaker)": (
        edit(SUBLAYER_OVERRIDE, REFERENCE_OVERRIDE.replace("{position}", "BackOfPrependList")),
        {"C6"}, []),
}


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def run_case(name, change, root):
    agent, rerun = root / "agent", root / "rerun"
    for folder in (agent, rerun):
        folder.mkdir(parents=True)
        run([sys.executable, str(HERE / "make_u2_assets.py"), "."], folder)
    script = change(REFERENCE, agent)
    for folder in (agent, rerun):
        (folder / "task.py").write_text(script)
        task = run([sys.executable, "task.py"], folder)
    out = run([sys.executable, str(HERE / "check_u2.py"), "."], rerun).stdout
    if task.returncode:
        out = f"task.py exited with {task.returncode}:\n{task.stderr}\n{out}"
    failed = set(re.findall(r"^FAIL  (C\d)", out, re.M))
    issues = re.findall(r"^ISSUE (.*)$", out, re.M)
    return failed, issues, out


def main():
    problems = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, (name, (change, want_failed, want_issues)) in enumerate(CASES.items()):
            failed, issues, out = run_case(name, change, Path(tmp) / str(i))
            issues_ok = len(issues) == len(want_issues) and all(
                any(w in i for i in issues) for w in want_issues)
            ok = failed == want_failed and issues_ok
            problems += not ok
            print(f"{'ok  ' if ok else 'BAD '} {name}: fails {sorted(failed) or 'nothing'}, "
                  f"{len(issues)} issue(s)")
            if not ok:
                print(f"     expected fails {sorted(want_failed) or 'nothing'}, issues {want_issues}\n{out}")
    print(f"\n{len(CASES) - problems} of {len(CASES)} cases behaved as expected")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
