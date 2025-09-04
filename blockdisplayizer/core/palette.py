"""Palette handling and colour matching."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import List

import numpy as np


@dataclass
class BlockColor:
    block_id: str
    rgb_srgb: tuple[int, int, int]
    rgb_lin: tuple[float, float, float]


@dataclass
class Palette:
    name: str
    items: List[BlockColor]


def _srgb_to_linear(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    def _c(c: float) -> float:
        c = c / 255.0
        if c <= 0.04045:
            return c / 12.92
        return ((c + 0.055) / 1.055) ** 2.4
    return tuple(_c(c) for c in rgb)


def load_palette(path: str) -> Palette:
    data = json.loads(Path(path).read_text())
    items = []
    for item in data["items"]:
        rgb = tuple(item["rgb"])
        items.append(
            BlockColor(
                block_id=item["block_id"],
                rgb_srgb=rgb,
                rgb_lin=_srgb_to_linear(rgb),
            )
        )
    return Palette(name=data.get("name", Path(path).stem), items=items)


def _luma(rgb_lin: tuple[float, float, float]) -> float:
    r, g, b = rgb_lin
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def nearest_block(
    rgb_lin: tuple[float, float, float],
    palette: Palette,
    method: str = "DE76",
    w_luma: float = 0.0,
) -> BlockColor:
    target = np.array(rgb_lin)
    best = None
    best_dist = float("inf")
    for item in palette.items:
        c = np.array(item.rgb_lin)
        diff = np.linalg.norm(target - c)
        if w_luma > 0:
            diff = (1 - w_luma) * diff + w_luma * abs(_luma(target) - _luma(c))
        if diff < best_dist:
            best = item
            best_dist = diff
    assert best is not None
    return best
