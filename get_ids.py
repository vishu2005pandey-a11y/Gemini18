"""
Run this script to find your Channel ID and Group ID.

Steps:
1. Add your bot as ADMIN to your channel AND group
2. Send any message in both the channel and group
3. Run: .\venv\Scripts\python get_ids.py
4. Copy the IDs shown and paste into .env
"""
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    from aiogram import Bot
    token = os.getenv("BOT_TOKEN", "")
    if not token:
        print("ERROR: BOT_TOKEN not set in .env")
        return

    bot = Bot(token=token)
    try:
        me = await bot.get_me()
        print(f"\n✅ Bot: @{me.username} (ID: {me.id})")
        print("\n📋 Getting updates to find chat IDs...")
        print("   Make sure you sent a message in your channel AND group recently.\n")

        updates = await bot.get_updates(limit=50)
        found = {}
        for u in updates:
            chat = None
            if u.message:
                chat = u.message.chat
            elif u.channel_post:
                chat = u.channel_post.chat

            if chat and chat.id not in found:
                found[chat.id] = chat

        if not found:
            print("❌ No updates found.")
            print("   → Send a message in your channel and group, then run this again.")
        else:
            print("Found these chats:\n")
            for chat_id, chat in found.items():
                ctype = chat.type
                title = getattr(chat, 'title', None) or getattr(chat, 'username', str(chat_id))
                print(f"  {'📢 Channel' if ctype == 'channel' else '💬 Group/Chat'}: {title}")
                print(f"  ID: {chat_id}")
                print(f"  Type: {ctype}")
                print()

        print("\n💡 Paste the correct IDs into your .env file:")
        print("   CHANNEL_ID=-100xxxxxxxxxx")
        print("   GROUP_ID=-100xxxxxxxxxx")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.session.close()

asyncio.run(main())
