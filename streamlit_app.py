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

# 🚨 MONGODB 24/7 HEARTBEAT START
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
# 🚨 MONGODB 24/7 HEARTBEAT END

# ⚡ ENHANCED DESIGNER THEME CSS
custom_css = """
<style>
    /* Modern Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main App Gradient Background */
    .stApp {
        background: linear-gradient(135deg, 
            #0f0c29 0%,
            #302b63 25%,
            #24243e 50%,
            #1a1a2e 75%,
            #16213e 100%);
        background-size: 400% 400%;
        animation: galaxyBackground 20s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes galaxyBackground {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glowing Stars Effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(2px 2px at 40px 70px, #fff, transparent),
            radial-gradient(2px 2px at 50px 160px, #ddd, transparent),
            radial-gradient(2px 2px at 90px 40px, #fff, transparent),
            radial-gradient(2px 2px at 130px 80px, #fff, transparent),
            radial-gradient(2px 2px at 160px 120px, #ddd, transparent);
        background-repeat: repeat;
        background-size: 200px 200px;
        opacity: 0.3;
        z-index: -1;
        animation: twinkle 4s infinite alternate;
    }
    
    @keyframes twinkle {
        0% { opacity: 0.2; }
        100% { opacity: 0.4; }
    }
    
    /* Premium Main Container */
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
    
    /* Premium Header */
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
    
    /* Premium Title */
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
    
    /* Premium Badge */
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
    
    /* Premium Cards */
    .premium-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        border-color: rgba(59, 130, 246, 0.3);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
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
    
    /* Premium Inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        background: rgba(15, 23, 42, 0.9) !important;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3) !important;
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
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Success Button */
    .success-btn > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Danger Button */
    .danger-btn > button {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Warning Button */
    .warning-btn > button {
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3) !important;
    }
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(30, 41, 59, 0.5);
        padding: 10px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        color: rgba(255, 255, 255, 0.6) !important;
        font-weight: 500 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Premium Stats */
    .premium-stat {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    
    .stat-value {
        font-size: 2.8rem;
        font-weight: 900;
        color: white;
        margin: 10px 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Premium Log Console */
    .log-console {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 15px;
        padding: 20px;
        font-family: 'Consolas', 'Monaco', monospace;
        color: #10b981;
        font-size: 14px;
        line-height: 1.6;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
    }
    
    .log-entry {
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 8px;
        background: rgba(16, 185, 129, 0.05);
        border-left: 3px solid #10b981;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* User Status Badges */
    .status-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .status-approved {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);
    }
    
    .status-rejected {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        box-shadow: 0 5px 15px rgba(239, 68, 68, 0.3);
    }
    
    /* Connection Status */
    .connection-status {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(15, 23, 42, 0.9);
        padding: 12px 20px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 1000;
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10b981;
        animation: pulseStatus 2s ease-in-out infinite;
    }
    
    @keyframes pulseStatus {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Premium Footer */
    .premium-footer {
        text-align: center;
        padding: 40px 20px;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
        position: relative;
    }
    
    .premium-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent, 
            #3b82f6, 
            #8b5cf6,
            transparent);
        border-radius: 3px;
    }
    
    /* Glass Effect */
    .glass-effect {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Neon Text */
    .neon-text {
        color: #fff;
        text-shadow: 
            0 0 5px #3b82f6,
            0 0 10px #3b82f6,
            0 0 15px #3b82f6,
            0 0 20px #8b5cf6;
        animation: neonPulse 1.5s ease-in-out infinite alternate;
    }
    
    @keyframes neonPulse {
        from { text-shadow: 0 0 5px #3b82f6, 0 0 10px #3b82f6; }
        to { text-shadow: 0 0 10px #3b82f6, 0 0 20px #8b5cf6; }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
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
    
    /* Loading Animation */
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 3px solid rgba(59, 130, 246, 0.1);
        border-radius: 50%;
        border-top-color: #3b82f6;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
"""

# Rest of your existing code remains the same with the new CSS applied
st.set_page_config(
    page_title="WALEED E2E PAID TOOL",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

# ... Rest of your existing functions and code ...

# MAIN APPLICATION LAYOUT
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

# Connection Status Indicator
st.markdown("""
<div class="connection-status">
    <div class="status-dot"></div>
    <span>Connected • MongoDB Active</span>
</div>
""", unsafe_allow_html=True)

# Your existing application logic continues here...
# [Keep all your existing functions and logic, they'll now use the new premium styling]

# Example of a premium card in your UI:
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.markdown("### 🚀 Automation Dashboard")
# Your existing dashboard content
st.markdown('</div>', unsafe_allow_html=True)

# Premium Footer
st.markdown("""
<div class="premium-footer">
    <div class="neon-text">WALEED E2E PAID TOOL</div>
    <p>Premium Automation Suite • Version 3.0</p>
    <p>© 2025 Waleed XD • All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close premium-container
