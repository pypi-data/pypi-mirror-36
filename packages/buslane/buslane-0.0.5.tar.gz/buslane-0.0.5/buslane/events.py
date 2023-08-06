import abc
from collections import defaultdict
from typing import TypeVar, Generic, Type, Dict, List

from buslane.utils import get_message_cls


class Event:
    pass


E = TypeVar('E', bound=Event)


class EventHandler(abc.ABC, Generic[E]):

    @abc.abstractmethod
    def handle(self, event: E) -> None:
        pass


class EventBus:

    def __init__(self) -> None:
        self._handlers: Dict[Type[Event], List[EventHandler]] = defaultdict(list)

    def register(self, handler: EventHandler) -> None:
        self._handlers[get_message_cls(type(handler), Event)].append(handler)

    def publish(self, event: Event) -> None:
        for handler in self._handlers[type(event)]:
            self.handle(event=event, handler=handler)

    def handle(self, event: Event, handler: EventHandler) -> None:
        handler.handle(event)
