"""Human and JSON command-line interface."""

from __future__ import annotations

import argparse
import asyncio
import json
from dataclasses import asdict
from pathlib import Path

from . import __version__
from .config import cache_directory, load_config
from .media.identifier import identify
from .models import MediaInfo, SubtitleResult
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
    search.add_argument("--media-title", default=None)
    search.add_argument("--season", type=int)
    search.add_argument("--episode", type=int)
    search.add_argument("--imdb-id", default=None)
    title = subparsers.add_parser("search-title")
    title.add_argument("title")
    title.add_argument("--year", type=int)
    title.add_argument("--season", type=int)
    title.add_argument("--episode", type=int)
    title.add_argument("--language", default="en")
    title.add_argument("--json", action="store_true")
    download = subparsers.add_parser("download-result")
    download.add_argument("result_id")
    download.add_argument("--json", action="store_true")
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
    if args.command == "download-result":
        return _download_cached_result(args.result_id, args.json, config)
    if args.command == "search":
        path = Path(args.file)
        media = identify(str(path), filename=path.name, media_title=args.media_title)
        if args.season is not None:
            media.season = args.season
        if args.episode is not None:
            media.episode = args.episode
        if args.imdb_id:
            media.imdb_id = args.imdb_id
    else:
        media = MediaInfo(args.title, year=args.year, season=args.season, episode=args.episode)
    providers = args.providers.split(",") if getattr(args, "providers", None) else config.providers
    registry = built_in_registry()
    response = asyncio.run(
        SearchOrchestrator(registry.select(providers), config.timeout).search(
            media, [args.language]
        )
    )
    _save_search_response(response)
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


def _save_search_response(response: object) -> None:
    cache_directory().mkdir(parents=True, exist_ok=True)
    cache_file = cache_directory() / "last-search.json"
    cache_file.write_text(json.dumps(asdict(response), default=str), encoding="utf-8")


def _download_cached_result(result_id: str, as_json: bool, config: object) -> int:
    cache_file = cache_directory() / "last-search.json"
    if not cache_file.exists():
        message = "No cached search results are available"
        print(json.dumps({"success": False, "message": message}) if as_json else message)
        return 1
    payload = json.loads(cache_file.read_text(encoding="utf-8"))
    matching = next(
        (item for item in payload.get("results", []) if item.get("result_id") == result_id), None
    )
    if matching is None:
        message = f"Unknown subtitle result: {result_id}"
        print(json.dumps({"success": False, "message": message}) if as_json else message)
        return 1
    result = SubtitleResult(**matching)
    provider = built_in_registry().get(result.provider)
    destination = config.download_directory
    path = asyncio.run(provider.download(result, destination))
    output = {"success": True, "path": str(path), "result_id": result_id}
    print(json.dumps(output) if as_json else str(path))
    return 0
