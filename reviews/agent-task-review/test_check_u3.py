"""Test check_u3.py against the reference solution and known mistakes.

Usage: python test_check_u3.py   (in a virtual environment with usd-core)

Each case edits the reference task.py, runs it in an "agent" folder, then
reruns it in a clean "rerun" folder with a fresh asset file, saving its output
to rerun-output.txt as the reviewer does, and checks the rerun folder. The
test passes if every case fails exactly the expected criteria and raises
exactly the expected issues.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = (HERE / "reference" / "U3" / "task.py").read_text()

SESSION = "with Usd.EditContext(reopened, reopened.GetSessionLayer()):"
SWITCH = """with Usd.EditContext(reopened, reopened.GetSessionLayer()):
    reopened.GetPrimAtPath("/World/Mug").GetVariantSets().GetVariantSet("color").SetVariantSelection("red")
show(reopened, "After switching")"""
DIRECT_BLUE = "UsdGeom.Gprim(mug).GetDisplayColorAttr().Set(Vt.Vec3fArray([Gf.Vec3f(0.0, 0.0, 1.0)]))\n"


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
    "absolute path built at run time": (edit('"./mug.usda"', 'str(HERE / "mug.usda")'), set(), []),
    "hardcoded absolute path": (edit('"./mug.usda"', '"{agent}/mug.usda"'), {"C4"}, ["hardcoded absolute path"]),
    "switched on the stage without the session layer, not saved": (edit(SESSION, "if True:"), set(), []),
    "switched to red, then saved": (
        edits(edit(SESSION, "if True:"),
              edit('show(reopened, "After switching")', 'show(reopened, "After switching")\nreopened.Save()')),
        {"C5", "C6"}, []),
    "never switched in code": (edit(SWITCH, ""), set(), ["shows no red"]),
    "color also set outside the variants": (
        edit("# 3. Select blue and save.", DIRECT_BLUE + "# 3. Select blue and save."),
        {"C6"}, ["shows no red"]),
    "variants named Red and Blue": (
        edit('{"red": (1.0, 0.0, 0.0), "blue": (0.0, 0.0, 1.0)}', '{"Red": (1.0, 0.0, 0.0), "Blue": (0.0, 0.0, 1.0)}'),
        {"C5", "C6"}, ["shows no red or blue"]),
    "asset file edited": (
        edit("stage.Save()\n", 'stage.Save()\n(HERE / "mug.usda").write_text('
             '(HERE / "mug.usda").read_text().replace("(0, 1, 0)", "(0, 1, 1)"))\n'),
        {"C2"}, []),
}


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def run_case(name, change, root):
    agent, rerun = root / "agent", root / "rerun"
    for folder in (agent, rerun):
        folder.mkdir(parents=True)
        run([sys.executable, str(HERE / "make_u3_assets.py"), "."], folder)
    script = change(REFERENCE, agent)
    for folder in (agent, rerun):
        (folder / "task.py").write_text(script)
        task = run([sys.executable, "task.py"], folder)
    (rerun / "rerun-output.txt").write_text(task.stdout + task.stderr)
    out = run([sys.executable, str(HERE / "check_u3.py"), "."], rerun).stdout
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
