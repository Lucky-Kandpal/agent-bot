
from telegram import Update
from telegram.ext import ContextTypes

from env_config import EXTERNAL_APIS
from api_req.call_external_api import call_external_api
from env_config import logger



async def convert_image_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()
    
    logger.info(f"Converting image for user {user.id}")
    
    # Try both possible file ID keys
    file_id = (
        context.user_data.get('last_file_id') or 
        context.user_data.get('last_photo_file_id')
    )
    
    if not file_id:
        logger.error(f"No file_id found in user_data for user {user.id}")
        return await query.edit_message_text(
            "❌ Could not find the photo to convert. Please send the image again."
        )

    try:
        logger.info(f"Downloading file {file_id}")
        tg_file = await context.bot.get_file(file_id)
        bio = await tg_file.download_as_bytearray()
        
        logger.info("Calling image converter API")
        api = EXTERNAL_APIS['image_converter']
        res = call_external_api(api, files={'file': (file_id, bio, 'image/jpeg')})
        
        url = res.get('converted_url')
        if not url:
            logger.error(f"No URL in API response: {res}")
            return await query.edit_message_text(
                "❌ Conversion failed: API returned no URL. Please try again."
            )

        logger.info(f"Successfully converted image, URL: {url[:50]}...")
        await query.edit_message_caption("🔄 Converting image…")
        
        # Send converted file
        doc = await query.message.reply_document(
            url, 
            filename="converted_image.jpg",
            caption="✨ Here's your converted image!"
        )
        logger.info(f"Sent converted file to user {user.id}")
        return doc

    except Exception as e:
        logger.error(f"Image conversion failed for user {user.id}: {str(e)}", exc_info=True)
        return await query.edit_message_text(
            f"❌ Conversion failed: {str(e)}. Please try again."
        )