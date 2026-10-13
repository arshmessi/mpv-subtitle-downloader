from pathlib import Path

ROOT = Path(__file__).parents[1]
LUA_SCRIPT = ROOT / "mpv" / "scripts" / "subtitle-aggregator.lua"
MPV_OPTIONS = ROOT / "mpv" / "script-opts" / "subtitle-aggregator.conf"


def test_repo_lua_script_uses_configured_python_and_structured_subprocess_args() -> None:
    script = LUA_SCRIPT.read_text(encoding="utf-8")

    assert "python_exe = 'python'" in script
    assert "'-u', '-m', 'mpv_subtitle_aggregator.cli'" in script
    assert "table.insert(command, '--media-title')" in script
    assert "table.insert(command, title)" in script
    assert "cmd /C" not in script
    assert "Users\\arshm" not in script


def test_repo_mpv_options_expose_portable_python_setting() -> None:
    options = MPV_OPTIONS.read_text(encoding="utf-8")

    assert "python_exe" in options
    assert "OPEN_SUBTITLES_API_KEY" not in options
    assert "Users\\arshm" not in options