"""Coordinate system conversions."""
from __future__ import annotations

import numpy as np
import trimesh


def to_minecraft_axes(mesh: trimesh.Trimesh, scale: float = 1.0) -> trimesh.Trimesh:
    """Convert from glTF coordinate system to Minecraft (X east, Y up, Z south).

    Parameters
    ----------
    mesh : trimesh.Trimesh
        Input mesh in glTF coordinates (+Y up, +Z forward).
    scale : float, optional
        Uniform scale factor to apply after conversion.
    """
    m = mesh.copy()
    transform = np.eye(4)
    transform[2, 2] = -1.0  # flip Z
    if scale != 1.0:
        transform[:3, :3] *= scale
    m.apply_transform(transform)
    return m
