import streamlit as st
import threading, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ------------------------------------------------------------------------------------
# 🛡️ DATABASE & SECURITY SIMULATION
# ------------------------------------------------------------------------------------
# Real world mein isse 'database.py' mein save karein
if "db_keys" not in st.session_state:
    st.session_state.db_keys = ["DEVIL-786", "ADMIN-FREE-2025", "VIP-KEY-99"]

if "approved_users" not in st.session_state:
    st.session_state.approved_users = {} # {username: password}

# ------------------------------------------------------------------------------------
# ⚡ PAGE CONFIG
# ------------------------------------------------------------------------------------
st.set_page_config(page_title="Dɘvɪl ELITE v2", page_icon="🔥", layout="wide")

# ------------------------------------------------------------------------------------
# 🎨 PREMIUM CYBERPUNK CSS
# ------------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500&display=swap');

    .stApp {
        background: radial-gradient(circle at top, #0d1b2a 0%, #000000 100%);
        color: #e0e1dd;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Glassmorphism Cards */
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 204, 0.2);
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        text-align: center;
        margin-bottom: 25px;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: #00f2fe !important;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* Animated Console */
    .logbox {
        background: #050505;
        border-left: 5px solid #00f2fe;
        border-radius: 10px;
        padding: 15px;
        height: 350px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        box-shadow: inset 0 0 15px #000;
    }

    /* Premium Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: black !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px;
        transition: 0.3s;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0, 242, 254, 0.4);
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        color: #00f2fe !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# 🔥 CORE LOGIC
# ------------------------------------------------------------------------------------
if "live_logs" not in st.session_state: st.session_state.live_logs = []

def live_log(msg: str):
    ts = time.strftime("%H:%M:%S")
    st.session_state.live_logs.append(f"[{ts}] > {msg}")
    if len(st.session_state.live_logs) > 100: st.session_state.live_logs.pop(0)

# ------------------------------------------------------------------------------------
# 🔐 AUTHENTICATION INTERFACE
# ------------------------------------------------------------------------------------
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "is_admin" not in st.session_state: st.session_state.is_admin = False

if not st.session_state.logged_in:
    st.markdown('<div class="main-card"><h1>Dɘvɪl UPDATE E2E</h1><p>Next-Gen Automation Protocol</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2, tab3 = st.tabs(["🔑 LOGIN", "🛡️ REGISTER", "⚡ ADMIN"])
        
        with tab1:
            u = st.text_input("Username", key="login_u")
            p = st.text_input("Password", type="password", key="login_p")
            if st.button("AUTHENTICATE"):
                if u in st.session_state.approved_users and st.session_state.approved_users[u] == p:
                    st.session_state.logged_in = True
                    st.session_state.user_id = u
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid Credentials")

        with tab2:
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            akey = st.text_input("Approval Key (Contact Admin)")
            if st.button("REQUEST ACCESS"):
                if akey in st.session_state.db_keys:
                    st.session_state.approved_users[nu] = np
                    st.success("Registration Successful! Please Login.")
                else:
                    st.error("Invalid Approval Key!")

        with tab3:
            admin_pass = st.text_input("Admin Secret", type="password")
            if st.button("ADMIN LOGIN"):
                if admin_pass == "devil888": # Admin password
                    st.session_state.is_admin = True
                    st.session_state.logged_in = True
                    st.session_state.user_id = "MASTER_ADMIN"
                    st.rerun()
    st.stop()

# ------------------------------------------------------------------------------------
# 🛠️ ADMIN PANEL
# ------------------------------------------------------------------------------------
if st.session_state.is_admin:
    with st.expander("🛠️ MASTER CONTROL PANEL"):
        st.subheader("Manage Approval Keys")
        new_key = st.text_input("Generate New Key")
        if st.button("Add Key"):
            st.session_state.db_keys.append(new_key)
            st.success(f"Key {new_key} Added!")
        
        st.write("Active Keys:", st.session_state.db_keys)
        st.write("Registered Users:", st.session_state.approved_users)
        if st.button("EXIT ADMIN MODE"):
            st.session_state.is_admin = False
            st.session_state.logged_in = False
            st.rerun()

# ------------------------------------------------------------------------------------
# 🚀 MAIN DASHBOARD
# ------------------------------------------------------------------------------------
st.markdown(f"### ⚡ SESSION ACTIVE: {st.session_state.user_id}")

c1, c2 = st.columns([1, 1])

with c1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    chat_id = st.text_input("Target Chat ID", placeholder="1000xxxxxxx")
    delay = st.slider("Message Delay (Seconds)", 5, 300, 15)
    cookies = st.text_area("FB Cookies", height=100)
    msg_list = st.text_area("Messages (One per line)", height=150)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.subheader("📡 Live Execution Console")
    st.markdown('<div class="logbox">', unsafe_allow_html=True)
    for log in reversed(st.session_state.live_logs):
        st.write(log)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# ⚙️ AUTOMATION ENGINE (LONG RUN OPTIMIZED)
# ------------------------------------------------------------------------------------
def devil_engine(cid, dly, ck, msgs, state):
    try:
        live_log("System: Initializing Driver...")
        opt = Options()
        opt.add_argument("--headless=new")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=opt)
        
        driver.get("https://www.facebook.com")
        for cookie in ck.split(";"):
            if "=" in cookie:
                name, val = cookie.split("=", 1)
                driver.add_cookie({"name": name.strip(), "value": val.strip(), "domain": ".facebook.com"})
        
        driver.get(f"https://www.facebook.com/messages/t/{cid}")
        time.sleep(8)
        
        msg_idx = 0
        msg_pool = [m.strip() for m in msgs.split("\n") if m.strip()]
        
        while state["active"]:
            current_msg = msg_pool[msg_idx % len(msg_pool)]
            try:
                # Optimized for speed and long-run
                box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
                box.send_keys(current_msg)
                box.send_keys("\n")
                live_log(f"SENT: {current_msg}")
                msg_idx += 1
            except Exception as e:
                live_log(f"Error: Box not found. Retrying...")
                driver.refresh()
                time.sleep(10)
            
            time.sleep(dly)
        
        driver.quit()
    except Exception as e:
        live_log(f"Fatal Crash: {str(e)}")

# ------------------------------------------------------------------------------------
# 🕹️ CONTROLS
# ------------------------------------------------------------------------------------
if "automation_state" not in st.session_state:
    st.session_state.automation_state = {"active": False}

btn_col1, btn_col2 = st.columns(2)

if btn_col1.button("▶️ START SERVER", use_container_width=True):
    if not cookies or not msg_list:
        st.warning("Please fill Cookies and Messages!")
    else:
        st.session_state.automation_state["active"] = True
        thread = threading.Thread(target=devil_engine, args=(chat_id, delay, cookies, msg_list, st.session_state.automation_state))
        thread.start()
        live_log("System: Engine Started in Background.")

if btn_col2.button("🛑 STOP SERVER", use_container_width=True):
    st.session_state.automation_state["active"] = False
    live_log("System: Stopping Engine...")

if st.button("LOGOUT"):
    st.session_state.logged_in = False
    st.rerun()

# Auto-refresh UI for logs
if st.session_state.automation_state["active"]:
    time.sleep(5)
    st.rerun()
