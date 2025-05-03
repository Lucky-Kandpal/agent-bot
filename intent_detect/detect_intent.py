from env_config import logger, DEFAULT_MODEL, groq_client
from system_prompt import SYSTEM_INTENT_PROMPT

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


