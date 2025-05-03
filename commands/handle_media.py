
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

# Dummy functions to simulate your app state
processing_users = set()

# async def is_busy(uid): return False
# def create_or_update_user(user): pass
# def build_service_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="svc_back")]])

# async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.message.from_user
#     uid = user.id
#     logger.info(f"Media received from user {uid}")

#     if uid in processing_users or await is_busy(uid):
#         return await update.message.reply_text("⏳ Please wait, I'm still processing your previous request...")

#     create_or_update_user(user)
#     processing_msg = await update.message.reply_text("🔄 Receiving your file...")

#     # Handle PHOTO
#     if update.message.photo:
#         photo = update.message.photo[-1]
#         logger.info(f"Photo received: {photo.file_id}")
#         context.user_data['last_file_id'] = photo.file_id
#         context.user_data['last_mime'] = 'image/jpeg'

#         kb = [
#             [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
#             [InlineKeyboardButton('⚙️ Convert Image', callback_data='svc_convert_img')],
#             [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#         ]
#         await processing_msg.delete()
#         return await update.message.reply_text("What would you like to do with this photo?", reply_markup=InlineKeyboardMarkup(kb))

#     # Handle DOCUMENTS
#     if update.message.document:
#         doc = update.message.document
#         mime = doc.mime_type or ''
#         logger.info(f"Document received: {doc.file_name} ({mime})")
#         context.user_data['last_file_id'] = doc.file_id
#         context.user_data['last_mime'] = mime

#         if mime.startswith('image/'):
#             kb = [
#                 [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
#                 [InlineKeyboardButton('⚙️ Convert Image', callback_data='svc_convert_img')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = "What would you like to do with this image file?"

#         elif mime.startswith('audio/'):
#             kb = [
#                 [InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = "What would you like to do with this audio file?"

#         elif mime.startswith('video/'):
#             kb = [
#                 [InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = "What would you like to do with this video file?"

#         elif mime == 'application/json':
#             kb = [
#                 [InlineKeyboardButton('🔎 Process JSON', callback_data='svc_process_json')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = "What would you like to do with this JSON file?"

#         elif mime == 'application/pdf':
#             kb = [
#                 [InlineKeyboardButton('📄 Process PDF', callback_data='svc_process_pdf')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = "What would you like to do with this PDF file?"

#         else:
#             await processing_msg.delete()
#             return await update.message.reply_text(
#                 f"❌ Unsupported document type: `{mime}`",
#                 parse_mode='Markdown',
#                 reply_markup=build_service_menu()
#             )

#         await processing_msg.delete()
#         return await update.message.reply_text(prompt, reply_markup=InlineKeyboardMarkup(kb))

#     # Handle AUDIO, VOICE, VIDEO as media
#     f = update.message.audio or update.message.voice or update.message.video
#     if f:
#         context.user_data['last_file_id'] = f.file_id
#         context.user_data['last_mime'] = getattr(f, 'mime_type', None) or (
#             'audio/ogg' if update.message.voice else 'video/mp4'
#         )

#         if update.message.audio or update.message.voice:
#             kb = [
#                 [InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = "What would you like to do with this audio/voice message?"

#         elif update.message.video:
#             kb = [
#                 [InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = "What would you like to do with this video?"

#         await processing_msg.delete()
#         return await update.message.reply_text(prompt, reply_markup=InlineKeyboardMarkup(kb))

#     # Nothing matched
#     await processing_msg.delete()
#     return await update.message.reply_text(
#         "❌ Unsupported file type. I can process:\n"
#         "- 📷 Photos\n"
#         "- 📄 Images / PDFs / JSON files\n"
#         "- 🎧 Audio and voice\n"
#         "- 🎬 Video files",
#         reply_markup=build_service_menu()
#     )
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

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



# async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.message.from_user
#     uid = user.id
#     logger.info(f"Media received from user {uid}")

#     # Prevent overlap
#     if uid in processing_users or await is_busy(uid):
#         return await update.message.reply_text("⏳ Please wait, I'm still processing your previous request...")

#     create_or_update_user(user)
#     processing_msg = await update.message.reply_text("🔄 Receiving your file...")

#     # 1️⃣ PHOTO branch
#     if update.message.photo:
#         photo = update.message.photo[-1]
#         logger.info(f"Photo received: {photo.file_id}")
#         context.user_data['last_photo_file_id'] = photo.file_id

#         kb = [
#             [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
#             [InlineKeyboardButton('⚙️ Convert Image',  callback_data='svc_convert_img')],
#             [InlineKeyboardButton('↩️ Back to Menu',    callback_data='svc_back')],
#         ]
#         await processing_msg.delete()
#         return await update.message.reply_text(
#             "What would you like to do with this photo?",
#             reply_markup=InlineKeyboardMarkup(kb)
#         )

#     # 2️⃣ Other media
#     f = update.message.audio or update.message.voice or update.message.video or update.message.document
#     if not f:
#         logger.warning(f"Unsupported media type from {uid}")
#         await processing_msg.delete()
#         return await update.message.reply_text(
#             "Unsupported file type. I can process photos, audio, video and voice messages only.",
#             reply_markup=build_service_menu()
#         )

#     logger.info(f"Received file object: {f}")
#     # Reject certain document types
#     if hasattr(f, 'mime_type'):
#         mt = f.mime_type
#         logger.info(f"File MIME Type: {mt}")
#         if (mt.startswith('application/') and mt not in ('application/json',)) or mt in ('application/pdf',):
#             await processing_msg.delete()
#             return await update.message.reply_text(
#                 f"Sorry, I can't process {mt} files. I only enhance audio/video.",
#                 reply_markup=build_service_menu()
#             )

#     caption = (update.message.caption or '').lower()
#     # No caption → suggest
#     if not caption:
#         kb = []
#         if hasattr(f, 'mime_type') and f.mime_type:
#             if f.mime_type.startswith('audio/') or isinstance(f, type(update.message.voice)):
#                 kb.append([InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')])
#             if f.mime_type.startswith('video/'):
#                 kb.append([InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')])
#         kb.append([InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')])

#         await processing_msg.delete()
#         return await update.message.reply_text(
#             "What would you like to do with this file?",
#             reply_markup=InlineKeyboardMarkup(kb)
#         )

#     # Caption present → interpret “clean”
#     svc = context.user_data.pop('svc', None)
#     is_audio = (hasattr(f, 'mime_type') and f.mime_type.startswith('audio/')) or isinstance(f, type(update.message.voice))
#     is_video = hasattr(f, 'mime_type') and f.mime_type.startswith('video/')
#     if 'clean' in caption or svc in ('clean_audio', 'clean_video'):
#         intent = 'clean_audio' if is_audio else 'clean_video' if is_video else None
#         if not intent:
#             await processing_msg.delete()
#             return await update.message.reply_text(
#                 "I can't determine file type. Only audio/video can be cleaned.",
#                 reply_markup=build_service_menu()
#             )

#         processing_users.add(uid)
#         await set_busy(uid, True)
#         try:
#             file_obj = await f.get_file()
#             bio = await file_obj.download_as_bytearray()
#             mime = f.mime_type if hasattr(f, 'mime_type') else ('audio/ogg' if is_audio else 'video/mp4')

#             api     = EXTERNAL_APIS['voice_cleaner'] if intent == 'clean_audio' else EXTERNAL_APIS['video_cleaner']
#             send_fn = update.message.reply_voice    if intent == 'clean_audio' else update.message.reply_video
#             rid     = create_request(uid, intent, file_type=mime)

#             await processing_msg.edit_text(f"🔄 Enhancing your {'audio' if intent=='clean_audio' else 'video'}...")
#             res = call_external_api(api, files={'file': (file_obj.file_unique_id, bio, mime)})
#             url = res.get('cleaned_url') or res.get('url')

#             if url:
#                 update_request(rid, 'done', output_url=url)
#                 await processing_msg.delete()
#                 return await send_fn(url, caption=f"Here's your enhanced {'audio' if intent=='clean_audio' else 'video'}!")

#             update_request(rid, 'failed', error=res.get('error'))
#             await processing_msg.delete()
#             return await update.message.reply_text(f"❌ Error: {res.get('error', 'Something went wrong')}")

#         except Exception as e:
#             logger.error(f"API error: {e}")
#             update_request(rid, 'failed', error=str(e))
#             await processing_msg.delete()
#             return await update.message.reply_text("❌ Error processing your file. Please try again later.")

#         finally:
#             processing_users.discard(uid)
#             await set_busy(uid, False)

#     # Fallback for unrecognized captions
#     await processing_msg.delete()
#     return await update.message.reply_text(
#         "🤔 I didn't understand that. Would you like to clean/enhance your file?",
#         reply_markup=build_service_menu()
#     )

