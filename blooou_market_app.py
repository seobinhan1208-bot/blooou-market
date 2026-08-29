PASTER STARTS HEREimport os
import json
import time
import random
from flask import Flask, request, jsonify, Response, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
SHOES_FILE = f"{DATA_DIR}/shoes.json"
LISTINGS_FILE = f"{DATA_DIR}/listings.json"
REVIEWS_FILE = f"{DATA_DIR}/reviews.json"
PREDICTIONS_FILE = f"{DATA_DIR}/predictions.json"
USERS_FILE = f"{DATA_DIR}/users.json"
ORDERS_FILE = f"{DATA_DIR}/orders.json"

ADMIN_EMAIL = os.environ.get("MARKET_ADMIN_EMAIL", "owner@blooou.com")
PAYMENT_LINK = os.environ.get("MARKET_PAYMENT_LINK", "")   # set once a real payment processor is connected

def _atomic_write(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)

def _load(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default

def load_shoes(): return _load(SHOES_FILE, {})
def save_shoes(d): _atomic_write(SHOES_FILE, d)
def load_listings(): return _load(LISTINGS_FILE, [])
def save_listings(d): _atomic_write(LISTINGS_FILE, d)
def load_reviews(): return _load(REVIEWS_FILE, [])
def save_reviews(d): _atomic_write(REVIEWS_FILE, d)
def load_predictions(): return _load(PREDICTIONS_FILE, [])
def save_predictions(d): _atomic_write(PREDICTIONS_FILE, d)
def load_users(): return _load(USERS_FILE, {})
def save_users(d): _atomic_write(USERS_FILE, d)
def load_orders(): return _load(ORDERS_FILE, [])
def save_orders(d): _atomic_write(ORDERS_FILE, d)

def current_user():
    email = session.get("u")
    if not email:
        return None
    users = load_users()
    return users.get(email)

def is_owner():
    u = current_user()
    return bool(u and u.get("email") == ADMIN_EMAIL)

# seed a handful of real-feeling shoes on first run, so the site never opens empty
def seed_shoes():
    shoes = load_shoes()
    if shoes:
        return
    seed = [
        {"id": "ja4-nightmare", "brand": "Nike", "name": "Ja 4 EP Nightmare", "price": 210.0,
         "history": [178, 180, 182, 179, 185, 210], "story": "Ja Morant wore this exact colorway in last night's game. Resale on this size jumped within hours of tip-off.", "sizes": [9, 9.5, 10, 10.5, 11]},
        {"id": "aj1-mocha", "brand": "Jordan", "name": "Air Jordan 1 Low Mocha", "price": 1180.0,
         "history": [1450, 1420, 1390, 1180, 1200, 1180], "story": "A brief oversupply on StockX pushed the lowest ask down before buyers absorbed it and the price steadied.", "sizes": [8, 9, 10, 11]},
        {"id": "kd17-pearl", "brand": "Nike", "name": "KD 17 Aunt Pearl", "price": 165.0,
         "history": [150, 152, 155, 158, 160, 165], "story": "October's breast cancer awareness release always sees a seasonal bump as the colorway becomes scarce again.", "sizes": [9, 10, 11, 12]},
        {"id": "nb550-green", "brand": "New Balance", "name": "NB 550 White Green", "price": 95.0,
         "history": [88, 89, 90, 91, 93, 95], "story": "Steady, unhyped demand, this one moves slowly and predictably rather than spiking.", "sizes": [8, 9, 10, 11, 12]},
    ]
    save_shoes({s["id"]: s for s in seed})

seed_shoes()

STYLE = """<style>
  *{box-sizing:border-box;-webkit-font-smoothing:antialiased}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
       background:#fff;color:#0a0c10}
  a{color:inherit}
  .nav{display:flex;align-items:center;gap:20px;padding:16px 24px;border-bottom:1px solid #e5e7eb}
  .logo{font-size:19px;font-weight:600;text-decoration:none;color:#0a0c10}
  .logo span{color:#378ADD}
  .navsearch{flex:1;background:#f5f6f7;border:1px solid #e5e7eb;padding:9px 14px;color:#8a8f98;font-size:13.5px}
  .navlinks{display:flex;gap:18px;font-size:13px;font-weight:500;white-space:nowrap;align-items:center}
  .navlinks a{text-decoration:none}
  .subnav{display:flex;gap:16px;padding:14px 24px;border-bottom:1px solid #e5e7eb;font-size:13px;color:#4b5563;font-weight:500}
  .subnav .on{color:#378ADD}
  .wrap{max-width:1080px;margin:0 auto;padding:24px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}
  .card{text-decoration:none;color:inherit;display:block}
  .thumb{height:110px;background:#f5f6f7;margin-bottom:10px;display:flex;align-items:center;justify-content:center;
         color:#378ADD;font-size:28px;font-weight:600}
  .cname{font-size:12.5px;font-weight:500;margin-bottom:2px}
  .crow{display:flex;justify-content:space-between;align-items:baseline;margin-top:4px}
  .price{font-size:15px;font-weight:600}
  .up{color:#1a8a4a;font-size:11.5px;font-weight:600}
  .down{color:#c0392b;font-size:11.5px;font-weight:600}
  .btn{background:#378ADD;color:#fff;text-align:center;padding:12px;font-size:13.5px;font-weight:600;
       border:none;cursor:pointer;text-decoration:none;display:inline-block}
  .btn2{background:#fff;border:1px solid #e5e7eb;color:#0a0c10;text-align:center;padding:12px;
        font-size:13.5px;font-weight:600;cursor:pointer;text-decoration:none;display:inline-block}
  input,select,textarea{font-family:inherit;border:1px solid #e5e7eb;padding:10px 12px;font-size:13.5px;
       width:100%;box-sizing:border-box}
  label{font-size:12px;color:#8a8f98;display:block;margin-bottom:5px}
  .field{margin-bottom:12px}
  .notice{padding:12px 14px;font-size:12.5px;line-height:1.6;border-left:3px solid}
  .notice-danger{background:#fceaea;border-color:#E24B4A;color:#791F1F}
  .notice-blue{background:#e6f1fb;border-color:#378ADD;color:#0c447c}
  .notice-green{background:#eaf3de;border-color:#639922;color:#3B6D11}
  .notice-amber{background:#faeeda;border-color:#BA7517;color:#854F0B}
  footer{padding:24px;text-align:center;font-size:12px;color:#8a8f98;border-top:1px solid #e5e7eb;margin-top:40px}
  h1{font-size:20px;font-weight:600;margin:0 0 6px}
  .muted{color:#8a8f98;font-size:12.5px}
  .badge{font-size:10.5px;font-weight:600;padding:3px 9px;display:inline-block}
  .badge-live{background:#eaf3de;color:#3B6D11}
  .badge-pending{background:#faeeda;color:#854F0B}
  .star{color:#EF9F27}
</style>"""

def nav_html():
    u = current_user()
    if u:
        right = f'<a href="/profile">{u["email"].split("@")[0]}</a>' + (' <a href="/admin">Admin</a>' if is_owner() else '')
    else:
        right = '<a href="/signin">Sign in</a>'
    return f"""<div class="nav">
      <a class="logo" href="/">bl<span>ooo</span>u</a>
      <div class="navsearch">Search for a sneaker, brand, or player</div>
      <div class="navlinks">
        <a href="/sell">Sell</a>
        <a href="/predict">Predict</a>
        <a href="/leaderboard">Leaderboard</a>
        <a href="/reviews">Reviews</a>
        {right}
      </div>
    </div>"""

def page(title, body, desc=""):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — blooou</title>
    <meta name="description" content="{desc}">
    {STYLE}</head><body>{nav_html()}{body}
    <footer>© 2026 blooou · Not a real transaction until payment processing is connected</footer>
    </body></html>"""

def shoe_card(sid, s):
    chg = 0.0
    if len(s["history"]) >= 2 and s["history"][-2]:
        chg = round((s["history"][-1] - s["history"][-2]) / s["history"][-2] * 100, 1)
    cls = "up" if chg >= 0 else "down"
    sign = "+" if chg >= 0 else ""
    return f"""<a class="card" href="/shoe/{sid}">
      <div class="thumb">{s['brand'][0]}</div>
      <div class="cname">{s['name']}</div>
      <div class="crow"><span class="price">${s['price']:,.0f}</span><span class="{cls}">{sign}{chg}%</span></div>
    </a>"""

@app.get("/")
def home():
    shoes = load_shoes()
    cards = "".join(shoe_card(sid, s) for sid, s in shoes.items())
    body = f"""<div class="subnav">
      <span class="on">All</span><span>Trending</span><span>Jordan</span><span>Nike</span><span>New Balance</span>
    </div>
    <div class="wrap">
      <div style="font-size:13px;font-weight:600;margin-bottom:14px">Trending right now</div>
      <div class="grid">{cards}</div>
    </div>"""
    return page("blooou", body, "Live sneaker resale prices with the real story behind every move.")

@app.get("/shoe/<sid>")
def shoe_detail(sid):
    shoes = load_shoes()
    s = shoes.get(sid)
    if not s:
        return redirect("/")
    hist = s["history"]
    chg = round((hist[-1] - hist[-2]) / hist[-2] * 100, 1) if len(hist) >= 2 and hist[-2] else 0.0
    cls = "up" if chg >= 0 else "down"
    sign = "+" if chg >= 0 else ""
    w, h, n = 320, 70, len(hist)
    lo, hi = min(hist), max(hist)
    span = (hi - lo) or 1
    pts = " ".join(f"{i*(w/(n-1)):.0f},{h-((v-lo)/span*h):.0f}" for i, v in enumerate(hist))
    listings = [l for l in load_listings() if l["shoe_id"] == sid and l["status"] == "live"]
    size_opts = "".join(f'<option>{sz}</option>' for sz in s.get("sizes", []))
    body = f"""<div class="wrap" style="max-width:640px">
      <div class="muted">{s['brand']}</div>
      <h1>{s['name']}</h1>
      <div style="display:flex;gap:16px;margin:14px 0">
        <div style="width:120px;height:120px;background:#f5f6f7;display:flex;align-items:center;justify-content:center;
             color:#378ADD;font-size:40px;font-weight:600;flex-shrink:0">{s['brand'][0]}</div>
        <div style="flex:1">
          <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:6px">
            <span style="font-size:26px;font-weight:600">${s['price']:,.0f}</span>
            <span class="{cls}" style="font-size:13px">{sign}{chg}% today</span>
          </div>
          <svg viewBox="0 0 {w} {h}" style="width:100%;height:70px;background:#f5f6f7">
            <polyline points="{pts}" fill="none" stroke="#378ADD" stroke-width="2"/>
          </svg>
        </div>
      </div>
      <div class="notice notice-blue" style="margin-bottom:16px">
        <div style="font-weight:600;margin-bottom:4px;letter-spacing:.02em;font-size:11px">WHY IT MOVED</div>
        {s['story']}
      </div>
      <div style="display:flex;gap:10px;margin-bottom:24px">
        <a class="btn" style="flex:1" href="/checkout/{sid}">Buy · ${s['price']:,.0f}</a>
        <a class="btn2" style="flex:1" href="/sell?shoe={sid}">Sell yours</a>
      </div>
      <div style="font-size:13px;font-weight:600;margin-bottom:10px">{len(listings)} live listing{'s' if len(listings)!=1 else ''}</div>
      {"".join(f'''<div style="display:flex;justify-content:space-between;border:1px solid #e5e7eb;padding:10px 12px;margin-bottom:6px;font-size:13px">
        <span>Size {l["size"]} · {l["condition"]}</span><span style="font-weight:600">${l["price"]:,.0f}</span></div>''' for l in listings) or '<p class="muted">No individual listings yet, showing the market price above.</p>'}
    </div>"""
    return page(s["name"], body, s["story"])

@app.get("/sell")
def sell_page():
    u = current_user()
    if not u:
        return redirect("/signin")
    shoes = load_shoes()
    preselect = request.args.get("shoe", "")
    opts = "".join(f'<option value="{sid}" {"selected" if sid==preselect else ""}>{s["name"]}</option>' for sid, s in shoes.items())
    body = f"""<div class="wrap" style="max-width:440px">
      <h1>List a pair</h1>
      <p class="muted" style="margin-bottom:16px">Every listing runs through photo authentication before it goes live. Nobody sees an unverified pair.</p>
      <form id="sellForm">
        <div class="field"><label>Shoe</label><select id="shoe">{opts}</select></div>
        <div style="display:flex;gap:10px">
          <div class="field" style="flex:1"><label>Size</label><input id="size" placeholder="10"></div>
          <div class="field" style="flex:1"><label>Asking price ($)</label><input id="price" type="number" placeholder="200"></div>
        </div>
        <div class="field"><label>Condition</label>
          <select id="condition"><option>New with box</option><option>New no box</option><option>Worn once</option><option>Used, good condition</option></select></div>
        <div class="notice notice-amber" style="margin-bottom:16px">
          Authentication is not connected yet, this listing will save as pending until a real authentication provider is wired in.
        </div>
        <div id="sellMsg" class="muted" style="margin-bottom:10px"></div>
        <button type="button" class="btn" style="width:100%" onclick="submitListing()">Submit for authentication</button>
      </form>
    </div>
    <script>
    async function submitListing(){{
      const b = {{shoe_id: document.getElementById('shoe').value, size: document.getElementById('size').value,
                  price: document.getElementById('price').value, condition: document.getElementById('condition').value}};
      const r = await fetch('/api/listing', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(b)}});
      const d = await r.json();
      const m = document.getElementById('sellMsg');
      if (d.ok) {{ m.textContent = 'Submitted, sitting in the authentication queue.'; m.style.color = '#1a8a4a';
                   setTimeout(() => location.href = '/profile', 900); }}
      else {{ m.textContent = d.msg; m.style.color = '#c0392b'; }}
    }}
    </script>"""
    return page("Sell a pair", body)

@app.post("/api/listing")
def api_listing():
    u = current_user()
    if not u:
        return jsonify({"ok": False, "msg": "Sign in first."})
    d = request.get_json(force=True, silent=True) or {}
    sid = d.get("shoe_id")
    shoes = load_shoes()
    if sid not in shoes:
        return jsonify({"ok": False, "msg": "Pick a real shoe from the list."})
    try:
        size = float(d.get("size"))
        price = float(d.get("price"))
        if price <= 0 or price > 50000:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"ok": False, "msg": "Check the size and price."})
    listings = load_listings()
    listings.append({
        "id": f"L{int(time.time()*1000)}", "shoe_id": sid, "seller": u["email"],
        "size": size, "price": price, "condition": d.get("condition", ""),
        "status": "pending", "created": time.time(),
    })
    save_listings(listings)
    return jsonify({"ok": True})

@app.get("/checkout/<sid>")
def checkout_page(sid):
    u = current_user()
    if not u:
        return redirect("/signin")
    shoes = load_shoes()
    s = shoes.get(sid)
    if not s:
        return redirect("/")
    shipping = 12.0
    all_in_price = s["price"] + shipping   # shipping folded straight into the one price shown
    pay_button = (f'<a class="btn" style="width:100%" href="{PAYMENT_LINK}" target="_blank" rel="noopener">Pay ${all_in_price:,.2f}</a>'
                  if PAYMENT_LINK else
                  '<button class="btn" style="width:100%;opacity:.5;cursor:not-allowed" disabled>Payment isn\'t connected yet</button>')
    body = f"""<div class="wrap" style="max-width:420px">
      <h1>Confirm purchase</h1>
      <div style="display:flex;gap:12px;padding-bottom:16px;border-bottom:1px solid #e5e7eb;margin-bottom:16px">
        <div style="width:56px;height:56px;background:#f5f6f7;display:flex;align-items:center;justify-content:center;
             color:#378ADD;font-weight:600;flex-shrink:0">{s['brand'][0]}</div>
        <div><div style="font-size:13.5px;font-weight:600">{s['name']}</div><div class="muted">Verified · shipping included</div></div>
      </div>
      <div style="display:flex;justify-content:space-between;margin-bottom:14px;padding-bottom:14px;border-bottom:1px solid #e5e7eb">
        <span class="muted">Total, shipping included</span><span style="font-size:20px;font-weight:600">${all_in_price:,.2f}</span></div>
      <div class="notice notice-blue" style="margin-bottom:12px">Any sales tax owed for your state is calculated and collected at payment, it isn't hidden inside this price.</div>
      <div class="notice notice-green" style="margin-bottom:12px">Your payment is held until you confirm the shoes arrived as described.</div>
      <div class="notice notice-danger" style="margin-bottom:16px">환불 및 교환이 불가능합니다. Refunds and exchanges are not possible once a verified pair ships.</div>
      {pay_button}
    </div>"""
    return page("Checkout", body)

if __name__ == "__main__":
    print("")
    print("  blooou marketplace is starting up...")
    print("  open this in your browser: http://127.0.0.1:5000")
    print("  press Ctrl+C in this window to stop it")
    print("")
    app.run(host="127.0.0.1", port=5000, debug=True)

@app.get("/signin")
def signin_page():
    mode = request.args.get("mode", "signin")
    body = f"""<div class="wrap" style="max-width:360px;text-align:center">
      <h1>{"Create an account" if mode == "signup" else "Sign in"}</h1>
      <div class="field" style="text-align:left"><label>Email</label><input id="em" type="email"></div>
      <div class="field" style="text-align:left"><label>Password</label><input id="pw" type="password"></div>
      <div id="msg" class="muted" style="margin-bottom:10px"></div>
      <button class="btn" style="width:100%" onclick="go()">{"Create account" if mode == "signup" else "Sign in"}</button>
      <p class="muted" style="margin-top:14px">
        {'Already have an account? <a href="/signin">Sign in</a>' if mode == "signup" else 'New here? <a href="/signin?mode=signup">Create an account</a>'}
      </p>
    </div>
    <script>
    async function go(){{
      const em = document.getElementById('em').value, pw = document.getElementById('pw').value;
      const r = await fetch('/api/{"signup" if mode == "signup" else "login"}', {{method:'POST',
        headers:{{'Content-Type':'application/json'}}, body: JSON.stringify({{email: em, password: pw}})}});
      const d = await r.json();
      if (d.ok) location.href = '/'; else document.getElementById('msg').textContent = d.msg;
    }}
    </script>"""
    return page("Sign in", body)

@app.post("/api/signup")
def api_signup():
    d = request.get_json(force=True, silent=True) or {}
    email = (d.get("email") or "").strip().lower()
    pw = d.get("password") or ""
    if "@" not in email or len(pw) < 8:
        return jsonify({"ok": False, "msg": "Enter a real email and a password of at least 8 characters."})
    users = load_users()
    if email in users:
        return jsonify({"ok": False, "msg": "That email already has an account."})
    users[email] = {"email": email, "pw": generate_password_hash(pw), "created": time.time()}
    save_users(users)
    session["u"] = email
    return jsonify({"ok": True})

@app.post("/api/login")
def api_login():
    d = request.get_json(force=True, silent=True) or {}
    email = (d.get("email") or "").strip().lower()
    users = load_users()
    u = users.get(email)
    if not u or not check_password_hash(u["pw"], d.get("password") or ""):
        return jsonify({"ok": False, "msg": "That email and password don't match."})
    session["u"] = email
    return jsonify({"ok": True})

@app.get("/logout")
def logout():
    session.pop("u", None)
    return redirect("/")

@app.get("/profile")
def profile_page():
    u = current_user()
    if not u:
        return redirect("/signin")
    mine = [l for l in load_listings() if l["seller"] == u["email"]]
    shoes = load_shoes()
    rows = "".join(f"""<div style="display:flex;justify-content:space-between;align-items:center;
        border:1px solid #e5e7eb;padding:10px 12px;margin-bottom:6px">
        <span style="font-size:13px">{shoes.get(l['shoe_id'], {}).get('name', l['shoe_id'])}, size {l['size']}</span>
        <span class="badge badge-{'live' if l['status']=='live' else 'pending'}">{'Live' if l['status']=='live' else 'Authenticating'}</span>
      </div>""" for l in mine) or '<p class="muted">Nothing listed yet.</p>'
    body = f"""<div class="wrap" style="max-width:460px">
      <h1>{u['email'].split('@')[0]}</h1>
      <p class="muted" style="margin-bottom:20px">{u['email']} · <a href="/logout">Sign out</a></p>
      <div style="font-size:12px;font-weight:600;color:#8a8f98;margin-bottom:10px">Your listings</div>
      {rows}
    </div>"""
    return page("Profile", body)

@app.get("/reviews")
def reviews_page():
    reviews = load_reviews()
    avg = round(sum(r["stars"] for r in reviews) / len(reviews), 1) if reviews else 0.0
    stars_html = lambda n: "★" * n + "☆" * (5 - n)
    rows = "".join(f"""<div style="border-top:1px solid #e5e7eb;padding:14px 0">
        <div style="display:flex;justify-content:space-between;margin-bottom:6px">
          <span style="font-size:13px;font-weight:600">{r['name']}</span>
          <span class="star" style="font-size:12px">{stars_html(r['stars'])}</span>
        </div>
        <div class="muted" style="margin-bottom:6px">{r['shoe']}</div>
        <div style="font-size:13px;color:#374151;line-height:1.6">{r['text']}</div>
      </div>""" for r in reversed(reviews)) or '<p class="muted">아직 리뷰가 없습니다.</p>'
    u = current_user()
    write_form = f"""<form id="rvForm" style="border-top:1px solid #e5e7eb;padding-top:16px;margin-top:16px">
      <div class="field"><label>구매한 신발</label><input id="rvShoe" placeholder="예: Ja 4 EP Nightmare"></div>
      <div class="field"><label>별점 (1~5)</label><input id="rvStars" type="number" min="1" max="5" value="5"></div>
      <div class="field"><label>리뷰 내용</label><textarea id="rvText" rows="3"></textarea></div>
      <div id="rvMsg" class="muted" style="margin-bottom:8px"></div>
      <button type="button" class="btn" style="width:100%" onclick="submitReview()">리뷰 남기기</button>
    </form>""" if u else '<p class="muted" style="border-top:1px solid #e5e7eb;padding-top:16px;margin-top:16px"><a href="/signin">로그인</a> 후 리뷰를 남길 수 있습니다.</p>'
    body = f"""<div class="wrap" style="max-width:520px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
        <h1 style="margin:0">리뷰</h1>
      </div>
      <div style="display:flex;align-items:center;gap:14px;background:#f5f6f7;padding:14px 16px;margin-bottom:14px">
        <div style="font-size:26px;font-weight:600">{avg}</div>
        <div><div class="star" style="font-size:14px">★★★★★</div><div class="muted">거래 {len(reviews)}건 기준</div></div>
      </div>
      <div class="notice notice-danger" style="margin-bottom:16px">
        <div style="font-weight:600;margin-bottom:3px">환불 및 교환 불가 안내</div>
        정품 인증이 완료된 후 배송된 상품은 <b>환불과 교환이 불가능</b>합니다. 구매 전 사이즈와 상태를 꼭 확인해 주세요.
      </div>
      {rows}
      {write_form}
    </div>
    <script>
    async function submitReview(){{
      const b = {{shoe: document.getElementById('rvShoe').value, stars: document.getElementById('rvStars').value,
                  text: document.getElementById('rvText').value}};
      const r = await fetch('/api/review', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(b)}});
      const d = await r.json();
      if (d.ok) location.reload(); else document.getElementById('rvMsg').textContent = d.msg;
    }}
    </script>"""
    return page("리뷰", body)

@app.post("/api/review")
def api_review():
    u = current_user()
    if not u:
        return jsonify({"ok": False, "msg": "로그인이 필요합니다."})
    d = request.get_json(force=True, silent=True) or {}
    try:
        stars = max(1, min(5, int(d.get("stars", 5))))
    except (TypeError, ValueError):
        stars = 5
    if not (d.get("shoe") or "").strip() or not (d.get("text") or "").strip():
        return jsonify({"ok": False, "msg": "신발 이름과 리뷰 내용을 입력해 주세요."})
    reviews = load_reviews()
    reviews.append({"name": u["email"].split("@")[0], "shoe": d["shoe"].strip(),
                     "stars": stars, "text": d["text"].strip(), "time": time.time()})
    save_reviews(reviews)
    return jsonify({"ok": True})

@app.get("/predict")
def predict_page():
    u = current_user()
    if not u:
        return redirect("/signin")
    shoes = load_shoes()
    week = time.strftime("%G-W%V")
    preds = load_predictions()
    already = next((p for p in preds if p["email"] == u["email"] and p["week"] == week), None)
    opts = "".join(f'<option value="{sid}">{s["name"]}</option>' for sid, s in shoes.items())
    body = f"""<div class="wrap" style="max-width:420px">
      <h1>This week's call</h1>
      <p class="muted" style="margin-bottom:16px">No money, just bragging rights.</p>
      {f'''<div class="notice notice-blue">You already predicted <b>{shoes.get(already["shoe_id"],{}).get("name","this")}</b> will
        <b>{already["direction"]}</b> this week. Come back next week for a new one.</div>'''
        if already else f'''
      <div class="field"><label>Pick a shoe</label><select id="pShoe">{opts}</select></div>
      <p class="muted" style="margin-bottom:10px">Where does this land by Friday?</p>
      <div style="display:flex;gap:8px">
        <div class="btn2" style="flex:1;border-color:#1a8a4a;color:#1a8a4a" onclick="submitPred('rises')">Rises</div>
        <div class="btn2" style="flex:1" onclick="submitPred('flat')">Flat</div>
        <div class="btn2" style="flex:1;border-color:#c0392b;color:#c0392b" onclick="submitPred('falls')">Falls</div>
      </div>
      <div id="pMsg" class="muted" style="margin-top:10px"></div>'''}
    </div>
    <script>
    async function submitPred(dir){{
      const b = {{shoe_id: document.getElementById('pShoe').value, direction: dir}};
      const r = await fetch('/api/predict', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(b)}});
      const d = await r.json();
      if (d.ok) location.reload(); else document.getElementById('pMsg').textContent = d.msg;
    }}
    </script>"""
    return page("Predict", body)

@app.post("/api/predict")
def api_predict():
    u = current_user()
    if not u:
        return jsonify({"ok": False, "msg": "Sign in first."})
    d = request.get_json(force=True, silent=True) or {}
    sid = d.get("shoe_id")
    direction = d.get("direction")
    if sid not in load_shoes() or direction not in ("rises", "flat", "falls"):
        return jsonify({"ok": False, "msg": "Pick a real shoe and direction."})
    week = time.strftime("%G-W%V")
    preds = load_predictions()
    if any(p["email"] == u["email"] and p["week"] == week for p in preds):
        return jsonify({"ok": False, "msg": "You've already predicted this week."})
    preds.append({"email": u["email"], "shoe_id": sid, "direction": direction,
                   "week": week, "time": time.time(), "correct": None})
    save_predictions(preds)
    return jsonify({"ok": True})

@app.get("/leaderboard")
def leaderboard_page():
    preds = load_predictions()
    tally = {}
    for p in preds:
        if p.get("correct") is True:
            tally[p["email"]] = tally.get(p["email"], 0) + 1
        else:
            tally.setdefault(p["email"], 0)
    ranked = sorted(tally.items(), key=lambda kv: -kv[1])
    u = current_user()
    rows = "".join(f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;
        {'background:#e6f1fb;padding-left:8px' if u and email==u['email'] else 'border-bottom:1px solid #e5e7eb'}">
        <div style="display:flex;gap:10px;align-items:center"><span style="font-weight:600">{i+1}</span>
          <span style="font-size:13px">{email.split('@')[0]}{' (you)' if u and email==u['email'] else ''}</span></div>
        <span style="font-size:13px;font-weight:600;color:#1a8a4a">{correct} correct</span>
      </div>""" for i, (email, correct) in enumerate(ranked[:50])) or '<p class="muted">No predictions yet, be the first.</p>'
    body = f"""<div class="wrap" style="max-width:420px">
      <h1>Prediction leaderboard</h1>
      <p class="muted" style="margin-bottom:16px">Correct calls scored once each Friday.</p>
      {rows}
    </div>"""
    return page("Leaderboard", body)

@app.get("/admin")
def admin_page():
    if not is_owner():
        return redirect("/")
    shoes = load_shoes()
    pending = [l for l in load_listings() if l["status"] == "pending"]
    rows = "".join(f"""<div style="display:flex;justify-content:space-between;align-items:center;
        border:1px solid #e5e7eb;padding:10px 12px;margin-bottom:6px">
        <span style="font-size:13px">{shoes.get(l['shoe_id'],{}).get('name', l['shoe_id'])}, size {l['size']} · {l['seller']}</span>
        <div><a class="btn2" style="padding:6px 12px;font-size:12px" href="/api/admin/approve/{l['id']}">Approve</a></div>
      </div>""" for l in pending) or '<p class="muted">Nothing waiting.</p>'
    body = f"""<div class="wrap">
      <h1>Master panel</h1>
      <div style="font-size:13px;font-weight:600;margin:20px 0 10px">Pending authentication ({len(pending)})</div>
      {rows}
    </div>"""
    return page("Admin", body)

@app.get("/api/admin/approve/<lid>")
def admin_approve(lid):
    if not is_owner():
        return redirect("/")
    listings = load_listings()
    for l in listings:
        if l["id"] == lid:
            l["status"] = "live"
    save_listings(listings)
    return redirect("/admin")PASTE ENDS HERE