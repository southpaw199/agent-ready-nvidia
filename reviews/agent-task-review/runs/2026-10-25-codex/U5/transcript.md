# Codex conversation

## User

I'm learning OpenUSD, an open-source framework for describing 3D scenes. Use only these two documentation sites to do this task: the OpenUSD documentation at openusd.org, and NVIDIA's Learn OpenUSD course at docs.nvidia.com/learn-openusd. Don't rely on what you remember about OpenUSD, and don't use other websites. If you use something you already knew rather than something you read in these docs, say so. Each time you rely on a docs page, tell me its URL.

Work only in the current folder. Create a Python virtual environment here and install the usd-core package from PyPI into it. When you're done, run your final script and show me its complete output, including any warnings. Then list the docs page, with its URL, behind each step.

This folder has several USD files at the top level, and a parts folder that some of them use. Don't change any of them. Write a Python script named task.py that checks every .usda file at the top level of this folder (not the parts folder) for these problems:

- missing_up_axis: the file doesn't specify the stage's up axis (upAxis).
- missing_meters_per_unit: the file doesn't specify the stage's units (metersPerUnit).
- broken_reference: the file refers to another file that can't be found, through a reference, a payload, or a sublayer, either directly or through a file it brings in.

The script should write report.json in this folder, mapping each file's name to a list of the codes for the problems found in it, with an empty list for a file that has none, and print the report. It should work on any folder of .usda files, not only these.

Then tell me how the script detects each problem.

## Assistant

I’ll read the two documentation sites, inspect the folder without changing the USD files, and build and run the checker in a local virtual environment. I’ll cite the pages used for each step.

## Activity

    $ pwd && rg --files -g 'AGENTS.md' -g '*.usda' -g '*.usd' -g '*.usdc' -g 'task.py' -g 'report.json' -g 'pyproject.toml' -g 'requirements*'
    /home/southpaw199/agent-runs/nvidia/2026-10-25-codex/U5
    parts/shelf.usda
    parts/lamp.usda
    good.usda
    two_problems.usda
    nested_broken_reference.usda
    no_units.usda
    no_up_axis.usda
    broken_reference.usda
    y_up_centimeters.usda
    ✓ • 0ms

## Activity

    $ ls -la && for f in *.usda parts/*.usda; do printf '\n%s\n' "$f"; cat "$f"; done
    total 40
    drwxr-xr-x  7 southpaw199 southpaw199 4096 Oct 25 22:01 .
    drwxr-xr-x 12 southpaw199 southpaw199 4096 Oct 25 21:18 ..
    dr-xr-xr-x  2 southpaw199 southpaw199   40 Oct 25 22:01 .agents
    dr-xr-xr-x  2 southpaw199 southpaw199   40 Oct 25 22:01 .aws
    dr-xr-xr-x  2 southpaw199 southpaw199   40 Oct 25 22:01 .codex
    dr-xr-xr-x  2 southpaw199 southpaw199   40 Oct 25 22:01 .git
    -rw-r--r--  1 southpaw199 southpaw199  196 Oct 25 22:00 broken_reference.usda
    -rw-r--r--  1 southpaw199 southpaw199  186 Oct 25 22:00 good.usda
    -rw-r--r--  1 southpaw199 southpaw199  188 Oct 25 22:00 nested_broken_reference.usda
    -rw-r--r--  1 southpaw199 southpaw199   80 Oct 25 22:00 no_units.usda
    -rw-r--r--  1 southpaw199 southpaw199   85 Oct 25 22:00 no_up_axis.usda
    drwxr-xr-x  2 southpaw199 southpaw199 4096 Oct 25 22:00 parts
    -rw-r--r--  1 southpaw199 southpaw199  150 Oct 25 22:00 two_problems.usda
    -rw-r--r--  1 southpaw199 southpaw199  105 Oct 25 22:00 y_up_centimeters.usda
    
    broken_reference.usda
    #usda 1.0
    (
        defaultPrim = "World"
        metersPerUnit = 1
        upAxis = "Z"
    )
    
    def Xform "World"
    {
        def "Chair" (
            prepend references = @./parts/missing_chair.usda@
        )
        {
        }
    }
    
    good.usda
    #usda 1.0
    (
        defaultPrim = "World"
        metersPerUnit = 1
        upAxis = "Z"
    )
    
    def Xform "World"
    {
        def "Lamp" (
            prepend references = @./parts/lamp.usda@
        )
        {
        }
    }
    
    nested_broken_reference.usda
    #usda 1.0
    (
        defaultPrim = "World"
        metersPerUnit = 1
        upAxis = "Z"
    )
    
    def Xform "World"
    {
        def "Shelf" (
            prepend references = @./parts/shelf.usda@
        )
        {
        }
    }
    
    no_units.usda
    #usda 1.0
    (
        defaultPrim = "World"
        upAxis = "Z"
    )
    
    def Xform "World"
    {
    }
    
    no_up_axis.usda
    #usda 1.0
    (
        defaultPrim = "World"
        metersPerUnit = 1
    )
    
    def Xform "World"
    {
    }
    
    two_problems.usda
    #usda 1.0
    (
        defaultPrim = "World"
    )
    
    def Xform "World"
    {
        def "Rug" (
            prepend payload = @./parts/missing_rug.usda@
        )
        {
        }
    }
    
    y_up_centimeters.usda
    #usda 1.0
    (
        defaultPrim = "World"
        metersPerUnit = 0.01
        upAxis = "Y"
    )
    
    def Xform "World"
    {
    }
    
    parts/lamp.usda
    #usda 1.0
    (
        defaultPrim = "Lamp"
        metersPerUnit = 1
        upAxis = "Z"
    )
    
    def Xform "Lamp"
    {
    }
    
    parts/shelf.usda
    #usda 1.0
    (
        defaultPrim = "Shelf"
        metersPerUnit = 1
        upAxis = "Z"
    )
    
    def Xform "Shelf" (
        prepend references = @./missing_books.usda@
    )
    {
    }
    ✓ • 0ms

## Activity

    $ curl -L --fail https://openusd.org/release/api/class_usd_utils_dependencies.html
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    
    ✗ (6) • 0ms

## Activity

    $ curl -L --fail https://openusd.org/release/api/dependencies_8h.html
    [Page content omitted from this record: https://openusd.org/release/api/dependencies_8h.html]
    ✓ • 381ms

## Activity

    $ python3 -m venv .venv && .venv/bin/python -m pip install usd-core
    WARNING: The directory '/home/southpaw199/.cache/pip' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you should use sudo's -H flag.
    WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x706bb6b85010>: Failed to establish a new connection: [Errno -2] Name or service not known')': /simple/usd-core/
    WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x706bb6b85790>: Failed to establish a new connection: [Errno -2] Name or service not known')': /simple/usd-core/
    WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x706bb6b85730>: Failed to establish a new connection: [Errno -2] Name or service not known')': /simple/usd-core/
    WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x706bb6b85b80>: Failed to establish a new connection: [Errno -2] Name or service not known')': /simple/usd-core/
    WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x706bb6b85a90>: Failed to establish a new connection: [Errno -2] Name or service not known')': /simple/usd-core/
    ERROR: Could not find a version that satisfies the requirement usd-core (from versions: none)
    ERROR: No matching distribution found for usd-core
    ✗ (1) • 10.89s

## Activity

    $ mkdir -p .docs && curl -L --fail -sS https://openusd.org/release/api/class_sdf_layer.html -o .docs/layer.html && curl -L --fail -sS https://openusd.org/release/api/class_sdf_prim_spec.html -o .docs/prim.html && curl -L --fail -sS https://openusd.org/release/api/class_sdf_list_op.html -o .docs/listop.html && curl -L --fail -sS https://openusd.org/release/api/group___usd_geom_up_axis__group.html -o .docs/axis.html && curl -L --fail -sS https://openusd.org/release/api/group___usd_geom_linear_units__group.html -o .docs/units.html && curl -L --fail -sS https://openusd.org/release/api/class_usd_stage.html -o .docs/stage.html
    ✓ • 2.37s

## Activity

    $ python3 - <<'PY'
        from html.parser import HTMLParser
        from pathlib import Path
        class Text(HTMLParser):
         def handle_data(self,d):
          if d.strip(): self.out.append(d.strip())
        for p in Path('.docs').glob('*.html'):
         t=Text(); t.out=[]; t.feed(p.read_text()); p.with_suffix('.txt').write_text('\n'.join(t.out))
        PY
        rg -n -A 12 -B 3 'FindOrOpenRelativeToLayer|ComputeAssetPathRelativeToLayer|Traverse\(|HasInfo|GetInfo|GetAddedOrExplicitItems|GetAppliedItems|HasAuthoredMetadata|fallback|HasAuthored' .docs/*.txt
    [Page content omitted from this record: https://openusd.org/release/api/group___usd_geom_up_axis__group.html]
    [Page content omitted from this record: https://openusd.org/release/api/group__sdf___file_format_plugin.html]
    [Page content omitted from this record: https://openusd.org/release/api/class_sdf_layer.html]
    [Page content omitted from this record: https://openusd.org/release/api/layer_utils_8h.html]
    [Page content omitted from this record: https://openusd.org/release/api/class_sdf_list_op.html]
    [Page content omitted from this record: https://docs.nvidia.com/learn-openusd/latest/stage-setting/index.html]
    [Page content omitted from this record: https://docs.nvidia.com/learn-openusd/latest/stage-setting/units.html]
    [Page content omitted from this record: https://openusd.org/release/api/class_sdf_prim_spec.html]
    [Page content omitted from this record: https://openusd.org/release/api/class_ar_resolver.html]
    [Page content omitted from this record: https://openusd.org/release/api/class_usd_stage.html]
    [Page content omitted from this record: https://openusd.org/release/api/group___usd_geom_linear_units__group.html]
    ✓ • 83ms

## Activity

    $ .venv/bin/python -m pip install --no-cache-dir --index-url https://pypi.org/simple usd-core
    Collecting usd-core
      Downloading usd_core-26.11-cp312-none-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (1.8 kB)
    Downloading usd_core-26.11-cp312-none-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (28.8 MB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 28.8/28.8 MB 11.6 MB/s eta 0:00:00
    Installing collected packages: usd-core
    Successfully installed usd-core-26.11
    ✓ • 4.10s

## Assistant

The docs distinguish authored metadata from fallback values, so reading the axis or units value alone would miss omissions. I’ll check what each file explicitly authors and follow references, payloads, and sublayers recursively, resolving paths relative to the file that contains them.

Sources: https://openusd.org/release/api/group___usd_geom_up_axis__group.html, https://openusd.org/release/api/group___usd_geom_linear_units__group.html, https://openusd.org/release/api/class_sdf_prim_spec.html, and https://openusd.org/release/api/class_sdf_layer.html.

## Activity

    $ curl -L --fail -sS https://openusd.org/release/api/group__sdf___file_format_plugin.html -o .docs/fileformat.html && curl -L --fail -sS https://openusd.org/release/api/class_ar_resolver.html -o .docs/resolver.html && curl -L --fail -sS https://docs.nvidia.com/learn-openusd/latest/stage-setting/units.html -o .docs/nvidia-units.html
    curl: (22) The requested URL returned error: 404
    ✗ (22) • 382ms

## Activity

    $ rg -n -A 14 -B 4 'Traverse|GetSubLayerPaths|GetObjectAtPath' .docs/layer.txt && sed -n '2040,2090p' .docs/layer.txt
    [Page content omitted from this record: https://openusd.org/release/api/class_sdf_layer.html]
    ✓ • 0ms

## Activity

    $ curl -L --fail -sS https://openusd.org/release/api/layer_utils_8h.html -o .docs/layer-utils.html && curl -L --fail -sS https://openusd.org/release/api/class_ar_resolver.html -o .docs/resolver.html && curl -L --fail -sS https://docs.nvidia.com/learn-openusd/latest/stage-setting/index.html -o .docs/nvidia-stage.html
    ✓ • 1.02s

## Activity

    $ .venv/bin/python - <<'PY'
        from pxr import Sdf
        l=Sdf.Layer.FindOrOpen('good.usda')
        print(l.pseudoRoot.HasInfo('upAxis'))
        def visit(p):
         s=l.GetObjectAtPath(p)
         if s.HasInfo('references'): print(p, s.GetInfo('references').GetAppliedItems())
        l.Traverse('/', visit)
        print(Sdf.ComputeAssetPathRelativeToLayer(l, './parts/missing.usda'))
        PY
    True
    /World/Lamp [Sdf.Reference('./parts/lamp.usda')]
    /home/southpaw199/agent-runs/nvidia/2026-10-25-codex/U5/parts/missing.usda
    ✓ • 51ms

## Activity

    $ python3 - <<'PY'
        from html.parser import HTMLParser
        from pathlib import Path
        class Text(HTMLParser):
         def handle_data(self,d):
          if d.strip(): self.out.append(d.strip())
        for n in ('layer-utils','resolver','nvidia-stage'):
         p=Path('.docs')/(n+'.html'); t=Text(); t.out=[]; t.feed(p.read_text()); p.with_suffix('.txt').write_text('\n'.join(t.out))
        PY
        rg -n -A 22 -B 2 'SdfComputeAssetPathRelativeToLayer|Resolve\(\)|Resolve an asset|units|upAxis|metersPerUnit' .docs/layer-utils.txt .docs/resolver.txt .docs/nvidia-stage.txt
    [Page content omitted from this record: https://openusd.org/release/api/layer_utils_8h.html]
    [Page content omitted from this record: https://docs.nvidia.com/learn-openusd/latest/stage-setting/index.html]
    [Page content omitted from this record: https://openusd.org/release/api/class_ar_resolver.html]
    ✓ • 0ms

## Activity

    file changes: Completed · 1 changes
    Add: /home/southpaw199/agent-runs/nvidia/2026-10-25-codex/U5/task.py
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

## Activity

    $ .venv/bin/python task.py
    {
      "broken_reference.usda": [
        "broken_reference"
      ],
      "good.usda": [],
      "nested_broken_reference.usda": [
        "broken_reference"
      ],
      "no_units.usda": [
        "missing_meters_per_unit"
      ],
      "no_up_axis.usda": [
        "missing_up_axis"
      ],
      "two_problems.usda": [
        "missing_up_axis",
        "missing_meters_per_unit",
        "broken_reference"
      ],
      "y_up_centimeters.usda": []
    }
    ✓ • 65ms

## Assistant

The checker found the direct missing reference, the nested missing reference, and the missing payload. `two_problems.usda` actually has all three requested problems. The final run produced no warnings.

I’m also checking temporary fixtures for nested sublayers, cycles, and missing texture paths. The dependency utility includes non-layer assets, so using it without filtering could incorrectly flag textures as broken references. Source: https://openusd.org/release/api/dependencies_8h.html.

## Activity

    $ .venv/bin/python - <<'PY'
        import json
        from pathlib import Path
        import subprocess
        import tempfile
        script = Path('task.py').resolve()
        with tempfile.TemporaryDirectory(prefix='.checker-test-', dir=Path.cwd()) as folder:
         p = Path(folder)
         header = '#usda 1.0\n(\n upAxis = "Y"\n metersPerUnit = 0.01\n'
         (p/'parts').mkdir()
         (p/'nested.usda').write_text(header+' subLayers = [@parts/child.usda@]\n)\n')
         (p/'parts/child.usda').write_text('#usda 1.0\n( subLayers = [@missing.usda@] )\n')
         (p/'cycle.usda').write_text(header+' subLayers = [@parts/back.usda@]\n)\n')
         (p/'parts/back.usda').write_text('#usda 1.0\n( subLayers = [@../cycle.usda@] )\n')
         (p/'texture.usda').write_text(header+')\ndef "Thing" {\n asset texture = @missing.png@\n}\n')
         (p/'internal.usda').write_text(header+')\ndef "Source" {}\ndef "Copy" (prepend references = </Source>) {}\n')
         result = subprocess.run([str(Path('.venv/bin/python').resolve()), str(script)], cwd=p, text=True, capture_output=True, check=True, timeout=20)
         report = json.loads(result.stdout)
         assert report == {'cycle.usda': [], 'internal.usda': [], 'nested.usda': ['broken_reference'], 'texture.usda': []}, report
         assert not result.stderr, result.stderr
         print('Passed: nested sublayers, cyclic dependencies, internal references, and exclusion of missing textures; parts files excluded from report.')
        PY
        .venv/bin/python task.py
    Traceback (most recent call last):
      File "<stdin>", line 16, in <module>
      File "/usr/lib/python3.12/subprocess.py", line 571, in run
        raise CalledProcessError(retcode, process.args,
    subprocess.CalledProcessError: Command '['/usr/bin/python3.12', '/home/southpaw199/agent-runs/nvidia/2026-10-25-codex/U5/task.py']' returned non-zero exit status 1.
    {
      "broken_reference.usda": [
        "broken_reference"
      ],
      "good.usda": [],
      "nested_broken_reference.usda": [
        "broken_reference"
      ],
      "no_units.usda": [
        "missing_meters_per_unit"
      ],
      "no_up_axis.usda": [
        "missing_up_axis"
      ],
      "two_problems.usda": [
        "missing_up_axis",
        "missing_meters_per_unit",
        "broken_reference"
      ],
      "y_up_centimeters.usda": []
    }
    ✓ • 245ms

## Activity

    $ .venv/bin/python - <<'PY'
        import json
        from pathlib import Path
        import subprocess
        import tempfile
        script = Path('task.py').absolute()
        python = Path('.venv/bin/python').absolute()
        with tempfile.TemporaryDirectory(prefix='.checker-test-', dir=Path.cwd()) as folder:
         p = Path(folder)
         header = '#usda 1.0\n(\n upAxis = "Y"\n metersPerUnit = 0.01\n'
         (p/'parts').mkdir()
         (p/'nested.usda').write_text(header+' subLayers = [@parts/child.usda@]\n)\n')
         (p/'parts/child.usda').write_text('#usda 1.0\n( subLayers = [@missing.usda@] )\n')
         (p/'cycle.usda').write_text(header+' subLayers = [@parts/back.usda@]\n)\n')
         (p/'parts/back.usda').write_text('#usda 1.0\n( subLayers = [@../cycle.usda@] )\n')
         (p/'texture.usda').write_text(header+')\ndef "Thing" {\n asset texture = @missing.png@\n}\n')
         (p/'internal.usda').write_text(header+')\ndef "Source" {}\ndef "Copy" (prepend references = </Source>) {}\n')
         result = subprocess.run([str(python), str(script)], cwd=p, text=True, capture_output=True, timeout=20)
         assert result.returncode == 0, result.stderr
         assert json.loads(result.stdout) == {'cycle.usda': [], 'internal.usda': [], 'nested.usda': ['broken_reference'], 'texture.usda': []}, result.stdout
         assert not result.stderr, result.stderr
         print('Passed: nested sublayers, cycles, internal references, missing texture exclusion, and top-level-only reporting.')
        PY
        .venv/bin/python task.py
    Passed: nested sublayers, cycles, internal references, missing texture exclusion, and top-level-only reporting.
    {
      "broken_reference.usda": [
        "broken_reference"
      ],
      "good.usda": [],
      "nested_broken_reference.usda": [
        "broken_reference"
      ],
      "no_units.usda": [
        "missing_meters_per_unit"
      ],
      "no_up_axis.usda": [
        "missing_up_axis"
      ],
      "two_problems.usda": [
        "missing_up_axis",
        "missing_meters_per_unit",
        "broken_reference"
      ],
      "y_up_centimeters.usda": []
    }
    ✓ • 244ms

## Assistant

Created [task.py](/home/southpaw199/agent-runs/nvidia/2026-10-25-codex/U5/task.py), [report.json](/home/southpaw199/agent-runs/nvidia/2026-10-25-codex/U5/report.json), and `.venv` with `usd-core 26.11`. The original USD files are unchanged.

Ran `.venv/bin/python task.py`. Complete output below; there were no warnings:

```json
{
  "broken_reference.usda": [
    "broken_reference"
  ],
  "good.usda": [],
  "nested_broken_reference.usda": [
    "broken_reference"
  ],
  "no_units.usda": [
    "missing_meters_per_unit"
  ],
  "no_up_axis.usda": [
    "missing_up_axis"
  ],
  "two_problems.usda": [
    "missing_up_axis",
    "missing_meters_per_unit",
    "broken_reference"
  ],
  "y_up_centimeters.usda": []
}
```

How it works, with documentation behind each step:

1. **Select files:** Python scans only `*.usda` files directly in the current working directory. Virtual environment setup, pip installation, file selection, and JSON output use my existing general Python knowledge—not OpenUSD documentation.

2. **Detect missing metadata:** The script calls `layer.pseudoRoot.HasInfo()` for `upAxis` and `metersPerUnit`. This checks whether the file explicitly specifies each key, so fallback values cannot hide omissions.
   - Layer metadata belongs to the pseudo-root: https://openusd.org/release/api/class_sdf_layer.html
   - `HasInfo()` checks whether a setting exists: https://openusd.org/release/api/class_sdf_prim_spec.html
   - Up-axis metadata and fallback behavior: https://openusd.org/release/api/group___usd_geom_up_axis__group.html
   - Units metadata and fallback behavior: https://openusd.org/release/api/group___usd_geom_linear_units__group.html

3. **Collect dependencies:** It reads sublayers and traverses authored specs for reference and payload list operations. `GetAppliedItems()` supplies the effective additions; unrelated texture paths are excluded.
   - Sublayers and layer traversal: https://openusd.org/release/api/class_sdf_layer.html
   - Metadata access: https://openusd.org/release/api/class_sdf_prim_spec.html
   - Effective list-operation items: https://openusd.org/release/api/class_sdf_list_op.html

4. **Detect broken references recursively:** It anchors each dependency path to its containing layer, asks the resolver whether it exists, and inspects found layers recursively. A visited set prevents cycles. An unresolved dependency adds `broken_reference`.
   - Relative path anchoring: https://openusd.org/release/api/layer_utils_8h.html
   - Resolution returns an empty path for missing assets: https://openusd.org/release/api/class_ar_resolver.html
   - Opening dependencies relative to their containing layer: https://openusd.org/release/api/class_sdf_layer.html

Additional checks passed for nested sublayers, cycles, internal references, missing-texture exclusion, and top-level-only reporting. All OpenUSD behavior used here was read from the cited documentation.
