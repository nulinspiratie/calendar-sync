import logging
from datetime import timedelta

from calendar_sync.calendar_synchronization import (
    synchronize_outlook_to_google_calendar,
)
from calendar_sync.config_tools import get_configuration


def main():
    logging.basicConfig(level=logging.INFO)
    config = get_configuration()

    results = synchronize_outlook_to_google_calendar(
        outlook_url=config["outlook_url"],
        google_calendar_id=config["google_calendar_id"],
    )

    return results


if __name__ == "__main__":
    main()
