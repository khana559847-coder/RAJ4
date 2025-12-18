import streamlit as st
import threading, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------------------------------------------------------------
# ⚡ PAGE CONFIG
# ------------------------------------------------------------------------------------
st.set_page_config(page_title="Dɘvɪl ELITE 2025", page_icon="💀", layout="wide")

# ------------------------------------------------------------------------------------
# 🎨 HIGH-END CYBERPUNK CSS
# ------------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');

    /* Global Style */
    .stApp {
        background: #050505;
        color: #00ffcc;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Modern Header */
    .header-box {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(157, 0, 255, 0.1));
        border-radius: 20px;
        border: 1px solid #00ffcc;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.2);
        margin-bottom: 30px;
    }
    .header-box h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        color: #00ffcc;
        text-shadow: 0 0 20px #00ffcc;
        margin: 0;
    }

    /* Glass Cards */
    .css-1r6slb0, .stCard {
        background: rgba(20, 20, 20, 0.8) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        padding: 20px !important;
    }

    /* Terminal Console */
    .terminal-box {
        background: #000 !important;
        border: 1px solid #9d00ff !important;
        border-radius: 10px;
        padding: 15px;
        height: 400px;
        overflow-y: auto;
        box-shadow: inset 0 0 20px rgba(157, 0, 255, 0.2);
    }
    .log-entry {
        font-size: 13px;
        margin-bottom: 5px;
        color: #9d00ff;
    }
    .log-success { color: #00ffcc; font-weight: bold; }

    /* Neon Buttons */
    div.stButton > button {
        width: 100%;
        background: transparent;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 10px;
        font-weight: bold;
        font-family: 'Orbitron', sans-serif;
        height: 50px;
        transition: 0.5s;
    }
    div.stButton > button:hover {
        background: #00ffcc !important;
        color: #000 !important;
        box-shadow: 0 0 25px #00ffcc;
    }

    /* Stop Button Override */
    div.stButton > button[kind="secondary"] {
        border-color: #ff0055 !important;
        color: #ff0055 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #ff0055 !important;
        color: #fff !important;
        box-shadow: 0 0 25px #ff0055;
    }

    /* Text Inputs */
    .stTextInput input, .stTextArea textarea {
        background: #111 !important;
        color: #00ffcc !important;
        border: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# 🔥 SESSION STATE
# ------------------------------------------------------------------------------------
if "logs" not in st.session_state: st.session_state.logs = []
if "running" not in st.session_state: st.session_state.running = False
if "count" not in st.session_state: st.session_state.count = 0

def add_log(msg, type="normal"):
    ts = time.strftime("%H:%M:%S")
    style = "log-success" if type == "success" else "log-entry"
    st.session_state.logs.append(f'<div class="{style}">[{ts}] {msg}</div>')
    if len(st.session_state.logs) > 100: st.session_state.logs.pop(0)

# ------------------------------------------------------------------------------------
# ⚙️ AUTOMATION ENGINE
# ------------------------------------------------------------------------------------
def run_automation(chat_id, delay, cookies_str, messages_str):
    try:
        add_log("SYSTEM: Booting Dɘvɪl Engine...", "success")
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.facebook.com")
        
        # Cookie injection
        for c in cookies_str.split(";"):
            if "=" in c:
                n, v = c.split("=" , 1)
                driver.add_cookie({"name": n.strip(), "value": v.strip(), "domain": ".facebook.com"})
        
        driver.get(f"https://www.facebook.com/messages/t/{chat_id}")
        add_log(f"SYSTEM: Connection established to {chat_id}", "success")
        
        msg_list = [m.strip() for m in messages_str.split("\n") if m.strip()]
        idx = 0
        
        while st.session_state.running:
            current_msg = msg_list[idx % len(msg_list)]
            try:
                # Find input box with wait
                box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
                )
                box.send_keys(current_msg)
                box.send_keys("\n")
                
                st.session_state.count += 1
                add_log(f"DISPATCHED [{st.session_state.count}]: {current_msg}", "success")
                idx += 1
                time.sleep(delay)
            except Exception:
                add_log("RETRY: Input box lost. Refreshing...")
                driver.refresh()
                time.sleep(10)
        
        driver.quit()
        add_log("SYSTEM: Engine offline.")
    except Exception as e:
        add_log(f"CRITICAL ERROR: {str(e)}")
        st.session_state.running = False

# ------------------------------------------------------------------------------------
# 🖥️ UI LAYOUT
# ------------------------------------------------------------------------------------
st.markdown('<div class="header-box"><h1>Dɘvɪl UPDATE E2E</h1><p>THE ULTIMATE FACEBOOK COMMANDER</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 🛠️ CONFIGURATION")
    c_id = st.text_input("TARGET CHAT ID", placeholder="Enter Chat ID...")
    d_time = st.number_input("DELAY (SECONDS)", min_value=1, value=15)
    f_cookies = st.text_area("FB COOKIES (JSON/Plain)", height=100, placeholder="Paste cookies here...")
    f_messages = st.text_area("MESSAGE LIST", height=150, placeholder="Message 1\nMessage 2...")
    
    st.divider()
    
    btn_start, btn_stop = st.columns(2)
    
    if btn_start.button("START ENGINE"):
        if not c_id or not f_cookies or not f_messages:
            st.error("Missing credentials!")
        else:
            if not st.session_state.running:
                st.session_state.running = True
                threading.Thread(target=run_automation, args=(c_id, d_time, f_cookies, f_messages)).start()
                st.toast("Engine Started!")

    if btn_stop.button("STOP ENGINE", kind="secondary"):
        st.session_state.running = False
        st.toast("Engine Stopping...")

with col2:
    st.markdown("### 📡 LIVE TERMINAL")
    log_html = f'<div class="terminal-box">{"".join(st.session_state.logs[::-1])}</div>'
    st.markdown(log_html, unsafe_allow_html=True)
    
    st.markdown(f"**MESSAGES SENT:** `{st.session_state.count}`")
    if st.session_state.running:
        st.success("🟢 ENGINE ACTIVE")
    else:
        st.error("🔴 ENGINE STANDBY")

# ------------------------------------------------------------------------------------
# 🔄 AUTO-REFRESH
# ------------------------------------------------------------------------------------
if st.session_state.running:
    time.sleep(3)
    st.rerun()
