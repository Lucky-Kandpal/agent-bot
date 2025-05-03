
from env_config import logger
from env_config import groq_client, DEFAULT_MODEL
from system_prompt import SYSTEM_CHAT_PROMPT


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


