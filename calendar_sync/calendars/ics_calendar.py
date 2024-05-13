from datetime import datetime
import ics
import requests
import logging
from arrow import Arrow


from calendar_sync.calendars.calendar_base import BaseCalendar


logger = logging.getLogger(__name__)


class IcsCalendar(BaseCalendar):
    def __init__(self, url):
        self.url = url
        self._calendar = None
        self.events = None

    def retrieve_events(self, time_start=None, time_end=None, max_results=100):
        if time_start is None:
            time_start = datetime.now()

        ics_text = requests.get(self.url).text
        ics_text = ics_text.replace(
            "(UTC+01:00) Brussels, Copenhagen, Madrid, Paris", "Europe/Copenhagen"
        )
        self._calendar = ics.Calendar(ics_text)
        self.events = list(self._calendar.events)

        filtered_events = []
        for event in self.events:
            if len(filtered_events) >= max_results:
                break
            if time_start is not None:
                begin = event.begin
                if isinstance(event.begin, Arrow):
                    begin = begin.naive
                if begin.astimezone() < time_start.astimezone():
                    continue
            if time_end is not None:
                end = event.end
                if isinstance(event.end, Arrow):
                    end = end.naive
                if end.astimezone() > time_end.astimezone():
                    continue
            # if time_end is not None and event.end.astimezone() > time_end.astimezone():
            # continue
            filtered_events.append(event)

        logger.info(f"Retrieved {len(filtered_events)} events")

        return filtered_events
