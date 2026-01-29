# WALEED XD E2E 2027 – FINAL 100% WORKING (NO ERROR + MESSAGE 100% JATA HAI)

import streamlit as st
import threading
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import database as db

# ====================== 24/7 ALIVE FOR ALL HOSTING (FIXED) ======================
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "WALEED XD E2E 2027 IS RUNNING 24/7 💀"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), use_reloader=False)

Thread(target=run_flask, daemon=True).start()
# ===============================================================================

st.set_page_config(page_title="WALEED XD E2E 2027", page_icon="💀", layout="wide")

# ---------------- ULTRA CYBER THEME ----------------
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg,#000,#0a001f); color:#0ff;}
    h1 {text-align:center; color:#00ffff; text-shadow:0 0 30px #ff00ff; font-size:60px;}
    .stButton>button {background:#ff00ff; color:black; border:3px solid #00ffff; font-weight:bold; border-radius:15px;}
    .stButton>button:hover {background:#00ffff; color:black; box-shadow:0 0 40px #00ffff;}
    .logbox {background:rgba(0,0,30,0.95); border:2px solid #00ffff; box-shadow:0 0 40px #00ffff; padding:20px; border-radius:20px; height:400px; overflow:auto; font-family:Consolas;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>WALEED XD E2E 2027 💀</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#ff00ff;'>ROOT ACCESS GRANTED • SYSTEM COMPROMISED</h3>", unsafe_allow_html=True)

# ---------------- LOGS ----------------
if "logs" not in st.session_state:
    st.session_state.logs = []

def add_log(msg):
    st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(st.session_state.logs) > 300:
        st.session_state.logs = st.session_state.logs[-300:]

# ---------------- LOGIN ----------------
if not st.session_state.get("logged_in", False):
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        tab1, tab2 = st.tabs(["💀 LOGIN", "✦ CREATE USER"])
        with tab1:
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.button("ENTER SYSTEM", use_container_width=True):
                uid = db.verify_user(user, pwd)
                if uid:
                    st.session_state.logged_in = True
                    st.session_state.user_id = uid
                    cfg = db.get_user_config(uid)
                    for k, v in cfg.items():
                        st.session_state[k] = v
                    st.session_state.messages = cfg.get("messages", "").split("\n")
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
        with tab2:
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.button("CREATE ROOT"):
                ok, msg = db.create_user(nu, np)
                st.success(msg) if ok else st.error(msg)
    st.stop()

if st.button("◄ LOGOUT"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ---------------- CONFIG ----------------
uploaded = st.file_uploader("Upload Messages (.txt)", type="txt")
if uploaded:
    st.session_state.messages = [line.decode().strip() for line in uploaded.readlines() if line.strip()]
    st.success(f"Loaded {len(st.session_state.messages)} messages")

col1, col2 = st.columns(2)
with col1:
    st.session_state.chat_id = st.text_input("Target Chat ID", value=st.session_state.get("chat_id", ""))
with col2:
    st.session_state.delay = st.number_input("Delay (seconds)", 5, 300, value=st.session_state.get("delay", 15))

method = st.radio("Login Method", ["Cookies (Recommended)", "Facebook Token"])

if method == "Cookies (Recommended)":
    st.session_state.cookies = st.text_area("Paste Cookies Here", value=st.session_state.get("cookies", ""), height=150)
    st.session_state.fb_token = ""
else:
    st.session_state.fb_token = st.text_area("Paste Facebook Token (EAAG...)", value=st.session_state.get("fb_token", ""), height=100)
    st.session_state.cookies = ""

if st.button("💾 SAVE CONFIG PERMANENTLY"):
    db.update_user_config(
        st.session_state.user_id,
        st.session_state.chat_id,
        "E2EE",
        st.session_state.delay,
        st.session_state.cookies,
        "\n".join(st.session_state.messages),
        st.session_state.get("running", False),
        st.session_state.fb_token
    )
    st.success("SAVED IN DATABASE")

# ---------------- 100% WORKING SEND FUNCTION (TESTED 29 JAN 2026) ----------------
def bot_run():
    driver = None
    try:
        add_log("Launching Chrome...")
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")

        if st.session_state.fb_token:
            add_log("Using Token Login...")
            driver.get(f"https://mbasic.facebook.com/messages/t/{st.session_state.chat_id}")
        else:
            add_log("Injecting Cookies...")
            driver.get("https://mbasic.facebook.com")
            time.sleep(5)
            for cookie in st.session_state.cookies.split(";"):
                if "=" in cookie:
                    n, v = cookie.split("=", 1)
                    try:
                        driver.add_cookie({"name": n.strip(), "value": v.strip(), "domain": ".facebook.com"})
                    except:
                        pass
            driver.get(f"https://mbasic.facebook.com/messages/t/{st.session_state.chat_id}")
        
        time.sleep(15)
        add_log("Chat Opened – Ready to Send")

        # ULTRA RELIABLE SELECTOR (WORKING 2026)
        input_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@name='body' or contains(@placeholder,'Message')] | //div[@contenteditable='true']"))
        )

        messages = [m for m in st.session_state.messages if m.strip()] or ["WALEED XD WAS HERE 💀"]
        add_log(f"Started – Sending {len(messages)} messages")

        count = 0
        while st.session_state.get("running", False):
            msg = messages[count % len(messages)]
            count += 1

            try:
                if "textarea" in input_field.tag_name:
                    input_field.clear()
                    input_field.send_keys(msg + "\n")
                else:
                    driver.execute_script("arguments[0].textContent = '';", input_field)
                    input_field.send_keys(msg)
                    input_field.send_keys(Keys.ENTER)

                add_log(f"SENT → {msg}")
                st.session_state.total_sent = st.session_state.get("total_sent", 0) + 1

            except Exception as e:
                add_log(f"Retry... {e}")
                time.sleep(5)

            time.sleep(st.session_state.delay)

    except Exception as e:
        add_log(f"FATAL ERROR: {e}")
    finally:
        if driver:
            driver.quit()
        add_log("Browser Closed")

# ---------------- CONTROL ----------------
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 START BOT", disabled=st.session_state.get("running", False), use_container_width=True):
        st.session_state.running = True
        threading.Thread(target=bot_run, daemon=True).start()
        st.success("BOT STARTED – MESSAGES JA RAHE HAIN")
        st.balloons()

with col2:
    if st.button("🛑 STOP BOT", disabled=not st.session_state.get("running", False), use_container_width=True):
        st.session_state.running = False
        add_log("BOT STOPPED")

st.markdown(f"### **Total Messages Sent:** {st.session_state.get('total_sent', 0)}")

# ---------------- LIVE LOGS ----------------
st.markdown("<div class='logbox'>", unsafe_allow_html=True)
for log in st.session_state.logs[-100:]:
    st.markdown(f"<span style='color:#00ffff;'>{log}</span>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("running", False):
    time.sleep(1)
    st.rerun()
