# Goodfield Kitchen — Restaurant Service Desk

Goodfield is an interactive restaurant operations dashboard built for managing live pickup, delivery, and dine-in orders during service. It allows staff to browse the menu catalog, build and place tickets, track kitchen queue urgency, monitor best-selling dishes, and optimize prep batch planning using deterministic in-memory fixtures.

---

## 1. Application Overview

### Core Functionality
- **Live Order Management**: Track incoming dine-in, pickup, and delivery tickets across real-time kitchen status stages (`new` → `preparing` → `ready` → `completed`).
- **Interactive Ticket Creation**: Search the menu, select items with custom paid modifiers (such as avocado additions), calculate order subtotals, and submit live tickets.
- **Kitchen Queue Prioritization**: Organize kitchen tickets dynamically by urgency and preserve first-in, first-out (FIFO) sequence for tickets with equal urgency.
- **Popular Dishes Analytics**: Rank top-selling dishes by aggregate units sold across order histories to surface guest favorites.
- **Prep Batch Optimization**: Determine the optimal combination of kitchen tickets fitting a prep-time capacity to maximize order fulfillment value.

### Technology Stack
- **Framework**: Python 3.12 with Flask
- **Build Tool / Dev Server**: Flask reloader (`start.sh`, served on `0.0.0.0:5000`)
- **Styling**: Vanilla CSS (custom design system, responsive grid layout, metric sparklines, modal dialogs)
- **Testing**: pytest (`tests/test_challenge.py`)
- **Data**: Bundled deterministic in-memory fixtures (`data.py`)

---

## 2. Debugging Challenge

QA engineers and floor staff have flagged several issues in the Goodfield Kitchen service desk platform. Your goal is to investigate the codebase, reproduce each bug, and implement the necessary fixes so that all automated test suites pass.

### Reported Issues & Tasks:

#### Issue 1: Menu Search Fails on Non-Alphabetical Menu Items
- **User Symptom**: When searching for menu items like "sandwich" in the order modal, matching items fail to appear in the results because binary search assumes the menu is sorted alphabetically, while the restaurant menu is ordered by category.
- **Task**: Update `search_menu_items` in `catalog.py` to return every menu item whose name contains the search query substring, case-insensitively, regardless of how the menu is ordered.

#### Issue 2: Popular Dishes Undercounts Quantities and Repeated Orders
- **User Symptom**: The "Guest favorites" panel ranks dishes incorrectly because the calculation collapses items into sets, ignoring item quantities and repeat orders, undercounting total units sold.
- **Task**: Fix `best_sellers` in `analytics.py` to tally the actual units sold across all order lines in sales history and ensure deterministic ordering for ties.

#### Issue 3: Kitchen Queue Sorts Tickets in Reverse Urgency
- **User Symptom**: In the "Kitchen pulse" panel, low-urgency tickets appear ahead of urgent tickets because the queue is sorted in ascending priority order instead of descending, and FIFO order is not maintained for equal-priority tickets.
- **Task**: Correct `kitchen_queue` in `kitchen.py` to sort tickets by urgency (priority) in descending order while preserving first-in, first-out (FIFO) order for tickets with equal priority.

#### Issue 4: Prep Planning Selects Suboptimal Ticket Batches
- **User Symptom**: The prep batch suggestion relies on a greedy value-density heuristic that misses the optimal combination of whole orders fitting within the prep-time capacity, leaving valuable tickets unselected.
- **Task**: Implement an optimal 0/1 knapsack selection algorithm in `choose_prep_batch` in `planner.py` that maximizes total ticket value within the given prep-time limit.

#### Issue 5: Order Total Omits Selected Item Modifiers
- **User Symptom**: When guests customize an item by adding modifiers (such as adding avocado for $2 to the smoky chicken sandwich), the calculated order total only accounts for the base item price, omitting modifier costs.
- **Task**: Update `order_total` in `pricing.py` to include the price of each selected modifier for every unit in the line item when calculating the total bill.

#### Issue 6: Order Status Transitions Bypass Kitchen Workflow Steps
- **User Symptom**: Orders can skip essential intermediate kitchen statuses (e.g., jumping directly from `new` to `ready` or reopening completed orders), disrupting kitchen operations and order integrity.
- **Task**: Update `transition_order` in `orders.py` to enforce that orders advance strictly one step at a time (`new` → `preparing` → `ready` → `completed`), rejecting any invalid transition by raising a `ValueError` without altering the order.

---

## 3. Expected Behavior After Fixing Bugs

After resolving the issues:
1. Searching the menu by substring (e.g., "sandwich") returns all matching items case-insensitively regardless of catalog configuration.
2. The popular dishes ranking accurately counts total units sold across order histories with deterministic tie-breaking.
3. Kitchen tickets in the queue are sorted with highest urgency first, maintaining FIFO order for equal priority tickets.
4. Prep planning selects the global optimal combination of tickets that maximizes total value within the specified prep-time budget (e.g., tickets `#1102` and `#1103` for a 10-minute limit).
5. Placing orders with item modifiers accurately incorporates modifier charges for all item quantities in the final total.
6. Order status transitions strictly follow the valid sequence (`new` → `preparing` → `ready` → `completed`), rejecting invalid or out-of-order changes.
7. All automated tests in `tests/` pass with exit code `0`.
