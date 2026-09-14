# Adding a provider

Create a local Python module and subclass `SubtitleProvider`:

```python
class MyProvider(SubtitleProvider):
    id = "my-provider"
    name = "My Provider"

    async def search(self, media, languages):
        return ProviderSearchResult([...])
```

Register the instance with `ProviderRegistry.register`. Provider code is local
code and is never downloaded or executed automatically. Keep credentials out of
source control and return provider-specific payloads in `raw_provider_data`.

Production providers should also declare accurate capabilities, isolate timeout
and authentication errors, normalize language/forced/hearing-impaired fields,
and add mocked search/download and malformed-response tests. Add opt-in live
tests only when credentials and network access are safe. Document endpoint,
authentication, terms, and current status in `docs/providers.md`.

Custom providers are local Python code and currently require explicit
registration; arbitrary remote provider code is never downloaded or executed.
