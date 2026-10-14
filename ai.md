# Goodfield Kitchen — Restaurant Service Desk

## Description

Goodfield Kitchen is an interactive restaurant operations dashboard built with Python Flask and vanilla JavaScript for managing live pickup, delivery, and dine-in orders.
It provides menu catalog search, kitchen ticket queue prioritization, best-selling dish analytics, and prep batch knapsack optimization using deterministic in-memory fixtures.

## Repository Structure

```text
restaurant-order-dashboard/
├── analytics.py            Sales analytics and popularity metrics
├── app.py                  Flask HTTP application, API endpoints, and live order state
├── catalog.py              Menu catalog querying and search
├── challenge.json          Runtime environment, port, build, start, and test configuration
├── conftest.py             Pytest configuration and test runner fixtures
├── data.py                 Deterministic in-memory fixtures (menu catalog, orders, sales history, tickets)
├── kitchen.py              Kitchen ticket queue management and prioritization
├── orders.py               Order lifecycle management and workflow state transitions
├── planner.py              Prep batch planning and capacity optimization
├── pricing.py              Order pricing, line item subtotals, and modifier charges
├── pytest.ini              Pytest configuration settings
├── README.md               Candidate-facing application and bug reproduction guide
├── requirements.txt        Python package dependencies
├── service.py              Service facade layer re-exporting operations
├── start.sh                Dev server startup script running Flask with reload
├── static/
│   ├── app.js              Client-side dashboard controller, order modal, and state rendering
│   └── styles.css          Responsive visual styles, grid layout, and operations design system
├── templates/
│   └── index.html          Goodfield Kitchen dashboard layout and structural markup
└── tests/
    └── test_challenge.py   Automated unit tests covering all six challenge issues
```

## Bugs and Bug Locations

### 1. Menu search fails on non-alphabetical menu items

- **Bug location:** `catalog.py`
- **How to observe it:** Search for "sandwich" in the order creation modal or call `search_menu_items("sandwich")`.
- **Failure:** Binary search assumes alphabetical ordering, failing to return matching items because menu entries are grouped by category.
- **Expected:** Substring search returns all matching menu items case-insensitively, regardless of menu configuration or category ordering.

### 2. Popular dishes ranking undercounts quantities and repeated orders

- **Bug location:** `analytics.py`
- **How to observe it:** Review the "Guest favorites" panel or inspect sales history aggregation.
- **Failure:** Collapsing order line items into a set discards item quantities and repeated order entries, undercounting popular dishes.
- **Expected:** Tally the actual units sold across all order lines in sales history and maintain deterministic ordering for ties.

### 3. Kitchen queue sorts tickets in reverse urgency

- **Bug location:** `kitchen.py`
- **How to observe it:** Inspect the "Kitchen pulse" panel or call `kitchen_queue()`.
- **Failure:** Tickets are sorted in ascending priority order instead of descending, and FIFO order is not maintained for tickets with equal urgency.
- **Expected:** Tickets are ordered by urgency (priority) in descending order, preserving first-in, first-out (FIFO) sequence on equal priority.

### 4. Prep planning selects suboptimal ticket batches

- **Bug location:** `planner.py`
- **How to observe it:** Check the prep batch suggestion for a capacity of 10 minutes.
- **Failure:** The greedy value-density heuristic selects suboptimal tickets (e.g., `#1101`), leaving higher-value combinations unselected.
- **Expected:** Optimal 0/1 knapsack selection finds the global best combination of whole tickets that maximizes total value within the prep capacity (tickets `#1102` and `#1103`).

### 5. Order total omits selected item modifiers

- **Bug location:** `pricing.py`
- **How to observe it:** Place an order with modifiers (such as adding avocado for $2 to the smoky chicken sandwich).
- **Failure:** The subtotal calculation only accounts for base item prices and ignores modifier charges.
- **Expected:** The subtotal includes the price of each selected modifier for every unit in the line item.

### 6. Order status transitions bypass kitchen workflow steps

- **Bug location:** `orders.py`
- **How to observe it:** Attempt an invalid status transition (e.g., jumping directly from `new` to `ready` or updating a completed ticket).
- **Failure:** Any requested status is accepted without validation, skipping kitchen steps or reopening completed orders.
- **Expected:** Orders strictly advance one step at a time (`new` → `preparing` → `ready` → `completed`), rejecting any invalid transition by raising a `ValueError`.

## Expected Behaviour After Fixing All Bugs

- Searching the menu by substring returns all matching items case-insensitively regardless of catalog configuration.
- The popular dishes ranking accurately counts total units sold across order histories with deterministic tie-breaking.
- Kitchen tickets in the queue are sorted with highest urgency first, maintaining FIFO order for equal-priority tickets.
- Prep planning selects the global optimal combination of tickets that maximizes total value within the specified prep-time budget.
- Placing orders with item modifiers accurately incorporates modifier charges for all item quantities in the final total.
- Order status transitions strictly enforce the kitchen workflow sequence (`new` → `preparing` → `ready` → `completed`), rejecting invalid or out-of-order changes.
- All automated unit tests in `tests/test_challenge.py` pass with exit code `0`.
