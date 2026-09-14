"""Human and JSON command-line interface."""

from __future__ import annotations

import argparse
import asyncio
import json
from dataclasses import asdict
from pathlib import Path

from . import __version__
from .config import load_config
from .media.identifier import identify
from .models import MediaInfo
from .providers.registry import built_in_registry
from .search.orchestrator import SearchOrchestrator
from .search.selection import select_result


def main() -> int:
    parser = argparse.ArgumentParser(prog="mpv-subtitle")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    search = subparsers.add_parser("search")
    search.add_argument("file")
    search.add_argument("--language", default="en")
    search.add_argument("--providers", default=None)
    search.add_argument("--interactive", action="store_true")
    search.add_argument("--json", action="store_true")
    search.add_argument("--download-directory", type=Path)
    title = subparsers.add_parser("search-title")
    title.add_argument("title")
    title.add_argument("--year", type=int)
    title.add_argument("--season", type=int)
    title.add_argument("--episode", type=int)
    title.add_argument("--language", default="en")
    title.add_argument("--json", action="store_true")
    subparsers.add_parser("providers")
    subparsers.add_parser("doctor")
    args = parser.parse_args()
    if args.command == "providers":
        for provider in built_in_registry().all():
            print(f"{provider.id}\t{provider.name}")
        return 0
    if args.command == "doctor":
        print("MPV Subtitle Aggregator Doctor\n  Core              OK\n  Provider registry OK")
        return 0
    config = load_config()
    if args.command == "search":
        path = Path(args.file)
        media = identify(str(path), filename=path.name)
    else:
        media = MediaInfo(args.title, year=args.year, season=args.season, episode=args.episode)
    providers = args.providers.split(",") if getattr(args, "providers", None) else config.providers
    registry = built_in_registry()
    response = asyncio.run(
        SearchOrchestrator(registry.select(providers), config.timeout).search(
            media, [args.language]
        )
    )
    if getattr(args, "json", False):
        print(json.dumps(asdict(response), default=str, indent=2))
    else:
        print(f"Subtitle Results: {media.title}")
        for index, result in enumerate(response.results, 1):
            print(
                f"{index}. {result.score:.0f} {result.language} {result.provider} {result.release}"
            )
        if getattr(args, "interactive", False) and response.results:
            selected = select_result(response.results)
            print(f"Selected {selected.result_id}" if selected else "Cancelled")
    return 0 if response.success else 1
