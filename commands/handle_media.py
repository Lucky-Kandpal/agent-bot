
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from env_config import logger
from memory_storage.all import users, processing_users
from memory_storage.all import create_or_update_user, is_busy, set_busy
from keyboards.build_service_menu import build_service_menu
from env_config import EXTERNAL_APIS
from api_req.call_external_api import call_external_api
from memory_storage.all import  processing_users, create_or_update_user, is_busy, set_busy, create_request, update_request

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    uid = user.id
    logger.info(f"Media received from user {uid}")

    # Prevent overlapping requests
    if uid in processing_users or await is_busy(uid):
        return await update.message.reply_text(
            "⏳ Please wait, I'm still processing your previous request..."
        )

    create_or_update_user(user)
    processing_msg = await update.message.reply_text("🔄 Receiving your file...")

    # 1️⃣ PHOTO branch
    if update.message.photo:
        photo = update.message.photo[-1]
        logger.info(f"Photo received: {photo.file_id}")
        context.user_data['last_photo_file_id'] = photo.file_id

        kb = [
            [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
            [InlineKeyboardButton('⚙️ Convert Image',  callback_data='svc_convert_img')],
            [InlineKeyboardButton('↩️ Back to Menu',    callback_data='svc_back')],
        ]
        await processing_msg.delete()
        return await update.message.reply_text(
            "What would you like to do with this photo?",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    # 2️⃣ JSON / PDF branch
    if update.message.document:
        doc = update.message.document
        mime = doc.mime_type or ''
        logger.info(f"Document received: {doc.file_name} ({mime})")

        # JSON
        if mime == 'application/json':
            context.user_data['last_doc_file_id'] = doc.file_id
            kb = [
                [InlineKeyboardButton('🔎 Process JSON', callback_data='svc_process_json')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            await processing_msg.delete()
            return await update.message.reply_text(
                "What would you like to do with this JSON?",
                reply_markup=InlineKeyboardMarkup(kb)
            )

        # PDF
        if mime == 'application/pdf':
            context.user_data['last_doc_file_id'] = doc.file_id
            kb = [
                [InlineKeyboardButton('📄 Process PDF', callback_data='svc_process_pdf')],
                [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
            ]
            await processing_msg.delete()
            return await update.message.reply_text(
                "What would you like to do with this PDF?",
                reply_markup=InlineKeyboardMarkup(kb)
            )

    # 3️⃣ Other media (audio/video)
    f = (
        update.message.audio
        or update.message.voice
        or update.message.video
    )
    if not f:
        logger.warning(f"Unsupported media type from {uid}")
        await processing_msg.delete()
        return await update.message.reply_text(
            "Unsupported file type. I can process photos, JSON, PDF, audio and video only.",
            reply_markup=build_service_menu()
        )

    logger.info(f"Received file object: {f}")

    # Reject unsupported documents masquerading as media
    if hasattr(f, 'mime_type'):
        mt = f.mime_type
        logger.info(f"File MIME Type: {mt}")
        if (mt.startswith('application/') and mt not in ('application/json',)) or mt in ('application/pdf',):
            await processing_msg.delete()
            return await update.message.reply_text(
                f"Sorry, I can't process {mt} files in this flow.",
                reply_markup=build_service_menu()
            )

    caption = (update.message.caption or '').lower()

    # No caption → suggest clean/enhance
    if not caption:
        kb = []
        if hasattr(f, 'mime_type') and f.mime_type.startswith('audio/') or isinstance(f, type(update.message.voice)):
            kb.append([InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')])
        if hasattr(f, 'mime_type') and f.mime_type.startswith('video/'):
            kb.append([InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')])
        kb.append([InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')])

        await processing_msg.delete()
        return await update.message.reply_text(
            "What would you like to do with this file?",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    # Caption present → interpret “clean” commands
    svc = context.user_data.pop('svc', None)
    is_audio = (hasattr(f, 'mime_type') and f.mime_type.startswith('audio/')) or isinstance(f, type(update.message.voice))
    is_video = hasattr(f, 'mime_type') and f.mime_type.startswith('video/')

    if 'clean' in caption or svc in ('clean_audio', 'clean_video'):
        intent = 'clean_audio' if is_audio else 'clean_video' if is_video else None
        if not intent:
            await processing_msg.delete()
            return await update.message.reply_text(
                "I can't determine file type. Only audio/video can be cleaned.",
                reply_markup=build_service_menu()
            )

        processing_users.add(uid)
        await set_busy(uid, True)
        try:
            file_obj = await f.get_file()
            bio = await file_obj.download_as_bytearray()
            mime = f.mime_type if hasattr(f, 'mime_type') else ('audio/ogg' if is_audio else 'video/mp4')

            api     = EXTERNAL_APIS['voice_cleaner'] if intent == 'clean_audio' else EXTERNAL_APIS['video_cleaner']
            send_fn = update.message.reply_voice    if intent == 'clean_audio' else update.message.reply_video
            rid     = create_request(uid, intent, file_type=mime)

            await processing_msg.edit_text(
                f"🔄 Enhancing your {'audio' if intent=='clean_audio' else 'video'}..."
            )
            res = call_external_api(api, files={'file': (file_obj.file_unique_id, bio, mime)})
            url = res.get('cleaned_url') or res.get('url')

            if url:
                update_request(rid, 'done', output_url=url)
                await processing_msg.delete()
                return await send_fn(
                    url,
                    caption=f"Here's your enhanced {'audio' if intent=='clean_audio' else 'video'}!"
                )

            update_request(rid, 'failed', error=res.get('error'))
            await processing_msg.delete()
            return await update.message.reply_text(
                f"❌ Error: {res.get('error', 'Something went wrong')}"
            )

        except Exception as e:
            logger.error(f"API error: {e}")
            update_request(rid, 'failed', error=str(e))
            await processing_msg.delete()
            return await update.message.reply_text(
                "❌ Error processing your file. Please try again later."
            )

        finally:
            processing_users.discard(uid)
            await set_busy(uid, False)

    # Fallback for unrecognized captions
    await processing_msg.delete()
    return await update.message.reply_text(
        "🤔 I didn't understand that. Would you like to clean/enhance your file?",
        reply_markup=build_service_menu()
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

