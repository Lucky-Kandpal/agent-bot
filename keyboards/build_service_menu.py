from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# ------ UI Keyboard ------
def build_service_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Image", callback_data="svc_image"), InlineKeyboardButton("📹 Video", callback_data="svc_video")],
        [InlineKeyboardButton("🎧 Clean Audio", callback_data="svc_clean_audio"), InlineKeyboardButton("🎬 Clean Video", callback_data="svc_clean_video")],
        [InlineKeyboardButton("💬 Chat (free)", callback_data="svc_chat"), InlineKeyboardButton("❓ Help", callback_data="svc_help")]
    ])