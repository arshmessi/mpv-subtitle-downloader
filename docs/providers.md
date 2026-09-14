# Providers

| Provider | Movies | TV | Hash | Title | Authentication | Status |
| --- | --- | --- | --- | --- | --- | --- |
| OpenSubtitles | yes | yes | yes | yes | endpoint/token dependent | adapter |
| SubDL | yes | yes | no | yes | endpoint dependent | adapter |
| SubSource | yes | yes | no | yes | endpoint dependent | adapter |

The built-in adapters use a small JSON transport contract so endpoint details
can be configured without coupling orchestration to a website's scraper.