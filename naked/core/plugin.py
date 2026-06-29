from abc import ABC, abstractmethod
from typing import Any

class Provider(ABC):
    """Clase base para todos los proveedores."""

    name: str = "provider"
    @abstractmethod
    async def search(self, username: str) -> Any:
        """Busca un usuario y devuelve el resultado."""
        raise NotImplementedError