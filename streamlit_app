import streamlit as st
import threading, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import database as db

# Page Config updated with new title
st.set_page_config(page_title="WALEED UPDATE E2E 2025", page_icon="⚡", layout="wide")

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
        st.markdown(f'<p style="margin:0; font-family:monospace; font-size:14px;">{line}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- NEW STYLISH CSS ----------------
st.markdown("""
<style>
    /* Full Page Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://i.postimg.cc/qq41rSVP/44e54h810v9b1.jpg');
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Modern Glassmorphism Card Style */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
        color: #fff;
    }

    /* Stop Button Color */
    button[kind="secondary"] {
        background: linear-gradient(45deg, #ff416c 0%, #ff4b2b 100%) !important;
        border: none !important;
        color: white !important;
    }

    /* Main Header */
    .main-header {
        text-align: center;
        color: #00f2fe;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 20px rgba(0,242,254,0.6);
        padding: 20px;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
    }

    /* Log Box Styling */
    .logbox {
        background: rgba(10, 10, 10, 0.85);
        color: #00ffcc;
        padding: 20px;
        height: 350px;
        overflow-y: auto;
        border-radius: 15px;
        border: 1px solid #00f2fe;
        box-shadow: inset 0 0 15px rgba(0,255,204,0.2);
    }

    /* Inputs and Areas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
    }
    
    label { color: #00f2fe !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>WALEED UPDATE E2E 2025</h1></div>', unsafe_allow_html=True)


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


# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    cols = st.columns([1,2,1])
    with cols[1]:
        tab1, tab2 = st.tabs(["🔑 Login", "👤 Create Account"])
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Access Dashboard"):
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
                    if cfg.get("running", False):
                        st.session_state.automation_running = True
                        st.session_state.automation_state.running = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with tab2:
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            npc = st.text_input("Confirm Password", type="password")
            if st.button("Register Now"):
                if np != npc:
                    st.error("Passwords do not match")
                else:
                    ok, msg = db.create_user(nu, np)
                    if ok: st.success("Account Created Successfully!")
                    else: st.error(msg)
    st.stop()


# ---------------- DASHBOARD ----------------
c1, c2 = st.columns([3, 1])
with c1:
    st.subheader(f"👋 Welcome back, ID: {st.session_state.user_id}")
with c2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.automation_running = False
        st.session_state.automation_state.running = False
        st.rerun()

st.divider()

# ---------------- CONFIG & FILE ----------------
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### ⚙️ Configuration")
    chat_id = st.text_input("Chat ID / URL", value=st.session_state.chat_id)
    chat_type = st.selectbox("Chat Method", ["E2EE", "CONVO"], index=0 if st.session_state.chat_type == "E2EE" else 1)
    delay = st.number_input("Speed Delay (Seconds)", 1, 300, value=st.session_state.delay)
    
with col_right:
    st.markdown("### 📝 Message Data")
    msg_file = st.file_uploader("Upload Message File (.txt)", type=["txt"])
    if msg_file:
        st.session_state.messages = msg_file.read().decode().split("\n")
        st.toast("Messages Loaded!", icon="✅")
    
    cookies = st.text_area("Paste Cookies Here", value=st.session_state.cookies, height=115)

if st.button("💾 SAVE CONFIGURATION"):
    db.update_user_config(
        st.session_state.user_id,
        chat_id, chat_type, delay,
        cookies, "\n".join(st.session_state.messages),
        running=st.session_state.automation_running
    )
    st.success("Config updated in database!")


# ---------------- AUTOMATION ENGINE ----------------
def setup_browser():
    opt = Options()
    opt.add_argument("--headless=new")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opt)

def find_input(driver, chat_type):
    sel = ["div[contenteditable='true']"] if chat_type == "E2EE" else ["div[contenteditable='true']", "textarea", "[role='textbox']"]
    for s in sel:
        try:
            return driver.find_element(By.CSS_SELECTOR, s)
        except: pass
    return None

def send_messages(cfg, stt):
    try:
        live_log("Initializing engine...")
        d = setup_browser()
        d.get("https://www.facebook.com")
        time.sleep(5)

        for c in (cfg.get("cookies") or "").split(";"):
            if "=" in c:
                n, v = c.split("=", 1)
                try:
                    d.add_cookie({"name":n.strip(), "value":v.strip(), "domain":".facebook.com", "path":"/"})
                except: pass

        d.get(f"https://www.facebook.com/messages/t/{cfg.get('chat_id','')}")
        time.sleep(8)
        live_log("✅ Connection established with Chat")

        box = find_input(d, cfg.get("chat_type"))
        if not box:
            live_log("❌ ERROR: Input box not found")
            stt.running = False
            return

        msgs = [m.strip() for m in (cfg.get("messages") or "").split("\n") if m.strip()]
        if not msgs: msgs = ["System Online"]

        while stt.running:
            msg = msgs[stt.message_rotation_index % len(msgs)]
            stt.message_rotation_index += 1
            try:
                box.send_keys(msg)
                box.send_keys("\n")
                stt.message_count += 1
                live_log(f"SENT >> {msg}")
            except Exception as e:
                live_log(f"⚠ Minor Error: {e}")
            time.sleep(cfg.get("delay", 15))

        live_log("System Offline")
        d.quit()
    except Exception as e:
        live_log(f"🛑 FATAL: {e}")

# ---------------- CONTROLS ----------------
st.divider()
st.subheader("🚀 Control Panel")

c_start, c_stop = st.columns(2)

if c_start.button("▶ START AUTOMATION", disabled=st.session_state.automation_running):
    cfg = db.get_user_config(st.session_state.user_id)
    cfg["running"] = True
    st.session_state.automation_running = True
    st.session_state.automation_state.running = True
    t = threading.Thread(target=send_messages, args=(cfg, st.session_state.automation_state))
    t.daemon = True
    t.start()
    st.rerun()

if c_stop.button("⏹ STOP AUTOMATION", disabled=not st.session_state.automation_running):
    st.session_state.automation_state.running = False
    st.session_state.automation_running = False
    live_log("🛑 Termination signal sent...")

# ---------------- LOGS ----------------
st.markdown("### 📡 System Activity")
st.info(f"Total Sent: {st.session_state.automation_state.message_count}")
render_live_console()

if st.session_state.automation_running:
    time.sleep(2)
    st.rerun()
