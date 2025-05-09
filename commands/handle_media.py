
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from env_config import logger
from memory_storage.all import users, processing_users
from memory_storage.all import create_or_update_user, is_busy, set_busy
from keyboards.build_service_menu import build_service_menu
from env_config import EXTERNAL_APIS
from memory_storage.all import  processing_users, create_or_update_user, is_busy
import logging


<<<<<<< HEAD

logger = logging.getLogger(__name__)

processing_users = set()

async def is_busy(uid): return False
def create_or_update_user(user): pass
def build_service_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="svc_back")]])
=======
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
# import logging
# from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import ContextTypes

# logger = logging.getLogger(__name__)

# processing_users = set()

# async def is_busy(uid): return False
# def create_or_update_user(user): pass
# def build_service_menu():
#     return InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="svc_back")]])

# async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.message.from_user
#     uid = user.id
#     logger.info(f"Media received from user {uid}")

#     if uid in processing_users or await is_busy(uid):
#         return await update.message.reply_text(
#             "⏳ Please wait, I'm still processing your previous request...",
#             reply_to_message_id=update.message.message_id
#         )

#     create_or_update_user(user)
#     processing_msg = await update.message.reply_text(
#         "🔄 Receiving your file...",
#         reply_to_message_id=update.message.message_id
#     )

#     # PHOTO
#     if update.message.photo:
#         photo = update.message.photo[-1]
#         file_id = photo.file_id
#         context.user_data['last_file_id'] = file_id
#         context.user_data['last_mime'] = 'image/jpeg'
#         context.user_data['last_file_name'] = "photo.jpg"

#         kb = [
#             [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
#             [InlineKeyboardButton('⚙️ Convert Image', callback_data='svc_convert_img')],
#             [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#         ]
#         await processing_msg.delete()
#         return await update.message.reply_text(
#             f"What would you like to do with this image?",
#             parse_mode="Markdown",
#             reply_markup=InlineKeyboardMarkup(kb),
#             reply_to_message_id=update.message.message_id
#         )

#     # DOCUMENT
#     if update.message.document:
#         doc = update.message.document
#         mime = doc.mime_type or ''
#         file_name = doc.file_name or 'unnamed'
#         file_id = doc.file_id

#         context.user_data['last_file_id'] = file_id
#         context.user_data['last_mime'] = mime
#         context.user_data['last_file_name'] = file_name

#         logger.info(f"Document received: {file_name} ({mime})")

#         if mime.startswith('image/'):
#             kb = [
#                 [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
#                 [InlineKeyboardButton('⚙️ Convert Image', callback_data='svc_convert_img')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = f"What would you like to do with this image file named *{file_name}*?"

#         elif mime.startswith('audio/'):
#             kb = [
#                 [InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = f"What would you like to do with this audio file named *{file_name}*?"

#         elif mime.startswith('video/'):
#             kb = [
#                 [InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = f"What would you like to do with this video file named *{file_name}*?"

#         elif mime == 'application/json':
#             kb = [
#                 [InlineKeyboardButton('🔎 Process JSON', callback_data='svc_process_json')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = f"What would you like to do with this JSON file named *{file_name}*?"

#         elif mime == 'application/pdf':
#             kb = [
#                 [InlineKeyboardButton('📄 Process PDF', callback_data='svc_process_pdf')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = f"What would you like to do with this PDF file named *{file_name}*?"

#         else:
#             await processing_msg.delete()
#             return await update.message.reply_text(
#                 f"❌ Unsupported document type: `{mime}`",
#                 parse_mode='Markdown',
#                 reply_markup=build_service_menu(),
#                 reply_to_message_id=update.message.message_id
#             )

#         await processing_msg.delete()
#         return await update.message.reply_text(
#             prompt,
#             parse_mode="Markdown",
#             reply_markup=InlineKeyboardMarkup(kb),
#             reply_to_message_id=update.message.message_id
#         )

#     # AUDIO, VOICE, VIDEO
#     f = update.message.audio or update.message.voice or update.message.video
#     if f:
#         file_id = f.file_id
#         file_name = getattr(f, 'file_name', None) or (
#             'voice.ogg' if update.message.voice else
#             'audio.mp3' if update.message.audio else
#             'video.mp4'
#         )
#         mime = getattr(f, 'mime_type', None) or (
#             'audio/ogg' if update.message.voice else
#             'audio/mpeg' if update.message.audio else
#             'video/mp4'
#         )

#         context.user_data['last_file_id'] = file_id
#         context.user_data['last_mime'] = mime
#         context.user_data['last_file_name'] = file_name

#         if update.message.audio or update.message.voice:
#             kb = [
#                 [InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = f"What would you like to do with this audio file named *{file_name}*?"

#         elif update.message.video:
#             kb = [
#                 [InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')],
#                 [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#             ]
#             prompt = f"What would you like to do with this video file named *{file_name}*?"

#         await processing_msg.delete()
#         return await update.message.reply_text(
#             prompt,
#             parse_mode="Markdown",
#             reply_markup=InlineKeyboardMarkup(kb),
#             reply_to_message_id=update.message.message_id
#         )

#     # UNSUPPORTED
#     await processing_msg.delete()
#     return await update.message.reply_text(
#         "❌ Unsupported file type. I can process:\n"
#         "- 📷 Photos\n"
#         "- 📄 Images / PDFs / JSON files\n"
#         "- 🎧 Audio and voice\n"
#         "- 🎬 Video files",
#         reply_markup=build_service_menu(),
#         reply_to_message_id=update.message.message_id
#     )


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from env_config import logger, EXTERNAL_APIS
from memory_storage.all import processing_users, create_or_update_user, is_busy, set_busy
from keyboards.build_service_menu import build_service_menu
from api_req.agent_resp import agent_response
from PIL import Image
import io
import zipfile
import tempfile
import subprocess
import os
from docs_conversion import convert_pdf_to_docx, convert_json_to_csv, convert_excel_to_pdf
>>>>>>> origin/main

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming media files with or without captions"""
    user = update.message.from_user
    uid = user.id
    caption = update.message.caption
    logger.info(f"Media received from user {uid}, caption: {caption}")

    if uid in processing_users or await is_busy(uid):
        return await update.message.reply_text(
            "⏳ Please wait, I'm still processing your previous request...",
            reply_to_message_id=update.message.message_id
        )
 
    create_or_update_user(user)
    processing_msg = await update.message.reply_text(
        "🔄 Processing your request...",
        reply_to_message_id=update.message.message_id
    )

    # Store file information
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        context.user_data['last_file_id'] = file_id
        context.user_data['last_mime'] = 'image/jpeg'
        context.user_data['last_file_name'] = "photo.jpg"
    elif update.message.document:
        doc = update.message.document
        context.user_data['last_file_id'] = doc.file_id
        context.user_data['last_mime'] = doc.mime_type or ''
        context.user_data['last_file_name'] = doc.file_name or 'file'
    elif update.message.video:
        video = update.message.video
        context.user_data['last_file_id'] = video.file_id
        context.user_data['last_mime'] = 'video/mp4'
        context.user_data['last_file_name'] = video.file_name or 'video.mp4'

    # Handle caption-based video conversions
    if caption and (update.message.video or (update.message.document and context.user_data.get('last_mime', '').startswith('video/'))):
        try:
            agent_result = await agent_response(caption, uid)
            intent = agent_result.get('service', 'unknown')
            confidence = agent_result.get('confidence', 0)
            logger.info(f"Video caption intent: {intent} with confidence {confidence}")

            if confidence > 80:
                file_id = context.user_data.get('last_file_id')
                file_name = context.user_data.get('last_file_name', 'video')
                if not file_id:
                    raise ValueError("No file available")

                file = await context.bot.get_file(file_id)
                video_bytes = await file.download_as_bytearray()

                # Save input video to temp file
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_in:
                    temp_in.write(video_bytes)
                    temp_in_path = temp_in.name

                # Set conversion parameters based on intent
                if intent == 'convert_to_gif':
                    output_ext = ".gif"
                    new_caption = "✨ *Here's your GIF!*"
                    command = [
                        "ffmpeg", "-y",
                        "-i", temp_in_path,
                        "-vf", "scale=480:-1:flags=lanczos,fps=15",
                        "-f", "gif",
                    ]
                elif intent == 'convert_to_mp4':
                    output_ext = ".mp4"
                    new_caption = "✨ *Here's your MP4 video!*"
                    command = [
                        "ffmpeg", "-y",
                        "-i", temp_in_path,
                        "-c:v", "libx264",
                        "-preset", "medium",
                        "-crf", "23",
                    ]
                elif intent == 'convert_to_webm':
                    output_ext = ".webm"
                    new_caption = "✨ *Here's your WebM video!*"
                    command = [
                        "ffmpeg", "-y",
                        "-i", temp_in_path,
                        "-c:v", "libvpx-vp9",
                        "-crf", "30",
                        "-b:v", "0",
                    ]
                else:
                    raise ValueError("Unsupported video conversion type")

                # Create output temp file and add to command
                with tempfile.NamedTemporaryFile(suffix=output_ext, delete=False) as temp_out:
                    output_path = temp_out.name
                    command.append(output_path)

                try:
                    subprocess.run(command, check=True, capture_output=True)
                    
                    # Read the converted file
                    with open(output_path, "rb") as f_out:
                        output_bytes = f_out.read()

                    output_buffer = io.BytesIO(output_bytes)
                    output_buffer.seek(0)
                    output_name = f"{file_name.rsplit('.', 1)[0]}{output_ext}"

                    await update.message.reply_document(
                        document=output_buffer,
                        filename=output_name,
                        caption=f"{new_caption}\n\n"
                                "🎯 Converted with optimized quality.\n"
                                "Need anything else? Just send another video! 😊",
                        parse_mode="Markdown",
                        reply_to_message_id=update.message.message_id
                    )

                except subprocess.CalledProcessError as e:
                    logger.error(f"FFmpeg error: {e.stderr.decode()}")
                    raise Exception("Video conversion failed")
                
                finally:
                    # Clean up temp files
                    os.remove(temp_in_path)
                    if os.path.exists(output_path):
                        os.remove(output_path)

                await processing_msg.delete()
                return

        except Exception as e:
            logger.error(f"Caption conversion error for video: {e}")
            await processing_msg.delete()
            return await update.message.reply_text(
                "❌ *Video Conversion Failed*\n\n"
                "Sorry, I couldn't convert your video. Please try again with a different video or format.",
                parse_mode="Markdown",
                reply_to_message_id=update.message.message_id
            )

    # Handle other media types and show appropriate menus
    mime_type = context.user_data.get('last_mime', '')
    if mime_type.startswith('image/'):
        kb = [
            [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
            [InlineKeyboardButton('⚙️ Convert Image', callback_data='svc_convert_img')],
            [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
        ]
        await processing_msg.delete()
        return await update.message.reply_text(
            "✨ Here's what I can do with your image:\n\n"
            "• *Enhance* the image quality\n"
            "• *Convert* to different formats\n"
            "Choose an option or type what you want!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb),
            reply_to_message_id=update.message.message_id
        )
    elif mime_type.startswith('video/'):
        kb = [
            [InlineKeyboardButton('🎬 Convert to GIF', callback_data='convert_to_gif')],
            [InlineKeyboardButton('🎥 Convert Format', callback_data='convert_video')],
            [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
        ]
        await processing_msg.delete()
        return await update.message.reply_text(
            "🎥 Here's what I can do with your video:\n\n"
            "• Convert to *GIF*\n"
            "• Convert to other formats\n"
            "Choose an option or type what you want!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb),
            reply_to_message_id=update.message.message_id
        )

    if caption and update.message.document:
        try:
            agent_result = await agent_response(caption, uid)
            intent = agent_result.get('service', 'unknown')
            confidence = agent_result.get('confidence', 0)
            logger.info(f"Document caption intent: {intent} with confidence {confidence}")

            if confidence > 80:
                file_id = context.user_data.get('last_file_id')
                file_name = context.user_data.get('last_file_name', 'document')
                mime_type = context.user_data.get('last_mime', '')
                
                if not file_id:
                    raise ValueError("No file available")

                file = await context.bot.get_file(file_id)
                doc_bytes = await file.download_as_bytearray()
                
                # Process PDF conversions
                if mime_type == 'application/pdf':
                    if intent in ['convert_pdf_to_docx', 'convert_to_word']:
                        result = await convert_pdf_to_docx(doc_bytes, file_name)
                    elif intent in ['convert_pdf_to_text', 'extract_text']:
                        result = await extract_text_from_pdf(doc_bytes, file_name)
                    else:
                        raise ValueError("Unsupported PDF conversion")

                # Process JSON conversions
                elif mime_type == 'application/json':
                    if intent in ['convert_json_to_csv', 'convert_to_csv']:
                        result = await convert_json_to_csv(doc_bytes, file_name)
                    elif intent == 'format_json':
                        result = await format_json_file(doc_bytes, file_name)
                    else:
                        raise ValueError("Unsupported JSON conversion")

                # Process Excel/CSV conversions
                elif mime_type in ['application/vnd.ms-excel', 
                                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                 'text/csv']:
                    if intent in ['convert_to_pdf', 'excel_to_pdf']:
                        result = await convert_excel_to_pdf(doc_bytes, file_name)
                    elif intent in ['convert_to_json', 'excel_to_json']:
                        result = await convert_excel_to_json(doc_bytes, file_name)
                    else:
                        raise ValueError("Unsupported spreadsheet conversion")
                else:
                    raise ValueError("Unsupported document type")

                if result.get('success'):
                    await update.message.reply_document(
                        document=result['file'],
                        filename=result['filename'],
                        caption=f"✨ *Conversion Complete!*\n{result.get('message', '')}",
                        parse_mode="Markdown",
                        reply_to_message_id=update.message.message_id
                    )
                else:
                    raise Exception(result.get('error', 'Conversion failed'))

                await processing_msg.delete()
                return

        except Exception as e:
            logger.error(f"Document conversion error: {e}")
            await processing_msg.delete()
            return await update.message.reply_text(
                "❌ *Conversion Failed*\n\n"
                f"Error: {str(e)}\n\n"
                "Please try again or choose a different format.",
                parse_mode="Markdown",
                reply_to_message_id=update.message.message_id
            )

    # Handle document type menus (when no caption)
    elif update.message.document:
        mime_type = context.user_data.get('last_mime', '')
        
        if mime_type == 'application/pdf':
            kb = [
                [InlineKeyboardButton('📄 Extract Text', callback_data='pdf_to_text')],
                [InlineKeyboardButton('📎 Convert to Word', callback_data='pdf_to_docx')],
                [InlineKeyboardButton('📦 Compress PDF', callback_data='compress_pdf')],
                [InlineKeyboardButton('↩️ Back', callback_data='svc_back')],
            ]
            menu_text = (
                "📑 Here's what I can do with your PDF:\n\n"
                "• *Extract* text content\n"
                "• *Convert* to Word format\n"
                "• *Compress* PDF size\n\n"
                "Choose an option or type your request!"
            )
            
        elif mime_type == 'application/json':
            kb = [
                [InlineKeyboardButton('📊 Convert to CSV', callback_data='json_to_csv')],
                [InlineKeyboardButton('📝 Format JSON', callback_data='format_json')],
                [InlineKeyboardButton('✅ Validate', callback_data='validate_json')],
                [InlineKeyboardButton('↩️ Back', callback_data='svc_back')],
            ]
            menu_text = (
                "🔤 Here's what I can do with your JSON:\n\n"
                "• *Convert* to CSV format\n"
                "• *Format* and prettify\n"
                "• *Validate* structure\n\n"
                "Choose an option or type your request!"
            )
            
        elif mime_type in ['application/vnd.ms-excel', 
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          'text/csv']:
            kb = [
                [InlineKeyboardButton('📄 Convert to PDF', callback_data='excel_to_pdf')],
                [InlineKeyboardButton('📊 Convert to JSON', callback_data='excel_to_json')],
                [InlineKeyboardButton('↩️ Back', callback_data='svc_back')],
            ]
            menu_text = (
                "📊 Here's what I can do with your spreadsheet:\n\n"
                "• Convert to *PDF*\n"
                "• Convert to *JSON*\n\n"
                "Choose an option or type your request!"
            )
        else:
            await processing_msg.delete()
            return await update.message.reply_text(
                f"❌ Unsupported document type: `{mime_type}`\n\n"
                "I can process:\n"
                "- PDF documents\n"
                "- JSON files\n"
                "- Excel/CSV spreadsheets",
                parse_mode="Markdown",
                reply_markup=build_service_menu(),
                reply_to_message_id=update.message.message_id
            )

        await processing_msg.delete()
        return await update.message.reply_text(
            menu_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb),
            reply_to_message_id=update.message.message_id
        )




# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ContextTypes
# from env_config import logger, EXTERNAL_APIS
# from memory_storage.all import processing_users, create_or_update_user, is_busy, set_busy
# from keyboards.build_service_menu import build_service_menu
# from api_req.agent_resp import agent_response
# from PIL import Image
# import io
# import zipfile

# async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handle incoming media files with or without captions"""
#     user = update.message.from_user
#     uid = user.id
#     caption = update.message.caption
#     logger.info(f"Media received from user {uid}, caption: {caption}")

#     if uid in processing_users or await is_busy(uid):
#         return await update.message.reply_text(
#             "⏳ Please wait, I'm still processing your previous request...",
#             reply_to_message_id=update.message.message_id
#         )

#     create_or_update_user(user)
#     processing_msg = await update.message.reply_text(
#         "🔄 Processing your request...",
#         reply_to_message_id=update.message.message_id
#     )

#     # Store file information
#     if update.message.photo:
#         file_id = update.message.photo[-1].file_id
#         context.user_data['last_file_id'] = file_id
#         context.user_data['last_mime'] = 'image/jpeg'
#         context.user_data['last_file_name'] = "photo.jpg"
#     elif update.message.document:
#         doc = update.message.document
#         context.user_data['last_file_id'] = doc.file_id
#         context.user_data['last_mime'] = doc.mime_type or ''
#         context.user_data['last_file_name'] = doc.file_name or 'file'
#     else:
#         f = update.message.audio or update.message.voice or update.message.video
#         if f:
#             context.user_data['last_file_id'] = f.file_id
#             context.user_data['last_mime'] = getattr(f, 'mime_type', None) or (
#                 'audio/ogg' if update.message.voice else
#                 'audio/mpeg' if update.message.audio else
#                 'video/mp4'
#             )
#             context.user_data['last_file_name'] = getattr(f, 'file_name', None) or (
#                 'voice.ogg' if update.message.voice else
#                 'audio.mp3' if update.message.audio else
#                 'video.mp4'
#             )

#     # Handle caption-based conversions for images
#     if caption and (update.message.photo or (update.message.document and context.user_data.get('last_mime', '').startswith('image/'))):
#         try:
#             agent_result = await agent_response(caption, uid)
#             intent = agent_result.get('service', 'unknown')
#             confidence = agent_result.get('confidence', 0)
#             logger.info(f"Caption intent: {intent} with confidence {confidence}")

#             if confidence > 80:
#                 file_id = context.user_data.get('last_file_id')
#                 file_name = context.user_data.get('last_file_name', 'image')
#                 if not file_id:
#                     raise ValueError("No file available")
                
#                 file = await context.bot.get_file(file_id)
#                 image_bytes = await file.download_as_bytearray()
#                 img = Image.open(io.BytesIO(image_bytes))

#                 output_buffer = io.BytesIO()
#                 if intent == 'convert_to_png':
#                     img.save(output_buffer, format='PNG')
#                     output_name = f"{file_name.rsplit('.', 1)[0]}.png"
#                     new_caption = "✨ *Here's your PNG image!*"
#                 elif intent == 'convert_to_jpg':
#                     img.convert('RGB').save(output_buffer, format='JPEG', quality=95)
#                     output_name = f"{file_name.rsplit('.', 1)[0]}.jpg"
#                     new_caption = "✨ *Here's your JPG image!*"
#                 elif intent == 'convert_to_pdf':
#                     img.convert('RGB').save(output_buffer, format='PDF')
#                     output_name = f"{file_name.rsplit('.', 1)[0]}.pdf"
#                     new_caption = "✨ *Here's your PDF file!*"
#                 elif intent == 'convert_to_webp':
#                     img.save(output_buffer, format='WebP', quality=95)
#                     output_name = f"{file_name.rsplit('.', 1)[0]}.webp"
#                     new_caption = "✨ *Here's your WebP image!*"
#                 elif intent == 'convert_to_zip':
#                     with zipfile.ZipFile(output_buffer, 'w') as zf:
#                         img_bytes = io.BytesIO()
#                         img.save(img_bytes, format=img.format)
#                         zf.writestr('image.' + img.format.lower(), img_bytes.getvalue())
#                     output_name = f"{file_name.rsplit('.', 1)[0]}.zip"
#                     new_caption = "✨ *Here's your ZIP archive!*"
#                 else:
#                     raise ValueError("Unsupported conversion type")
#                 output_buffer.seek(0)
#                 # Send converted file
#                 await update.message.reply_document(
#                     document=output_buffer,
#                     filename=output_name,
#                     caption=f"{new_caption}\n\n"
#                             "🎯 Converted with optimized quality.\n"
#                             "Need anything else? Just send another image! 😊",
#                     parse_mode="Markdown",
#                     reply_to_message_id=update.message.message_id
#                 )
#                 await processing_msg.delete()
#                 return

#         except Exception as e:
#             logger.error(f"Caption conversion error: {e}")
#             await processing_msg.delete()
#             return await update.message.reply_text(
#                 "❌ *Conversion Failed*\n\n"
#                 "Sorry, I couldn't convert your image. Please try again with a different image or format.",
#                 parse_mode="Markdown",
#                 reply_to_message_id=update.message.message_id
#             )

#     # If no caption or conversion was not triggered, show options based on file type
#     mime_type = context.user_data.get('last_mime', '')
#     if mime_type.startswith('image/'):
#         kb = [
#             [InlineKeyboardButton('🖼️ Enhance Image', callback_data='svc_enhance_image')],
#             [InlineKeyboardButton('⚙️ Convert Image', callback_data='svc_convert_img')],
#             [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#         ]
#         await processing_msg.delete()
#         return await update.message.reply_text(
#             "✨ Here's what I can do with your image:\n\n"
#             "• *Enhance* the image quality\n"
#             "• *Convert* to different formats (PDF, PNG, JPG, WebP)\n"
#             "• Create a ZIP archive\n\n"
#             "Choose an option or tell me what you'd like in the caption! Examples:\n"
#             "- 'convert to pdf'\n"
#             "- 'make it png'\n"
#             "- 'convert to jpg'",
#             parse_mode="Markdown",
#             reply_markup=InlineKeyboardMarkup(kb),
#             reply_to_message_id=update.message.message_id
#         )
#     elif mime_type.startswith('audio/'):
#         kb = [
#             [InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')],
#             [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#         ]
#         await processing_msg.delete()
#         return await update.message.reply_text(
#             "🎵 I can enhance your audio file! Would you like to:\n\n"
#             "• Remove background noise\n"
#             "• Improve clarity\n"
#             "• Enhance voice quality",
#             parse_mode="Markdown",
#             reply_markup=InlineKeyboardMarkup(kb),
#             reply_to_message_id=update.message.message_id
#         )
#     elif mime_type.startswith('video/'):
#         kb = [
#             [InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')],
#             [InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')],
#         ]
#         await processing_msg.delete()
#         return await update.message.reply_text(
#             "🎥 I can enhance your video! Would you like to:\n\n"
#             "• Improve video quality\n"
#             "• Stabilize shaky footage\n"
#             "• Enhance colors",
#             parse_mode="Markdown",
#             reply_markup=InlineKeyboardMarkup(kb),
#             reply_to_message_id=update.message.message_id
#         )
#     # Unsupported file type
#     await processing_msg.delete()
#     return await update.message.reply_text(
#         "❌ Unsupported file type. I can process:\n"
#         "- 📷 Photos and Images\n"
#         "- 🎵 Audio and Voice messages\n"
#         "- 🎥 Video files\n\n"
#         "Please send me one of these file types!",
#         reply_markup=build_service_menu(),
#         reply_to_message_id=update.message.message_id
#     )


