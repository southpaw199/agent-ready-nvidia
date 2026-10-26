"""Check an agent's U5 output against the success criteria.

Usage:  python check_u5.py <folder>

The folder must hold the report.json the agent's script wrote, plus the files
make_u5_assets.py created: the main set, or the holdout set made with
--holdout. The checker tells which set it's looking at from the files present.
On the main set it scores C1 to C5; on the holdout set, the same checks count
as C6, which shows the script works on files it hasn't seen. It reads
report.json and the agent's task.py; it doesn't run the script or need usd-core.

NOTE lines say how task.py finds the problems: OpenUSD's built-in UsdValidation
validators, usdchecker, or checks written by hand. ISSUE lines flag things in
task.py for the reviewer to read and confirm: a hardcoded absolute path or
folder, or main-set file names written into the script. They don't fail a check.
"""
import ast
import json
import sys
from pathlib import Path

from make_u5_assets import SETS

CODES = {"missing_up_axis", "missing_meters_per_unit", "broken_reference"}
METADATA = {"missing_up_axis", "missing_meters_per_unit"}
# Names that show which route task.py takes.
BUILT_IN = {"UsdValidation", "ValidationRegistry", "ValidationContext", "GetOrLoadValidatorByName",
            "GetValidatorsByKeywords", "GetAllValidatorMetadata"}
BY_HAND = {"HasAuthoredMetadata", "GetCompositionErrors", "ComputeAllDependencies", "GetCompositionArcs",
           "GetExternalReferences", "GetCompositionAssetDependencies", "PrimCompositionQuery",
           "StageHasAuthoredMetersPerUnit",
           # Checks written at the layer level, without composing a stage.
           "HasInfo", "pseudoRoot", "GetPseudoRoot", "subLayerPaths", "GetSubLayerPaths",
           "FindOrOpenRelativeToLayer", "ComputeAssetPathRelativeToLayer", "GetResolver", "Resolve"}


def which_set(d):
    for name, (files, expected) in SETS.items():
        if all((d / f).exists() for f in expected):
            return name, files, expected
    return None, {}, {}


def source_notes(script, main_names):
    if not script.exists():
        return [], [f"{script.name} not found; source checks skipped"]
    tree = ast.parse(script.read_text())
    strings = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    names |= {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    names |= {a.name.split(".")[-1] for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
              for a in n.names}
    routes = [label for label, found in (
        ("built-in UsdValidation validators", names & BUILT_IN),
        ("usdchecker", any("usdchecker" in s for s in strings)),
        ("checks written by hand", names & BY_HAND)) if found]
    notes = [f"how task.py finds the problems: {', '.join(routes) or 'unclear; read task.py'}"]
    issues = []
    # A folder path counts too, since the script works on a whole folder. Prim paths
    # such as /World/Chair don't match.
    hardcoded = [s for s in strings if s.startswith(("/", "~")) and (
        ".usd" in s or s.startswith("~") or any(root in s for root in ("/home/", "/Users/", "/tmp/", "/mnt/")))]
    if hardcoded:
        issues.append(f"hardcoded absolute path(s) in task.py: {hardcoded}. They break when the "
                      "code moves; build paths at run time, for example from __file__")
    listed = sorted({s for s in strings if s in main_names})
    if listed:
        issues.append(f"task.py names main-set files {listed}, so it may only handle the files it was "
                      "shown; the holdout rerun (C6) tests this")
    return issues, notes


def main(folder):
    d = Path(folder)
    results = []  # (criterion id, passed, detail)
    which, files, expected = which_set(d)
    if which is None:
        sys.exit(f"{d} doesn't hold the main or holdout set from make_u5_assets.py")
    tag = "holdout: " if which == "holdout" else ""

    def check(cid, ok, detail):
        results.append(("C6" if which == "holdout" else cid, bool(ok), tag + detail))

    report_path = d / "report.json"
    try:
        report = json.loads(report_path.read_text())
        shape_ok = isinstance(report, dict) and all(
            isinstance(v, list) and all(isinstance(c, str) for c in v) for v in report.values())
    except (OSError, ValueError) as error:
        report, shape_ok = {}, False
        check("C1", False, f"report.json can't be read as JSON: {error}")
    else:
        check("C1", shape_ok, "report.json is a JSON object mapping each file to a list of codes")
    report = {Path(k).name: v for k, v in report.items()} if shape_ok else {}

    for name, text in files.items():
        p = d / name
        check("C2", p.exists() and p.read_text() == text, f"{name} unchanged from make_u5_assets.py")

    check("C3", set(report) == set(expected),
          f"report covers exactly the top-level files: missing {sorted(set(expected) - set(report)) or 'none'}, "
          f"extra {sorted(set(report) - set(expected)) or 'none'}")
    unknown = sorted({c for v in report.values() for c in v} - CODES)
    meta_wrong = {f: sorted(set(report.get(f, [])) & METADATA) for f in expected
                  if set(report.get(f, [])) & METADATA != set(expected[f]) & METADATA}
    check("C4", not meta_wrong and bool(report),
          f"up-axis and units codes right for every file; wrong: {meta_wrong or 'none'}")
    ref_wrong = {f: "broken_reference" in report.get(f, []) for f in expected
                 if ("broken_reference" in report.get(f, [])) != ("broken_reference" in expected[f])}
    check("C5", not ref_wrong and not unknown,
          f"broken_reference right for every file, including nested ones and payloads"
          f"{' and sublayers' if which == 'holdout' else ''}; wrong: {ref_wrong or 'none'}; "
          f"unknown codes: {unknown or 'none'}")

    main_names = set(SETS["main"][1]) | {Path(f).name for f in SETS["main"][0]}
    issues, notes = source_notes(d / "task.py", main_names)
    notes.insert(0, f"file set: {which}")
    return report_out(results, notes, issues)


def report_out(results, notes, issues=()):
    for cid, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {cid}  {detail}")
    for n in notes:
        print(f"NOTE  {n}")
    for i in issues:
        print(f"ISSUE {i}")
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)} of {len(results)} checks passed; {len(issues)} issue(s) to review")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
