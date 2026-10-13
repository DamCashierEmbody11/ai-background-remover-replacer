"""Shared contracts every remover/replacer plugin must satisfy."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import numpy as np


@dataclass(frozen=True, slots=True)
class PluginMeta:
    name: str
    version: str
    kind: str  # "remover" | "replacer" | "matting"
    description: str
    author: str = "unknown"


@runtime_checkable
class BackgroundRemover(Protocol):
    """A remover returns a float32 alpha mask in [0, 1], shape (H, W)."""

    meta: PluginMeta

    def load(self, model_dir: str) -> None: ...

    def predict(self, rgb: np.ndarray) -> np.ndarray: ...


@runtime_checkable
class BackgroundReplacer(Protocol):
    """A replacer composites foreground over a background image."""

    meta: PluginMeta

    def composite(
        self,
        foreground_rgb: np.ndarray,
        alpha: np.ndarray,
        background_rgb: np.ndarray,
    ) -> np.ndarray: ...