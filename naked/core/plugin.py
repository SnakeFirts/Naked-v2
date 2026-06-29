from abc import ABC, abstractmethod

class Provider(ABC):

    name: str

    @abstractmethod
    async def search(self, username: str):
        pass