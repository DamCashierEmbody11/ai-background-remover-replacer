"""Runtime settings loaded from TOML with sane Windows-desktop defaults."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


DEFAULT_CONFIG_PATHS = (
    Path.cwd() / "bgremover.toml",
    Path.home() / ".config" / "bgremover" / "config.toml",
)


@dataclass(slots=True)
class Settings:
    device: str = "cpu"
    model_dir: Path = field(default_factory=lambda: Path.cwd() / "models")
    plugin_dir: Path = field(default_factory=lambda: Path.cwd() / "plugins")
    output_dir: Path = field(default_factory=lambda: Path.cwd() / "output")
    max_side: int = 2048
    alpha_matting: bool = True
    log_level: str = "INFO"

    @classmethod
    def load(cls, path: Path | None = None) -> "Settings":
        candidates = (path,) if path else DEFAULT_CONFIG_PATHS
        for candidate in candidates:
            if candidate and candidate.is_file():
                with candidate.open("rb") as fh:
                    raw = tomllib.load(fh)
                return cls(**{k: _coerce(v) for k, v in raw.get("bgremover", raw).items()})
        return cls()

    def ensure_dirs(self) -> None:
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)


def _coerce(value: object) -> object:
    if isinstance(value, str) and value.startswith(("/", "~", "C:\\")):
        return Path(value).expanduser()
    return value