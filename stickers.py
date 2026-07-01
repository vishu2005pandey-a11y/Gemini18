"""
Alpha Bot — Animated sticker file_ids from getmodpc pack.
These are sent as actual animated stickers before key messages.
"""

# getmodpc pack stickers — file_ids for direct sending
STICKERS = {
    "welcome":   "CAACAgUAAxUAAWpEg1lL8nXQ_VNzmf981BNPQWONAAI9GgAC_soAAVRVttG-9nuHsTwE",  # ⚡️
    "success":   "CAACAgUAAxUAAWpEg2N_fXFQ0FH7g7bCOzTmAAGRFwACFxsAAlpe-VcvDzPx5aBXdTwE",  # 🛍
    "warning":   "CAACAgUAAxUAAWpEg2DiI8YgnaBfOI26ynTvMlB6AAJyFgACA7IBVKDLaTcrznIgPAQ",   # ⚠️
    "money":     "CAACAgUAAxUAAWpEg2d_rzPXHaZuVDA3ebBZkOi6AAL0FwACKYMAAVQ7cAXVa9ImMzwE",  # 💸
    "ban":       "CAACAgUAAxUAAWpEg2ERmHFSsK6Sa9Mqn8rya3yOAALIGgACMzsAAVR4_JESyKduPDwE",  # 🚫
}

async def send_sticker(bot, chat_id: int, sticker_key: str):
    """Send an animated sticker. Silently fails if sticker unavailable."""
    file_id = STICKERS.get(sticker_key)
    if not file_id:
        return
    try:
        await bot.send_sticker(chat_id, file_id)
    except Exception:
        pass  # Never break the flow for a sticker
