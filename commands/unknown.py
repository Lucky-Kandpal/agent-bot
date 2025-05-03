from telegram import Update
from telegram.ext import ContextTypes
from env_config import logger
from keyboards.build_service_menu import build_service_menu



async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles any command that doesn't match the registered handlers."""
    logger.warning(f"Received unknown command from user {update.effective_user.id}")
    await update.message.reply_text(
        "I don't recognize that command. Try /help to see what I can do.",
        reply_markup=build_service_menu()
    )
