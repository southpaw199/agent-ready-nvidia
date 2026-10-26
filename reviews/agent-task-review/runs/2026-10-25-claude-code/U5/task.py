"""Check every top-level .usda file in a folder for missing stage metrics and
broken references, payloads, or sublayers, then write and print report.json.

Usage: python task.py [folder]   (defaults to the folder containing this script)
"""
import json
import sys
from pathlib import Path

from pxr import Sdf, Usd, UsdGeom, UsdUtils


def check_file(path):
    problems = []

    # Stage metadata lives in the root (or session) layer, so open the stage
    # without loading payloads; the dependency check below covers those.
    stage = Usd.Stage.Open(str(path), Usd.Stage.LoadNone)
    if not stage.HasAuthoredMetadata("upAxis"):
        problems.append("missing_up_axis")
    if not UsdGeom.StageHasAuthoredMetersPerUnit(stage):
        problems.append("missing_meters_per_unit")

    # Recursively walks sublayers, references and payloads, including those
    # in files that this file brings in, and collects paths that don't resolve.
    _layers, _assets, unresolved = UsdUtils.ComputeAllDependencies(
        Sdf.AssetPath(str(path)))
    if unresolved:
        problems.append("broken_reference")

    return problems


def main():
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent).resolve()
    report = {}
    for path in sorted(folder.glob("*.usda")):
        try:
            report[path.name] = check_file(path)
        except Exception as exc:
            print(f"Could not open {path.name}: {exc}", file=sys.stderr)

    (folder / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
