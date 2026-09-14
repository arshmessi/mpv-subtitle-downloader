# Support matrix

| Feature                          | Local file                             | Jellyfin/HTTP stream                   |
| -------------------------------- | -------------------------------------- | -------------------------------------- |
| Filename/title identification    | yes                                    | metadata-dependent                     |
| Embedded subtitle handling       | MPV-owned; aggregator does not inspect | MPV-owned; aggregator does not inspect |
| Media hash matching              | possible                               | no                                     |
| Title/year/episode matching      | yes                                    | yes, when metadata exists              |
| Subtitle beside video            | configurable                           | no; use local cache                    |
| Cached external subtitle loading | yes                                    | yes                                    |
| MPV alternative selection        | yes                                    | yes                                    |

The application never hashes an HTTP stream or writes beside a remote URL.
