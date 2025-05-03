import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging
from system_prompt import SYSTEM_INTENT_PROMPT, SYSTEM_CHAT_PROMPT, AGENT_SYSTEM_PROMPT
from commands.start_cmd import start
from keyboards.build_service_menu import build_service_menu
from env_config import token, WEBHOOK_URL, EXTERNAL_APIS, groq_client, app_port, DEFAULT_MODEL
from memory_storage.all import users, requests, processing_users, create_or_update_user, is_busy, set_busy, create_request, update_request
from menu.menu_route import menu_route
from commands.handle_media import handle_media
from commands.document_handle import handle_document
from commands.handle_text import handle_text
from commands.help_command import help_command
from commands.unknown import unknown
from commands.enhance_image_callback import enhance_image_callback
from commands.convert_image_callback import convert_image_callback
from commands.process_json_callback import process_json_callback
from commands.process_pdf_callback import process_pdf_callback
from telegram import Update
logging.basicConfig(filename="app.log",level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


# Entry point
def main():
    app = ApplicationBuilder().token(token).build()
    
    # Command handlers
    # CallbackQuery handlers
    app.add_handler(CallbackQueryHandler(enhance_image_callback, pattern=r'^svc_enhance_image$'))
    app.add_handler(CallbackQueryHandler(convert_image_callback, pattern=r'^svc_convert_img$'))
    app.add_handler(CallbackQueryHandler(process_json_callback, pattern=r'^svc_process_json$'))
    app.add_handler(CallbackQueryHandler(process_pdf_callback,  pattern=r'^svc_process_pdf$'))
    app.add_handler(CallbackQueryHandler(menu_route,            pattern=r'^svc_back$'))


    # Media handlers
    app.add_handler(MessageHandler(filters.PHOTO,          handle_media))
    app.add_handler(MessageHandler(filters.Document.ALL,   handle_media))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.VIDEO, handle_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Catch-all for unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, lambda u, c: u.message.reply_text("❌ Unknown command.")))

    # Start the bot using webhook
    logger.info("Starting webhook...")
    port = int(app_port)
    app.run_webhook(
        listen='0.0.0.0',
        port=port,
        url_path='/webhook',
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

if __name__ == '__main__':
    main()