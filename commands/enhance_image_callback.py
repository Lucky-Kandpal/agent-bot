from telegram import Update
from telegram.ext import ContextTypes

from env_config import EXTERNAL_APIS
from api_req.call_external_api import call_external_api


async def enhance_image_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    file_id = context.user_data.get('last_photo_file_id')
    if not file_id:
        return await query.edit_message_text("❌ Could not find the photo to enhance.")

    tg_file = await context.bot.get_file(file_id)
    bio     = await tg_file.download_as_bytearray()

    api = EXTERNAL_APIS['image_enhancer']
    res = call_external_api(api, files={'file': (file_id, bio, 'image/jpeg')})
    url = res.get('enhanced_url')

    if url:
        await query.edit_message_caption("✨ Here’s your enhanced image!")
        return await query.message.reply_photo(url)
    else:
        return await query.edit_message_text("❌ Enhancement failed. Please try again.")

