

from telegram import Update
from telegram.ext import ContextTypes

from env_config import EXTERNAL_APIS
from api_req.call_external_api import call_external_api



async def process_json_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    file_id = context.user_data.get('last_doc_file_id')
    if not file_id:
        return await query.edit_message_text("❌ JSON file not found.")

    tg_file = await context.bot.get_file(file_id)
    bio     = await tg_file.download_as_bytearray()

    api = EXTERNAL_APIS['json_processor']
    res = call_external_api(api, files={'file': (file_id, bio, 'application/json')})
    result = res.get('result')

    if result:
        await query.edit_message_caption("🔎 JSON processed:")
        return await query.message.reply_text(f"```json\n{result}\n```", parse_mode='Markdown')
    else:
        return await query.edit_message_text("❌ JSON processing failed.")

