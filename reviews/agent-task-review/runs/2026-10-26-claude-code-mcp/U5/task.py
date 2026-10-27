"""Check every top-level .usda file in a folder for common stage problems.

Usage: python task.py [FOLDER]   (FOLDER defaults to the folder this script is in)

Writes FOLDER/report.json mapping each file name to a list of problem codes:
  missing_up_axis          - the file does not author the upAxis stage metadatum
  missing_meters_per_unit  - the file does not author the metersPerUnit stage metadatum
  broken_reference         - a reference, payload or sublayer (in this file or in any
                             layer it brings in) points at a file that can't be found
  unreadable_file          - the file itself could not be opened as a USD layer, so
                             the other checks could not run
"""

import json
import sys
from pathlib import Path

from pxr import Ar, Sdf, Tf, Usd, UsdGeom


def open_layer(identifier):
    """Open a layer, returning None if it can't be opened (FindOrOpen raises on bad files)."""
    try:
        return Sdf.Layer.FindOrOpen(identifier)
    except Tf.ErrorException:
        return None


def has_broken_reference(root_layer):
    """Walk sublayers, references and payloads recursively; return True if any is missing."""
    resolver = Ar.GetResolver()
    visited = set()
    pending = [root_layer]
    while pending:
        layer = pending.pop()
        if layer.identifier in visited:
            continue
        visited.add(layer.identifier)
        # Asset paths authored in sublayer, reference and payload fields of this layer
        # (direct dependencies only, so we recurse ourselves).
        for asset_path in layer.GetCompositionAssetDependencies():
            if not asset_path:
                continue
            # Anchor relative paths to the layer they were authored in.
            identifier = layer.ComputeAbsolutePath(asset_path)
            if not resolver.Resolve(identifier):
                return True
            # Found but not openable: we can't follow it, so treat it as broken too.
            dependency = open_layer(identifier)
            if dependency is None:
                return True
            pending.append(dependency)
    return False


def check_file(path):
    root_layer = open_layer(str(path))
    if root_layer is None:
        return ["unreadable_file"]

    problems = []
    # Stage metadata is read only from the root and session layers, so this asks
    # whether the file itself authors the value (not just the fallback).
    stage = Usd.Stage.Open(root_layer, Usd.Stage.LoadNone)
    if not stage.HasAuthoredMetadata("upAxis"):
        problems.append("missing_up_axis")
    if not UsdGeom.StageHasAuthoredMetersPerUnit(stage):
        problems.append("missing_meters_per_unit")
    if has_broken_reference(root_layer):
        problems.append("broken_reference")
    return problems


def main():
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent).resolve()
    report = {
        path.name: check_file(path)
        for path in sorted(folder.glob("*.usda"))
        if path.is_file()
    }
    (folder / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
