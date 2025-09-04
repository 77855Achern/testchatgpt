"""Export RectPatches to BDEngine JSON project."""
from __future__ import annotations

import json
from typing import List
import numpy as np

from .greedy_surface import RectPatch
from .math3d import compose_trs_matrix, mat3_from_basis


def export_bdengine_project(
    patches: List[RectPatch], block_ids: List[str], path: str
) -> None:
    entities = []
    for p, b in zip(patches, block_ids):
        R = mat3_from_basis(p.t1, p.n, p.t2)
        M = compose_trs_matrix(p.center, R, np.array([p.size_u, p.thickness, p.size_v]))
        entities.append(
            {
                "type": "block_display",
                "block_state": b,
                "transformation": M.T.flatten().tolist(),
                "brightness": {"sky": 15, "block": 15},
            }
        )
    data = {"version": 1, "entities": entities}
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2)
