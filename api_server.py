"""
Alpha Bot — Mini App REST API Server
Run alongside main.py using: python api_server.py
The Mini App (Next.js) calls this to get product, orders, wallet data.
"""
import asyncio
import logging
import json
import uuid
from aiohttp import web
import database as db
from config import PRODUCT_NAME, LINKS_SOLD_COUNTER_BASE, PAYMENT_TIMEOUT_MINUTES
import payments

log = logging.getLogger(__name__)


# ── Handlers ──────────────────────────────────────────────────────────────────

async def products_handler(request: web.Request) -> web.Response:
    products = await db.get_products()
    result = []
    from config import LINKS_SOLD_COUNTER_BASE
    sold_db = await db.get_total_links_sold()
    sold = LINKS_SOLD_COUNTER_BASE + sold_db
    avg_rating, review_count = await db.get_avg_rating()
    for p in products:
        stock = await db.get_stock_count(p["id"])
        result.append({
            "id": p["id"],
            "name": p["name"],
            "description": p["description"],
            "price": p["price"],
            "image_url": p["image_url"],
            "stock": stock,
            "sold": sold,
            "rating": avg_rating if avg_rating else 4.8,
            "reviews": review_count
        })
    return web.json_response(result)


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
        links = await db.get_order_links(o["order_id"])
        result.append({
            "order_id":   o["order_id"],
            "quantity":   o["quantity"],
            "amount_usd": o["amount_usd"],
            "currency":   o["currency"],
            "status":     o["status"],
            "paid_at":    o["paid_at"],
            "links":      links,
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
    badge = db.compute_badge(stats["links"])

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


async def leaderboard_handler(request: web.Request) -> web.Response:
    period = request.rel_url.query.get("period", "alltime")
    if period not in ("weekly", "monthly", "alltime"):
        period = "alltime"
    rows = await db.get_leaderboard(period=period, limit=10)
    return web.json_response(rows)


async def reviews_handler(request: web.Request) -> web.Response:
    rows = await db.get_reviews(limit=20)
    result = []
    for r in rows:
        result.append({
            "id":         r["id"],
            "user_id":    r["user_id"],
            "order_id":   r["order_id"],
            "rating":     r["rating"],
            "comment":    r["comment"],
            "created_at": r["created_at"],
            "username":   r["username"],
        })
    return web.json_response(result)


async def create_order_handler(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"error": "invalid json"}, status=400)

    user_id = body.get("user_id")
    product_id = body.get("product_id", 1)
    qty = body.get("qty", 1)

    if not user_id:
        return web.json_response({"error": "missing user_id"}, status=400)

    try:
        uid = int(user_id)
        product_id = int(product_id)
        qty = int(qty)
        if qty < 1:
            raise ValueError
    except (ValueError, TypeError):
        return web.json_response({"error": "invalid parameters"}, status=400)

    # Check stock
    stock = await db.get_stock_count(product_id)
    if stock < qty:
        return web.json_response({"error": "insufficient_stock", "available": stock}, status=409)

    product = await db.get_product(product_id)
    if not product:
        return web.json_response({"error": "invalid_product"}, status=404)
    price = product["price"]
    amount = round(price * qty, 2)
    order_id = payments.generate_order_id()

    # Create Cryptomus invoice
    invoice = await payments.create_invoice(
        order_id=order_id,
        amount_usd=amount,
        lifetime=PAYMENT_TIMEOUT_MINUTES * 60,
    )

    if not invoice:
        return web.json_response({"error": "payment_provider_unavailable"}, status=503)

    payment_uuid = invoice.get("uuid", "")
    address = invoice.get("address", "")
    crypto_amount = float(invoice.get("amount", 0) or 0)
    currency = invoice.get("currency", "USDT")
    payment_url = invoice.get("url", "")

    # Save order to DB
    await db.create_order(
        order_id=order_id,
        user_id=uid,
        product_id=product_id,
        qty=qty,
        amount_usd=amount,
        payment_id=payment_uuid,
        address=address,
        crypto_amount=crypto_amount,
        currency=currency,
    )

    return web.json_response({
        "order_id":      order_id,
        "address":       address,
        "crypto_amount": crypto_amount,
        "currency":      currency,
        "payment_url":   payment_url,
        "timeout":       PAYMENT_TIMEOUT_MINUTES * 60,
        "amount_usd":    amount,
    })


async def check_payment_handler(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"error": "invalid json"}, status=400)

    order_id = body.get("order_id")
    if not order_id:
        return web.json_response({"error": "missing order_id"}, status=400)

    order = await db.get_order(order_id)
    if not order:
        return web.json_response({"error": "order not found"}, status=404)

    # Already paid — return links
    if order["status"] == "paid":
        links = await db.get_order_links(order_id)
        return web.json_response({"status": "paid", "links": links})

    if order["status"] in ("expired", "cancelled"):
        return web.json_response({"status": order["status"], "links": []})

    # Check with Cryptomus
    payment_uuid = order["payment_id"]
    if not payment_uuid:
        return web.json_response({"status": "pending", "links": []})

    result = await payments.check_payment(payment_uuid)
    if not result:
        return web.json_response({"status": "pending", "links": []})

    payment_status = result.get("payment_status", "")

    if payments.is_payment_confirmed(payment_status):
        # Pop links and mark paid
        links = await db.pop_links(order["product_id"], order["quantity"])
        if not links:
            log.error("Out of stock when fulfilling order %s", order_id)
            return web.json_response({"status": "paid", "links": []})
        await db.mark_order_paid(order_id, links)

        # Reward referral
        reward = await db.get_referral_reward()
        await db.reward_referral(order["user_id"], reward)

        return web.json_response({"status": "paid", "links": links})

    return web.json_response({"status": "pending", "links": []})


async def cancel_order_handler(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"error": "invalid json"}, status=400)

    order_id = body.get("order_id")
    if not order_id:
        return web.json_response({"error": "missing order_id"}, status=400)

    order = await db.get_order(order_id)
    if not order:
        return web.json_response({"error": "not found"}, status=404)

    if order["status"] != "pending":
        return web.json_response({"error": "cannot_cancel", "status": order["status"]}, status=400)

    await db.mark_order_cancelled(order_id)
    return web.json_response({"ok": True})


async def add_review_handler(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"error": "invalid json"}, status=400)

    user_id = body.get("user_id")
    order_id = body.get("order_id")
    rating = body.get("rating")
    comment = body.get("comment", "")

    if not all([user_id, order_id, rating]):
        return web.json_response({"error": "missing fields"}, status=400)

    try:
        uid = int(user_id)
        r = int(rating)
        if not (1 <= r <= 5):
            raise ValueError
    except (ValueError, TypeError):
        return web.json_response({"error": "invalid"}, status=400)

    already = await db.has_reviewed_order(order_id)
    if already:
        return web.json_response({"error": "already_reviewed"}, status=409)

    await db.add_review(uid, order_id, r, comment)
    return web.json_response({"ok": True})


# ── CORS middleware ────────────────────────────────────────────────────────────
@web.middleware
async def cors_middleware(request: web.Request, handler):
    if request.method == "OPTIONS":
        resp = web.Response()
    else:
        try:
            resp = await handler(request)
        except Exception as e:
            log.exception("Unhandled error: %s", e)
            resp = web.json_response({"error": "internal_server_error"}, status=500)
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp


async def init_app() -> web.Application:
    await db.get_db()
    app = web.Application(middlewares=[cors_middleware])
    app.router.add_get("/products",      products_handler)
    app.router.add_get("/orders",        orders_handler)
    app.router.add_get("/wallet",        wallet_handler)
    app.router.add_get("/user",          user_handler)
    app.router.add_get("/referral",      referral_handler)
    app.router.add_get("/leaderboard",   leaderboard_handler)
    app.router.add_get("/reviews",       reviews_handler)
    app.router.add_post("/create_order", create_order_handler)
    app.router.add_post("/check_payment", check_payment_handler)
    app.router.add_post("/cancel_order", cancel_order_handler)
    app.router.add_post("/add_review",   add_review_handler)
    # OPTIONS pre-flight for all routes
    app.router.add_route("OPTIONS", "/{path_info:.*}", lambda r: web.Response())
    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log.info("Starting API server on http://0.0.0.0:8080")

    async def _main():
        app = await init_app()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()
        log.info("API server running on http://0.0.0.0:8080")
        # Run forever
        try:
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()

    asyncio.run(_main())
