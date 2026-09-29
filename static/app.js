const $ = (selector) => document.querySelector(selector);
let dashboard = { menu: [], orders: [], popular: [], kitchen_queue: [], prep_batch: [] };
let activeFilter = "all";
const cart = new Map();
const nextStatus = { new: "preparing", preparing: "ready", ready: "completed" };
const statusLabel = { new: "New", preparing: "Preparing", ready: "Ready", completed: "Completed" };

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
}

async function loadDashboard() {
  try {
    const response = await fetch("api/state", { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error("Could not load service data.");
    dashboard = await response.json();
    renderOrders();
    renderQueue();
    renderPopular();
    renderMenu();
    $("#nav-orders").textContent = dashboard.orders.filter((order) => order.status !== "completed").length;
  } catch (error) {
    $("#order-list").innerHTML = `<div class="empty-state">${escapeHtml(error.message)} Try refreshing in a moment.</div>`;
  }
}

function renderOrders() {
  const active = dashboard.orders.filter((order) => order.status !== "completed");
  const visible = dashboard.orders.filter((order) => activeFilter === "all" ? true : order.status === activeFilter);
  const counts = { all: dashboard.orders.length, new: 0, preparing: 0, ready: 0 };
  active.forEach((order) => counts[order.status] = (counts[order.status] || 0) + 1);
  Object.entries(counts).forEach(([key, count]) => {
    const node = $(`#${key}-count`);
    if (node) node.textContent = count;
  });
  $("#orders-value").innerHTML = `${48 + Math.max(0, dashboard.orders.length - 4)}<span class="trend">↑ 8.2%</span>`;
  $("#order-list").innerHTML = visible.length ? visible.map((order) => {
    const itemSummary = order.items.map((item) => `${item.quantity} × ${escapeHtml(item.name)}`).join(", ");
    const action = nextStatus[order.status]
      ? `<button class="order-action" data-order="${escapeHtml(order.id)}" data-status="${nextStatus[order.status]}">${nextStatus[order.status] === "completed" ? "Complete" : `Mark ${statusLabel[nextStatus[order.status]]}`}</button>`
      : "";
    return `<article class="order-row"><div class="order-id">${escapeHtml(order.id)}<small>${escapeHtml(order.created_at)}</small></div><div class="guest">${escapeHtml(order.guest)}<small>${escapeHtml(order.channel)}</small></div><div class="order-items">${itemSummary}</div><div class="order-total"><span class="status-pill status-${escapeHtml(order.status)}">${statusLabel[order.status] || escapeHtml(order.status)}</span><small>$${Number(order.total).toFixed(2)}</small>${action}</div></article>`;
  }).join("") : `<div class="empty-state">No ${activeFilter === "all" ? "orders" : `${activeFilter} orders`} right now.</div>`;
  document.querySelectorAll(".order-action").forEach((button) => button.addEventListener("click", () => advanceOrder(button.dataset.order, button.dataset.status)));
}

function renderQueue() {
  const queue = dashboard.kitchen_queue || [];
  $("#active-tickets").textContent = queue.length;
  $("#kitchen-queue").innerHTML = queue.length ? queue.slice(0, 3).map((ticket, index) => {
    const order = dashboard.orders.find((row) => row.id === ticket.id);
    const name = order ? order.items.map((item) => item.name).join(", ") : "Prep ticket";
    return `<div class="queue-row"><span class="queue-num">${index + 1}</span><div><strong>${escapeHtml(ticket.id)} · ${escapeHtml(name)}</strong><small>Urgency ${escapeHtml(ticket.priority)} · position ${escapeHtml(ticket.received_order)}</small></div><span class="queue-time">${escapeHtml(ticket.prep_minutes)} min</span></div>`;
  }).join("") : `<div class="empty-state small">No active kitchen tickets.</div>`;
  $("#prep-batch").textContent = (dashboard.prep_batch || []).join(" + ") || "No orders";
}

function renderPopular() {
  const icons = ["🍝", "🥪", "🍟", "🥗", "🍰"];
  const popular = dashboard.popular || [];
  $("#popular-list").innerHTML = popular.slice(0, 3).map((item, index) => `<div class="popular-row"><span class="food-thumb">${icons[index % icons.length]}</span><div><strong>${escapeHtml(item.name)}</strong><small>Popular this service</small></div><span class="pop-value">#${index + 1}</span></div>`).join("");
}

function renderMenu() {
  const query = $("#menu-search").value.trim().toLocaleLowerCase();
  const matches = query ? dashboard.menu.filter((item) => item.name.toLocaleLowerCase().includes(query)) : dashboard.menu;
  $("#modal-menu").innerHTML = matches.map((item) => `<button class="menu-item" type="button" data-menu="${escapeHtml(item.id)}"><span><strong>${escapeHtml(item.name)}</strong><small>${escapeHtml(item.category)} · ${escapeHtml(item.prep_minutes)} min</small></span><b>$${Number(item.price).toFixed(2)}　＋</b></button>`).join("") || `<div class="empty-state small">No menu items match that search.</div>`;
  document.querySelectorAll(".menu-item").forEach((button) => button.addEventListener("click", () => addToCart(button.dataset.menu)));
}

function addToCart(menuId) {
  const menuItem = dashboard.menu.find((item) => item.id === menuId);
  if (!menuItem) return;
  const current = cart.get(menuId) || { menu_id: menuId, name: menuItem.name, quantity: 0, unit_price: menuItem.price, modifiers: [] };
  current.quantity += 1;
  current.modifiers = menuId === "m2" && $("#add-avocado").checked ? [{ name: "Avocado", price: 2 }] : [];
  cart.set(menuId, current);
  updateCart();
}

function updateCart() {
  const rows = [...cart.values()];
  const count = rows.reduce((sum, item) => sum + item.quantity, 0);
  const total = rows.reduce((sum, item) => sum + item.quantity * (item.unit_price + item.modifiers.reduce((extra, modifier) => extra + modifier.price, 0)), 0);
  $("#cart-count").textContent = `${count} item${count === 1 ? "" : "s"}`;
  $("#cart-total").textContent = `$${total.toFixed(2)}`;
  $("#submit-order").disabled = count === 0;
}

async function advanceOrder(orderId, status) {
  try {
    const response = await fetch(`api/orders/${encodeURIComponent(orderId)}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status }) });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Could not update order.");
    }
    await loadDashboard();
  } catch (error) { window.alert(error.message); }
}

async function submitOrder() {
  const guest = $("#guest-name").value.trim() || "Walk-in guest";
  const button = $("#submit-order");
  button.disabled = true;
  try {
    const response = await fetch("api/orders", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ guest, channel: "Pickup", items: [...cart.values()] }) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Could not place order.");
    cart.clear();
    updateCart();
    $("#order-message").textContent = `${result.id} is in the kitchen queue.`;
    await loadDashboard();
    window.setTimeout(closeModal, 800);
  } catch (error) {
    $("#order-message").textContent = error.message;
    button.disabled = false;
  }
}

function openModal() {
  $("#order-modal").hidden = false;
  $("#guest-name").focus();
}
function closeModal() {
  $("#order-modal").hidden = true;
  $("#order-message").textContent = "";
}

document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
  tab.classList.add("active");
  activeFilter = tab.dataset.filter;
  renderOrders();
}));
$("#new-order-button").addEventListener("click", openModal);
$("#close-modal").addEventListener("click", closeModal);
$("#refresh-button").addEventListener("click", loadDashboard);
$("#view-all").addEventListener("click", () => {
  activeFilter = "all";
  document.querySelectorAll(".tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.filter === "all"));
  renderOrders();
});
$("#menu-search").addEventListener("input", renderMenu);
$("#submit-order").addEventListener("click", submitOrder);
$("#order-modal").addEventListener("click", (event) => { if (event.target.id === "order-modal") closeModal(); });
document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeModal(); });
loadDashboard();
window.setInterval(loadDashboard, 5000);
