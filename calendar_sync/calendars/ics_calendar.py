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
        self.all_events = None
        self.events = None
        self._ics_text = None

    def retrieve_events(self, time_start=None, time_end=None, max_results=100):
        if time_start is None:
            time_start = datetime.now()

        self._ics_text = requests.get(self.url).text
        ics_text = self._ics_text.replace(
            "(UTC+01:00) Brussels, Copenhagen, Madrid, Paris", "Europe/Copenhagen"
        )
        ics_text = ics_text.replace("Customized Time Zone", "Europe/Copenhagen")
        self._calendar = ics.Calendar(ics_text)

        self.all_events = list(self._calendar.events)
        logger.info(f"Retrieved {len(self.all_events)} events")

        self.events = self.filter_events(
            self.all_events, time_start, time_end, max_results
        )
        logger.info(f"Filtered to {len(self.events)} events")
        return self.events
