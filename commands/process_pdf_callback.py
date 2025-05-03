
from telegram import Update
from telegram.ext import ContextTypes

from env_config import EXTERNAL_APIS
from api_req.call_external_api import call_external_api




async def process_pdf_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    file_id = context.user_data.get('last_doc_file_id')
    if not file_id:
        return await query.edit_message_text("❌ PDF file not found.")

    tg_file = await context.bot.get_file(file_id)
    bio     = await tg_file.download_as_bytearray()

    api = EXTERNAL_APIS['pdf_processor']
    res = call_external_api(api, files={'file': (file_id, bio, 'application/pdf')})
    summary = res.get('summary')

    if summary:
        await query.edit_message_caption("📄 PDF processed:")
        return await query.message.reply_text(summary)
    else:
        return await query.edit_message_text("❌ PDF processing failed.")

