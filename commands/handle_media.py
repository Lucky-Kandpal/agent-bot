
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from env_config import logger
from memory_storage.all import users, processing_users
from memory_storage.all import create_or_update_user, is_busy, set_busy
from keyboards.build_service_menu import build_service_menu
from env_config import EXTERNAL_APIS
from memory_storage.all import  processing_users, create_or_update_user, is_busy
import logging



logger = logging.getLogger(__name__)

processing_users = set()

async def is_busy(uid): return False
def create_or_update_user(user): pass
def build_service_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="svc_back")]])

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    uid = user.id
    logger.info(f"Media received from user {uid}")

    if uid in processing_users or await is_busy(uid):
        return await update.message.reply_text(
            "⏳ Please wait, I'm still processing your previous request...",
            reply_to_message_id=update.message.message_id
        )
 
    create_or_update_user(user)
    processing_msg = await update.message.reply_text(
        "🔄 Receiving your file...",
        reply_to_message_id=update.message.message_id
    )

    # PHOTO
    if update.message.photo:
        photo = update.message.photo[-1]
        file_id = photo.file_id
        context.user_data['last_file_id'] = file_id
        context.user_data['last_mime'] = 'image/jpeg'
        context.user_data['last_file_name'] = "photo.jpg"

        kb = [
            [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
            [InlineKeyboardButton('⚙️ Convert Image', callback_data='svc_convert_img')],
            [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
        ]
        await processing_msg.delete()
        return await update.message.reply_text(
            f"What would you like to do with this image named *photo.jpg*?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb),
            reply_to_message_id=update.message.message_id
        )

    # DOCUMENT
    if update.message.document:
        doc = update.message.document
        mime = doc.mime_type or ''
        file_name = doc.file_name or 'unnamed'
        file_id = doc.file_id

        context.user_data['last_file_id'] = file_id
        context.user_data['last_mime'] = mime
        context.user_data['last_file_name'] = file_name

        logger.info(f"Document received: {file_name} ({mime})")

        if mime.startswith('image/'):
            kb = [
                [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
                [InlineKeyboardButton('⚙️ Convert Image', callback_data='svc_convert_img')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            prompt = f"What would you like to do with this image file named *{file_name}*?"

        elif mime.startswith('audio/'):
            kb = [
                [InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            prompt = f"What would you like to do with this audio file named *{file_name}*?"

        elif mime.startswith('video/'):
            kb = [
                [InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            prompt = f"What would you like to do with this video file named *{file_name}*?"

        elif mime == 'application/json':
            kb = [
                [InlineKeyboardButton('🔎 Process JSON', callback_data='svc_process_json')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            prompt = f"What would you like to do with this JSON file named *{file_name}*?"

        elif mime == 'application/pdf':
            kb = [
                [InlineKeyboardButton('📄 Process PDF', callback_data='svc_process_pdf')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            prompt = f"What would you like to do with this PDF file named *{file_name}*?"

        else:
            await processing_msg.delete()
            return await update.message.reply_text(
                f"❌ Unsupported document type: `{mime}`",
                parse_mode='Markdown',
                reply_markup=build_service_menu(),
                reply_to_message_id=update.message.message_id
            )

        await processing_msg.delete()
        return await update.message.reply_text(
            prompt,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb),
            reply_to_message_id=update.message.message_id
        )

    # AUDIO, VOICE, VIDEO
    f = update.message.audio or update.message.voice or update.message.video
    if f:
        file_id = f.file_id
        file_name = getattr(f, 'file_name', None) or (
            'voice.ogg' if update.message.voice else
            'audio.mp3' if update.message.audio else
            'video.mp4'
        )
        mime = getattr(f, 'mime_type', None) or (
            'audio/ogg' if update.message.voice else
            'audio/mpeg' if update.message.audio else
            'video/mp4'
        )

        context.user_data['last_file_id'] = file_id
        context.user_data['last_mime'] = mime
        context.user_data['last_file_name'] = file_name

        if update.message.audio or update.message.voice:
            kb = [
                [InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            prompt = f"What would you like to do with this audio file named *{file_name}*?"

        elif update.message.video:
            kb = [
                [InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            prompt = f"What would you like to do with this video file named *{file_name}*?"

        await processing_msg.delete()
        return await update.message.reply_text(
            prompt,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb),
            reply_to_message_id=update.message.message_id
        )

    # UNSUPPORTED
    await processing_msg.delete()
    return await update.message.reply_text(
        "❌ Unsupported file type. I can process:\n"
        "- 📷 Photos\n"
        "- 📄 Images / PDFs / JSON files\n"
        "- 🎧 Audio and voice\n"
        "- 🎬 Video files",
        reply_markup=build_service_menu(),
        reply_to_message_id=update.message.message_id
    )

