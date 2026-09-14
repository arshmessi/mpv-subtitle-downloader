# Known limitations

- Only the embedded provider is credential-free today; network provider
  adapters require their endpoint or API configuration.
- Anonymous subtitle websites are not treated as supported providers until a
  maintained, permitted integration is verified with tests.
- HTTP streams cannot be hashed and rely on metadata/title matching.
- Filename identification is heuristic and can be corrected from the MPV menu.
- Automatic subtitle synchronization and translation are not implemented.
- Provider websites can change, rate-limit, or block automated requests.
