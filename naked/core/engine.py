class NakedEngine:
    def __init__(self, registry):
        self.registry = registry
    
    async def search(self, username):

        results = []
        for provider in self.registry.providers:

            result = await provider.search(username)

            results.append(result)

        return results