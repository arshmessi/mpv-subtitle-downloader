# Providers

| Provider           | Network | Movies | TV  | Hash | Authentication         | Status              |
| ------------------ | ------- | ------ | --- | ---- | ---------------------- | ------------------- |
| Embedded subtitles | no      | yes    | yes | no   | none; FFmpeg required  | implemented         |
| OpenSubtitles.com  | yes     | yes    | yes | yes  | API key                | implemented adapter |
| SubDL              | yes     | yes    | yes | no   | endpoint configuration | generic adapter     |
| SubSource          | yes     | yes    | yes | no   | endpoint configuration | generic adapter     |

The built-in network adapters use injectable transports and normalized result
contracts. A provider is not considered fully operational merely because its
module imports: endpoint behavior, authentication, rate limits, and download
responses must be verified with mocked and opt-in live tests.

Anonymous website integrations are not listed as supported until a maintained
and permitted integration is implemented and tested.
