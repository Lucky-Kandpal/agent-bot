
from telegram import Update
from telegram.ext import ContextTypes
from env_config import logger, EXTERNAL_APIS
from memory_storage.all import processing_users, create_or_update_user, is_busy, set_busy, create_request, update_request
from keyboards.build_service_menu import build_service_menu
from api_req.call_external_api import call_external_api
from api_req.chat_resp import chat_response
from api_req.agent_resp import agent_response


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    uid = user.id
    text = update.message.text.strip()
    logger.info(f"Text from {uid}: {text[:30]}...")
    
    # Check if user is busy
    if uid in processing_users or await is_busy(uid):
        logger.info(f"User {uid} is busy. Ignoring new request.")
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
        logger.debug(f"Reply to user: {reply}")
        await processing_msg.delete()
        return await update.message.reply_text(
            reply, 
            reply_markup=build_service_menu() if show_menu else None
        )
    
    # Specific service handling (when service was previously selected)
    if svc in ('image', 'video'):
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


