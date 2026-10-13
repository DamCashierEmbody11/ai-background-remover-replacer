"""Loader: discovers plugins from entry-points and a local plugins/ dir."""
from __future__ import annotations

import importlib
import importlib.metadata as md
import importlib.util
import logging
from pathlib import Path

from bgremover.core.contracts import PluginMeta

log = logging.getLogger(__name__)
ENTRY_GROUP = "bgremover.plugins"


def iter_entry_point_plugins() -> list[object]:
    found: list[object] = []
    for ep in md.entry_points(group=ENTRY_GROUP):
        try:
            found.append(ep.load())
        except Exception as exc:  # noqa: BLE001 — one bad plugin must not kill discovery
            log.warning("entry-point plugin %s failed to load: %s", ep.name, exc)
    return found


def iter_directory_plugins(plugin_dir: Path) -> list[object]:
    found: list[object] = []
    if not plugin_dir.is_dir():
        return found
    for path in sorted(plugin_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        try:
            spec = importlib.util.spec_from_file_location(f"bgremover_plugin_{path.stem}", path)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "PLUGIN"):
                found.append(module.PLUGIN)
        except Exception as exc:  # noqa: BLE001
            log.warning("directory plugin %s failed to load: %s", path.name, exc)
    return found


def meta_of(instance: object) -> PluginMeta:
    meta = getattr(instance, "meta", None)
    if not isinstance(meta, PluginMeta):
        raise TypeError(f"{instance!r} does not expose a PluginMeta")
    return meta
</｜｜DSML｜｜ parameter>