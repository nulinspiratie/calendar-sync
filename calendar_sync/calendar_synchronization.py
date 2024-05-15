import logging
from datetime import timedelta, datetime

from calendar_sync.calendars.ics_calendar import IcsCalendar
from calendar_sync.calendars.google_calendar import GoogleCalendar
from calendar_sync.event_tools import compare_events

logger = logging.getLogger(__name__)


def synchronize_outlook_to_google_calendar(
    outlook_url: str,
    google_calendar_id: str,
    timedelta: timedelta = None,
    **events_query,
):
    logging.info("Synchronizing Outlook to Google Calendar")

    if timedelta is not None:
        events_query["time_start"] = datetime.now() + timedelta

    logging.info("Loading Outlook ICS calendar")
    outlook_calendar = IcsCalendar(url=outlook_url)
    outlook_events = outlook_calendar.retrieve_events(**events_query)

    logging.info("Loading Google Calendar")
    google_calendar = GoogleCalendar(calendar_id=google_calendar_id)
    google_events = google_calendar.retrieve_events(**events_query)

    events_comparison = compare_events(google_events, outlook_events)
    common_events = events_comparison[0]
    extra_google_events = events_comparison[1]
    extra_outlook_events = events_comparison[2]
    logger.info(
        f"Common events: {len(common_events)}, "
        f"Extra Google events: {len(extra_google_events)}, "
        f"Extra Outlook events: {len(extra_outlook_events)}"
    )

    for extra_google_event in extra_google_events:
        google_calendar.remove_event(extra_google_event)

    for extra_outlook_event in extra_outlook_events:
        google_calendar.add_event(extra_outlook_event)

    logging.info("Synchronization finished")

    return {
        "outlook_calendar": outlook_calendar,
        "google_calendar": google_calendar,
        "outlook_events": outlook_events,
        "google_events": google_events,
        "common_events": common_events,
        "extra_google_events": extra_google_events,
        "extra_outlook_events": extra_outlook_events,
    }
