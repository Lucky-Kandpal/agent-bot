

from telegram import Update
from telegram.ext import ContextTypes
# from db import create_or_update_user
from env_config import logger
from keyboards.build_service_menu import build_service_menu
# ------ Handlers ------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    # create_or_update_user(user)
    logger.info(f"/start by {user.id}")
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋\n\nI'm ViralBoost, your media enhancement assistant. I can help you generate images, videos, and clean up audio/video files.\n\nUse the menu below or just tell me what you'd like to do:",
        reply_markup=build_service_menu()
    )