# Support matrix

| Feature                       | Local file       | Jellyfin/HTTP stream      |
| ----------------------------- | ---------------- | ------------------------- |
| Filename/title identification | yes              | metadata-dependent        |
| Embedded subtitle inspection  | yes, with FFmpeg | no                        |
| Media hash matching           | possible         | no                        |
| Title/year/episode matching   | yes              | yes, when metadata exists |
| Subtitle beside video         | configurable     | no; use local cache       |
| Cached subtitle loading       | yes              | yes                       |
| MPV alternative selection     | yes              | yes                       |

The application never attempts to hash an HTTP stream or write beside a remote
URL.
