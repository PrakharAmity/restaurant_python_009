"""Kitchen ticket queue management and prioritization."""
from data import PREP_TICKETS


def kitchen_queue(tickets=None):
    """Order tickets by urgency descending, then original queue position."""
    rows = PREP_TICKETS if tickets is None else tickets
    return sorted(rows, key=lambda ticket: (ticket["priority"], ticket["received_order"]))
