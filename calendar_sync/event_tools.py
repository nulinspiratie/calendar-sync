from datetime import datetime


def events_are_same(event1, event2, verbose=False):
    local_timezone = datetime.now().astimezone().tzinfo
    for attr in ["summary", "begin", "end", "description", "location", "status"]:
        event1_attr = getattr(event1, attr)
        event2_attr = getattr(event2, attr)
        if not event1_attr and not event2_attr:
            continue

        if attr == "description":
            event1_attr = event1_attr[:8192]
            event2_attr = event2_attr[:8192]

        if attr in ["begin", "end"]:
            event1_attr = event1_attr.astimezone(local_timezone)
            event2_attr = event2_attr.astimezone(local_timezone)

        if event1_attr != event2_attr:
            if verbose:
                print(f"{attr}: {getattr(event1, attr)} != {getattr(event2, attr)}")
            return False
    else:
        return True


def compare_events(events1, events2):
    """Compares two `ics.Event` lists and returns a tuple of three lists:
    - events that are in both lists
    - events that are in the first list but not in the second list
    - events that are in the second list but not in the first list
    """
    events_in_both = []
    events_only_in_first = []
    events_only_in_second = []

    for event1 in events1:
        for event2 in events2:
            if events_are_same(event1, event2):
                events_in_both.append(event1)
                break
        else:
            events_only_in_first.append(event1)

    for event2 in events2:
        for event1 in events1:
            if events_are_same(event1, event2):
                break
        else:
            events_only_in_second.append(event2)

    return (events_in_both, events_only_in_first, events_only_in_second)


def print_events(*events, indent=0):
    if len(events) == 1 and isinstance(events[0], (list, tuple)):
        events = events[0]

    for event in events:
        print(
            f"{' ' * indent}{event.begin.isoformat()} - {event.end.isoformat()} | {event.summary}"
        )
