from telegram import Update
from telegram.ext import ContextTypes
from env_config import logger
from memory_storage.all import create_or_update_user
from keyboards.build_service_menu import build_service_menu


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    create_or_update_user(user)
    logger.info(f"/help by {user.id}")
    
    help_text = (
        "🤖 *100Viral Bot Help*\n\n"
        "*Available Services:*\n"
        "• 🖼 *Image Generation* - Create images from text descriptions\n"
        "• 📹 *Video Generation* - Create short videos from text prompts\n"
        "• 🎧 *Audio Cleaning* - Enhance and clean audio files\n"
        "• 🎬 *Video Cleaning* - Enhance and clean video files\n"
        "• 💬 *Chat* - Ask questions or get help (Free)\n\n"
        "*Commands:*\n"
        "• /start - Show main menu\n"
        "• /help - Show this help message\n\n"
        "You can also just type your request and I'll try to understand what you need!"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown", reply_markup=build_service_menu())

