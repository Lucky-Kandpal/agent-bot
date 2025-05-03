from env_config import logger
import httpx



# ------ External APIs ------
def call_external_api(api_url, files=None, json=None):
    logger.info(f"Calling API: {api_url}")
    if files:
        logger.debug(f"Files being sent: {files}")
    if json:
        logger.debug(f"JSON being sent: {json}")
    try:
        r = httpx.post(api_url, files=files, json=json)
        logger.info(f"API response status: {r.status_code}")
        logger.debug(f"API response content: {r.text}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"API error: {e}")
        return {"error": str(e)}
