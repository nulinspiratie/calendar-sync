from abc import ABC, abstractmethod
from datetime import datetime


class BaseCalendar(ABC):
    @abstractmethod
    def retrieve_events(self, time_start=None, time_end=None, max_results=100):
        pass

    @staticmethod
    def filter_events(events, time_start=None, time_end=None, max_results=100):

        local_timezone = datetime.now().astimezone().tzinfo

        filtered_events = []
        for event in events:
            if isinstance(max_results, int) and len(filtered_events) >= max_results:
                break
            if time_start is not None:
                if event.begin.astimezone(local_timezone) < time_start.astimezone(
                    local_timezone
                ):
                    continue
            if time_end is not None:
                if event.end.astimezone(local_timezone) > time_end.astimezone(
                    local_timezone
                ):
                    continue
            filtered_events.append(event)

        return filtered_events


class BaseWriteCalendar(BaseCalendar):
    @abstractmethod
    def add_event(self, event):
        pass

    @abstractmethod
    def remove_event(self, event):
        pass
