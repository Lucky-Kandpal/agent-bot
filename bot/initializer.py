from telegram.ext import ApplicationBuilder
import logging
from env_config import token, app_port, WEBHOOK_URL
from bot.handlers_register import register_handlers
logger = logging.getLogger(__name__)

def create_app():
    app = ApplicationBuilder().token(token).build()
    register_handlers(app)
    return app

def run_app(app):
    logger.info("Starting webhook...")
    port = int(app_port)
    app.run_webhook(
        listen='0.0.0.0',
        port=port,
        url_path='/webhook',
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )
