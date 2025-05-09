from telegram import Update
from telegram.ext import ContextTypes
from env_config import logger
import tempfile
import subprocess
import os
import io
import asyncio

async def convert_to_gif_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GIF conversion with timeout and optimization"""
    query = update.callback_query
    await query.answer()
    
    file_id = context.user_data.get('last_file_id')
    file_name = context.user_data.get('last_file_name', 'video.mp4')
    
    if not file_id:
        return await query.message.edit_text(
            "❌ No video found to convert. Please send a video first."
        )

    processing_msg = await query.message.edit_text(
        "🎥 *Converting to GIF...*\n\n"
        "Optimizing your video, this might take a moment.\n"
        "☕️ Please wait...",
        parse_mode="Markdown"
    )
    
    try:
        # Download the video file
        file = await context.bot.get_file(file_id)
        video_bytes = await file.download_as_bytearray()

        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_in:
            temp_in.write(video_bytes)
            temp_in_path = temp_in.name

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as temp_out:
            output_path = temp_out.name

        # Optimized ffmpeg command for GIF conversion
        command = [
            "ffmpeg", "-y",
            "-i", temp_in_path,
            "-vf", "scale=480:-1:flags=lanczos,fps=12,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-t", "00:00:10",  # Limit to first 10 seconds
            "-loop", "0",
            output_path
        ]
        
        # Run ffmpeg with timeout
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for completion with timeout
            try:
                await asyncio.wait_for(process.communicate(), timeout=30.0)
            except asyncio.TimeoutError:
                process.kill()
                raise Exception("Conversion timed out - video might be too long or complex")
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg failed with return code {process.returncode}")
            
            # Read and send the converted GIF
            with open(output_path, "rb") as f_out:
                output_bytes = f_out.read()

            # Check file size
            if len(output_bytes) > 50 * 1024 * 1024:  # 50MB limit
                raise Exception("Resulting GIF is too large")

            output_buffer = io.BytesIO(output_bytes)
            output_buffer.seek(0)
            output_name = f"{file_name.rsplit('.', 1)[0]}.gif"

            await query.message.reply_document(
                document=output_buffer,
                filename=output_name,
                caption="✨ *Here's your GIF!*\n\n"
                        "🎯 Optimized for size and quality.\n"
                        "💡 Tip: For better results, try shorter videos!",
                parse_mode="Markdown"
            )
            await processing_msg.delete()

        except asyncio.TimeoutError:
            logger.error("GIF conversion timed out")
            raise Exception("Conversion took too long - try a shorter video")

    except Exception as e:
        logger.error(f"GIF conversion error: {e}")
        await processing_msg.edit_text(
            f"❌ *Conversion Failed*\n\n"
            f"Error: {str(e)}\n\n"
            "Try these tips:\n"
            "• Use a shorter video (under 10 seconds)\n"
            "• Choose a lower quality video\n"
            "• Trim the video before converting",
            parse_mode="Markdown"
        )
    
    finally:
        # Cleanup temporary files
        if 'temp_in_path' in locals() and os.path.exists(temp_in_path):
            os.remove(temp_in_path)
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)