
from dotenv import load_dotenv
import os
import logging
from groq import Groq


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename="app.log",level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Config
token = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
EXTERNAL_APIS = { 
    "text_to_image": os.getenv("API_TEXT_TO_IMAGE"),
    "text_to_video": os.getenv("API_TEXT_TO_VIDEO"),
    "voice_cleaner": os.getenv("API_VOICE_CLEANER"),
    "video_cleaner": os.getenv("API_VIDEO_CLEANER"),
    "image_enhancer": os.getenv("API_IMAGE_ENHANCER"),
    "image_converter":os.getenv("API_IMAGE_CONVERTER"),
    "json_processor":os.getenv("API_JSON_PROCESSOR"),
    "pdf_processor":os.getenv("API_PDF_PROCESSOR"),

}

# LLM client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # Fast default model
app_port=os.getenv('PORT', 5000)