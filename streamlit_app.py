import streamlit as st
import threading, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ------------------------------------------------------------------------------------
# ⚡ PAGE CONFIG & STYLING
# ------------------------------------------------------------------------------------
st.set_page_config(page_title="Dɘvɪl UPDATE E2E 2025", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #ff0055, #7000ff);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(112, 0, 255, 0.3);
    }
    .logbox {
        background: #000000;
        border: 1px solid #7000ff;
        border-radius: 10px;
        padding: 15px;
        height: 350px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #7000ff !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>Dɘvɪl UPDATE E2E 2025</h1></div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# 🔥 SYSTEM STATE
# ------------------------------------------------------------------------------------
if "live_logs" not in st.session_state: st.session_state.live_logs = []
if "automation_running" not in st.session_state: st.session_state.automation_running = False
if "msg_count" not in st.session_state: st.session_state.msg_count = 0

def live_log(msg):
    ts = time.strftime("%H:%M:%S")
    st.session_state.live_logs.append(f"[{ts}] {msg}")
    if len(st.session_state.live_logs) > 50: st.session_state.live_logs.pop(0)

# ------------------------------------------------------------------------------------
# ⚙️ ENGINE (Fixed Logic)
# ------------------------------------------------------------------------------------
def start_engine(cid, dly, ck, msgs):
    try:
        live_log("🚀 Driver Initializing...")
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        
        driver.get("https://www.facebook.com")
        for c in ck.split(";"):
            if "=" in c:
                n, v = c.split("=", 1)
                driver.add_cookie({"name": n.strip(), "value": v.strip(), "domain": ".facebook.com"})
        
        driver.get(f"https://www.facebook.com/messages/t/{cid}")
        time.sleep(5)
        
        msg_list = [m.strip() for m in msgs.split("\n") if m.strip()]
        i = 0
        while st.session_state.automation_running:
            try:
                msg = msg_list[i % len(msg_list)]
                # Target common message box selectors
                box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
                box.send_keys(msg)
                box.send_keys("\n")
                
                st.session_state.msg_count += 1
                live_log(f"SENT: {msg}")
                i += 1
                time.sleep(dly)
            except:
                live_log("⚠️ Error: Retrying connection...")
                driver.refresh()
                time.sleep(10)
        
        driver.quit()
    except Exception as e:
        live_log(f"❌ Fatal: {str(e)}")
        st.session_state.automation_running = False

# ------------------------------------------------------------------------------------
# 🖥️ DASHBOARD UI
# ------------------------------------------------------------------------------------
col1, col2 = st.columns([1, 1.2], gap="medium")

with col1:
    st.subheader("⚙️ Configuration")
    chat_id = st.text_input("Target Chat ID", placeholder="e.g. 1000123456789")
    delay = st.number_input("Delay (Seconds)", min_value=1, value=15)
    cookies = st.text_area("FB Cookies", height=100)
    messages = st.text_area("Message List (One per line)", height=150)
    
    st.divider()
    
    # --- FIXED BUTTONS ---
    btn_start, btn_stop = st.columns(2)
    
    if btn_start.button("START SERVER"):
        if chat_id and cookies and messages:
            st.session_state.automation_running = True
            t = threading.Thread(target=start_engine, args=(chat_id, delay, cookies, messages))
            t.start()
            st.rerun()
        else:
            st.warning("Please fill all fields!")

    # Fixed: "type" used instead of "kind" to avoid TypeError
    if btn_stop.button("STOP SERVER", type="secondary"):
        st.session_state.automation_running = False
        live_log("🛑 Stopping engine...")

with col2:
    st.subheader("📡 Live Console")
    st.markdown('<div class="logbox">', unsafe_allow_html=True)
    for log in reversed(st.session_state.live_logs):
        st.markdown(f'<p style="color:#00ffcc; margin:0; font-size:14px;">{log}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.metric("Messages Dispatched", st.session_state.msg_count)

# Auto-refresh when running
if st.session_state.automation_running:
    time.sleep(2)
    st.rerun()
