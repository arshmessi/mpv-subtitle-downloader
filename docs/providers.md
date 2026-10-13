# Providers

| Provider          | Network | Movies | TV  | Hash | Authentication              | Status                    |
| ----------------- | ------- | ------ | --- | ---- | --------------------------- | ------------------------- |
| SubDL (public)    | yes     | yes    | no  | no   | none for public movie pages | implemented movie adapter |
| TVSubtitles.net   | yes     | no     | yes | no   | none                        | implemented TV adapter    |
| OpenSubtitles.com | yes     | yes    | yes | yes  | API key                     | implemented adapter       |
| SubDL API         | yes     | yes    | yes | no   | endpoint/API configuration  | optional adapter          |
| SubSource API     | yes     | yes    | yes | no   | endpoint/API configuration  | optional adapter          |

The public SubDL adapter searches current public movie pages and downloads the
public English SRT archives exposed by those pages. TVSubtitles searches exact
series/season/episode pages and resolves English subtitle archives without an
account or API key. Anime providers are not yet enabled by default.

The authenticated network adapters use normalized result contracts and isolate
provider failures. A provider is not considered fully operational merely because
its module imports: endpoint behavior, authentication, rate limits, and download
responses must be verified with mocked and opt-in live tests.

Anonymous website integrations are not listed as supported until a maintained
and permitted integration is implemented and tested.
