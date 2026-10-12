"""Sales analytics and menu performance metrics."""
from data import SALES_HISTORY


def best_sellers(history=None, limit=5):
    """Return menu ids ordered by units sold, highest first."""
    rows = SALES_HISTORY if history is None else history
    totals = {}
    for order in rows:
        for menu_id in {line["menu_id"] for line in order["items"]}:
            totals[menu_id] = totals.get(menu_id, 0) + 1
    return sorted(totals, key=lambda item_id: (-totals[item_id], item_id))[:limit]
