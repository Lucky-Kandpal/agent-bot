from telegram.ext import CallbackQueryHandler, MessageHandler, filters, CommandHandler
from commands.start_cmd import start
from commands.enhance_image_callback import enhance_image_callback
from commands.convert_image_callback import convert_image_callback
from commands.process_json_callback import process_json_callback
from commands.process_pdf_callback import process_pdf_callback
from menu.menu_route import menu_route
from commands.handle_media import handle_media
from commands.handle_text import handle_text

def register_handlers(app):
    app.add_handler(CommandHandler('start', start))
    
    # CallbackQuery handlers
    app.add_handler(CallbackQueryHandler(enhance_image_callback, pattern=r'^svc_enhance_image$'))
    app.add_handler(CallbackQueryHandler(convert_image_callback, pattern=r'^svc_convert_img$'))
    app.add_handler(CallbackQueryHandler(process_json_callback, pattern=r'^svc_process_json$'))
    app.add_handler(CallbackQueryHandler(process_pdf_callback, pattern=r'^svc_process_pdf$'))
    app.add_handler(CallbackQueryHandler(menu_route, pattern=r'^svc_back$'))
    
    # Media handlers
    app.add_handler(MessageHandler(filters.PHOTO, handle_media))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_media))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.VIDEO, handle_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Catch-all for unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, lambda update, context: update.message.reply_text("❌ Unknown command.")))