"""Check top-level USDA files in the current working directory, read-only.

OpenUSD API sources:
https://openusd.org/release/api/class_sdf_layer.html
https://openusd.org/release/api/class_sdf_spec.html
https://openusd.org/release/api/layer_utils_8h.html
https://openusd.org/release/api/class_ar_resolver.html
"""

import json
from pathlib import Path
import sys

from pxr import Ar, Sdf


def has_broken_reference(root):
    """Walk authored composition dependencies, including unselected variants.

    A visited set terminates cycles. Missing assets get the requested code;
    existing but unreadable layers raise an error instead of being mislabeled.
    """
    pending = [root]
    visited = set()
    broken = False
    while pending:
        layer = pending.pop()
        if layer.identifier in visited:
            continue
        visited.add(layer.identifier)
        for asset in sorted(layer.GetCompositionAssetDependencies()):
            if not asset:  # Internal references have no external file.
                continue
            anchored = Sdf.ComputeAssetPathRelativeToLayer(layer, asset)
            if not Ar.GetResolver().Resolve(anchored):
                broken = True
                print(
                    f"WARNING: {Path(root.identifier).name}: "
                    f"{layer.identifier} cannot resolve {asset}",
                    file=sys.stderr,
                )
                continue
            dependency = Sdf.Layer.FindOrOpenRelativeToLayer(layer, asset)
            if dependency is None:
                raise RuntimeError(f"Cannot load existing dependency: {anchored}")
            pending.append(dependency)
    return broken


def main():
    report = {}
    for path in sorted(Path.cwd().glob("*.usda")):
        if not path.is_file():
            continue
        layer = Sdf.Layer.FindOrOpen(str(path))
        if layer is None:
            raise RuntimeError(f"Cannot load input: {path}")
        problems = []
        # Check the file's own metadata, without composed or fallback values.
        for key, code in (
            ("upAxis", "missing_up_axis"),
            ("metersPerUnit", "missing_meters_per_unit"),
        ):
            if not layer.pseudoRoot.HasInfo(key):
                problems.append(code)
        if has_broken_reference(layer):
            problems.append("broken_reference")
        report[path.name] = problems
    output = json.dumps(report, indent=2) + "\n"
    Path("report.json").write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
