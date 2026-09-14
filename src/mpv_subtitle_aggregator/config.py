"""TOML configuration with sensible Windows defaults."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AppConfig:
    providers: list[str] = field(default_factory=lambda: ["opensubtitles", "subdl", "subsource"])
    excluded_providers: list[str] = field(default_factory=list)
    language: str = "en"
    profile: str = "default"
    interactive_selection: bool = False
    auto_select_best: bool = True
    timeout: float = 15.0
    download_directory: Path = field(default_factory=lambda: cache_directory() / "subtitles")
    show_provider_status: bool = True


def config_path() -> Path:
    root = Path(os.environ.get("APPDATA", Path.home() / ".config"))
    return root / "mpv-subtitle-aggregator" / "config.toml"


def cache_directory() -> Path:
    return Path(os.environ.get("LOCALAPPDATA", Path.home() / ".cache")) / "mpv-subtitle-aggregator"


def load_config(path: Path | None = None) -> AppConfig:
    target = path or config_path()
    if not target.exists():
        return AppConfig()
    with target.open("rb") as file:
        data: dict[str, Any] = tomllib.load(file)
    providers = data.get("providers", {})
    enabled = [
        key
        for key, value in providers.items()
        if isinstance(value, dict) and value.get("enabled", True)
    ]
    return AppConfig(
        providers=enabled or AppConfig().providers,
        language=str(data.get("language", "en")),
        profile=str(data.get("profile", "default")),
        interactive_selection=bool(data.get("interactive_selection", False)),
        auto_select_best=bool(data.get("auto_select_best", True)),
        timeout=float(data.get("timeout", 15.0)),
        show_provider_status=bool(data.get("show_provider_status", True)),
    )
