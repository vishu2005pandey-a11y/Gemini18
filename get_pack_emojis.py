"""
Get ALL emoji IDs from a custom emoji pack.
Usage: .\\venv\\Scripts\\python get_pack_emojis.py
"""
import asyncio
from dotenv import load_dotenv
import os, json

load_dotenv()

# Paste your custom_emoji_id from the forwarded sticker here
KNOWN_EMOJI_ID = "6053315100117309042"  # from getmodpc pack

async def main():
    from aiogram import Bot
    token = os.getenv("BOT_TOKEN", "")
    bot = Bot(token=token)

    try:
        print("Fetching emoji pack...\n")

        # Get the sticker set using custom emoji ID
        stickers = await bot.get_custom_emoji_stickers([KNOWN_EMOJI_ID])
        if not stickers:
            print("No stickers found.")
            return

        sticker = stickers[0]
        set_name = sticker.set_name
        print(f"Pack name: {set_name}")
        print(f"Fetching full pack...\n")

        # Get full sticker set
        pack = await bot.get_sticker_set(set_name)
        print(f"Pack: {pack.name}")
        print(f"Title: {pack.title}")
        print(f"Total stickers: {len(pack.stickers)}\n")
        print("=" * 60)
        print(f"{'Emoji':<10} {'Custom Emoji ID':<25} {'Format'}")
        print("=" * 60)

        results = {}
        for s in pack.stickers:
            cid = s.custom_emoji_id or "N/A"
            emoji = s.emoji or "?"
            print(f"{emoji:<10} {cid:<25}")
            results[emoji] = cid

        # Save to file
        with open("emoji_ids.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 60)
        print(f"Saved {len(results)} emoji IDs to emoji_ids.json")
        print("\nCopy-paste format for locales/en.py:")
        print("-" * 60)
        for emoji, cid in results.items():
            varname = f"E_{emoji}"
            print(f'_e("{cid}", "{emoji}")')

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await bot.session.close()

asyncio.run(main())
