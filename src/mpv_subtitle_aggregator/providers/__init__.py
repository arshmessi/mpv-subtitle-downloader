"""Subtitle provider contracts and built-in adapters."""

from .base import ProviderCapabilities, SubtitleProvider
from .registry import ProviderRegistry, built_in_registry

__all__ = ["ProviderCapabilities", "ProviderRegistry", "SubtitleProvider", "built_in_registry"]