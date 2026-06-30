"""
Alpha Bot — Mini App REST API Server
Run alongside main.py using: python api_server.py
The Mini App (Next.js) calls this to get product, orders, wallet data.
"""
import asyncio
import logging
from aiohttp import web
import database as db
from config import PRODUCT_NAME, LINKS_SOLD_COUNTER_BASE

log = logging.getLogger(__name__)


async def product_handler(request: web.Request) -> web.Response:
    price = await db.get_price()
    stock = await db.get_stock_count()
    sold_db = await db.get_total_links_sold()
    sold = LINKS_SOLD_COUNTER_BASE + sold_db
    avg_rating, review_count = await db.get_avg_rating()

    return web.json_response({
        "name": PRODUCT_NAME,
        "price": price,
        "stock": stock,
        "sold": sold,
        "rating": avg_rating or 4.8,
        "reviews": review_count,
        "description": "Premium Gemini AI Pro access for 18 months via instant redemption link.",
    })


async def orders_handler(request: web.Request) -> web.Response:
    user_id = request.rel_url.query.get("user_id")
    if not user_id:
        return web.json_response([])
    try:
        uid = int(user_id)
    except ValueError:
        return web.json_response([])

    orders = await db.get_user_orders(uid)
    result = []
    for o in orders:
        result.append({
            "order_id":   o["order_id"],
            "quantity":   o["quantity"],
            "amount_usd": o["amount_usd"],
            "currency":   o["currency"],
            "status":     o["status"],
            "paid_at":    o["paid_at"],
        })
    return web.json_response(result)


async def wallet_handler(request: web.Request) -> web.Response:
    user_id = request.rel_url.query.get("user_id")
    if not user_id:
        return web.json_response({"balance": 0, "deposits": []})
    try:
        uid = int(user_id)
    except ValueError:
        return web.json_response({"balance": 0, "deposits": []})

    user = await db.get_user(uid)
    balance = user["referral_balance"] if user else 0.0
    return web.json_response({"balance": balance, "deposits": []})


async def user_handler(request: web.Request) -> web.Response:
    user_id = request.rel_url.query.get("user_id")
    if not user_id:
        return web.json_response({"error": "missing user_id"}, status=400)
    try:
        uid = int(user_id)
    except ValueError:
        return web.json_response({"error": "invalid"}, status=400)

    user = await db.get_user(uid)
    if not user:
        return web.json_response({"error": "not found"}, status=404)

    stats = await db.get_user_stats(uid)
    from database import compute_badge
    badge = compute_badge(stats["links"])

    return web.json_response({
        "user_id":          user["user_id"],
        "username":         user["username"],
        "first_name":       user["first_name"],
        "join_date":        user["join_date"],
        "language":         user["language"],
        "badge":            badge,
        "total_orders":     stats["orders"],
        "links_bought":     stats["links"],
        "total_spent":      stats["spent"],
        "referral_balance": user["referral_balance"],
    })


async def referral_handler(request: web.Request) -> web.Response:
    user_id = request.rel_url.query.get("user_id")
    if not user_id:
        return web.json_response({})
    try:
        uid = int(user_id)
    except ValueError:
        return web.json_response({})

    stats = await db.get_referral_stats(uid)
    return web.json_response(stats)


# ── CORS middleware ────────────────────────────────────────────────────────────
@web.middleware
async def cors_middleware(request: web.Request, handler):
    if request.method == "OPTIONS":
        resp = web.Response()
    else:
        resp = await handler(request)
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp


async def init_app() -> web.Application:
    await db.get_db()
    app = web.Application(middlewares=[cors_middleware])
    app.router.add_get("/product",  product_handler)
    app.router.add_get("/orders",   orders_handler)
    app.router.add_get("/wallet",   wallet_handler)
    app.router.add_get("/user",     user_handler)
    app.router.add_get("/referral", referral_handler)
    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log.info("Starting API server on http://0.0.0.0:8080")
    app = asyncio.get_event_loop().run_until_complete(init_app())
    web.run_app(app, host="0.0.0.0", port=8080)
