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