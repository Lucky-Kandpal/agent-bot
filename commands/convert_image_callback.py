
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from env_config import EXTERNAL_APIS
from api_req.call_external_api import call_external_api
import io
from env_config import logger

import io
import zipfile

async def convert_image_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    logger.info(f"inside convert_image_callback, query:- {query}, user:- {query.from_user.id}, data:- {query.data}")

    await query.answer()

    # 1. Retrieve the stored file info
    file_id = context.user_data.get('last_file_id')
    file_name = context.user_data.get('last_file_name', 'image')
    mime_type = context.user_data.get('last_mime', '')

    if not file_id:
        return await query.edit_message_text("❌ Could not find the file to convert.")

    # 2. Build conversion options based on file type
    conversion_kb = []
    
    # For images
    if mime_type.startswith('image/'):
        extension = file_name.rsplit('.', 1)[-1].lower()
        
        # Add PDF conversion option
        conversion_kb.append([InlineKeyboardButton('📄 Convert to PDF', callback_data='convert_to_pdf')])
        
        # Add ZIP option
        conversion_kb.append([InlineKeyboardButton('📦 Convert to ZIP', callback_data='convert_to_zip')])
        
        # Format conversion options
        if extension == 'jpg' or extension == 'jpeg':
            conversion_kb.append([InlineKeyboardButton('🖼️ Convert to PNG', callback_data='convert_to_png')])
        elif extension == 'png':
            conversion_kb.append([InlineKeyboardButton('🖼️ Convert to JPG', callback_data='convert_to_jpg')])
        
        # Add WebP option
        conversion_kb.append([InlineKeyboardButton('🌐 Convert to WebP', callback_data='convert_to_webp')])
        
    # Add back button
    conversion_kb.append([InlineKeyboardButton('↩️ Back', callback_data='svc_back')])

    # 3. Update the message with conversion options
    await query.edit_message_text(
        f"Please choose how you'd like to convert *{file_name}*:",
        reply_markup=InlineKeyboardMarkup(conversion_kb),
        parse_mode="Markdown"
    )

# async def convert_image_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     logger.info(f"inside convert_image_callback, query:- {query}, user:- {query.from_user.id}, data:- {query.data}, message:- {query.message}")

#     await query.answer()

#     # 1. Retrieve the stored file info
#     file_id   = context.user_data.get('last_file_id')
#     file_name = context.user_data.get('last_file_name', 'image')

#     if not file_id:
#         return await query.edit_message_text("❌ Could not find the file to convert.")

#     # 2. Download the image bytes from Telegram
#     tg_file    = await context.bot.get_file(file_id)
#     orig_bytes = await tg_file.download_as_bytearray()

#     # 3. Mock “conversion” into a ZIP (you could call your real API here)
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, mode='w') as z:
#         # store the original image under its original name
#         z.writestr(file_name, orig_bytes)
#     zip_buffer.seek(0)
#     zip_name = file_name.rsplit('.', 1)[0] + '.zip'
#     zip_buffer.name = zip_name

#     # 4. Remove the inline‑keyboard prompt
#     await query.delete_message()

#     # 5. Reply with the “converted” ZIP file 
#     return await query.message.reply_document(
#         document=zip_buffer,
#         filename=zip_name,
#         caption=f"📦 Here’s your converted file: *{zip_name}*",
#         parse_mode="Markdown",
#         reply_to_message_id=query.message.reply_to_message.message_id
#     )
