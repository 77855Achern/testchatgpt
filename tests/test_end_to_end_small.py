import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import trimesh

from blockdisplayizer.core.voxelize import make_grid, surface_mark
from blockdisplayizer.core.normals import voxel_normals
from blockdisplayizer.core.orient_quant import quantize_normals, build_charts
from blockdisplayizer.core.greedy_surface import chart_to_rectangles
from blockdisplayizer.core.palette import load_palette, nearest_block
from blockdisplayizer.core.export_mcfunc import export_mcfunction
from blockdisplayizer.core.export_bdengine import export_bdengine_project


def test_end_to_end_small(tmp_path: Path):
    mesh = trimesh.creation.box(extents=(1, 1, 1))
    grid = make_grid(mesh, s=0.5, margin=0.1)
    surface_mark(grid, mesh)
    nmap = voxel_normals(grid, mesh)
    idx = quantize_normals(nmap, mode="snap_0_45_90", tol_deg=10.0)
    charts = build_charts(grid, idx, min_size=1)
    patches = []
    for ch in charts:
        patches.extend(chart_to_rectangles(ch, grid, thickness=grid.s))
    assert 1 <= len(patches) <= 20
    palette = load_palette(
        str(Path(__file__).resolve().parents[1] / "blockdisplayizer/assets/palettes/concrete_terracotta.json")
    )
    block_ids = [nearest_block((1.0, 1.0, 1.0), palette).block_id for _ in patches]
    mcfunc_path = tmp_path / "build.mcfunction"
    export_mcfunction(patches, block_ids, str(mcfunc_path))
    assert mcfunc_path.exists() and mcfunc_path.read_text().strip()
    bd_path = tmp_path / "project.json"
    export_bdengine_project(patches, block_ids, str(bd_path))
    assert bd_path.exists() and bd_path.read_text().strip()
