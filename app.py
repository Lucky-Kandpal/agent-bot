import os
import logging
import logging
from env_config import token, WEBHOOK_URL, app_port
from menu.menu_route import menu_route
from commands.handle_media import handle_media
from commands.handle_text import handle_text
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters, CommandHandler
from commands.enhance_image_callback import enhance_image_callback
from commands.convert_image_callback import convert_image_callback
from commands.process_json_callback import process_json_callback
from commands.process_pdf_callback import process_pdf_callback
from commands.start_cmd import start
from commands.conversion_handlers import (
    convert_to_pdf_handler,
    convert_to_zip_handler,
    convert_to_png_handler,
    convert_to_jpg_handler,
    convert_to_webp_handler
)

logging.basicConfig(filename="app.log",level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Entry point
def main():
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    
    # CallbackQuery handlers
    app.add_handler(CallbackQueryHandler(enhance_image_callback, pattern=r'^svc_enhance_image$'))
    app.add_handler(CallbackQueryHandler(convert_image_callback, pattern=r'^svc_convert_img$'))
    app.add_handler(CallbackQueryHandler(process_json_callback, pattern=r'^svc_process_json$'))
    app.add_handler(CallbackQueryHandler(process_pdf_callback,  pattern=r'^svc_process_pdf$'))
    app.add_handler(CallbackQueryHandler(menu_route, pattern=r'^svc_back$'))


# Inside main() function, add these handlers:
    app.add_handler(CallbackQueryHandler(convert_to_pdf_handler, pattern=r'^convert_to_pdf$'))
    app.add_handler(CallbackQueryHandler(convert_to_zip_handler, pattern=r'^convert_to_zip$'))
    app.add_handler(CallbackQueryHandler(convert_to_png_handler, pattern=r'^convert_to_png$'))
    app.add_handler(CallbackQueryHandler(convert_to_jpg_handler, pattern=r'^convert_to_jpg$'))
    app.add_handler(CallbackQueryHandler(convert_to_webp_handler, pattern=r'^convert_to_webp$'))
    # Media handlers
    app.add_handler(MessageHandler(filters.PHOTO,handle_media))
    app.add_handler(MessageHandler(filters.Document.ALL,handle_media))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.VIDEO,handle_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_text))

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