import sys
print("--- DEBUG START ---")
print(f"Python version: {sys.version}")
print(f"Sys path: {sys.path}")

try:
    import mpv_subtitle_aggregator
    print("Successfully imported mpv_subtitle_aggregator")
    from mpv_subtitle_aggregator.cli import main
    print("Successfully imported main from cli")
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()

print("--- DEBUG END ---")
