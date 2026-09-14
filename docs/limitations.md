# Known limitations

- The verified credential-free provider currently supports public SubDL movie
  pages; TV/anime public support is not claimed yet.
- OpenSubtitles, SubDL API, and SubSource API adapters require user configuration.
- MPV owns embedded subtitle tracks; the aggregator never inspects, removes, or
  replaces them.
- HTTP streams cannot be hashed and rely on metadata/title matching.
- Filename identification is heuristic and can be corrected from the MPV menu.
- Automatic synchronization and translation are not implemented.
- Provider websites can change, rate-limit, or block automated requests.
