from datetime import datetime, date
from ics import Event
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def print_google_events(*events):
    if not events:
        print("No upcoming events found.")
        return

    # Prints the start and name of the next 10 events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))

        print(f"{start:20}", end=" | ")

        if "summary" in event:
            print(f'{event["summary"]:30}', end=" | ")
        elif event.get("visibility") == "private":
            print("PRIVATE", end=" | ")
        else:
            print("NO SUMMARY", end=" | ")
        print(event)


def google_event_to_ics_event(google_event):
    attrs = {}

    if "dateTime" in google_event["start"]:
        attrs["begin"] = datetime.fromisoformat(google_event["start"]["dateTime"])
    else:
        attrs["begin"] = date.fromisoformat(google_event["start"]["date"])
    timezone = pytz.timezone(google_event["start"]["timeZone"])
    attrs["begin"] = attrs["begin"].astimezone(timezone)

    if "dateTime" in google_event["end"]:
        attrs["end"] = datetime.fromisoformat(google_event["end"]["dateTime"])
    else:
        attrs["end"] = date.fromisoformat(google_event["end"]["date"])
    attrs["end"] = attrs["end"].astimezone(timezone)
    timezone = pytz.timezone(google_event["end"]["timeZone"])

    if "summary" in google_event:
        attrs["summary"] = google_event["summary"]
    if "id" in google_event:
        attrs["uid"] = google_event["id"]
    if "description" in google_event:
        attrs["description"] = google_event["description"]
    if "location" in google_event:
        attrs["location"] = google_event["location"]
    if "htmlLink" in google_event:
        attrs["url"] = google_event["htmlLink"]
    if "status" in google_event:
        attrs["status"] = google_event["status"]
    if "created" in google_event:
        attrs["created"] = datetime.fromisoformat(google_event["created"])
    if "updated" in google_event:
        attrs["last_modified"] = datetime.fromisoformat(google_event["updated"])

    event = Event(**attrs)
    return event


def ics_event_to_google_event(ics_event):
    local_timezone = datetime.now().astimezone().tzinfo
    google_event = {
        "start": {"dateTime": ics_event.begin.astimezone(local_timezone).isoformat()},
        "end": {"dateTime": ics_event.end.astimezone(local_timezone).isoformat()},
    }
    if ics_event.summary:
        google_event["summary"] = ics_event.summary
    if ics_event.description:
        google_event["description"] = ics_event.description
    if ics_event.location:
        google_event["location"] = ics_event.location
    return google_event
