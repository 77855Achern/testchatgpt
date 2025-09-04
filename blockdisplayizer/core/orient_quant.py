"""Normal quantisation and chart construction."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .voxelize import VoxelGrid

# Predefined direction sets
_dirs6 = np.array(
    [
        [1, 0, 0],
        [-1, 0, 0],
        [0, 1, 0],
        [0, -1, 0],
        [0, 0, 1],
        [0, 0, -1],
    ],
    dtype=float,
)
_dirs18 = np.vstack([
    _dirs6,
    [[1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0],
     [1, 0, 1], [1, 0, -1], [-1, 0, 1], [-1, 0, -1],
     [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, -1]],
])
_dirs18 = (_dirs18.T / np.linalg.norm(_dirs18, axis=1)).T
_dirs26 = np.vstack([
    _dirs18,
    [[1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
     [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]],
])
_dirs26 = (_dirs26.T / np.linalg.norm(_dirs26, axis=1)).T

DIRS = {
    "6": _dirs6,
    "18": _dirs18,
    "26": _dirs26,
    "snap_0_45_90": _dirs26,
}


def quantize_normals(nmap: np.ndarray, mode: str, tol_deg: float) -> np.ndarray:
    dirs = DIRS[mode]
    flat = nmap.reshape(-1, 3)
    idxmap = np.full(flat.shape[0], -1, dtype=int)
    mask = np.linalg.norm(flat, axis=1) > 0
    flat_norm = flat[mask]
    dots = flat_norm @ dirs.T
    best = np.argmax(dots, axis=1)
    angles = np.degrees(np.arccos(np.clip(dots[np.arange(len(flat_norm)), best], -1.0, 1.0)))
    valid = angles <= tol_deg
    idxmap[np.nonzero(mask)[0][valid]] = best[valid]
    return idxmap.reshape(nmap.shape[:3])


@dataclass
class Chart:
    mask: np.ndarray
    dir_idx: int
    voxels: list[tuple[int, int, int]]
    basis: tuple[np.ndarray, np.ndarray, np.ndarray]


def _basis_from_dir(n: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = n / np.linalg.norm(n)
    up = np.array([0.0, 1.0, 0.0])
    if abs(np.dot(n, up)) > 0.9:
        up = np.array([1.0, 0.0, 0.0])
    t1 = np.cross(up, n)
    t1 /= np.linalg.norm(t1)
    t2 = np.cross(n, t1)
    return t1, t2, n


def build_charts(grid: VoxelGrid, idxmap: np.ndarray, min_size: int) -> list[Chart]:
    charts: list[Chart] = []
    visited = np.zeros(grid.dims, dtype=bool)
    dirs = DIRS["snap_0_45_90"]  # use superset for basis
    for x in range(grid.dims[0]):
        for y in range(grid.dims[1]):
            for z in range(grid.dims[2]):
                if not grid.occ[x, y, z]:
                    continue
                idx = idxmap[x, y, z]
                if idx < 0 or visited[x, y, z]:
                    continue
                queue = [(x, y, z)]
                voxels = []
                mask = np.zeros(grid.dims, dtype=bool)
                while queue:
                    vx, vy, vz = queue.pop()
                    if (
                        vx < 0
                        or vy < 0
                        or vz < 0
                        or vx >= grid.dims[0]
                        or vy >= grid.dims[1]
                        or vz >= grid.dims[2]
                    ):
                        continue
                    if visited[vx, vy, vz] or idxmap[vx, vy, vz] != idx:
                        continue
                    visited[vx, vy, vz] = True
                    voxels.append((vx, vy, vz))
                    mask[vx, vy, vz] = True
                    for dx, dy, dz in [
                        (1, 0, 0),
                        (-1, 0, 0),
                        (0, 1, 0),
                        (0, -1, 0),
                        (0, 0, 1),
                        (0, 0, -1),
                    ]:
                        queue.append((vx + dx, vy + dy, vz + dz))
                if len(voxels) >= min_size:
                    basis = _basis_from_dir(dirs[idx])
                    charts.append(Chart(mask=mask, dir_idx=idx, voxels=voxels, basis=basis))
    return charts
