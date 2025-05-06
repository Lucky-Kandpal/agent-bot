from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from env_config import logger
import tempfile
import subprocess
import os
import io

async def convert_video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video format conversion menu"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🎬 GIF", callback_data="convert_to_gif"),
            InlineKeyboardButton("📹 MP4", callback_data="convert_to_mp4"),
            InlineKeyboardButton("🎥 WebM", callback_data="convert_to_webm"),
        ],
        [
            InlineKeyboardButton("🔄 Compress", callback_data="compress_video"),
            InlineKeyboardButton("✨ Enhance", callback_data="enhance_video"),
        ],
        [InlineKeyboardButton("↩️ Back", callback_data="svc_back")]
    ]
    
    await query.message.edit_text(
        "🎥 *Choose Video Operation:*\n\n"
        "• *Convert to GIF*: Create animated GIF\n"
        "• *Convert to MP4*: Best compatibility\n"
        "• *Convert to WebM*: Better compression\n"
        "• *Compress*: Reduce file size\n"
        "• *Enhance*: Improve quality\n\n"
        "💡 You can also use commands like:\n"
        "- `turn into gif`\n"
        "- `convert to mp4`\n"
        "- `make it smaller`",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Import in app.py:
# from commands.video_handlers import convert_video_handler