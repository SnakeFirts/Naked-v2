from naked.core.plugin import Provider

class Registry:
    def __init__(self):
        self._providers: list[Provider] = []

    def register(self, provider: Provider):
        self._providers.append(provider)

    @property
    def providers(self):
        return self._providers