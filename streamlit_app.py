import streamlit as st
import threading, time, os, hashlib, requests, json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 1. DATABASE INTEGRATION (With Approval Logic)
try:
    import database as db
except ImportError:
    st.error("Critical: 'database.py' not found!")
    # Dummy placeholder for structure
    class DummyDB:
        def verify_user(self, u, p): return {"user_id": u, "is_approved": False}
        def get_user_config(self, uid): return {}
        def update_user_config(self, *args, **kwargs): pass
    db = DummyDB()

# 2. MONGODB 24/7 HEARTBEAT (From Dstreamlit_app)
def setup_mongodb_heartbeat():
    def keep_alive():
        while True:
            try:
                from pymongo import MongoClient
                conn = "mongodb+srv://dineshsavita76786_user_db:WALEED_XD@cluster0.3xxvjpo.mongodb.net/?retryWrites=true&w=majority"
                client = MongoClient(conn, serverSelectionTimeoutMS=5000)
                db_conn = client['streamlit_db']
                db_conn.heartbeat.update_one(
                    {'app_id': 'Rafay_Khan_automation'},
                    {'$set': {'last_heartbeat': datetime.now(), 'status': 'active'}},
                    upsert=True
                )
                client.close()
            except: pass
            time.sleep(300)
    threading.Thread(target=keep_alive, daemon=True).start()

if 'mongodb_started' not in st.session_state:
    setup_mongodb_heartbeat()
    st.session_state.mongodb_started = True

# 3. PREMIUM CSS THEME (Glassmorphism & Neon)
st.set_page_config(page_title="Dɘvɪl UPDATE E2E 2025", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    /* Full Background */
    .stApp {
        background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    /* Main Container */
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    /* Status Indicators */
    .status-running { color: #00ff88; font-weight: bold; text-shadow: 0 0 10px #00ff88; }
    .status-stopped { color: #ff4b2b; font-weight: bold; text-shadow: 0 0 10px #ff4b2b; }
    /* Custom Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border: none; border-radius: 10px;
        height: 3em; width: 100%; transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02); box-shadow: 0 0 15px #00d2ff;
    }
    .log-box {
        background: #000000; border: 1px solid #00d2ff;
        border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace;
        height: 300px; overflow-y: auto; color: #00ff88;
    }
</style>
""", unsafe_allow_html=True)

# 4. INITIALIZATION
if "automation_state" not in st.session_state:
    st.session_state.automation_state = type('obj', (object,), {'running': False, 'logs': [], 'index': 0})()

def live_log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.automation_state.logs.append(f"[{ts}] {msg}")

# 5. AUTOMATION ENGINE
def run_automation(cfg, state):
    driver = None
    try:
        live_log("🔧 Initializing Dark Engine...")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        
        driver.get("https://www.facebook.com")
        if cfg.get('cookies'):
            for c in cfg['cookies'].split(';'):
                if '=' in c:
                    n, v = c.strip().split('=', 1)
                    driver.add_cookie({'name': n, 'value': v, 'domain': '.facebook.com'})
        
        driver.get(f"https://www.facebook.com/messages/t/{cfg['chat_id']}")
        time.sleep(5)
        
        msgs = [m.strip() for m in cfg['messages'].split('\n') if m.strip()]
        while state.running:
            msg = f"{cfg.get('prefix', '')} {msgs[state.index % len(msgs)]}"
            # Selenium Send Logic
            try:
                box = driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")
                box.send_keys(msg + Keys.ENTER)
                live_log(f"✅ Sent: {msg}")
            except:
                live_log("⚠️ Box not found, retrying...")
            
            state.index += 1
            time.sleep(int(cfg.get('delay', 15)))
    except Exception as e:
        live_log(f"❌ Error: {str(e)[:50]}")
    finally:
        if driver: driver.quit()

# 6. LOGIN & APPROVAL UI
if 'logged_in' not in st.session_state:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ Dɘvɪl E2E - LOGIN")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    
    if st.button("Access Dashboard"):
        result = db.verify_user(user, pw)
        if result:
            if result.get('is_approved'):
                st.session_state.logged_in = True
                st.session_state.user_id = user
                st.rerun()
            else:
                st.warning("⏳ Your account is pending Approval. Contact Admin.")
        else:
            st.error("Invalid Credentials")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. MAIN DASHBOARD
else:
    st.markdown(f"### Welcome, {st.session_state.user_id} | Status: {'🟢 Running' if st.session_state.automation_state.running else '🔴 Stopped'}")
    
    tab1, tab2 = st.tabs(["🎮 Controls", "📝 Configuration"])
    
    with tab2:
        with st.container():
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            u_cfg = db.get_user_config(st.session_state.user_id)
            c_cookies = st.text_area("Cookies", value=u_cfg.get('cookies', ''), height=100)
            c_cid = st.text_input("Target Chat ID", value=u_cfg.get('chat_id', ''))
            c_msgs = st.text_area("Messages (One per line)", value=u_cfg.get('messages', ''))
            c_pre = st.text_input("Prefix", value=u_cfg.get('prefix', ''))
            c_delay = st.slider("Delay (Seconds)", 5, 300, int(u_cfg.get('delay', 15)))
            
            if st.button("Save Settings"):
                db.update_user_config(st.session_state.user_id, cookies=c_cookies, chat_id=c_cid, messages=c_msgs, prefix=c_pre, delay=c_delay)
                st.success("Settings Saved!")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab1:
        col_l, col_r = st.columns([1, 1])
        with col_l:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            if not st.session_state.automation_state.running:
                if st.button("▶️ START AUTOMATION"):
                    st.session_state.automation_state.running = True
                    cfg = db.get_user_config(st.session_state.user_id)
                    threading.Thread(target=run_automation, args=(cfg, st.session_state.automation_state)).start()
                    st.rerun()
            else:
                if st.button("⏹️ STOP AUTOMATION"):
                    st.session_state.automation_state.running = False
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="log-box">', unsafe_allow_html=True)
            for log in st.session_state.automation_state.logs[-15:]:
                st.write(log)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br><center>Dɘvɪl E2E v2.0 - Powered by WALEED XD</center>', unsafe_allow_html=True)
