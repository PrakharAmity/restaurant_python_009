"""Restaurant operations logic. The challenge is to repair six marked behaviors."""
from data import BATCH_CANDIDATES, MENU, PREP_TICKETS, SALES_HISTORY


def search_menu_items(query, menu=None):
    """Find menu entries whose name contains query, without regard to case."""
    items = MENU if menu is None else menu
    target = query.casefold().strip()
    # BUG 1 (DSA / easy): binary search assumes alphabetical order, but menu
    # entries are grouped by how the restaurant configured its menu.
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        name = items[mid]["name"].casefold()
        if target in name:
            return [items[mid]]
        if target < name:
            hi = mid - 1
        else:
            lo = mid + 1
    return []


def best_sellers(history=None, limit=5):
    """Return menu ids ordered by units sold, highest first."""
    rows = SALES_HISTORY if history is None else history
    totals = {}
    for order in rows:
        # BUG 2 (DSA / easy-medium): collapsing lines into a set discards
        # quantity and repeated menu items, undercounting popular dishes.
        for menu_id in {line["menu_id"] for line in order["items"]}:
            totals[menu_id] = totals.get(menu_id, 0) + 1
    return sorted(totals, key=lambda item_id: (-totals[item_id], item_id))[:limit]


def kitchen_queue(tickets=None):
    """Order tickets by urgency descending, then original queue position."""
    rows = PREP_TICKETS if tickets is None else tickets
    # BUG 3 (DSA / medium): urgency is sorted ascending; ties should remain FIFO.
    return sorted(rows, key=lambda ticket: (ticket["priority"], ticket["received_order"]))


def choose_prep_batch(capacity, candidates=None):
    """Choose the most valuable set of whole orders fitting prep capacity."""
    rows = BATCH_CANDIDATES if candidates is None else candidates
    # BUG 4 (DSA / hard): value-density greedy is not optimal for 0/1 knapsack.
    chosen = []
    remaining = capacity
    for item in sorted(rows, key=lambda row: row["value"] / row["prep_minutes"], reverse=True):
        if item["prep_minutes"] <= remaining:
            chosen.append(item["id"])
            remaining -= item["prep_minutes"]
    return chosen


def order_total(items):
    """Calculate the menu subtotal including paid modifiers."""
    # BUG 5 (restaurant workflow): modifier prices are omitted from the bill.
    return round(sum(line["quantity"] * line["unit_price"] for line in items), 2)


ALLOWED_TRANSITIONS = {"new": "preparing", "preparing": "ready", "ready": "completed"}


def transition_order(order, next_status):
    """Advance an order exactly one step through the kitchen workflow."""
    # BUG 6 (restaurant workflow): any requested status is accepted, including
    # skipping kitchen steps or reopening a completed ticket.
    order["status"] = next_status
    return order
