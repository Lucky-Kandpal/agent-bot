from memory_storage.all import users, processing_users
from memory_storage.all import create_or_update_user, is_busy
from env_config import logger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.build_service_menu import build_service_menu


async def menu_route(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    user = q.from_user
    data = q.data
    await q.answer()
    
    create_or_update_user(user)
    logger.info(f"Callback '{data}' by {user.id}")
    
    # Check if user is busy with another task
    if user.id in processing_users or await is_busy(user.id):
        await q.message.reply_text("⏳ I'm still processing your previous request. Please wait until it completes.")
        return
    
    if data == 'svc_back':
        return await q.edit_message_text(
            "Main Menu - Select a service or just ask me what you need:",
            reply_markup=build_service_menu()
        )
    
    if data == 'svc_help':
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
            "• /help - Show this help message"
        )
        return await q.edit_message_text(help_text, parse_mode="Markdown", reply_markup=build_service_menu())
    
    if data == 'svc_chat':
        context.user_data['svc'] = 'chat'
        return await q.edit_message_text(
            "💬 *Chat Mode Activated*\n\nYou can now chat with me for free. Ask me anything!",
            parse_mode="Markdown"
        )
    
    svc = data.replace('svc_', '')
    context.user_data['svc'] = svc
    
    prompts = {
        'image': '🖼 *Image Generation*\n\nSend a text prompt describing the image you want to create.',
        'video': '📹 *Video Generation*\n\nSend a text prompt describing the video you want to create.',
        'clean_audio': '🎧 *Audio Cleaning*\n\nUpload an audio file or voice message to enhance.',
        'clean_video': '🎬 *Video Cleaning*\n\nUpload a video file to enhance.'
    }
    
    # Add a back button
    keyboard = [[InlineKeyboardButton("↩️ Back to Menu", callback_data="svc_back")]]
    
    return await q.edit_message_text(
        prompts.get(svc, 'Select an option.'), 
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
