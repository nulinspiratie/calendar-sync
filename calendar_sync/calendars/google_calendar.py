import os
from datetime import datetime, timedelta
import logging

from calendar_sync.config_tools import get_root_folder
from ics.event import Event

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from calendar_sync.calendars.calendar_base import BaseWriteCalendar
from calendar_sync.google_tools import (
    google_event_to_ics_event,
    ics_event_to_google_event,
    print_google_events,
)

logger = logging.getLogger(__name__)


class GoogleCalendar(BaseWriteCalendar):
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        self._creds = self.get_credentials()
        self._service = build("calendar", "v3", credentials=self._creds)
        self._google_events = None
        self.events = None

    @staticmethod
    def get_credentials():
        SCOPES = [
            # "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/calendar",
        ]
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        token_path = get_root_folder() / "token.json"
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                credentials_path = get_root_folder() / "credentials.json"
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            token_path.write_text(creds.to_json())
        return creds

    def _retrieve_events_raw(self, time_start=None, time_end=None, max_results=100):
        local_timezone = datetime.now().astimezone().tzinfo
        # Call the Calendar API
        if time_start is None:
            time_start = datetime.now().astimezone(local_timezone).isoformat()
        elif isinstance(time_start, datetime):
            time_start = time_start.astimezone(local_timezone).isoformat()

        if isinstance(time_end, datetime):
            time_end = time_end.astimezone(local_timezone).isoformat()

        events_result = (
            self._service.events()
            .list(
                calendarId=self.calendar_id,
                timeMin=time_start,
                timeMax=time_end,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        self._google_events = events_result.get("items", [])

        self.events = list(map(google_event_to_ics_event, self._google_events))

        return self.events

    def retrieve_events(self, time_start=None, time_end=None, max_results=100):
        # Call the Calendar API
        if time_start is None:
            time_start = datetime.now()

        # Get events starting earlier, and more results, then filter afterwards
        # This ensures similar behaviour as other calendars
        time_start_earlier = time_start - timedelta(days=1)

        local_timezone = datetime.now().astimezone().tzinfo
        time_start_earlier = time_start.astimezone(local_timezone)

        self.all_events = self._retrieve_events_raw(
            time_start=time_start_earlier,
            time_end=time_end,
            max_results=max_results + 100,
        )
        logger.info(f"Retrieved {len(self.events)} events")

        self.events = self.filter_events(
            self.all_events, time_start, time_end, max_results
        )
        return self.events

    def add_event(self, event):
        if isinstance(event, Event):
            google_event = ics_event_to_google_event(event)
        else:
            google_event = event

        if not isinstance(google_event, dict):
            raise ValueError("Event must be a dictionary or ics.Event object")

        saved_event = (
            self._service.events()
            .insert(calendarId=self.calendar_id, body=google_event)
            .execute()
        )
        logger.info(f"Added event {event.begin} | {event.summary}")

    def remove_event(self, event):
        if isinstance(event, Event):
            google_event = next(e for e in self._google_events if e["id"] == event.uid)
        else:
            google_event = event

        self._service.events().delete(
            calendarId=self.calendar_id, eventId=google_event["id"]
        ).execute()

        logger.info(f"Removed event {event.begin} | {event.summary}")

    def remove_all_events(self):
        self.retrieve_events(max_results=500)
        for event in self._google_events:
            self.remove_event(event)

    def print_events(self, *events):
        if not events:
            events = self.events
        print_google_events(*events)
