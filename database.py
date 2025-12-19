# database.py - Complete working version
import sqlite3
import hashlib
import json
from datetime import datetime

def init_db():
    """Initialize database with tables"""
    conn = sqlite3.connect('waleed_tool.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            approval_status TEXT DEFAULT 'pending',
            approval_key TEXT,
            real_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            automation_running INTEGER DEFAULT 0
        )
    ''')
    
    # User configurations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_configs (
            user_id INTEGER PRIMARY KEY,
            chat_id TEXT,
            name_prefix TEXT,
            delay INTEGER DEFAULT 5,
            cookies TEXT,
            messages_file_content TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create a new user"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return False, "Username already exists"
        
        # Create user
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return True, "User created successfully", user_id
    except Exception as e:
        return False, f"Error: {str(e)}"

def verify_user(username, password):
    """Verify user credentials"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    except:
        return None

def get_approval_status(user_id):
    """Get approval status for a user"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT approval_status FROM users WHERE id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 'pending'
    except:
        return 'pending'

def set_approval_key(user_id, approval_key):
    """Set approval key for a user"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET approval_key = ? WHERE id = ?",
            (approval_key, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_approval_key(user_id):
    """Get approval key for a user"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT approval_key FROM users WHERE id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    except:
        return None

def update_approval_status(user_id, status):
    """Update approval status"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET approval_status = ? WHERE id = ?",
            (status, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except:
        return False

def update_user_real_name(user_id, real_name):
    """Update user's real name"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET real_name = ? WHERE id = ?",
            (real_name, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_user_real_name(user_id):
    """Get user's real name"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT real_name FROM users WHERE id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else ""
    except:
        return ""

def get_username(user_id):
    """Get username by ID"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT username FROM users WHERE id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else ""
    except:
        return ""

def set_automation_running(user_id, running):
    """Set automation running status"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET automation_running = ? WHERE id = ?",
            (1 if running else 0, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_automation_running(user_id):
    """Get automation running status"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT automation_running FROM users WHERE id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return bool(result[0]) if result else False
    except:
        return False

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages_file_content):
    """Update user configuration"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        # Check if config exists
        cursor.execute("SELECT user_id FROM user_configs WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            # Update existing
            cursor.execute('''
                UPDATE user_configs SET 
                chat_id = ?, name_prefix = ?, delay = ?, cookies = ?, messages_file_content = ?
                WHERE user_id = ?
            ''', (chat_id, name_prefix, delay, cookies, messages_file_content, user_id))
        else:
            # Insert new
            cursor.execute('''
                INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, cookies, messages_file_content)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, chat_id, name_prefix, delay, cookies, messages_file_content))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Config update error: {e}")
        return False

def get_user_config(user_id):
    """Get user configuration"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT chat_id, name_prefix, delay, cookies, messages_file_content FROM user_configs WHERE user_id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'chat_id': result[0] or '',
                'name_prefix': result[1] or '',
                'delay': result[2] or 5,
                'cookies': result[3] or '',
                'messages_file_content': result[4] or ''
            }
        else:
            return {
                'chat_id': '',
                'name_prefix': '',
                'delay': 5,
                'cookies': '',
                'messages_file_content': ''
            }
    except:
        return {
            'chat_id': '',
            'name_prefix': '',
            'delay': 5,
            'cookies': '',
            'messages_file_content': ''
        }

def get_pending_approvals():
    """Get all users with pending approval"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, approval_key, real_name FROM users 
            WHERE approval_status = 'pending' 
            ORDER BY created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    except:
        return []

def get_approved_users():
    """Get all approved users"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, approval_key, real_name, automation_running FROM users 
            WHERE approval_status = 'approved' 
            ORDER BY created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    except:
        return []

def get_all_users():
    """Get all users"""
    try:
        conn = sqlite3.connect('waleed_tool.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, approval_status, real_name, approval_key FROM users 
            ORDER BY created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    except:
        return []

# Initialize database when module is imported
init_db()
