"""
Send a message with premium emojis to your log group,
then run this script to get the entity IDs.

Usage:
  .\venv\Scripts\python get_emoji_ids.py
"""
import asyncio
from dotenv import load_dotenv
import os, json

load_dotenv()

async def main():
    from aiogram import Bot
    token = os.getenv("BOT_TOKEN", "")
    bot = Bot(token=token)

    try:
        me = await bot.get_me()
        print(f"Bot: @{me.username}\n")

        updates = await bot.get_updates(limit=10)
        for u in updates:
            msg = u.message
            if not msg:
                continue
            if msg.entities:
                for ent in msg.entities:
                    if hasattr(ent, 'custom_emoji_id') and ent.custom_emoji_id:
                        print(f"Custom Emoji ID: {ent.custom_emoji_id}")
                        print(f"  Offset: {ent.offset}, Length: {ent.length}")
                        print(f"  Text:   {msg.text[ent.offset:ent.offset+ent.length]}\n")
    finally:
        await bot.session.close()

asyncio.run(main())
