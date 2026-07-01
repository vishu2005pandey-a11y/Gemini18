"""Test animated sticker sending."""
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

async def main():
    from aiogram import Bot
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    bot = Bot(token=os.getenv("BOT_TOKEN"),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    admin_id = int(os.getenv("ADMIN_IDS","").split(",")[0])

    try:
        # Send animated sticker from getmodpc pack
        stickers = {
            "⚡️ Lightning": "CAACAgUAAxUAAWpEg1lL8nXQ_VNzmf981BNPQWONAAI9GgAC_soAAVRVttG-9nuHsTwE",
            "💸 Money":     "CAACAgUAAxUAAWpEg2d_rzPXHaZuVDA3ebBZkOi6AAL0FwACKYMAAVQ7cAXVa9ImMzwE",
            "⚠️ Warning":   "CAACAgUAAxUAAWpEg2DiI8YgnaBfOI26ynTvMlB6AAJyFgACA7IBVKDLaTcrznIgPAQ",
            "🛍 Shop":      "CAACAgUAAxUAAWpEg2N_fXFQ0FH7g7bCOzTmAAGRFwACFxsAAlpe-VcvDzPx5aBXdTwE",
            "🚫 Ban":       "CAACAgUAAxUAAWpEg2ERmHFSsK6Sa9Mqn8rya3yOAALIGgACMzsAAVR4_JESyKduPDwE",
        }

        for name, file_id in stickers.items():
            try:
                await bot.send_sticker(admin_id, file_id)
                print(f"✅ Sent: {name}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed {name}: {e}")

        print("\nCheck Telegram — animated stickers should appear!")
    finally:
        await bot.session.close()

asyncio.run(main())
