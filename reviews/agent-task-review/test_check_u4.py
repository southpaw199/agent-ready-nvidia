"""Test check_u4.py against the reference solution and known mistakes.

Usage: python test_check_u4.py   (in a virtual environment with usd-core)

Each case edits the reference task.py, runs it in an "agent" folder, then
reruns it in a clean "rerun" folder with a fresh asset file, as the reviewer
does, and checks the rerun folder. The test passes if every case fails
exactly the expected criteria and raises exactly the expected issues.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = (HERE / "reference" / "U4" / "task.py").read_text()

ADD_REF = 'crate.GetPrim().GetReferences().AddReference("./crate.usda")'
BUILD_INSTANCED = 'build(HERE / "instanced.usda", instanceable=True)'
# The same 1,000 crates in instanced.usda, with a PointInstancer instead of instanceable prims.
POINT_INSTANCED = '''def build_points(path):
    stage = Usd.Stage.CreateNew(str(path))
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())
    instancer = UsdGeom.PointInstancer.Define(stage, "/World/Crates")
    proto = stage.DefinePrim("/World/Crates/Prototypes/Crate")
    proto.GetReferences().AddReference("./crate.usda")
    instancer.CreatePrototypesRel().SetTargets([proto.GetPath()])
    instancer.CreatePositionsAttr(
        [Gf.Vec3f(SPACING * (i % COLUMNS), SPACING * (i // COLUMNS), 0) for i in range(COUNT)])
    instancer.CreateProtoIndicesAttr([0] * COUNT)
    stage.Save()


build_points(HERE / "instanced.usda")'''


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
    "absolute path built at run time": (edit('"./crate.usda"', 'str(HERE / "crate.usda")'), set(), []),
    "hardcoded absolute path": (edit('"./crate.usda"', '"{agent}/crate.usda"'), {"C4", "C5"},
                                ["hardcoded absolute path"]),
    "point instancing instead of scenegraph instancing": (edit(BUILD_INSTANCED, POINT_INSTANCED), set(), []),
    "instanced.usda never marked instanceable": (
        edit("crate.GetPrim().SetInstanceable(instanceable)", "pass"), {"C5"}, []),
    "references.usda marked instanceable too": (
        edit('build(HERE / "references.usda", instanceable=False)',
             'build(HERE / "references.usda", instanceable=True)'), {"C4"}, []),
    "grid with 25 columns instead of 40": (
        edit("COUNT, COLUMNS, SPACING = 1000, 40, 2.0", "COUNT, COLUMNS, SPACING = 1000, 25, 2.0"),
        {"C4", "C5", "C6"}, []),
    "copies instead of references in references.usda": (
        edit(ADD_REF, 'if instanceable:\n            ' + ADD_REF + '\n        else:\n'
             '            UsdGeom.Cube.Define(stage, crate.GetPath().AppendChild("Body"))'),
        {"C4", "C6"}, []),
    "counts typed by hand": (
        edits(edit("prims = sum(1 for _ in stage.Traverse())",
                   'prims = 2001 if name == "references.usda" else 1001'),
              edit("{len(stage.GetPrototypes())} prototype(s)",
                   "{0 if name == 'references.usda' else 1} prototype(s)")),
        set(), ["typed by hand"]),
    "asset file edited": (
        edit('build(HERE / "references.usda", instanceable=False)\n',
             'build(HERE / "references.usda", instanceable=False)\n(HERE / "crate.usda").write_text('
             '(HERE / "crate.usda").read_text().replace("0.55", "0.6"))\n'),
        {"C2"}, []),
}


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def run_case(name, change, root):
    agent, rerun = root / "agent", root / "rerun"
    for folder in (agent, rerun):
        folder.mkdir(parents=True)
        run([sys.executable, str(HERE / "make_u4_assets.py"), "."], folder)
    script = change(REFERENCE, agent)
    for folder in (agent, rerun):
        (folder / "task.py").write_text(script)
        task = run([sys.executable, "task.py"], folder)
    out = run([sys.executable, str(HERE / "check_u4.py"), "."], rerun).stdout
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
