"""Order lifecycle management and workflow state transitions."""

ALLOWED_TRANSITIONS = {"new": "preparing", "preparing": "ready", "ready": "completed"}


def transition_order(order, next_status):
    """Advance an order exactly one step through the kitchen workflow."""
    order["status"] = next_status
    return order
