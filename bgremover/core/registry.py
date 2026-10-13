"""In-memory plugin registry keyed by plugin name."""
from __future__ import annotations

from typing import Iterator

from bgremover.core.contracts import PluginMeta


class PluginRegistry:
    def __init__(self) -> None:
        self._meta: dict[str, PluginMeta] = {}
        self._instances: dict[str, object] = {}

    def register(self, meta: PluginMeta, instance: object) -> None:
        if meta.name in self._meta:
            raise ValueError(f"plugin already registered: {meta.name}")
        self._meta[meta.name] = meta
        self._instances[meta.name] = instance

    def get(self, name: str) -> object:
        try:
            return self._instances[name]
        except KeyError as exc:
            raise KeyError(f"unknown plugin: {name}") from exc

    def items(self) -> Iterator[tuple[str, PluginMeta]]:
        yield from self._meta.items()

    def __contains__(self, name: object) -> bool:
        return name in self._meta

    def __len__(self) -> int:
        return len(self._meta)