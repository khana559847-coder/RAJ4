import streamlit as st
import threading, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Try to import database, if fails provide dummy functions to prevent ValueError
try:
    import database as db
except ImportError:
    st.error("Error: 'database.py' file not found! Please make sure it is in the same folder.")
    class DummyDB:
        def verify_user(self, u, p): return None
        def create_user(self, u, p): return False, "Database connection error"
        def get_user_config(self, uid): return {}
        def update_user_config(self, *args, **kwargs): pass
    db = DummyDB()

# ------------------------------------------------------------------------------------
# ⚡ PAGE CONFIG & NAME
# ------------------------------------------------------------------------------------
st.set_page_config(page_title=" Dɘvɪl UPDATE E2E 2025", page_icon="🛡️", layout="wide")

# ------------------------------------------------------------------------------------
# 🔥 LIVE LOGS SYSTEM
# ------------------------------------------------------------------------------------
def init_live_logs(max_lines: int = 200):
    if "live_logs" not in st.session_state:
        st.session_state.live_logs = []
    if "live_logs_max" not in st.session_state:
        st.session_state.live_logs_max = max_lines

def live_log(msg: str):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    init_live_logs()
    st.session_state.live_logs.append(line)
    if len(st.session_state.live_logs) > st.session_state.live_logs_max:
        st.session_state.live_logs = st.session_state.live_logs[-st.session_state.live_logs_max:]

def render_live_console():
    st.markdown('<div class="logbox">', unsafe_allow_html=True)
    for line in st.session_state.live_logs[-100:]:
        st.markdown(f'<p style="margin:0; font-family:monospace; color:#00ffcc; font-size:14px;">{line}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# 🎨 LUXURY NEON THEME CSS
# ------------------------------------------------------------------------------------
st.markdown("""
<style>
    /* Premium Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://i.postimg.cc/qq41rSVP/44e54h810v9b1.jpg');
        background-size: cover;
        background-attachment: fixed;
    }

    /* Modern Title Card */
    .main-header {
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(0, 255, 204, 0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 30px;
    }
    .main-header h1 {
        color: #00f2fe;
        text-transform: uppercase;
        letter-spacing: 5px;
        font-family: 'Segoe UI', sans-serif;
        text-shadow: 0 0 15px #00f2fe;
    }

    /* Stylish Log Console */
    .logbox {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #00f2fe;
        border-radius: 15px;
        padding: 20px;
        height: 300px;
        overflow-y: auto;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
    }

    /* Neon Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white !important;
        border: none;
        border-radius: 50px;
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.4s ease;
        text-transform: uppercase;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px #00f2fe;
    }

    /* Stop Button - Red Glow */
    .stButton [data-testid="baseButton-secondary"] {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important;
        box-shadow: 0 0 10px rgba(255, 75, 43, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>Dɘvɪl UPDATE E2E 2025</h1></div>', unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "automation_running" not in st.session_state: st.session_state.automation_running = False
if "automation_state" not in st.session_state:
    st.session_state.automation_state = type('obj',(object,),{
        "running": False,
        "message_count": 0,
        "message_rotation_index": 0
    })()

init_live_logs()

# ---------------- LOGIN & SIGNUP (FIXED) ----------------
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        tab1, tab2 = st.tabs(["🔑 LOGIN", "🛡️ REGISTER"])
        with tab1:
            u = st.text_input("Username", key="l_user")
            p = st.text_input("Password", type="password", key="l_pass")
            if st.button("Enter Dashboard"):
                uid = db.verify_user(u, p)
                if uid:
                    st.session_state.logged_in = True
                    st.session_state.user_id = uid
                    cfg = db.get_user_config(uid)
                    st.session_state.chat_id = cfg.get("chat_id", "")
                    st.session_state.chat_type = cfg.get("chat_type", "E2EE")
                    st.session_state.delay = cfg.get("delay", 15)
                    st.session_state.cookies = cfg.get("cookies", "")
                    st.session_state.messages = cfg.get("messages", "").split("\n") if cfg.get("messages") else []
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

        with tab2:
            nu = st.text_input("Choose Username", key="r_user")
            np = st.text_input("Choose Password", type="password", key="r_pass")
            npc = st.text_input("Confirm Password", type="password", key="r_pass_c")
            if st.button("Register Now"):
                if not nu or not np:
                    st.warning("Please fill all fields")
                elif np != npc:
                    st.error("Passwords do not match")
                else:
                    try:
                        ok, msg = db.create_user(nu, np)
                        if ok: st.success("Registration Successful! Please login.")
                        else: st.error(msg)
                    except Exception as e:
                        st.error(f"Database Error: {e}")
    st.stop()

# ---------------- DASHBOARD ----------------
col_head1, col_head2 = st.columns([4, 1])
col_head1.subheader(f"⚡ SYSTEM ACTIVE: USER {st.session_state.user_id}")
if col_head2.button("LOGOUT"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- CONFIG AREA ----------------
st.divider()
c_cfg1, c_cfg2 = st.columns(2)

with c_cfg1:
    chat_id = st.text_input("Target Chat ID", value=st.session_state.chat_id)
    chat_type = st.selectbox("Method", ["E2EE", "CONVO"], index=0 if st.session_state.chat_type == "E2EE" else 1)
    delay = st.number_input("Delay (Seconds)", 1, 300, value=st.session_state.delay)

with c_cfg2:
    msg_file = st.file_uploader("Upload Message List (.txt)", type=["txt"])
    if msg_file:
        st.session_state.messages = msg_file.read().decode().split("\n")
        st.toast("Messages Loaded!")
    cookies = st.text_area("FB Cookies", value=st.session_state.cookies, height=100)

if st.button("SAVE SYSTEM SETTINGS"):
    db.update_user_config(st.session_state.user_id, chat_id, chat_type, delay, cookies, "\n".join(st.session_state.messages))
    st.success("Configuration Saved!")

# ---------------- ENGINE ----------------
def setup_browser():
    opt = Options()
    opt.add_argument("--headless=new")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opt)

def find_input(driver, chat_type):
    sel = ["div[contenteditable='true']"] if chat_type == "E2EE" else ["div[contenteditable='true']", "textarea", "[role='textbox']"]
    for s in sel:
        try: return driver.find_element(By.CSS_SELECTOR, s)
        except: pass
    return None

def send_messages(cfg, stt):
    try:
        live_log("🚀 Initializing Dɘvɪl Engine...")
        d = setup_browser()
        d.get("https://www.facebook.com")
        time.sleep(5)
        for c in (cfg.get("cookies") or "").split(";"):
            if "=" in c:
                n, v = c.split("=", 1)
                try: d.add_cookie({"name":n.strip(), "value":v.strip(), "domain":".facebook.com", "path":"/"})
                except: pass
        d.get(f"https://www.facebook.com/messages/t/{cfg.get('chat_id','')}")
        time.sleep(10)
        box = find_input(d, cfg.get("chat_type"))
        if not box:
            live_log("❌ Error: Message box not found!")
            stt.running = False
            return
        msgs = [m.strip() for m in (cfg.get("messages") or "").split("\n") if m.strip()]
        while stt.running:
            msg = msgs[stt.message_rotation_index % len(msgs)]
            stt.message_rotation_index += 1
            box.send_keys(msg)
            box.send_keys("\n")
            stt.message_count += 1
            live_log(f"SENT: {msg}")
            time.sleep(cfg.get("delay", 15))
        d.quit()
    except Exception as e:
        live_log(f"Fatal Error: {e}")

# ---------------- CONTROLS ----------------
st.divider()
st.subheader("🚀 Automation Controls")
c_btn1, c_btn2 = st.columns(2)

if c_btn1.button("START SERVER", disabled=st.session_state.automation_running):
    cfg = db.get_user_config(st.session_state.user_id)
    st.session_state.automation_running = True
    st.session_state.automation_state.running = True
    t = threading.Thread(target=send_messages, args=(cfg, st.session_state.automation_state))
    t.start()

if c_btn2.button("STOP SERVER", key="stop_btn", disabled=not st.session_state.automation_running):
    st.session_state.automation_state.running = False
    st.session_state.automation_running = False
    live_log("🛑 Stopping server...")

st.info(f"MESSAGES DISPATCHED: {st.session_state.automation_state.message_count}")
render_live_console()

if st.session_state.automation_running:
    time.sleep(2)
    st.rerun()
