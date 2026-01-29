# database.py → WALEED XD E2E 2027 EDITION (TOKEN SUPPORT + ZERO ERROR)

users = {}      # {username: {"password": hashed_pass, "id": user_id}}
configs = {}    # {user_id: full_config_dict}
next_id = 1

import hashlib
def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()

def create_user(username, password):
    global next_id
    if any(u.lower() == username.lower() for u in users):
        return False, "Username already taken!"
    
    user_id = next_id
    next_id += 1
    users[username] = {"id": user_id, "password": hash_pwd(password)}
    configs[user_id] = {
        "chat_id": "", "chat_type": "E2EE", "delay": 15,
        "cookies": "", "messages": "", "running": False, "fb_token": ""
    }
    return True, "ROOT USER CREATED SUCCESSFULLY"

def verify_user(username, password):
    for name, data in users.items():
        if name.lower() == username.lower() and data["password"] == hash_pwd(password):
            return data["id"]
    return None

def get_user_config(user_id):
    return configs.get(user_id, {
        "chat_id": "", "chat_type": "E2EE", "delay": 15,
        "cookies": "", "messages": "", "running": False, "fb_token": ""
    })

def update_user_config(user_id, chat_id, chat_type, delay, cookies, messages, running=False, fb_token=""):
    if user_id not in configs:
        configs[user_id] = {}
    
    configs[user_id].update({
        "chat_id": chat_id or "",
        "chat_type": chat_type or "E2EE",
        "delay": int(delay) if delay else 15,
        "cookies": cookies or "",
        "messages": messages or "",
        "running": bool(running),
        "fb_token": fb_token or ""
    })

# OPTIONAL: Default admin (remove if not needed)
# create_user("waleedxd", "waleed123")

print("WALEED XD E2E 2027 DATABASE LOADED — TOKEN + COOKIES SUPPORT ACTIVE 💀✦")
