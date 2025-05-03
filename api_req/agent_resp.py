from env_config import logger, DEFAULT_MODEL, groq_client
from system_prompt import AGENT_SYSTEM_PROMPT
import json
import re


async def agent_response(text, user_id=None):
    """Enhanced agent response that understands user intent and guides appropriately"""
    logger.info(f"Agent processing: '{text}'")
    
    try:
        res = groq_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": AGENT_SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.2, max_completion_tokens=500, top_p=1
        )
        logger.info(f"Agent raw response: {res}")
        response_text = res.choices[0].message.content.strip()
        logger.info(f"Agent raw response: {response_text[:100]}...")
        
        # Parse JSON response (handle potential errors)
        try:
            response = json.loads(response_text)
            logger.info(f"Parsed agent response: {response}")
            logger.info(f"Agent intent: {response.get('service')} (confidence: {response.get('confidence')})")
            
            # Add default show_menu value if missing
            if "show_menu" not in response:
                response["show_menu"] = True
                
            return response
        except json.JSONDecodeError as e:
            # If JSON parsing fails, extract what we can using regex
            service_match = re.search(r'"service":\s*"(\w+)"', response_text)
            service = service_match.group(1) if service_match else "chat"
            
            # Extract the response part or use the whole text
            response_match = re.search(r'"response":\s*"([^"]+)"', response_text)
            user_response = response_match.group(1) if response_match else response_text
            logger.error(f"JSON parsing error: {e}")
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


