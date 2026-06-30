from collections import defaultdict
from collections.abc import Callable
from typing import Any

class EventBus:

    def __init__(self):

        self._listeners = defaultdict(list)

    def subscribe(self, event_type, callback: Callable):

        self._listeners[event_type].append(callback)

    def emit(self, event):

        for callback in self._listeners[type(event)]:

            callback(event)