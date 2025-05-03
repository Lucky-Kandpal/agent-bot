
from datetime import datetime
from env_config import logger
import uuid

# In-memory storage
users = {}  # Store user data
requests = {}  # Store request data
processing_users = set()  # Track processing state



async def is_busy(user_id):
    busy = users.get(str(user_id), {}).get("busy", False)
    logger.debug(f"User {user_id} busy={busy}")
    return busy

async def set_busy(user_id, busy):
    if str(user_id) in users:
        users[str(user_id)]["busy"] = busy
        logger.debug(f"Set busy={busy} for {user_id}")




# ------ Request tracking ------
def create_request(uid, service, input_text=None, file_type=None):
    request_id = str(uuid.uuid4())
    requests[request_id] = {
        "user_id": uid,
        "service": service,
        "input_text": input_text,
        "file_type": file_type,
        "status": "pending",
        "created_at": datetime.now()
    }
    logger.info(f"Request {request_id} created: {service} by {uid}")
    return request_id




def update_request(rid, status, output_url=None, error=None):
    if rid in requests:
        requests[rid]["status"] = status
        requests[rid]["updated_at"] = datetime.now()
        if output_url:
            requests[rid]["output_url"] = output_url
        if error:
            requests[rid]["error"] = error
        logger.info(f"Request {rid} updated: {status}")





# ------ In-memory storage helpers ------
def create_or_update_user(user):
    logger.info(f"Upserting user {user.id}")
    
    # Create or update user in the in-memory dictionary
    if str(user.id) not in users:
        users[str(user.id)] = {
            "full_name": user.full_name,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "language_code": user.language_code,
            "is_bot": user.is_bot,
            "busy": False,
            "last_activity": datetime.now(),
            "created_at": datetime.now()
        }
        logger.info(f"Created new user record for {user.id}")
    else:
        users[str(user.id)].update({
            "full_name": user.full_name,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "language_code": user.language_code,
            "is_bot": user.is_bot,
            "last_activity": datetime.now()
        })
