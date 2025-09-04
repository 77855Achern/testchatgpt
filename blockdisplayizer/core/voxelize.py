"""Simple surface voxelisation utilities."""
from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np
import trimesh


@dataclass
class VoxelGrid:
    s: float
    origin: np.ndarray
    dims: tuple[int, int, int]
    occ: np.ndarray


def make_grid(mesh: trimesh.Trimesh, s: float, margin: float = 1.0) -> VoxelGrid:
    bounds = mesh.bounds
    origin = bounds[0] - margin * s
    max_corner = bounds[1] + margin * s
    dims = np.ceil((max_corner - origin) / s).astype(int)
    occ = np.zeros(dims, dtype=bool)
    return VoxelGrid(s=s, origin=origin, dims=tuple(dims), occ=occ)


def surface_mark(grid: VoxelGrid, mesh: trimesh.Trimesh) -> None:
    """Mark voxels that intersect the mesh surface.

    A simple approach sampling surface points. Not a perfect triangle-AABB test
    but sufficient for small meshes and tests.
    """
    count = max(1000, len(mesh.faces) * 10)
    samples, _ = trimesh.sample.sample_surface(mesh, count)
    idx = ((samples - grid.origin) / grid.s).astype(int)
    valid = (
        (idx[:, 0] >= 0)
        & (idx[:, 1] >= 0)
        & (idx[:, 2] >= 0)
        & (idx[:, 0] < grid.dims[0])
        & (idx[:, 1] < grid.dims[1])
        & (idx[:, 2] < grid.dims[2])
    )
    idx = idx[valid]
    grid.occ[idx[:, 0], idx[:, 1], idx[:, 2]] = True
