"""Greedy surface meshing producing rectangular patches."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .voxelize import VoxelGrid
from .orient_quant import Chart


@dataclass
class RectPatch:
    center: np.ndarray
    t1: np.ndarray
    t2: np.ndarray
    n: np.ndarray
    size_u: float
    size_v: float
    thickness: float
    voxels: list[tuple[int, int, int]]


def chart_to_rectangles(chart: Chart, grid: VoxelGrid, thickness: float) -> list[RectPatch]:
    """Create a single rectangle covering all voxels in the chart.

    This is a simplified greedy mesher suitable for small charts.
    """
    vox = np.array(chart.voxels)
    centers = grid.origin + (vox + 0.5) * grid.s
    t1, t2, n = chart.basis
    u = centers @ t1
    v = centers @ t2
    min_u, max_u = u.min(), u.max()
    min_v, max_v = v.min(), v.max()
    center = (
        t1 * (min_u + max_u) / 2
        + t2 * (min_v + max_v) / 2
        + n * grid.s / 2
    )
    size_u = max_u - min_u + grid.s
    size_v = max_v - min_v + grid.s
    patch = RectPatch(
        center=center,
        t1=t1,
        t2=t2,
        n=n,
        size_u=size_u,
        size_v=size_v,
        thickness=thickness,
        voxels=chart.voxels,
    )
    return [patch]
