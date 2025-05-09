from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from env_config import logger
from keyboards.build_service_menu import build_service_menu  # Import the function
# from commands.handle_media import build_service_menu

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, processing_msg):
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

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE, processing_msg):
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

async def handle_audio_video(update: Update, context: ContextTypes.DEFAULT_TYPE, processing_msg):
    f = update.message.audio or update.message.voice or update.message.video
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