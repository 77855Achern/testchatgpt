# BlockDisplayizer

BlockDisplayizer converts glTF models into Minecraft `block_display` entities. The
pipeline voxelizes a mesh, groups surface voxels into rectangles, assigns block
colours from a palette and exports either a `.mcfunction` or a small JSON project
for the [BDEngine](https://github.com/SpaceNull/bdengine).

## Installation

The project targets **Python 3.11**. Create a virtual environment and install
requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the desktop tool:

```bash
python blockdisplayizer/app.py
```

Typical workflow inside the GUI:

1. **Import** – select a `.glb`/`.gltf` file, adjust scale and load.
2. **Voxelize** – choose voxel size and create a surface voxel grid.
3. **Orient** – quantise normals and build charts, then generate rectangles.
4. **Colours** – select a palette and match rectangles to Minecraft blocks.
5. **Export** – write a `mcfunction` and/or BDEngine JSON project.

The resulting mcfunction contains `/summon minecraft:block_display` commands.
The JSON project has the following structure:

```json
{
  "version": 1,
  "entities": [
    {
      "type": "block_display",
      "block_state": "minecraft:white_concrete",
      "transformation": [16 floats column-major],
      "brightness": {"sky":15, "block":15}
    }
  ]
}
```

## Testing

Run the included unit test which exercises a tiny end‑to‑end pipeline:

```bash
pytest
```

## Performance notes

* Use **surface only** voxelisation for large meshes.
* Smaller voxel sizes improve fidelity but increase runtime and entity counts.
* Greedy rectangles merge adjacent voxels; large charts reduce command count.

## Known limitations

* The voxeliser uses random surface sampling and is not a robust triangle–AABB
  test; for complex meshes results may differ slightly.
* Colour sampling uses a single average colour per patch without texture
  look‑ups.
* The ModernGL preview is a minimal stub and does not represent the final
  exported geometry.

## License

This project is released under the [MIT License](LICENSE).
