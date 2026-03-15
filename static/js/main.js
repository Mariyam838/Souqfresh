let activeCategory = "All";
let toastTimer = null;

/* ─── SPLASH: generate particles ─── */
(function() {
  const container = document.getElementById("particles");
  if (!container) return;
  for (let i = 0; i < 25; i++) {
    const p = document.createElement("div");
    p.className = "particle";
    const size = Math.random() * 3 + 1;
    p.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random() * 100}%;
      animation-duration:${8 + Math.random() * 12}s;
      animation-delay:${Math.random() * 8}s;
      opacity:${0.2 + Math.random() * 0.4};
    `;
    container.appendChild(p);
  }
})();

/* ─── ENTER APP ─── */
function enterApp() {
  const splash = document.getElementById("splash");
  const app = document.getElementById("app");
  splash.classList.add("leaving");
  setTimeout(() => {
    splash.style.display = "none";
    app.className = "app-visible";
    loadProducts();
  }, 650);
}

/* ─── PRODUCTS ─── */
async function loadProducts() {
  const q = (document.getElementById("search") || {}).value || "";
  const grid = document.getElementById("products-grid");
  const noResults = document.getElementById("no-results");
  const countEl = document.getElementById("section-count");

  grid.innerHTML = Array(10).fill(`
    <div style="background:#fff">
      <div class="skel skel-img"></div>
      <div class="skel skel-line"></div>
      <div class="skel skel-line2"></div>
    </div>`).join("");

  const params = new URLSearchParams({ cat: activeCategory, q });
  const res = await fetch(`/api/products?${params}`);
  const items = await res.json();

  countEl.textContent = items.length ? `${items.length} items` : "";

  if (!items.length) {
    grid.innerHTML = "";
    noResults.style.display = "block";
    return;
  }
  noResults.style.display = "none";
  grid.innerHTML = items.map(renderCard).join("");
}

const emojiMap = {
  "Fruits":"🍎","Vegetables":"🥦","Dairy":"🥛",
  "Meat":"🥩","Bakery":"🍞","Drinks":"🥤",
  "Snacks":"🍿","Organic":"🌿"
};

function renderCard(p) {
  const badge = p.cat === "Meat"
    ? `<div class="halal-badge">Halal</div>`
    : p.cat === "Organic"
    ? `<div class="organic-badge">Organic</div>`
    : "";
  const emoji = emojiMap[p.cat] || "🛒";
  return `
    <div class="product-card">
      <div class="product-img-wrap">
        ${badge}
        <img class="product-img" src="${p.img}" alt="${p.name}" loading="lazy"
             onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="product-img-fallback">${emoji}</div>
      </div>
      <div class="product-info">
        <div>
          <div class="product-name">${p.name}</div>
          <div class="product-origin">${p.origin}</div>
        </div>
        <div class="product-bottom">
          <div class="product-price">AED ${p.price.toFixed(2)} <small>/ item</small></div>
          <button class="add-btn ${p.in_cart ? "in-cart" : ""}"
                  onclick="addToCart(${p.id}, event)">${p.in_cart ? "✓" : "+"}</button>
        </div>
      </div>
    </div>`;
}

/* ─── CATEGORY ─── */
function setCategory(cat, btn) {
  activeCategory = cat;
  document.querySelectorAll(".cat-pill").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  document.getElementById("section-title").textContent = cat === "All" ? "All Products" : cat;
  loadProducts();
}

/* ─── ADD TO CART ─── */
async function addToCart(id, e) {
  const btn = e.currentTarget || e.target;
  btn.disabled = true;
  const res = await fetch("/api/cart/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  });
  const data = await res.json();
  updateCartCount(data.cart_count);
  showToast(data.message);
  await loadProducts();
  btn.disabled = false;
}

/* ─── CART OPEN / CLOSE ─── */
async function openCart() {
  await renderCart();
  document.getElementById("cart-backdrop").classList.add("open");
  document.getElementById("cart-drawer").classList.add("open");
  document.body.style.overflow = "hidden";
}
function closeCart() {
  document.getElementById("cart-backdrop").classList.remove("open");
  document.getElementById("cart-drawer").classList.remove("open");
  document.body.style.overflow = "";
}

/* ─── RENDER CART ─── */
async function renderCart() {
  const res = await fetch("/api/cart");
  const data = await res.json();
  const bodyEl = document.getElementById("cart-items");
  const footEl = document.getElementById("cart-footer");
  if (!data.items.length) {
    bodyEl.innerHTML = `
      <div class="empty-basket">
        <span style="font-size:48px;display:block;margin-bottom:12px">🛒</span>
        Your basket is empty<br>
        <span style="font-size:12px;opacity:0.5">Browse and add some items!</span>
      </div>`;
    footEl.innerHTML = "";
    return;
  }
  bodyEl.innerHTML = data.items.map(i => `
    <div class="cart-item">
      <img class="cart-item-img" src="${i.img}" alt="${i.name}" onerror="this.style.background='#F0E9DC'">
      <div class="cart-item-info">
        <div class="cart-item-name">${i.name}</div>
        <div class="cart-item-origin">${i.origin}</div>
        <div class="qty-row">
          <button class="qty-btn" onclick="updateQty(${i.id},-1)">−</button>
          <span class="qty-val">${i.qty}</span>
          <button class="qty-btn" onclick="updateQty(${i.id},1)">+</button>
        </div>
      </div>
      <div class="cart-item-total">AED ${(i.price * i.qty).toFixed(2)}</div>
    </div>`).join("");
  footEl.innerHTML = `
    <div class="total-line"><span>Subtotal</span><span>AED ${data.subtotal.toFixed(2)}</span></div>
    <div class="total-line"><span>Delivery</span><span>AED ${data.delivery.toFixed(2)}</span></div>
    <div class="total-line final"><span>Total</span><span>AED ${data.total.toFixed(2)}</span></div>
    <button class="checkout-btn" onclick="checkout()">Place Order →</button>`;
}

/* ─── QTY ─── */
async function updateQty(id, delta) {
  const res = await fetch("/api/cart/update", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ id, delta })
  });
  const data = await res.json();
  updateCartCount(data.cart_count);
  renderCart(); loadProducts();
}

/* ─── CHECKOUT ─── */
async function checkout() {
  const res = await fetch("/api/checkout", { method: "POST" });
  const data = await res.json();
  if (data.success) {
    closeCart();
    updateCartCount(0);
    loadProducts();
    showOrderModal(data);
  }
}

/* ─── ORDER MODAL ─── */
function showOrderModal(data) {
  const orderNum = Math.floor(Math.random() * 90000) + 10000;
  document.getElementById("order-id").textContent = orderNum;

  const itemCount = data.item_count || "—";
  const subtotal = data.subtotal ? data.subtotal.toFixed(2) : (data.total - 10).toFixed(2);

  document.getElementById("order-details").innerHTML = `
    <div class="order-detail-row">
      <span class="lbl">Order #</span>
      <span class="val">${orderNum}</span>
    </div>
    <div class="order-detail-row">
      <span class="lbl">Items</span>
      <span class="val">${data.items_count || "Multiple"}</span>
    </div>
    <div class="order-detail-row">
      <span class="lbl">Subtotal</span>
      <span class="val">AED ${subtotal}</span>
    </div>
    <div class="order-detail-row">
      <span class="lbl">Delivery</span>
      <span class="val">AED 10.00</span>
    </div>
    <div class="order-detail-row total-row">
      <span class="lbl">Total Paid</span>
      <span class="val">AED ${data.total.toFixed(2)}</span>
    </div>`;

  document.getElementById("order-backdrop").classList.add("open");
  document.getElementById("order-modal").classList.add("open");
  document.body.style.overflow = "hidden";
  launchConfetti();
}

function closeOrderModal() {
  document.getElementById("order-backdrop").classList.remove("open");
  document.getElementById("order-modal").classList.remove("open");
  document.body.style.overflow = "";
}

function launchConfetti() {
  const colors = ["#C9A84C","#E8CB78","#F0DFA0","#8A5E1A","#fff","#4CAF50","#FF9800"];
  for (let i = 0; i < 80; i++) {
    setTimeout(() => {
      const el = document.createElement("div");
      el.className = "confetti-piece";
      const size = Math.random() * 8 + 4;
      const isCircle = Math.random() > 0.5;
      el.style.cssText = `
        left:${Math.random() * 100}vw;
        top:0;
        width:${size}px;
        height:${isCircle ? size : size * 0.4}px;
        background:${colors[Math.floor(Math.random() * colors.length)]};
        border-radius:${isCircle ? "50%" : "2px"};
        animation-duration:${1.5 + Math.random() * 2}s;
        animation-delay:0s;
        opacity:1;
      `;
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 3500);
    }, i * 25);
  }
}

/* ─── HELPERS ─── */
function updateCartCount(n) {
  document.getElementById("cart-count").textContent = n;
  document.getElementById("cart-label").textContent = n ? "Basket" : "Cart";
}
function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg; t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2800);
}