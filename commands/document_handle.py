from memory_storage.all import users
from memory_storage.all import processing_users, create_or_update_user, is_busy
from env_config import logger
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.build_service_menu import build_service_menu
from commands.handle_media import handle_media



async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for document files (PDF, JSON, etc.)"""
    user = update.message.from_user
    uid = user.id
    logger.info(f"Document from {uid}")
    
    if uid in processing_users or await is_busy(uid):
        return await update.message.reply_text("⏳ Please wait, I'm still processing your previous request...")
    
    create_or_update_user(user)
    doc = update.message.document
    
    if not doc:
        return
    
    mime_type = doc.mime_type if hasattr(doc, 'mime_type') else "unknown"
    
    # Handle unsupported file types with friendly message
    if mime_type in ['application/pdf', 'application/json', 'text/plain', 'application/msword',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        file_type = mime_type.split('/')[-1].upper()
        
        return await update.message.reply_text(
            f"I notice you've uploaded a {file_type} file. Currently, I can't process this file type for enhancement.\n\n"
            f"Here's what I can do for you instead:\n"
            f"• Generate images from text descriptions\n"
            f"• Generate videos from text prompts\n"
            f"• Clean and enhance audio files\n"
            f"• Clean and enhance video files\n"
            f"• Answer your questions via chat (free)\n\n"
            f"Would you like to try one of these services instead?",
            reply_markup=build_service_menu()
        )
    
    # For other document types, let the media handler try to process it
    # This handles audio/video files sent as documents
    await handle_media(update, context)
