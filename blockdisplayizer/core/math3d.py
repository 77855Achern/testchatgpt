"""Basic 3D math helpers."""
from __future__ import annotations

import numpy as np


def compose_trs_matrix(
    translation: np.ndarray, rotation_3x3: np.ndarray, scale: np.ndarray
) -> np.ndarray:
    m = np.eye(4)
    m[:3, :3] = rotation_3x3 * scale[np.newaxis, :]
    m[:3, 3] = translation
    return m


def mat3_from_basis(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    m = np.column_stack([x, y, z])
    return m


def quat_from_mat3(R: np.ndarray) -> np.ndarray:
    """Convert rotation matrix to quaternion (x, y, z, w)."""
    q = np.empty(4)
    t = np.trace(R)
    if t > 0:
        r = np.sqrt(1 + t)
        w = 0.5 * r
        r = 0.5 / r
        q[0] = (R[2, 1] - R[1, 2]) * r
        q[1] = (R[0, 2] - R[2, 0]) * r
        q[2] = (R[1, 0] - R[0, 1]) * r
        q[3] = w
    else:
        i = np.argmax([R[0, 0], R[1, 1], R[2, 2]])
        j = (i + 1) % 3
        k = (i + 2) % 3
        r = np.sqrt(1 + R[i, i] - R[j, j] - R[k, k])
        q[i] = 0.5 * r
        r = 0.5 / r
        q[3] = (R[k, j] - R[j, k]) * r
        q[j] = (R[j, i] + R[i, j]) * r
        q[k] = (R[k, i] + R[i, k]) * r
    return q
