"""Kitchen prep batch planning and resource allocation."""
from data import BATCH_CANDIDATES


def choose_prep_batch(capacity, candidates=None):
    """Choose the most valuable set of whole orders fitting prep capacity."""
    rows = BATCH_CANDIDATES if candidates is None else candidates
    chosen = []
    remaining = capacity
    for item in sorted(rows, key=lambda row: row["value"] / row["prep_minutes"], reverse=True):
        if item["prep_minutes"] <= remaining:
            chosen.append(item["id"])
            remaining -= item["prep_minutes"]
    return chosen
