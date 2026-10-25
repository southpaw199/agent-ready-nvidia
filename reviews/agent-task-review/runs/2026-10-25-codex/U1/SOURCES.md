# Sources

All OpenUSD behavior used in task.py was read from the two requested documentation sites. General Python, shell, virtual environment, pip, and RGB (red = 1, 0, 0) knowledge was pre-existing. The half-size offsets and bounds are arithmetic derived from the requested four-meter edge length and the documented cube centering.

Setup used general Python and pip knowledge, not an OpenUSD documentation page:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir --index-url https://pypi.org/simple usd-core
.venv/bin/python task.py
```

Installed package: usd-core 26.11 from PyPI, as explicitly requested. PyPI was used for installation only, not as an OpenUSD documentation source.

1. Create and save scene.usda: https://openusd.org/release/tut_helloworld.html . Set metersPerUnit to 1.0 and upAxis to Z: https://docs.nvidia.com/learn-openusd/latest/beyond-basics/units.html .
2. Define /World as an Xform and set it as the default prim: https://docs.nvidia.com/learn-openusd/latest/composition-basics/default-prim.html .
3. Define /World/Box, set size, and author the matching local extent: https://openusd.org/release/api/class_usd_geom_cube.html . This page says cubes are centered at the origin and that authoring size requires authoring extent. Red displayColor: https://openusd.org/release/api/class_usd_geom_gprim.html . Translate the cube by (0, 0, 2): https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/xformcommonapi.html . Color uses displayColor, documented as a display/modeling color in the absence of a shader.
4. Save and reopen: https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html . Query units and up axis: the units page in step 1. Query default prim and traverse paths: https://docs.nvidia.com/learn-openusd/latest/beyond-basics/stage-traversal.html . Query type name: the Hello World page in step 1. Query size: the cube page in step 3. Compute world bounds: https://openusd.org/release/api/class_usd_geom_b_box_cache.html . Convert to an axis-aligned range: https://openusd.org/release/api/class_gf_b_box3d.html .

The geometric ground is the plane z = 0; no extra ground prim is needed. Local bounds (-2, -2, -2) to (2, 2, 2), translated by (0, 0, 2), give world bounds (-2, -2, 0) to (2, 2, 4).
