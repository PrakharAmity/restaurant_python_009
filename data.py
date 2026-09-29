"""Small, deterministic restaurant data set used by the offline demo."""

MENU = [
    {"id": "m1", "name": "Crispy cauliflower", "category": "Small plates", "price": 9.5, "prep_minutes": 8},
    {"id": "m2", "name": "Smoky chicken sandwich", "category": "Mains", "price": 16, "prep_minutes": 14},
    {"id": "m3", "name": "House fries", "category": "Sides", "price": 5, "prep_minutes": 6},
    {"id": "m4", "name": "Lemon olive oil cake", "category": "Dessert", "price": 8, "prep_minutes": 7},
    {"id": "m5", "name": "Roasted tomato pasta", "category": "Mains", "price": 18, "prep_minutes": 16},
    {"id": "m6", "name": "Citrus spritz", "category": "Drinks", "price": 7, "prep_minutes": 2},
]

ORDERS = [
    {"id": "#1048", "guest": "Maya Chen", "channel": "Pickup", "status": "preparing", "created_at": "12:42", "items": [{"menu_id": "m2", "name": "Smoky chicken sandwich", "quantity": 2, "unit_price": 16, "modifiers": [{"name": "Avocado", "price": 2}]}], "total": 38},
    {"id": "#1047", "guest": "Oliver James", "channel": "Table 12", "status": "ready", "created_at": "12:38", "items": [{"menu_id": "m5", "name": "Roasted tomato pasta", "quantity": 1, "unit_price": 18, "modifiers": []}, {"menu_id": "m3", "name": "House fries", "quantity": 1, "unit_price": 5, "modifiers": []}], "total": 25},
    {"id": "#1046", "guest": "Ari Patel", "channel": "Delivery", "status": "new", "created_at": "12:36", "items": [{"menu_id": "m1", "name": "Crispy cauliflower", "quantity": 2, "unit_price": 9.5, "modifiers": []}], "total": 19},
    {"id": "#1045", "guest": "Sofia Rivera", "channel": "Table 04", "status": "preparing", "created_at": "12:31", "items": [{"menu_id": "m5", "name": "Roasted tomato pasta", "quantity": 2, "unit_price": 18, "modifiers": []}], "total": 36},
]

SALES_HISTORY = [
    {"items": [{"menu_id": "m2", "quantity": 2}, {"menu_id": "m3", "quantity": 1}]},
    {"items": [{"menu_id": "m2", "quantity": 1}, {"menu_id": "m5", "quantity": 2}]},
    {"items": [{"menu_id": "m5", "quantity": 1}, {"menu_id": "m2", "quantity": 1}]},
]

PREP_TICKETS = [
    {"id": "#1048", "priority": 3, "received_order": 2, "prep_minutes": 14},
    {"id": "#1047", "priority": 1, "received_order": 1, "prep_minutes": 7},
    {"id": "#1046", "priority": 3, "received_order": 1, "prep_minutes": 8},
]

BATCH_CANDIDATES = [
    {"id": "#1101", "prep_minutes": 6, "value": 12},
    {"id": "#1102", "prep_minutes": 5, "value": 10},
    {"id": "#1103", "prep_minutes": 5, "value": 10},
]
