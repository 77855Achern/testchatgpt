"""Compute per-voxel normals from mesh faces."""
from __future__ import annotations

import numpy as np
import trimesh

from .voxelize import VoxelGrid


def voxel_normals(grid: VoxelGrid, mesh: trimesh.Trimesh) -> np.ndarray:
    nmap = np.zeros(grid.occ.shape + (3,), dtype=float)
    tris = mesh.triangles
    normals = mesh.face_normals
    areas = mesh.area_faces
    centroids = tris.mean(axis=1)
    idx = ((centroids - grid.origin) / grid.s).astype(int)
    for i, vox in enumerate(idx):
        x, y, z = vox
        if (
            0 <= x < grid.dims[0]
            and 0 <= y < grid.dims[1]
            and 0 <= z < grid.dims[2]
            and grid.occ[x, y, z]
        ):
            nmap[x, y, z] += normals[i] * areas[i]
    occ = grid.occ
    norms = np.linalg.norm(nmap, axis=-1, keepdims=True)
    norms[norms == 0] = 1.0
    nmap = nmap / norms
    nmap[~occ] = 0.0
    return nmap
