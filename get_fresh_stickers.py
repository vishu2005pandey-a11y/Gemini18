"""
Get FRESH file_ids for getmodpc stickers valid for THIS bot.
Step 1: Run this script — it sends you a menu
Step 2: Forward any sticker from @getmodpc pack to this bot in private
Step 3: Bot will print the fresh file_id
"""
import asyncio
from dotenv import load_dotenv
import os, json
load_dotenv()

PACK_NAME = "getmodpc"

async def main():
    from aiogram import Bot
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    bot = Bot(token=os.getenv("BOT_TOKEN"),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    admin_id = int(os.getenv("ADMIN_IDS","").split(",")[0])

    try:
        me = await bot.get_me()
        print(f"Bot: @{me.username}")

        # Get sticker set directly
        print(f"\nFetching pack '{PACK_NAME}'...")
        pack = await bot.get_sticker_set(PACK_NAME)
        print(f"Pack: {pack.title} — {len(pack.stickers)} stickers")

        # Send first 10 stickers to admin to get fresh file_ids
        print("\nSending stickers to your Telegram...")
        fresh = {}

        # Send all unique emoji stickers (skip duplicates)
        seen_emojis = set()
        sent = 0
        for s in pack.stickers:
            if s.emoji in seen_emojis:
                continue
            if s.emoji in ["📱"]:  # skip phone duplicates
                continue
            seen_emojis.add(s.emoji)
            try:
                msg = await bot.send_sticker(admin_id, s.file_id)
                fresh[s.emoji] = {
                    "file_id": msg.sticker.file_id,
                    "custom_emoji_id": s.custom_emoji_id,
                    "emoji": s.emoji
                }
                print(f"✅ {s.emoji} — {s.custom_emoji_id}")
                sent += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"❌ {s.emoji}: {e}")

        # Save fresh IDs
        with open("fresh_stickers.json", "w", encoding="utf-8") as f:
            json.dump(fresh, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Done! {sent} stickers sent & saved to fresh_stickers.json")
        print("Check Telegram — animated stickers should be playing!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback; traceback.print_exc()
    finally:
        await bot.session.close()

asyncio.run(main())
