from copy import deepcopy

from flask import Flask, jsonify, render_template, request

from data import MENU, ORDERS
from service import best_sellers, choose_prep_batch, kitchen_queue, order_total, transition_order

app = Flask(__name__)
orders = deepcopy(ORDERS)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/state")
def state():
    popular_ids = best_sellers()
    popular = [{"id": item_id, "name": next(item["name"] for item in MENU if item["id"] == item_id)} for item_id in popular_ids]
    return jsonify({
        "menu": MENU,
        "orders": orders,
        "popular": popular,
        "kitchen_queue": kitchen_queue(),
        "prep_batch": choose_prep_batch(10),
    })


@app.post("/api/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    items = payload.get("items", [])
    if not items or any(item.get("quantity", 0) < 1 for item in items):
        return jsonify({"error": "Add at least one item with a valid quantity."}), 400
    new_order = {
        "id": f"#{1049 + len(orders) - len(ORDERS)}",
        "guest": payload.get("guest", "Walk-in guest"),
        "channel": payload.get("channel", "Pickup"),
        "status": "new",
        "created_at": "Now",
        "items": items,
        "total": order_total(items),
    }
    orders.insert(0, new_order)
    return jsonify(new_order), 201


@app.patch("/api/orders/<order_id>")
def update_order(order_id):
    order = next((row for row in orders if row["id"] == order_id), None)
    if order is None:
        return jsonify({"error": "Order not found."}), 404
    payload = request.get_json(silent=True) or {}
    next_status = payload.get("status")
    if not next_status:
        return jsonify({"error": "A status is required."}), 400
    try:
        transition_order(order, next_status)
    except ValueError as error:
        return jsonify({"error": str(error)}), 409
    return jsonify(order)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
