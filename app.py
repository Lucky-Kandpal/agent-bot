import os
import logging
import httpx
import json
import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Config
token = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
EXTERNAL_APIS = {
    "text_to_image": os.getenv("API_TEXT_TO_IMAGE"),
    "text_to_video": os.getenv("API_TEXT_TO_VIDEO"),
    "voice_cleaner": os.getenv("API_VOICE_CLEANER"),
    "video_cleaner": os.getenv("API_VIDEO_CLEANER"),
}

# LLM client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # Fast default model

# Prompt templates
SYSTEM_INTENT_PROMPT = """
You are an assistant that classifies user requests into specific service categories. 
Respond with exactly one of: 'image', 'video', 'clean_audio', 'clean_video', 'chat', 'unknown'.
"""

SYSTEM_CHAT_PROMPT = """
You are a helpful AI assistant for a Telegram bot called ViralBoost that offers various media services:
- Image generation from text prompts (costs 10 coins)
- Video generation from text prompts (costs 10 coins)
- Audio cleaning/enhancement (costs 10 coins)
- Video cleaning/enhancement (costs 10 coins)
- Free text chat (which you're providing now)

When users ask about these services, explain them briefly along with their cost.
When users ask general questions, answer helpfully and concisely using simple, easy language.
If asked about your capabilities, mention you can help with media creation, media enhancement, and answer questions.

Keep responses friendly, helpful and under 150 tokens when possible.
"""

AGENT_SYSTEM_PROMPT = """
You are an agentic assistant that helps users understand what they want, then guides them to the right service.
Available services:
1. Image generation from text (costs 10 coins)
2. Video generation from text (costs 10 coins)
3. Audio cleaning/enhancement (costs 10 coins)
4. Video cleaning/enhancement (costs 10 coins)
5. Free text chat for general questions

Think step by step to understand what the user wants, then recommend the specific service they need.
If the user is asking an educational question like "how does ChatGPT work?" or similar general knowledge questions, 
label it as "chat" with high confidence and provide a simple, easy-to-understand answer without suggesting services.

Your response should follow this JSON format:
{
  "thought": "Your internal reasoning about what the user wants",
  "service": "image|video|clean_audio|clean_video|chat|unknown",
  "confidence": 0-100,
  "response": "Your helpful response to the user explaining what they should do next",
  "show_menu": true|false
}

Set "show_menu" to false for pure informational queries where offering services would be inappropriate.
Set "show_menu" to true when the user might benefit from seeing service options.
"""

# Firebase setup
cred = credentials.Certificate("./viralboost-a9b2c-firebase-adminsdk-osgd2-af2a69fa3a.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Track processing state
processing_users = set()

# ------ Firestore helpers ------
def create_or_update_user(user):
    logger.info(f"Upserting user {user.id}")
    ref = db.collection("users").document(str(user.id))
    base = {
        "full_name": user.full_name,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
        "is_bot": user.is_bot,
        "last_activity": firestore.SERVER_TIMESTAMP,
    }
    if not ref.get().exists:
        base.update({"wallet_balance": 100, "busy": False, "created_at": firestore.SERVER_TIMESTAMP})
        logger.info(f"Created wallet for {user.id} with 100 coins")
    ref.set(base, merge=True)

async def deduct_wallet(user_id, amount):
    ref = db.collection("users").document(str(user_id))
    doc = ref.get()
    if doc.exists:
        bal = doc.to_dict().get("wallet_balance", 0)
        if bal >= amount:
            ref.update({
                "wallet_balance": bal - amount,
                "total_spent": firestore.Increment(amount)
            })
            db.collection("transactions").add({
                "user_id": str(user_id), "amount": -amount,
                "type": "service_payment", "balance_after": bal - amount,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            logger.info(f"Deducted {amount} from {user_id}, new balance {bal-amount}")
            return True
        logger.info(f"Insufficient balance for {user_id}: {bal}")
    return False

async def get_balance(user_id):
    """Get user's current balance"""
    doc = db.collection("users").document(str(user_id)).get()
    if doc.exists:
        return doc.to_dict().get("wallet_balance", 0)
    return 0

async def is_busy(user_id):
    busy = (db.collection("users").document(str(user_id)).get().to_dict() or {}).get("busy", False)
    logger.debug(f"User {user_id} busy={busy}")
    return busy

async def set_busy(user_id, busy):
    db.collection("users").document(str(user_id)).update({"busy": busy})
    logger.debug(f"Set busy={busy} for {user_id}")

# ------ Request tracking ------
def create_request(uid, service, input_text=None, file_type=None):
    ref = db.collection("requests").document()
    ref.set({
        "user_id": uid, "service": service,
        "input_text": input_text, "file_type": file_type,
        "status": "pending", "created_at": firestore.SERVER_TIMESTAMP
    })
    logger.info(f"Request {ref.id} created: {service} by {uid}")
    return ref.id

def update_request(rid, status, output_url=None, error=None):
    data = {"status": status, "updated_at": firestore.SERVER_TIMESTAMP}
    if output_url: data["output_url"] = output_url
    if error: data["error"] = error
    db.collection("requests").document(rid).update(data)
    logger.info(f"Request {rid} updated: {status}")

# ------ External APIs ------
def call_external_api(api_url, files=None, json=None):
    logger.info(f"Calling API: {api_url}")
    try:
        r = httpx.post(api_url, files=files, json=json)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"API error: {e}")
        return {"error": str(e)}

# ------ LLM utilities ------
def detect_intent(text):
    logger.info(f"Detecting intent for: '{text}'")
    try:
        res = groq_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "system", "content": SYSTEM_INTENT_PROMPT}, {"role": "user", "content": text}],
            temperature=0.0, max_completion_tokens=10, top_p=1
        )
        intent = res.choices[0].message.content.strip().lower()
        logger.info(f"Intent: {intent}")
        return intent
    except Exception as e:
        logger.error(f"Intent detection failed: {e}")
        return "unknown"

def chat_response(text):
    logger.info(f"Chat response for: '{text}'")
    try:
        res = groq_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "system", "content": SYSTEM_CHAT_PROMPT}, {"role": "user", "content": text}],
            temperature=0.7, max_completion_tokens=250, top_p=1
        )
        reply = res.choices[0].message.content.strip()
        logger.info(f"Chatbot replied: {len(reply)} chars")
        return reply
    except Exception as e:
        logger.error(f"Chat response failed: {e}")
        return "I'm having trouble connecting to my AI service right now. Please try again in a moment."

async def agent_response(text, user_id=None):
    """Enhanced agent response that understands user intent and guides appropriately"""
    logger.info(f"Agent processing: '{text}'")
    context = ""
    
    # Add user context if provided
    if user_id:
        balance = await get_balance(user_id)
        context = f"This user has {balance} coins in their wallet. "
    
    try:
        res = groq_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": AGENT_SYSTEM_PROMPT + context},
                {"role": "user", "content": text}
            ],
            temperature=0.2, max_completion_tokens=500, top_p=1
        )
        response_text = res.choices[0].message.content.strip()
        logger.info(f"Agent raw response: {response_text[:100]}...")
        
        # Parse JSON response (handle potential errors)
        try:
            response = json.loads(response_text)
            logger.info(f"Agent intent: {response.get('service')} (confidence: {response.get('confidence')})")
            
            # Add default show_menu value if missing
            if "show_menu" not in response:
                response["show_menu"] = True
                
            return response
        except json.JSONDecodeError:
            # If JSON parsing fails, extract what we can using regex
            service_match = re.search(r'"service":\s*"(\w+)"', response_text)
            service = service_match.group(1) if service_match else "chat"
            
            # Extract the response part or use the whole text
            response_match = re.search(r'"response":\s*"([^"]+)"', response_text)
            user_response = response_match.group(1) if response_match else response_text
            
            return {
                "service": service,
                "confidence": 70,
                "response": user_response,
                "show_menu": True
            }
    except Exception as e:
        logger.error(f"Agent response failed: {e}")
        return {
            "service": "chat",
            "confidence": 100,
            "response": "I'm having trouble understanding your request right now. Could you try again or select a specific service from the menu?",
            "show_menu": True
        }

# ------ UI Keyboard ------
def build_service_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Image", callback_data="svc_image"), InlineKeyboardButton("📹 Video", callback_data="svc_video")],
        [InlineKeyboardButton("🎧 Clean Audio", callback_data="svc_clean_audio"), InlineKeyboardButton("🎬 Clean Video", callback_data="svc_clean_video")],
        [InlineKeyboardButton("💬 Chat (free)", callback_data="svc_chat"), InlineKeyboardButton("💰 Wallet", callback_data="svc_wallet")],
        [InlineKeyboardButton("❓ Help", callback_data="svc_help")]
    ])

# ------ Handlers ------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    create_or_update_user(user)
    logger.info(f"/start by {user.id}")
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋\n\nI'm ViralBoost, your media enhancement assistant. I can help you generate images, videos, and clean up audio/video files.\n\nUse the menu below or just tell me what you'd like to do:",
        reply_markup=build_service_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    create_or_update_user(user)
    logger.info(f"/help by {user.id}")
    
    help_text = (
        "🤖 *ViralBoost Bot Help*\n\n"
        "*Available Services:*\n"
        "• 🖼 *Image Generation* - Create images from text descriptions (10 coins)\n"
        "• 📹 *Video Generation* - Create short videos from text prompts (10 coins)\n"
        "• 🎧 *Audio Cleaning* - Enhance and clean audio files (10 coins)\n"
        "• 🎬 *Video Cleaning* - Enhance and clean video files (10 coins)\n"
        "• 💬 *Chat* - Ask questions or get help (Free)\n\n"
        "*Commands:*\n"
        "• /start - Show main menu\n"
        "• /wallet - Check your balance\n"
        "• /history - View your request history\n"
        "• /help - Show this help message\n\n"
        "You can also just type your request and I'll try to understand what you need!"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown", reply_markup=build_service_menu())

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    create_or_update_user(user)
    bal = (db.collection("users").document(str(user.id)).get().to_dict() or {}).get("wallet_balance", 0)
    logger.info(f"/wallet {user.id} -> {bal}")
    
    wallet_text = (
        f"💰 *Your Wallet*\n\n"
        f"Balance: *{bal} coins*\n\n"
        f"*Service costs:*\n"
        f"• Image generation: 10 coins\n"
        f"• Video generation: 10 coins\n"
        f"• Audio cleaning: 10 coins\n"
        f"• Video cleaning: 10 coins\n"
        f"• Chat: Free"
    )
    
    await update.message.reply_text(wallet_text, parse_mode="Markdown")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    create_or_update_user(update.message.from_user)
    docs = db.collection("requests").where("user_id","==",str(uid)).order_by("created_at",firestore.Query.DESCENDING).limit(5).stream()
    
    lines = ["📜 *Your Recent Requests*\n"]
    for d in docs:
        x = d.to_dict(); t = x.get('created_at'); ts = t.strftime("%Y-%m-%d %H:%M") if isinstance(t, datetime) else str(t)
        status_emoji = "✅" if x['status'] == 'done' else "❌" if x['status'] == 'failed' else "⏳"
        lines.append(f"• {status_emoji} {x['service']} - {ts}")
    
    logger.info(f"/history {uid} -> {len(lines)-1} items")
    await update.message.reply_text("\n".join(lines) if len(lines) > 1 else "No request history found.", parse_mode="Markdown")

async def topup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    create_or_update_user(user)
    logger.info(f"/topup by {user.id}")
    if user.id not in [123456789]:  # Admin IDs
        return await update.message.reply_text("❌ Not authorized.")
    
    # Simple admin top-up interface
    await update.message.reply_text(
        "💰 *Admin Top-up Panel*\n\nReply with: `topup <user_id> <amount>`",
        parse_mode="Markdown"
    )

async def process_topup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user.id not in [123456789]:  # Admin IDs
        return
        
    text = update.message.text
    if not text.startswith("topup "):
        return
        
    parts = text.split()
    if len(parts) != 3:
        return await update.message.reply_text("❌ Format: `topup <user_id> <amount>`", parse_mode="Markdown")
        
    try:
        target_id = parts[1]
        amount = int(parts[2])
        
        # Add coins to user
        user_ref = db.collection("users").document(target_id)
        if not user_ref.get().exists:
            return await update.message.reply_text("❌ User not found")
            
        current = user_ref.get().to_dict().get("wallet_balance", 0)
        user_ref.update({"wallet_balance": current + amount})
        
        # Record transaction
        db.collection("transactions").add({
            "user_id": target_id,
            "amount": amount,
            "type": "admin_topup",
            "admin_id": str(user.id),
            "balance_after": current + amount,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        
        logger.info(f"Admin {user.id} topped up {target_id} with {amount} coins")
        await update.message.reply_text(f"✅ Added {amount} coins to user {target_id}")
    except Exception as e:
        logger.error(f"Topup error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def menu_route(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    user = q.from_user
    data = q.data
    await q.answer()
    
    create_or_update_user(user)
    logger.info(f"Callback '{data}' by {user.id}")
    
    # Check if user is busy with another task
    if user.id in processing_users or await is_busy(user.id):
        await q.message.reply_text("⏳ I'm still processing your previous request. Please wait until it completes.")
        return
    
    if data == 'svc_back':
        return await q.edit_message_text(
            "Main Menu - Select a service or just ask me what you need:",
            reply_markup=build_service_menu()
        )
    
    if data == 'svc_wallet':
        bal = (db.collection("users").document(str(user.id)).get().to_dict() or {}).get("wallet_balance", 0)
        return await q.edit_message_text(
            f"💰 *Your Wallet*\n\nBalance: *{bal} coins*\n\nPaid services cost 10 coins per use.",
            parse_mode="Markdown"
        )
    
    if data == 'svc_chat':
        context.user_data['svc'] = 'chat'
        return await q.edit_message_text(
            "💬 *Chat Mode Activated*\n\nYou can now chat with me for free. Ask me anything!",
            parse_mode="Markdown"
        )
    
    if data == 'svc_help':
        help_text = (
            "🤖 *ViralBoost Bot Help*\n\n"
            "*Available Services:*\n"
            "• 🖼 *Image Generation* - Create images from text descriptions (10 coins)\n"
            "• 📹 *Video Generation* - Create short videos from text prompts (10 coins)\n"
            "• 🎧 *Audio Cleaning* - Enhance and clean audio files (10 coins)\n"
            "• 🎬 *Video Cleaning* - Enhance and clean video files (10 coins)\n"
            "• 💬 *Chat* - Ask questions or get help (Free)\n\n"
            "*Commands:*\n"
            "• /start - Show main menu\n"
            "• /wallet - Check your balance\n"
            "• /history - View your request history\n"
            "• /help - Show this help message"
        )
        return await q.edit_message_text(help_text, parse_mode="Markdown", reply_markup=build_service_menu())
    
    svc = data.replace('svc_', '')
    context.user_data['svc'] = svc
    
    prompts = {
        'image': '🖼 *Image Generation*\n\nSend a text prompt describing the image you want to create.\n\nThis will cost 10 coins.',
        'video': '📹 *Video Generation*\n\nSend a text prompt describing the video you want to create.\n\nThis will cost 10 coins.',
        'clean_audio': '🎧 *Audio Cleaning*\n\nUpload an audio file or voice message to enhance.\n\nThis will cost 10 coins.',
        'clean_video': '🎬 *Video Cleaning*\n\nUpload a video file to enhance.\n\nThis will cost 10 coins.'
    }
    
    # Add a back button
    keyboard = [[InlineKeyboardButton("↩️ Back to Menu", callback_data="svc_back")]]
    
    return await q.edit_message_text(
        prompts.get(svc, 'Select an option.'), 
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    uid = user.id
    text = update.message.text.strip()
    logger.info(f"Text from {uid}: {text[:30]}...")
    
    # Handle admin commands
    if text.startswith("topup ") and uid in [123456789]:
        return await process_topup(update, context)
    
    # Check if user is busy
    if uid in processing_users or await is_busy(uid):
        return await update.message.reply_text("⏳ Please wait, I'm still processing your previous request...")
    
    create_or_update_user(user)
    svc = context.user_data.pop('svc', None)
    
    # Add a processing indicator
    processing_msg = await update.message.reply_text("🔄 Processing your request...")
    
    # If in chat mode or no specific service was selected
    if svc == 'chat' or not svc:
        # Use the agent to determine what the user wants
        agent_result = await agent_response(text, uid)
        intent = agent_result.get('service', 'chat')
        confidence = agent_result.get('confidence', 0)
        show_menu = agent_result.get('show_menu', True)
        
        logger.info(f"Agent determined service: {intent} with confidence {confidence}, show_menu: {show_menu}")
        
        # If high confidence and not chat/unknown, process as service
        if intent in ('image', 'video', 'clean_audio', 'clean_video') and confidence > 80:
            # Show service-specific instructions for file uploads
            if intent in ('clean_audio', 'clean_video'):
                await processing_msg.delete()
                return await update.message.reply_text(
                    f"To clean {'audio' if intent == 'clean_audio' else 'video'}, please upload the file you want to enhance.",
                    reply_markup=build_service_menu() if show_menu else None
                )
                
            # Process text-to-media services
            if intent in ('image', 'video'):
                # Check wallet balance
                if not await deduct_wallet(uid, 10):
                    await processing_msg.delete()
                    return await update.message.reply_text(
                        "💸 You need 10 coins for this service. Check /wallet for your balance.",
                        reply_markup=build_service_menu() if show_menu else None
                    )
                
                # Process the request
                processing_users.add(uid)
                await set_busy(uid, True)
                rid = create_request(uid, intent, input_text=text)
                
                try:
                    api = EXTERNAL_APIS['text_to_image'] if intent == 'image' else EXTERNAL_APIS['text_to_video']
                    res = call_external_api(api, json={'text': text})
                    url = res.get('url')
                    
                    if url:
                        update_request(rid, 'done', output_url=url)
                        await processing_msg.delete()
                        if intent == 'image':
                            return await update.message.reply_photo(url, caption="Here's your generated image!")
                        else:
                            return await update.message.reply_video(url, caption="Here's your generated video!")
                    
                    update_request(rid, 'failed', error=res.get('error'))
                    await processing_msg.delete()
                    return await update.message.reply_text(f"❌ Error: {res.get('error', 'Something went wrong')}")
                finally:
                    processing_users.discard(uid)
                    await set_busy(uid, False)
        
        # For chat or low confidence, respond with agent's response
        reply = agent_result.get('response', chat_response(text))
        await processing_msg.delete()
        return await update.message.reply_text(
            reply, 
            reply_markup=build_service_menu() if show_menu else None
        )
    
    # Specific service handling (when service was previously selected)
    if svc in ('image', 'video'):
        # Check wallet
        if not await deduct_wallet(uid, 10):
            await processing_msg.delete()
            return await update.message.reply_text("💸 You need 10 coins. Check /wallet.")
        
        processing_users.add(uid)
        await set_busy(uid, True)
        rid = create_request(uid, svc, input_text=text)
        
        try:
            api = EXTERNAL_APIS['text_to_image'] if svc == 'image' else EXTERNAL_APIS['text_to_video']
            res = call_external_api(api, json={'text': text})
            url = res.get('url')
            
            if url:
                update_request(rid, 'done', output_url=url)
                await processing_msg.delete()
                if svc == 'image':
                    return await update.message.reply_photo(url, caption="Here's your generated image!")
                else:
                    return await update.message.reply_video(url, caption="Here's your generated video!")
            
            update_request(rid, 'failed', error=res.get('error'))
            await processing_msg.delete()
            return await update.message.reply_text(f"❌ Error: {res.get('error', 'Something went wrong')}")
        finally:
            processing_users.discard(uid)
            await set_busy(uid, False)
    
    # Default fallback
    await processing_msg.delete()
    return await update.message.reply_text(
        "I didn't understand. Please select a service from the menu or ask me a question.",
        reply_markup=build_service_menu()
    )

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    uid = user.id
    logger.info(f"Media from {uid}")
    
    if uid in processing_users or await is_busy(uid):
        return await update.message.reply_text("⏳ Please wait, I'm still processing your previous request...")
    
    create_or_update_user(user)
    
    # Add processing indicator
    processing_msg = await update.message.reply_text("🔄 Receiving your file...")
    
    # Get file from various sources
    f = update.message.audio or update.message.voice or update.message.video or update.message.document
    
    if not f:
        logger.warning(f"Unknown media type from {uid}")
        await processing_msg.delete()
        return await update.message.reply_text(
            "Unsupported file type. I can process audio, video, and voice messages only.",
            reply_markup=build_service_menu()
        )
    
    # Check for unsupported file types
    if hasattr(f, 'mime_type'):
        mime_type = f.mime_type
        if mime_type and (mime_type.startswith('application/') or mime_type in ['application/pdf', 'application/json']):
            logger.info(f"Unsupported file type: {mime_type}")
            await processing_msg.delete()
            return await update.message.reply_text(
                f"Sorry, I can't process {mime_type} files. I can only work with audio and video files for enhancement. "
                f"For text content in documents, you can try typing your question or request directly.",
                reply_markup=build_service_menu()
            )
    
    caption = (update.message.caption or '').lower()
    
    # If no caption, suggest services based on file type
    if not caption:
        kb = []
        if hasattr(f, 'mime_type') and f.mime_type:
            if f.mime_type.startswith('audio/') or isinstance(f, type(update.message.voice)):
                kb.append([InlineKeyboardButton('🎧 Clean Audio', callback_data='svc_clean_audio')])
            if f.mime_type.startswith('video/'):
                kb.append([InlineKeyboardButton('🎬 Clean Video', callback_data='svc_clean_video')])
        kb.append([InlineKeyboardButton('↩️ Back to Menu', callback_data='svc_back')])
        
        await processing_msg.delete()
        return await update.message.reply_text(
            "What would you like to do with this file?", 
            reply_markup=InlineKeyboardMarkup(kb)
        )
    
    # Determine intent from caption or context
    # Determine intent from caption or context
    svc = context.user_data.pop('svc', None)
    file_is_audio = (hasattr(f, 'mime_type') and f.mime_type and f.mime_type.startswith('audio/')) or isinstance(f, type(update.message.voice))
    file_is_video = hasattr(f, 'mime_type') and f.mime_type and f.mime_type.startswith('video/')
    
    # Determine the appropriate service based on file type
    if 'clean' in caption or svc in ('clean_audio', 'clean_video'):
        intent = 'clean_audio' if file_is_audio else 'clean_video' if file_is_video else None
        
        if not intent:
            await processing_msg.delete()
            return await update.message.reply_text(
                "I can't determine the file type. I can process audio or video files only.",
                reply_markup=build_service_menu()
            )
        
        # Check wallet
        if not await deduct_wallet(uid, 10):
            await processing_msg.delete()
            return await update.message.reply_text(
                "💸 You need 10 coins for cleaning services. Check /wallet.",
                reply_markup=build_service_menu()
            )
        
        processing_users.add(uid)
        await set_busy(uid, True)
        
        try:
            file_obj = await f.get_file()
            bio = await file_obj.download_as_bytearray()
            mime = f.mime_type if hasattr(f, 'mime_type') else 'audio/ogg' if file_is_audio else 'video/mp4'
            
            api = EXTERNAL_APIS['voice_cleaner'] if intent == 'clean_audio' else EXTERNAL_APIS['video_cleaner']
            send_fn = update.message.reply_voice if intent == 'clean_audio' else update.message.reply_video
            
            rid = create_request(uid, intent, file_type=mime)
            
            # Update processing message
            await processing_msg.edit_text(f"🔄 Enhancing your {'audio' if intent == 'clean_audio' else 'video'}...")
            
            try:
                res = call_external_api(api, files={'file': (file_obj.file_unique_id, bio, mime)})
                url = res.get('cleaned_url') or res.get('url')
                
                if url:
                    update_request(rid, 'done', output_url=url)
                    await processing_msg.delete()
                    return await send_fn(
                        url, 
                        caption=f"Here's your enhanced {'audio' if intent == 'clean_audio' else 'video'}!"
                    )
                
                update_request(rid, 'failed', error=res.get('error'))
                await processing_msg.delete()
                return await update.message.reply_text(f"❌ Error: {res.get('error', 'Something went wrong')}")
            except Exception as e:
                logger.error(f"API processing error: {str(e)}")
                update_request(rid, 'failed', error=str(e))
                await processing_msg.delete()
                return await update.message.reply_text("❌ Error processing your file. Please try again later.")
        finally:
            processing_users.discard(uid)
            await set_busy(uid, False)
    else:
        await processing_msg.delete()
        return await update.message.reply_text(
            "I'm not sure what you want me to do with this file. Would you like me to clean/enhance it?",
            reply_markup=build_service_menu()
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for document files (PDF, JSON, etc.)"""
    user = update.message.from_user
    uid = user.id
    logger.info(f"Document from {uid}")
    
    if uid in processing_users or await is_busy(uid):
        return await update.message.reply_text("⏳ Please wait, I'm still processing your previous request...")
    
    create_or_update_user(user)
    doc = update.message.document
    
    if not doc:
        return
    
    mime_type = doc.mime_type if hasattr(doc, 'mime_type') else "unknown"
    
    # Handle unsupported file types with friendly message
    if mime_type in ['application/pdf', 'application/json', 'text/plain', 'application/msword',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        file_type = mime_type.split('/')[-1].upper()
        
        return await update.message.reply_text(
            f"I notice you've uploaded a {file_type} file. Currently, I can't process this file type for enhancement.\n\n"
            f"Here's what I can do for you instead:\n"
            f"• Generate images from text descriptions (10 coins)\n"
            f"• Generate videos from text prompts (10 coins)\n"
            f"• Clean and enhance audio files (10 coins)\n"
            f"• Clean and enhance video files (10 coins)\n"
            f"• Answer your questions via chat (free)\n\n"
            f"Would you like to try one of these services instead?",
            reply_markup=build_service_menu()
        )
    
    # For other document types, let the media handler try to process it
    # This handles audio/video files sent as documents
    await handle_media(update, context)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles any command that doesn't match the registered handlers."""
    logger.warning(f"Received unknown command from user {update.effective_user.id}")
    await update.message.reply_text(
        "I don't recognize that command. Try /help to see what I can do.",
        reply_markup=build_service_menu()
    )


# Entry point
def main():
    app = ApplicationBuilder().token(token).build()
    
    # Command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('wallet', wallet))
    app.add_handler(CommandHandler('history', history))
    app.add_handler(CommandHandler('topup', topup))
    
    # Interactive handlers
    app.add_handler(CallbackQueryHandler(menu_route))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.VIDEO, handle_media))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    # Start the bot using webhook
    logger.info("Starting webhook...")
    app.run_webhook(
        listen='0.0.0.0', 
        port=5000, 
        url_path='/webhook', 
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

if __name__ == '__main__':
    main()