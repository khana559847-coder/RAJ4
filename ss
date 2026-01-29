# ██████╗░███████╗███████╗  ██████╗░██████╗░░█████╗░
# ██╔══██╗██╔════╝╚════██║  ╚════██╗╚════██╗██╔═══╝░
# ██████╔╝█████╗░░░░███╔═╝  ░░███╔═╝░░███╔═╝███████╗
# ██╔══██╗██╔══╝░░██╔══╝░░  ██╔══╝░░██╔══╝░░██╔══██║
# ██║░░██║███████╗███████╗  ███████╗██║░░░░░██║░░██║
# ╚═╝░░╚═╝╚══════╝╚══════╝  ╚══════╝╚═╝░░░░░╚═╝░░╚═╝
#                     WALEED XD E2E 2027 💀✦

import streamlit as st
import threading, time, os, json, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import database as db

# ====================== 24/7 KEEP ALIVE FOR ALL HOSTING ======================
from threading import Thread
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "WALEED XD E2E 2027 IS ALIVE FOREVER 💀"
def run_flask():
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
Thread(target=run_flask, daemon=True).start()
# ===============================================================================

st.set_page_config(page_title="WALEED XD E2E 2027", page_icon="💀", layout="wide")

# -------------------------------- ULTRA DARK THEME --------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #000000, #0a001f);
        background-attachment: fixed;
    }
    .css-1d391kg {background: rgba(10,0,35,0.9) !important;}
    .stButton>button {background: #ff00ff; color: black; border: 2px solid #00ffff; font-weight: bold;}
    .stButton>button:hover {background: #00ffff; color: black; box-shadow: 0 0 20px #00ffff;}
    .logbox {background: rgba(0,0,20,0.9); border: 2px solid #00ffff; box-shadow: 0 0 30px #00ffff;}
    h1, h2, h3 {color: #00ffff; text-shadow: 0 0 20px #ff00ff;}
    .css-1y0t8qx {color: #00ffff !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center; color:#00ffff; text-shadow: 0 0 30px #ff00ff; font-size:60px;'>
WALEED XD E2E 2027 💀✦
</h1>
<h3 style='text-align:center; color:#ff00ff;'>SYSTEM COMPROMISED • ROOT = ME</h3>
""", unsafe_allow_html=True)

# ---------------- LIVE LOGS SYSTEM ----------------
def live_log(msg: str):
    ts = time.strftime("%H:%M:%S")
    line = f"<span style='color:#00ffff;'>[{ts}]</span> <span style='color:#ff00ff;'>{msg}</span>"
    st.session_state.live_logs.append(line)
    if len(st.session_state.live_logs) > 200:
        st.session_state.live_logs = st.session_state.live_logs[-200:]

if "live_logs" not in st.session_state: st.session_state.live_logs = []

# ---------------- SESSION STATE ----------------
for key in ["logged_in","automation_running","user_id","chat_id","chat_type","delay","cookies","fb_token","messages"]:
    if key not in st.session_state: st.session_state[key] = "" if key in ["cookies","fb_token"] else ([] if key=="messages" else False if key in ["logged_in","automation_running"] else 15 if key=="delay" else "E2EE")

st.session_state.automation_state = type('obj',(object,),{"running":False,"message_count":0,"message_rotation_index":0})()

# ---------------- LOGIN SYSTEM ----------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab1, tab2 = st.tabs(["💀 LOGIN", "✦ CREATE ACCOUNT"])
        with tab1:
            u = st.text_input("Username", key="login_u")
            p = st.text_input("Password", type="password", key="login_p")
            if st.button("ENTER THE MATRIX", use_container_width=True):
                uid = db.verify_user(u, p)
                if uid:
                    st.session_state.logged_in = True
                    st.session_state.user_id = uid
                    cfg = db.get_user_config(uid)
                    for k,v in cfg.items():
                        if k in st.session_state: st.session_state[k] = v
                    st.session_state.messages = cfg.get("messages","").split("\n")
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
        with tab2:
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            npc = st.text_input("Confirm Password", type="password")
            if st.button("CREATE ROOT USER"):
                if np != npc: st.error("PASSWORD NOT MATCH")
                elif len(np) < 4: st.error("PASSWORD TOO WEAK")
                else:
                    ok, msg = db.create_user(nu, np)
                    st.success(msg) if ok else st.error(msg)
    st.stop()

# ---------------- DASHBOARD ----------------
st.markdown(f"### 💀 WELCOME BACK ROOT USER → {st.session_state.user_id}")
if st.button("◄ LOGOUT"): 
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

# ---------------- UPLOAD MESSAGES ----------------
uploaded = st.file_uploader("UPLOAD MESSAGES (.txt)", type="txt")
if uploaded:
    st.session_state.messages = [line.decode().strip() for line in uploaded.readlines() if line.strip()]
    st.success(f"LOADED {len(st.session_state.messages)} MESSAGES")

# ---------------- CONFIG ----------------
st.markdown("### ⚙️ CONFIGURATION")
col1, col2 = st.columns(2)
with col1:
    st.session_state.chat_id = st.text_input("CHAT ID / USER ID", st.session_state.chat_id)
    st.session_state.chat_type = st.selectbox("CHAT TYPE", ["E2EE", "NORMAL CONVO"], 0 if "E2EE" in st.session_state.chat_type else 1)
with col2:
    st.session_state.delay = st.number_input("DELAY (seconds)", 5, 300, st.session_state.delay)

login_method = st.radio("LOGIN METHOD", ["COOKIES (Recommended)", "FACEBOOK TOKEN (EAAG...)"])

if login_method == "COOKIES (Recommended)":
    st.session_state.cookies = st.text_area("PASTE COOKIES (EditThisCookie Extension)", st.session_state.cookies, height=160)
    st.session_state.fb_token = ""
else:
    st.session_state.fb_token = st.text_area("PASTE FACEBOOK TOKEN", st.session_state.fb_token, height=100)
    st.session_state.cookies = ""

if st.button("SAVE CONFIG PERMANENTLY", use_container_width=True):
    db.update_user_config(
        st.session_state.user_id,
        st.session_state.chat_id,
        st.session_state.chat_type,
        st.session_state.delay,
        st.session_state.cookies,
        "\n".join(st.session_state.messages),
        st.session_state.automation_running,
        st.session_state.fb_token
    )
    st.success("CONFIG SAVED IN ROOT DATABASE")

# ---------------- ULTRA STRONG BROWSER (2027 PROOF) ----------------
def get_browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120,130)}.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => false});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});
        window.chrome = {runtime: {}, app: {}, loadTimes: () => {}};
        delete navigator.__proto__.webdriver;
        """
    })
    return driver

# ---------------- SEND MESSAGES (TOKEN + COOKIES BOTH WORKING) ----------------
def automation_core(cfg, state):
    driver = None
    try:
        live_log("INITIALIZING ULTRA BROWSER...")
        driver = get_browser()

        if cfg.get("fb_token"):
            live_log("USING FACEBOOK TOKEN METHOD...")
            driver.get(f"https://graph.facebook.com/v20.0/me/messages?access_token={cfg['fb_token']}")
            time.sleep(5)
            # Token method se direct API hit kar sakte hain lekin UI se bhi send kar rahe hain safety ke liye
            driver.get(f"https://m.facebook.com/messages/t/{cfg['chat_id']}")
        else:
            live_log("INJECTING COOKIES...")
            driver.get("https://facebook.com")
            time.sleep(5)
            for cookie in cfg.get("cookies","").split(";"):
                if "=" in cookie:
                    n, v = cookie.split("=",1)
                    try: driver.add_cookie({"name":n.strip(),"value":v.strip(),"domain":".facebook.com"})
                    except: pass
            driver.get(f"https://www.facebook.com/messages/t/{cfg['chat_id']}")
        
        time.sleep(15)
        live_log("CHAT OPENED SUCCESSFULLY")

        # BEST SELECTOR FOR 2027
        input_box = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[contenteditable='true'][data-lexical-editor='true'], div[contenteditable='true']"))
        )

        msgs = [m for m in cfg.get("messages","").split("\n") if m.strip()] or ["WALEED XD WAS HERE 💀"]
        live_log(f"STARTED • {len(msgs)} Messages • Delay {cfg['delay']}s")

        while state.running:
            msg = msgs[state.message_rotation_index % len(msgs)]
            state.message_rotation_index += 1

            try:
                driver.execute_script("arguments[0].innerHTML = '';", input_box)
                input_box.click()
                input_box.send_keys(msg)
                time.sleep(1.2)
                driver.execute_script("""
                    arguments[0].dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', code:'Enter', keyCode:13, bubbles:true}));
                    arguments[0].dispatchEvent(new KeyboardEvent('keyup', {key:'Enter', code:'Enter', keyCode:13, bubbles:true}));
                """, input_box)
                state.message_count += 1
                live_log(f"SENT → {msg}")
            except:
                live_log("RETRYING SEND...")

            # SESSION ALIVE HACK
            driver.execute_script("document.cookie='presence=EDvF3EtimeF1700000000%3DPCWvF3EtimeF1700000000%3D'; path=/; domain=.facebook.com; secure=true;")
            time.sleep(cfg.get("delay",15))

    except Exception as e:
        live_log(f"CRITICAL ERROR: {e}")
    finally:
        if driver: driver.quit()
        live_log("BROWSER CLOSED • SESSION ENDED")

# ---------------- CONTROL PANEL ----------------
st.markdown("### 🚀 AUTOMATION CONTROL")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("START BOT", disabled=st.session_state.automation_running, use_container_width=True):
        cfg = db.get_user_config(st.session_state.user_id)
        st.session_state.automation_running = True
        st.session_state.automation_state.running = True
        threading.Thread(target=automation_core, args=(cfg, st.session_state.automation_state), daemon=True).start()
        st.success("WALEED XD BOT ACTIVATED")
        st.balloons()
with c2:
    if st.button("STOP BOT", disabled=not st.session_state.automation_running, use_container_width=True):
        st.session_state.automation_state.running = False
        st.session_state.automation_running = False
        live_log("BOT STOPPED BY ROOT")
        st.warning("STOPPED")

with c3:
    st.write(f"**SENT:** {st.session_state.automation_state.message_count}")

# ---------------- LIVE LOGS ----------------
st.markdown("### 📡 LIVE LOGS")
st.markdown('<div class="logbox">', unsafe_allow_html=True)
for log in st.session_state.live_logs[-80:]:
    st.markdown(log, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.automation_running:
    time.sleep(1)
    st.rerun()
