from abc import ABC, abstractmethod


class BaseCalendar(ABC):
    @abstractmethod
    def retrieve_events(self, time_start=None, time_end=None, max_results=100):
        pass


class BaseWriteCalendar(BaseCalendar):
    @abstractmethod
    def add_event(self, event):
        pass

    @abstractmethod
    def remove_event(self, event):
        pass
