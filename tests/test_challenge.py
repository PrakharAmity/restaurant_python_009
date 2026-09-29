import pytest

from service import best_sellers, choose_prep_batch, kitchen_queue, order_total, search_menu_items, transition_order


def expect_equal(actual, expected, message):
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def test_menu_search_finds_items_in_configured_order():
    actual = [item["id"] for item in search_menu_items("sandwich")]
    expect_equal(actual, ["m2"], "Menu substring search")


def test_best_sellers_counts_units_not_order_presence():
    history = [
        {"items": [{"menu_id": "pasta", "quantity": 5}, {"menu_id": "fries", "quantity": 1}]},
        {"items": [{"menu_id": "fries", "quantity": 1}]},
    ]
    actual = best_sellers(history, 2)
    expect_equal(actual, ["pasta", "fries"], "Best seller unit ranking")


def test_kitchen_queue_prioritizes_urgent_tickets_and_keeps_fifo_ties():
    tickets = [
        {"id": "later-urgent", "priority": 4, "received_order": 2},
        {"id": "normal", "priority": 1, "received_order": 1},
        {"id": "first-urgent", "priority": 4, "received_order": 1},
    ]
    actual = [ticket["id"] for ticket in kitchen_queue(tickets)]
    expect_equal(actual, ["first-urgent", "later-urgent", "normal"], "Kitchen urgency and FIFO ordering")


def test_prep_batch_finds_global_best_combination():
    actual = choose_prep_batch(10)
    expect_equal(actual, ["#1102", "#1103"], "Optimal prep batch under 10 minutes")


def test_order_total_includes_modifier_prices():
    items = [{"quantity": 2, "unit_price": 16, "modifiers": [{"name": "Avocado", "price": 2}]}]
    actual = order_total(items)
    expect_equal(actual, 36, "Modifier-aware order total")


def test_order_cannot_skip_kitchen_steps():
    order = {"id": "#test", "status": "new"}
    try:
        transition_order(order, "ready")
    except ValueError:
        return
    raise AssertionError(f"Expected invalid transition to be rejected; order became {order['status']}")
