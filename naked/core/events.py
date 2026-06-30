from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Event:
    timestamp: datetime = datetime.now()
    
@dataclass(slots=True)
class SearchStarted(Event):
    username: str


@dataclass(slots=True)
class SearchFinished(Event):
    username: str


@dataclass(slots=True)
class ProviderLoaded(Event):
    provider: str


@dataclass(slots=True)
class ProviderFailed(Event):
    provider: str
    error: Exception