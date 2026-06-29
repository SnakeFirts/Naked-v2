class Registry:

    def __init__(self):
        self.providers = []

    def register(self, provider):
        self.providers.append(provider)

    def get_all(self):
        return self.providers