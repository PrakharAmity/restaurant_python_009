"""Menu catalog operations and item lookup."""
from data import MENU


def search_menu_items(query, menu=None):
    """Find menu entries whose name contains query, without regard to case."""
    items = MENU if menu is None else menu
    target = query.casefold().strip()
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
