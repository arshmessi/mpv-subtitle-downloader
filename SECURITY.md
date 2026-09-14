# Security

Do not publish API keys, passwords, cookies, downloaded subtitles, or debug logs
containing credentials. Custom providers execute locally and must be reviewed
before installation. Report security issues privately to the repository
maintainers rather than posting secrets in a public issue.

Subtitle searches send selected media identification fields to enabled external
providers. The video file itself is not uploaded. Local file hashes may be sent
only to providers whose capabilities and configuration use hash search; HTTP
streams are never hashed.
