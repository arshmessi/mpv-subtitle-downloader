# Troubleshooting

## The menu does nothing

Confirm the Lua file is in MPV's `scripts` directory, the options file is in
`script-opts`, and the backend is on `PATH`. Run `mpv-subtitle doctor` and start
MPV with verbose logging to check script loading.

## No results

Try a title search directly:

```powershell
mpv-subtitle search-title "100 Meters" --year 2025 --language en
```

MPV owns embedded tracks and the aggregator does not inspect or extract them.
Network adapters may require endpoint configuration or credentials.

## Jellyfin identity is wrong

Use the MPV subtitle menu's **Correct media title and search** action. HTTP
streams cannot be hashed; title and metadata matching is expected.

## A downloaded subtitle does not load

Check the cache directory, file permissions, and subtitle validation output.
Only recognized subtitle formats are loaded, and HTML error pages are rejected.

## One provider fails

Provider failures are isolated. Check the provider report in JSON output and
run `mpv-subtitle providers`; another enabled provider can still return results.
