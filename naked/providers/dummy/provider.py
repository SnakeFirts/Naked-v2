from naked.core.plugin import Provider

class DummyProvider(Provider):

    name = "dummy"

    async def search(self, username):

        return {

            "platform": self.name,

            "username": username,

            "exists": True
        }