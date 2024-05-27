Synchronizer from Outlook calendar to Google calendar

This application synchronizes events from an ICS calendar to a Google calendar. The application is built using Python and the Google Calendar API.

## Installation instructions

### Prerequisites
1. Python 3.9 or higher
2. Poetry

### Steps

1. Clone the repository
2. Install dependencies using Poetry: `poetry install`
3. Request credentials from project owner.
   Create a GitHub issue if necessary.
   Add these credential to root-level file `credentials.json`
4. Add `config.toml` to package root with the following content:
   ```toml
   outlook_url = "https://outlook.office365.com/....ics" # URL to the ICS calendar
google_calendar_id = "google/calendar/id" # Google calendar ID```
5. Run `python calendar_sync/main.py`
   This should bring you to the Google Authorization page, follow the necessary steps to authorize the application.

Once authorization is complete, the calendars will perform a one-way sync to Google Calendar until Google Calendar has the same events as the ICS calendar

## Privacy Policy

Your privacy is important to us. Please review our [Privacy Policy](PRIVACY_POLICY.md) for more information.

## Terms of Service

Please review our [Terms of Service](TERMS_OF_SERVICE.md) before using the application.