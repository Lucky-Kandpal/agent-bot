from telegram import Update
from telegram.ext import ContextTypes
from env_config import logger
import io
from PIL import Image
import zipfile
from api_req.call_external_api import call_external_api
from env_config import EXTERNAL_APIS

async def convert_to_pdf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    file_id = context.user_data.get('last_file_id')
    file_name = context.user_data.get('last_file_name', 'image.jpg')
    original_message_id = query.message.reply_to_message.message_id if query.message.reply_to_message else query.message.message_id
    
    if not file_id:
        return await query.edit_message_text("❌ Could not find the image to convert.")

    processing_msg = await query.message.edit_text(
        "🎨 *Processing your image...*\n\n"
        "Converting to PDF format. This will just take a moment!\n"
        "☕️ Please wait...",
        parse_mode="Markdown"
    )
    
    try:
        # Download and convert image
        file = await context.bot.get_file(file_id)
        image_bytes = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(image_bytes))
        
        pdf_buffer = io.BytesIO()
        img.convert('RGB').save(pdf_buffer, format='PDF')
        pdf_buffer.seek(0)
        pdf_name = f"{file_name.rsplit('.', 1)[0]}.pdf"
        
        # Send final PDF
        await query.message.reply_document(
            document=pdf_buffer,
            filename=pdf_name,
            caption=(
                "✨ *Here's your PDF!*\n\n"
                "📄 Successfully converted your image.\n"
                "🎯 Quality has been optimized for best results.\n\n"
                "Need anything else? Just send me another image! 😊"
            ),
            parse_mode="Markdown",
            reply_to_message_id=original_message_id
        )
        # Clean up
        await processing_msg.delete()
        
    except Exception as e:
        logger.error(f"PDF conversion error: {e}")
        await query.message.edit_text(
            "❌ *Conversion Failed*\n\n"
            "Sorry, I couldn't convert your image to PDF.\n"
            "Please try again with a different image or format.",
            parse_mode="Markdown"
        )

async def convert_to_zip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    file_id = context.user_data.get('last_file_id')
    file_name = context.user_data.get('last_file_name', 'image')
    original_message_id = query.message.reply_to_message.message_id if query.message.reply_to_message else query.message.message_id
    
    if not file_id:
        return await query.edit_message_text("❌ Could not find the image to convert.")
    
    await query.message.edit_text(
        "📦 *Creating ZIP archive...*\n"
        "Compressing your image, please wait...",
        parse_mode="Markdown"
    )
    
    try:
        file = await context.bot.get_file(file_id)
        image_bytes = await file.download_as_bytearray()
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            zf.writestr(file_name, image_bytes)
        
        zip_buffer.seek(0)
        zip_name = f"{file_name.rsplit('.', 1)[0]}.zip"
        
        await query.message.reply_document(
            document=zip_buffer,
            filename=zip_name,
            caption=(
                "📦 *Here's your ZIP archive!*\n\n"
                "Successfully compressed your image.\n"
                "Need anything else? Just send me another file! 😊"
            ),
            parse_mode="Markdown",
            reply_to_message_id=original_message_id
        )
        await query.message.delete()
        
    except Exception as e:
        logger.error(f"ZIP creation error: {e}")
        await query.message.edit_text(
            "❌ *Compression Failed*\n\n"
            "Sorry, I couldn't create the ZIP archive.\n"
            "Please try again with a different image.",
            parse_mode="Markdown"
        )

async def convert_to_png_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    file_id = context.user_data.get('last_file_id')
    file_name = context.user_data.get('last_file_name', 'image.jpg')
    original_message_id = query.message.reply_to_message.message_id if query.message.reply_to_message else query.message.message_id
    
    if not file_id:
        return await query.edit_message_text("❌ Could not find the image to convert.")
    
    await query.message.edit_text(
        "🖼️ *Converting to PNG...*\n"
        "Processing your image, please wait...",
        parse_mode="Markdown"
    )
    
    try:
        file = await context.bot.get_file(file_id)
        image_bytes = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(image_bytes))
        
        png_buffer = io.BytesIO()
        img.save(png_buffer, format='PNG')
        png_buffer.seek(0)
        png_name = f"{file_name.rsplit('.', 1)[0]}.png"
        
        await query.message.reply_document(
            document=png_buffer,
            filename=png_name,
            caption=(
                "✨ *Here's your PNG image!*\n\n"
                "🖼️ Successfully converted with preserved quality.\n"
                "Need anything else? Just send me another image! 😊"
            ),
            parse_mode="Markdown",
            reply_to_message_id=original_message_id
        )
        await query.message.delete()
        
    except Exception as e:
        logger.error(f"PNG conversion error: {e}")
        await query.message.edit_text(
            "❌ *Conversion Failed*\n\n"
            "Sorry, I couldn't convert to PNG.\n"
            "Please try again with a different image.",
            parse_mode="Markdown"
        )

async def convert_to_jpg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    file_id = context.user_data.get('last_file_id')
    file_name = context.user_data.get('last_file_name', 'image.png')
    original_message_id = query.message.reply_to_message.message_id if query.message.reply_to_message else query.message.message_id
    
    if not file_id:
        return await query.edit_message_text("❌ Could not find the image to convert.")
    
    await query.message.edit_text(
        "🖼️ *Converting to JPG...*\n"
        "Processing your image, please wait...",
        parse_mode="Markdown"
    )
    
    try:
        file = await context.bot.get_file(file_id)
        image_bytes = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(image_bytes))
        
        jpg_buffer = io.BytesIO()
        img.convert('RGB').save(jpg_buffer, format='JPEG', quality=95)
        jpg_buffer.seek(0)
        jpg_name = f"{file_name.rsplit('.', 1)[0]}.jpg"
        
        await query.message.reply_document(
            document=jpg_buffer,
            filename=jpg_name,
            caption=(
                "✨ *Here's your JPG image!*\n\n"
                "🖼️ Successfully converted with optimized quality.\n"
                "Need anything else? Just send me another image! 😊"
            ),
            parse_mode="Markdown",
            reply_to_message_id=original_message_id
        )
        await query.message.delete()
        
    except Exception as e:
        logger.error(f"JPG conversion error: {e}")
        await query.message.edit_text(
            "❌ *Conversion Failed*\n\n"
            "Sorry, I couldn't convert to JPG.\n"
            "Please try again with a different image.",
            parse_mode="Markdown"
        )

async def convert_to_webp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    file_id = context.user_data.get('last_file_id')
    file_name = context.user_data.get('last_file_name', 'image')
    original_message_id = query.message.reply_to_message.message_id if query.message.reply_to_message else query.message.message_id
    
    if not file_id:
        return await query.edit_message_text("❌ Could not find the image to convert.")
    
    await query.message.edit_text(
        "🌐 *Converting to WebP...*\n"
        "Processing your image, please wait...",
        parse_mode="Markdown"
    )
    
    try:
        file = await context.bot.get_file(file_id)
        image_bytes = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(image_bytes))
        
        webp_buffer = io.BytesIO()
        img.save(webp_buffer, format='WebP', quality=95)
        webp_buffer.seek(0)
        webp_name = f"{file_name.rsplit('.', 1)[0]}.webp"
        
        await query.message.reply_document(
            document=webp_buffer,
            filename=webp_name,
            caption=(
                "✨ *Here's your WebP image!*\n\n"
                "🌐 Successfully converted with web optimization.\n"
                "Need anything else? Just send me another image! 😊"
            ),
            parse_mode="Markdown",
            reply_to_message_id=original_message_id
        )
        await query.message.delete()
        
    except Exception as e:
        logger.error(f"WebP conversion error: {e}")
        await query.message.edit_text(
            "❌ *Conversion Failed*\n\n"
            "Sorry, I couldn't convert to WebP.\n"
            "Please try again with a different image.",
            parse_mode="Markdown"
        )