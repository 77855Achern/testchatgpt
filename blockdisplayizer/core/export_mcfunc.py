"""Export RectPatches to Minecraft mcfunction commands."""
from __future__ import annotations

from typing import List

import numpy as np

from .greedy_surface import RectPatch
from .math3d import compose_trs_matrix, mat3_from_basis


def patch_to_block_display_cmd(p: RectPatch, block_id: str) -> str:
    R = mat3_from_basis(p.t1, p.n, p.t2)
    M = compose_trs_matrix(p.center, R, np.array([p.size_u, p.thickness, p.size_v]))
    # column-major list
    arr = M.T.flatten()
    matrix = ",".join(f"{v:.6f}" for v in arr)
    cmd = (
        f"/summon minecraft:block_display 0 0 0 {{block_state:{{Name:\"{block_id}\"}},"
        f"transformation:[{matrix}],brightness:{{sky:15,block:15}}}}"
    )
    return cmd


def export_mcfunction(patches: List[RectPatch], block_ids: List[str], path: str) -> None:
    lines = [patch_to_block_display_cmd(p, b) for p, b in zip(patches, block_ids)]
    with open(path, "w", encoding="utf8") as f:
        f.write("\n".join(lines))
