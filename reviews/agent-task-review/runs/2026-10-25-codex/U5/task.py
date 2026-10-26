"""Check top-level USDA files in the current working directory, read-only.

Composition arcs are inspected in authored layers, including variant specs,
rather than only in the currently composed/loaded scene. Missing textures and
other asset-valued attributes are outside this check's scope.
"""

import json
from pathlib import Path

from pxr import Ar, Sdf


def composition_paths(layer):
    """Collect sublayers and effective reference/payload list-op additions."""
    paths = list(layer.subLayerPaths)

    def visit(path):
        spec = layer.GetObjectAtPath(path)
        for key in ("references", "payload"):
            if spec.HasInfo(key):
                for arc in spec.GetInfo(key).GetAppliedItems():
                    # An empty asset path is an internal arc, not a missing file.
                    if arc.assetPath:
                        paths.append(arc.assetPath)

    layer.Traverse(Sdf.Path.absoluteRootPath, visit)
    return paths


def has_broken_reference(root):
    pending = [root]
    visited = set()
    broken = False
    while pending:
        layer = pending.pop()
        if layer.identifier in visited:
            continue
        visited.add(layer.identifier)
        for asset_path in composition_paths(layer):
            anchored = Sdf.ComputeAssetPathRelativeToLayer(layer, asset_path)
            if not Ar.GetResolver().Resolve(anchored):
                broken = True
                continue
            child = Sdf.Layer.FindOrOpenRelativeToLayer(layer, asset_path)
            if child is None:
                # An existing but unreadable layer is not a missing file.
                raise RuntimeError(f"Cannot read {asset_path!r} from {layer.identifier!r}")
            pending.append(child)
    return broken


def main():
    report = {}
    for path in sorted(Path.cwd().glob("*.usda")):
        if not path.is_file():
            continue
        layer = Sdf.Layer.FindOrOpen(str(path))
        if layer is None:
            raise RuntimeError(f"Cannot read {path}")
        problems = []
        # Layer metadata lives on the pseudo-root. HasInfo ignores fallbacks
        # and checks this file itself, not metadata in referenced assets.
        if not layer.pseudoRoot.HasInfo("upAxis"):
            problems.append("missing_up_axis")
        if not layer.pseudoRoot.HasInfo("metersPerUnit"):
            problems.append("missing_meters_per_unit")
        if has_broken_reference(layer):
            problems.append("broken_reference")
        report[path.name] = problems
    output = json.dumps(report, indent=2) + "\n"
    Path("report.json").write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
