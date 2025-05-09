import os
import logging
from bot.initializer import create_app, run_app

logging.basicConfig(filename="app.log", level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

def main():
    app = create_app()
    run_app(app)

if __name__ == '__main__':
    main()
