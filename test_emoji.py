"""
Test premium emoji rendering.
Run: .\\venv\\Scripts\\python test_emoji.py
"""
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    from aiogram import Bot
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    token = os.getenv("BOT_TOKEN", "")
    admin_ids = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        me = await bot.get_me()
        print(f"Bot: @{me.username}")
        print(f"Sending test to admin: {admin_ids[0]}")

        # Test 1 — plain tg-emoji tag
        msg1 = (
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>🧪 EMOJI TEST</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Test 1 — getmodpc IDs:</b>\n"
            '<tg-emoji emoji-id="6053061091456457277">⚡️</tg-emoji> Lightning\n'
            '<tg-emoji emoji-id="6053163053980063912">🔥</tg-emoji> Fire\n'
            '<tg-emoji emoji-id="6053314026375485069">💎</tg-emoji> Diamond\n'
            '<tg-emoji emoji-id="6052941558221642149">👑</tg-emoji> Crown\n'
            '<tg-emoji emoji-id="6053189188856059704">✅</tg-emoji> Check\n'
            '<tg-emoji emoji-id="6052869226677410910">❌</tg-emoji> Cross\n'
            '<tg-emoji emoji-id="6053315100117309042">⚠️</tg-emoji> Warning\n'
            '<tg-emoji emoji-id="6053030296540946080">🎉</tg-emoji> Party\n\n'
            "<b>If animated = Premium emoji working ✅</b>\n"
            "<b>If static = IDs need fix ❌</b>"
        )

        await bot.send_message(admin_ids[0], msg1, parse_mode="HTML")
        print("✅ Test message sent! Check your Telegram.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await bot.session.close()

asyncio.run(main())
