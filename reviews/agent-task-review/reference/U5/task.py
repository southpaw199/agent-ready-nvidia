"""U5 reference solution: flag problems in .usda files with OpenUSD's built-in validators.

Checks every .usda file at the top level of this folder for missing upAxis,
missing metersPerUnit, and files it refers to that can't be found, and
writes report.json mapping each file's name to its problem codes. Uses the
UsdValidation framework in usd-core rather than checks written by hand:
usdGeomValidators:StageMetadataChecker for the metadata, and
usdUtilsValidators:MissingReferenceValidator, which follows references,
payloads, and sublayers into every file the stage depends on.
"""
import json
from pathlib import Path

from pxr import Usd, UsdValidation

HERE = Path(__file__).resolve().parent
VALIDATORS = ("usdGeomValidators:StageMetadataChecker", "usdUtilsValidators:MissingReferenceValidator")
CODES = {
    "MissingUpAxisMetadata": "missing_up_axis",
    "MissingMetersPerUnitMetadata": "missing_meters_per_unit",
    "UnresolvableDependency": "broken_reference",
}

registry = UsdValidation.ValidationRegistry()
context = UsdValidation.ValidationContext([registry.GetOrLoadValidatorByName(n) for n in VALIDATORS])

report = {}
for path in sorted(HERE.glob("*.usda")):
    stage = Usd.Stage.Open(str(path))
    errors = context.Validate(stage)
    report[path.name] = sorted({CODES[e.GetName()] for e in errors if e.GetName() in CODES})

(HERE / "report.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
