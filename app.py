import asyncio
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import requests

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = "8589070914:AAE_Bt-4Of0ylRv5NTh-Rfp-B08_tjDEVrw"  # अपना बॉट टोकन यहाँ डालें

# Your cookies from above (same as original)
cookies_dict = {
    "C": "SH3243707977",
    "M": "SH3243707977",
    "A": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJzaGVpbl9yaW5hZGFzZmt0ODQ0QGdtYWlsLmNvbSIsInBrSWQiOiI1N2M5YzA4Zi00M2I2LTRjZTQtOTY4MS1hZjRlZWY3N2Q4YmUiLCJjbGllbnROYW1lIjoid2ViX2NsaWVudCIsInJvbGVzIjpbeyJuYW1lIjoiUk9MRV9DVVNUT01FUkdST1VQIn1dLCJtb2JpbGUiOiI4OTI3MjY3MjA4IiwidGVuYW50SWQiOiJTSEVJTiIsImV4cCI6MTc2NzQ0ODE1OCwidXVpZCI6IjU3YzljMDhmLTQzYjYtNGNlNC05NjgxLWFmNGVlZjc3ZDhiZSIsImlhdCI6MTc2NDg1NjE1OCwiZW1haWwiOiJyaW5hZGFzZmt0ODQ0QGdtYWlsLmNvbSJ9.iiJ8CGndcuOGJb1uAtoyxPYE9utUQje9zz9zAnx5zQs8MC1WFrw390ngUmRciwqMwZCvUnW9qJY6LB6GcSd9nii9Id-n47IHfID-iBVgI2OpE__VukQFwYUEjUXzaDLW-wsErCvhSq6llSTAMmf9yNN_EqwAH3gAzweiBpah6nq5x1-2JhKrXAGzwHVKRf_GbxgBQ_exaXmKIFJOyzup_EjH0W_uvm5sLvFNGsjzqmbpvqPaCiftXrhsmSSps0OxrsKWH86aAw7HeHqtCiLfhj2-y2YV3BTUV1yuibbKzzpaxmZsx0d80LetsP9tilaXSBiHEEs66Rw6WTj4ipzvXQ",
    "R": "eyJhbGciOiJSUzI1NiJ9.eyJzZXNzaW9uIjp7InNlc3Npb25JZCI6ImMwNGEzODQyLWUxNzktNGUyYi05OGQzLTMzZGI4YTIxNDBiNiIsImNsaWVudE5hbWUiOiJ3ZWJfY2xpZW50Iiwicm9sZXMiOlt7Im5hbWUiOiJST0xFX0NVU1RPTUVSR1JPVVAifV0sInR5cGUiOiJyZWZyZXNoIiwidGVuYW50SWQiOiJTSEVJTiIsInN1YiI6InNoZWluX3JpbmFkYXNma3Q4NDRAZ21haWwuY29tIiwiZXhwIjoxNzgwNDA4MTU4LCJpYXQiOjE3NjQ4NTYxNTh9LlN6b082X3FMMkZNV0QwZDlBbTAza3pLaWFQY0Ryb0c0TzNGTXhVQ095NF9GQXZ2MUN2VktZZldacUNNS0p3VzJJYWNvUDNsazlSRlktWWItVFR3MlRuWFd6U1B1ZWdVVEJNM1ZCbmVZdTlYRlJMWXZMcUxDUVlnSFBLcnlNQTJ3eFUySnZZbHFOS3ljdXo0R2hVWVhkMG5wVnY2enRCVldNMGFqb0NyTVZUVjFvcmk3MURUWVJGaFBPTTdOYzEzS3JFeE1oeGJHZnZGWDNER0tDUXBrZ2dXR3NpMlRwbHJsdjFvWlgwZUlMRy1Hak5TMFFEN0pBc1hOd09ZQ0Y1M2xDRktuWXhWazNCNjZrcS1NT3E3emhHeHBtSTk3OWJsM2dXb0tOWnVBM0o5RkxvNkE5akpqTTItSGRPMlk5Rk1XRmdEMVlfd2wxQmFSVXlOb2dtT3RNU3ciLCJhIjoiayJ9.UTYdWt4ywNFFawRWDyLpDGLX3aZ6T_4_18oN4b8TYyVcN2qEVS1qPKQyUTvmsnD6MS5H_pKvZVjLwKBZQdCbBBRLIV2aF_s4D4eTF0jvB7AdNVNqEbhweECbfeqt2FSg_wfIQ3kYnwSHtKDc2lglgdu6NnvBYv1iDKidRh4jV5WJjzCXD3WpUfKq7gey4-2bTocwT8Fqw4F4xYw8oM-K0LYnBEx4lqWhjAgxfivH9tZ9ce4QwRcRDCu-pO0KqIY-eQZ2bGSdx9nQZYK0Qa9AEnLkTK0X9qZJXUnIsHtZIRzRgIJCkZOrfWW48E6rCQz2LEb6F8crKjJ8GhC0n1tWQ",
    "_ga": "GA1.1.1436561791.1764840068",
    "_gid": "GA1.2.991438247.1764855826",
    "_fbp": "fb.1.1764855826477.973236095401202595",
    "_gcl_au": "1.1.2029191440.1764840325",
    "bm_mi": "5707CB7663DCB00DCF85835BCE91B741~YAAQJMgsMeg2AqeaAQAAAtSa6R52wUJLu6xM4MpQ0xq5Rj7kO0TZGTawqYnIXykYaTRsLLtEHHB/27XTyUzxkXjf4sp3aMqpA6hAW4yf6XX5F0A7PfE6VDh6Y3YgsUbZCWd62471AkhaccZzmACt2CZ0m+U3/P8Si3RKekqtmR8I4fQAdODFMr+tuAUtIS7kaItjJXB6oNzS/DvxNf6xFlWqxxYcQ1AJ4mUXjtoi585iqAvAeNbUfB+fXjpksxbqeY9NbbvTcj4jP7mUBmlpRy+CsDt24ozu5CtHW/ZPNAxED7bPM3q7QMIHeGlTfOALjAJ+Tw==~1",
    "bm_sz": "6003BDC26CCA71802C48FCD9C0C6DCDD~YAAQNLEsMeWkX6CaAQAAqfDs6R4v/WiK5e3N4XG8vhK0dimu1WhRV8tl9sH+NGx59P1XzjGHO4UCo4QnuyeCG7ygYR8xIXnblaCeO8WhtOCRNlnHBzGmt+JUXy0j4FmH6gSenC5EcK+u+gLvFIdsrJ5oj2aalGp6ZeKw4Fw2Yz/92N5e+A2D+9Fyy0Nulo8hOzUuSarE5ZHjVi6x/O3N2buMs/AnnL0eLcZj4zTe2YPCKomNV0kiGmTJ3kylh5P0onC38Oa/38YvcV7ZOFAwKDNMGUCnMmAefvoDey9/Q0cuwUIw+vpubHjj4GP7Pj6lyZKLl3pXcN+6hZvsuwplqOL6qwVNLsWCxVp8iv/ZVas2WCIaHLJXXTr5RKydx0v/ihV4MmxseoMrNf+RneXGU/nZgDn0bn+CDHYGsNMi/ZZucwNEu99K0kAfySLlf8D5ENCH8QkWT0ojwLfNFb3IdWWgOhI77mceaog9MY76XZNilPccpIbe6h7kMUv/BNFt8E3UB/ZtLhp+D0ot7zix+qRwEo7Xxw1c5uGFJrcX4T0VRa7ONdSAXUs0PZcQ0bqQthWc4CXpmXZeZEsild9ghHsQc8NJcjiC8zr8Tu4etzU=~3553337~3294263",
    "bm_sv": "B602A9A59E0202E139487ED191946E78~YAAQNLEsMcalX6CaAQAAB+/v6R6PUZQvZ/c7EDHbL5uPZGzIgH3+sBvcSyUYtyxx7xcjyNw8QDPtM/tWXYiFnW6URK5dYGCKj4O6HPvjLr+jXCdvRyYztXMa/jZYhsDzsLjp7uA+5fU+bTLJh7xFquwUb8k1otdhvDWVMWIa+zuFD7wzVyLm1X8O/Fx/fKDWIIE305Td09rTR8t4tcS0aM+OgWSfvwEtXa/wvZsf0NgIIccQpQmze2fOKZbMqCjk0zmTch8=~1",
    "bookingType": "SHEIN",
    "CI": "57c9c08f-43b6-4ce4-9681-af4eef77d8be",
    "customerType": "New",
    "deviceId": "WBmtmWblwncD3H6AZ-2Pa",
    "EI": "F2sjGM%2FCsoPwMWDAwJHoS8gQEoeqjJj1lovnIWr5WZQGM8gh4IruiphDO4o61KtE",
    "G": "M",
    "GUID": "6aabce64-e86d-4153-89a5-97549940f34d",
    "LS": "LOGGED_IN",
    "MN": "8927267208",
    "PK": "2SNWYivGMWIBZdUE6%2F4YzpVMMb95SeDZBhxMIwrummbZnqnvXJwUGaTGkrt1eRGl",
    "SN": "Pradip",
    "U": "rinadasfkt844%40gmail.com",
    "V": "1",
    "_fpuuid": "WBmtmWblwncD3H6AZ-2Pa"
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-tenant-id": "SHEIN",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://www.sheinindia.in/cart",
    "origin": "https://www.sheinindia.in"
}

BASE_DATA_DIR = "user_data"  # सभी यूज़र डेटा इस फोल्डर में जाएगा

# ==================== USER-SPECIFIC FILE MANAGEMENT ====================
def get_user_folders(user_id):
    """Get user-specific folder paths"""
    user_folder = os.path.join(BASE_DATA_DIR, str(user_id))
    return user_folder

def initialize_user_files(user_id, session_id=None):
    """Initialize folders and files for a specific user"""
    user_folder = get_user_folders(user_id)
    
    # Create user folder if not exists
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    
    # Generate session-specific log file
    if session_id is None:
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create session-specific folder
    session_folder = os.path.join(user_folder, f"session_{session_id}")
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)
    
    log_file = os.path.join(session_folder, f"session_{session_id}_log.txt")
    
    # Write log header
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=== SHEIN COUPON TEST LOG ===\n")
        f.write(f"User ID: {user_id}\n")
        f.write(f"Session: {session_id}\n")
        f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 40 + "\n\n")
    
    return log_file, session_folder, session_id

def save_coupon_instantly(user_id, session_id, coupon_code, discount_amount, min_purchase):
    """Save coupon to user's session-specific folder"""
    try:
        if min_purchase > 0:
            return False
        
        user_folder = get_user_folders(user_id)
        session_folder = os.path.join(user_folder, f"session_{session_id}")
        
        if not os.path.exists(session_folder):
            os.makedirs(session_folder)
        
        filename = os.path.join(session_folder, f"{discount_amount}_rupees.txt")
        
        # Read existing coupons from this session only
        existing_coupons = set()
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_coupons = set(line.strip() for line in f if line.strip())
        
        # Add new coupon if not already exists in this session
        if coupon_code not in existing_coupons:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"{coupon_code}\n")
            return True
        else:
            return False
    
    except Exception as e:
        print(f"❌ Error saving coupon for user {user_id} session {session_id}: {e}")
        return False

def log_test_result(log_file, coupon_code, status, details=""):
    """Log test result to user's log file"""
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%H:%M:%S")
            if status == "active":
                f.write(f"[{timestamp}] ✅ {coupon_code} - ACTIVE - {details}\n")
            elif status == "not_applicable":
                f.write(f"[{timestamp}] ❌ {coupon_code} - NOT APPLICABLE\n")
            elif status == "error":
                f.write(f"[{timestamp}] ⚠️  {coupon_code} - ERROR: {details}\n")
            elif status == "skipped":
                f.write(f"[{timestamp}] ⏭️  {coupon_code} - SKIPPED: {details}\n")
    except Exception as e:
        print(f"⚠️  Could not log result: {e}")

def cleanup_old_sessions(user_id, keep_last=5):
    """Clean up old session folders, keep only last N sessions"""
    try:
        user_folder = get_user_folders(user_id)
        
        if not os.path.exists(user_folder):
            return
        
        # Get all session folders
        session_folders = []
        for item in os.listdir(user_folder):
            if item.startswith("session_"):
                item_path = os.path.join(user_folder, item)
                if os.path.isdir(item_path):
                    session_folders.append((item_path, os.path.getmtime(item_path)))
        
        # Sort by modification time (oldest first)
        session_folders.sort(key=lambda x: x[1])
        
        # Delete oldest session folders, keep only last N
        if len(session_folders) > keep_last:
            for i in range(len(session_folders) - keep_last):
                import shutil
                shutil.rmtree(session_folders[i][0])
                print(f"🗑️  Cleaned up old session: {os.path.basename(session_folders[i][0])}")
    
    except Exception as e:
        print(f"⚠️  Error cleaning up sessions: {e}")

# ==================== COUPON TESTING FUNCTIONS ====================
def test_coupon(user_id, session_id, log_file, coupon_code, expected_amount=None, min_purchase=0):
    """Test a single coupon on the cart"""
    
    if expected_amount == 500 and min_purchase > 0:
        log_test_result(log_file, coupon_code, "skipped", f"Min purchase ₹{min_purchase}")
        return {"status": "skipped", "code": coupon_code, "reason": f"Min purchase ₹{min_purchase}"}
    
    payload = {
        "voucherId": coupon_code,
        "device": {"client_type": "MSITE"}
    }
    
    try:
        response = requests.post(
            "https://www.sheinindia.in/api/cart/apply-voucher",
            json=payload,
            headers=headers,
            cookies=cookies_dict,
            timeout=10
        )
    except Exception as e:
        error_msg = f"Network error: {e}"
        log_test_result(log_file, coupon_code, "error", error_msg)
        return {"status": "error", "code": coupon_code, "error": str(e)}
    
    if response.status_code == 200:
        try:
            result = response.json()
            applied_vouchers = result.get("appliedVouchers", [])
            voucher_amount = result.get("voucherAmount", {}).get("value", 0)
            total_price = result.get("totalPrice", {}).get("value", 0)
            
            if applied_vouchers or voucher_amount > 0:
                if voucher_amount > 0:
                    saved = save_coupon_instantly(user_id, session_id, coupon_code, voucher_amount, min_purchase)
                
                log_test_result(log_file, coupon_code, "active", f"₹{voucher_amount} off")
                return {
                    "status": "active",
                    "code": coupon_code,
                    "discount_amount": voucher_amount,
                    "new_total": total_price,
                    "saved": saved if voucher_amount > 0 else False
                }
            else:
                log_test_result(log_file, coupon_code, "not_applicable")
                return {
                    "status": "not_applicable",
                    "code": coupon_code
                }
                
        except json.JSONDecodeError:
            error_msg = "Invalid JSON response"
            log_test_result(log_file, coupon_code, "error", error_msg)
            return {
                "status": "error",
                "code": coupon_code,
                "error": error_msg
            }
    else:
        error_msg = f"HTTP {response.status_code}"
        try:
            error_data = response.json()
            detailed_error = error_data.get('errorMessage', {}).get('errors', [{}])[0].get('message', '')
            if detailed_error:
                error_msg = f"{error_msg} - {detailed_error}"
        except:
            pass
        
        log_test_result(log_file, coupon_code, "error", error_msg)
        return {
            "status": "error",
            "code": coupon_code,
            "error": error_msg
        }

def parse_coupon_text(text):
    """Parse coupon codes from text (one per line or comma separated)"""
    coupons = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Try to extract coupon code (assume it's alphanumeric, 8-20 chars)
        import re
        possible_codes = re.findall(r'[A-Za-z0-9]{8,20}', line)
        
        for code in possible_codes:
            coupons.append({
                "code": code,
                "original_line": line
            })
    
    return coupons

def get_summary_text(results):
    """Generate summary text from test results"""
    active_by_amount = {}
    skipped = []
    not_applicable = []
    errors = []
    
    for result in results:
        if result["status"] == "active":
            amount = result.get("discount_amount", 0)
            if amount not in active_by_amount:
                active_by_amount[amount] = []
            active_by_amount[amount].append(result["code"])
        elif result["status"] == "skipped":
            skipped.append(result["code"])
        elif result["status"] == "not_applicable":
            not_applicable.append(result["code"])
        else:
            errors.append(result["code"])
    
    total_tested = len(results)
    total_active = sum(len(codes) for codes in active_by_amount.values())
    
    summary = f"**Testing Completed**\n\n"
    summary += f"✅ **Total Tested:** {total_tested}\n"
    summary += f"✅ **Active Coupons:** {total_active}\n"
    summary += f"⏭️  **Skipped:** {len(skipped)}\n"
    summary += f"❌ **Not Applicable:** {len(not_applicable)}\n"
    summary += f"⚠️  **Errors:** {len(errors)}\n\n"
    
    if active_by_amount:
        summary += "💰 **Active Coupons by Amount:**\n"
        for amount in sorted(active_by_amount.keys(), reverse=True):
            count = len(active_by_amount[amount])
            summary += f"  • ₹{amount}: {count} coupons\n"
    
    return summary

def get_download_buttons(user_id, session_id):
    """Create inline keyboard for download options for THIS user session"""
    user_folder = get_user_folders(user_id)
    session_folder = os.path.join(user_folder, f"session_{session_id}")
    
    keyboard = []
    
    if os.path.exists(session_folder):
        files = sorted([f for f in os.listdir(session_folder) if f.endswith("_rupees.txt")])
        
        # Group buttons in rows of 2
        for i in range(0, len(files), 2):
            row = []
            if i < len(files):
                amount = files[i].replace("_rupees.txt", "")
                callback_data = f"dwn:{user_id}:{session_id}:{amount}"
                row.append(InlineKeyboardButton(
                    f"₹{amount} Coupons", 
                    callback_data=callback_data
                ))
            if i+1 < len(files):
                amount = files[i+1].replace("_rupees.txt", "")
                callback_data = f"dwn:{user_id}:{session_id}:{amount}"
                row.append(InlineKeyboardButton(
                    f"₹{amount} Coupons", 
                    callback_data=callback_data
                ))
            keyboard.append(row)
    
    # Add session-specific buttons
    keyboard.append([
        InlineKeyboardButton(
            "📄 This Session Log", 
            callback_data=f"log:{user_id}:{session_id}"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            "📊 All Active (This Session)", 
            callback_data=f"all:{user_id}:{session_id}"
        )
    ])
    
    # Add clear data button
    keyboard.append([
        InlineKeyboardButton(
            "🗑️ Clear All My Data", 
            callback_data=f"clear:{user_id}"
        )
    ])
    
    # Add button to list all sessions
    keyboard.append([
        InlineKeyboardButton(
            "📋 My Previous Sessions", 
            callback_data=f"listsessions:{user_id}"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

# ==================== TELEGRAM BOT HANDLERS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    user_id = update.effective_user.id
    
    welcome_text = (
        "🎟️ *Shein Coupon Checker BOT*\n\n"
        "Send coupon codes (one per line) and I'll test them for you."
    )
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    user_id = update.effective_user.id
    
    help_text = (
        f"👤 **User ID:** `{user_id}`\n"
        "*Help Guide*\n\n"
        "1. *Bulk Testing:* Send multiple coupon codes (one per line)\n"
        "2. *Session-based Storage:* Each scan session's coupons are saved separately\n"
        "3. *Private Results:* Only you can see/download your coupons\n"
        "4. *Auto-Cleanup:* Old sessions are automatically deleted (keeps last 5)\n\n"
        "*Commands:*\n"
        "`/start` - Welcome message\n"
        "`/help` - This help guide\n"
        "`/test` - Start new testing session\n"
        "`/clear` - Clear all your data\n"
        "`/status` - Check your storage status\n"
        "`/listsessions` - List all your previous sessions\n\n"
        "*How to use:*\n"
        "Just send coupon codes (one per line) and I'll test them automatically.\n"
        "Each session's results are saved separately."
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start testing mode."""
    await update.message.reply_text(
        "🔍 *Test Mode*\n\n"
        "Please send coupon codes to test.\n"
        "Format: One coupon code per line.\n\n"
        "Example:\n"
        "```\n"
        "ABCD1234EFGH\n"
        "WXYZ5678IJKL\n"
        "MNOP9012QRST\n"
        "```\n\n"
        "*Note:* Each test session is saved separately.",
        parse_mode='Markdown'
    )

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear all user data."""
    user_id = update.effective_user.id
    user_folder = get_user_folders(user_id)
    
    if os.path.exists(user_folder):
        import shutil
        shutil.rmtree(user_folder)
        message = "✅ All your data has been cleared!"
    else:
        message = "ℹ️ No data found to clear."
    
    await update.message.reply_text(message)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check user's storage status."""
    user_id = update.effective_user.id
    user_folder = get_user_folders(user_id)
    
    if not os.path.exists(user_folder):
        await update.message.reply_text("📭 No data stored yet.")
        return
    
    # Count files and sizes
    total_size = 0
    file_count = 0
    session_count = 0
    
    for root, dirs, files in os.walk(user_folder):
        for file in files:
            filepath = os.path.join(root, file)
            total_size += os.path.getsize(filepath)
            file_count += 1
    
    # Count session folders
    session_folders = []
    for item in os.listdir(user_folder):
        if item.startswith("session_"):
            item_path = os.path.join(user_folder, item)
            if os.path.isdir(item_path):
                session_count += 1
                session_folders.append(item)
    
    status_text = f"👤 **User ID:** `{user_id}`\n\n"
    status_text += f"📊 **Storage Usage:**\n"
    status_text += f"• Files: {file_count}\n"
    status_text += f"• Size: {total_size/1024:.1f} KB\n"
    status_text += f"• Sessions: {session_count}\n\n"
    
    if session_folders:
        status_text += "📋 **Your Recent Sessions:**\n"
        recent_sessions = sorted(session_folders, reverse=True)[:5]
        for session in recent_sessions:
            session_id = session.replace("session_", "")
            session_path = os.path.join(user_folder, session)
            
            # Count coupons in this session
            coupon_count = 0
            if os.path.exists(session_path):
                for file in os.listdir(session_path):
                    if file.endswith("_rupees.txt"):
                        filepath = os.path.join(session_path, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                coupon_count += len(f.readlines())
                        except:
                            pass
            
            status_text += f"• `{session_id}`: {coupon_count} coupons\n"
    else:
        status_text += "📋 **Your Sessions:** None yet\n"
    
    status_text += f"\n🗑️ Use `/clear` to delete all data"
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def listsessions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all user sessions."""
    user_id = update.effective_user.id
    user_folder = get_user_folders(user_id)
    
    if not os.path.exists(user_folder):
        await update.message.reply_text("📭 No sessions found.")
        return
    
    session_folders = []
    for item in os.listdir(user_folder):
        if item.startswith("session_"):
            item_path = os.path.join(user_folder, item)
            if os.path.isdir(item_path):
                session_folders.append(item)
    
    if not session_folders:
        await update.message.reply_text("📭 No sessions found.")
        return
    
    session_folders.sort(reverse=True)
    
    keyboard = []
    for session in session_folders[:10]:  # Show last 10 sessions
        session_id = session.replace("session_", "")
        keyboard.append([
            InlineKeyboardButton(
                f"📂 Session {session_id[:8]}...",
                callback_data=f"viewsession:{user_id}:{session_id}"
            )
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"📋 **Your Sessions**\n\n"
        f"Total: {len(session_folders)} sessions\n"
        f"Click on a session to view/download its coupons:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Store active sessions
user_sessions = {}

async def handle_coupon_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming coupon codes."""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    # Parse coupon codes from message
    coupons_data = parse_coupon_text(user_message)
    
    if not coupons_data:
        await update.message.reply_text(
            "❌ No valid coupon codes found.\n"
            "Please send one coupon code per line.\n\n"
            "Example:\n"
            "```\n"
            "COUPON1234\n"
            "DISCOUNT5678\n"
            "SAVE9012\n"
            "```",
            parse_mode='Markdown'
        )
        return
    
    # Clean up old sessions first
    cleanup_old_sessions(user_id)
    
    # Generate session ID
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize user files for this session
    log_file, session_folder, session_id = initialize_user_files(user_id, session_id)
    
    # Store session info
    user_sessions[user_id] = {
        "session_id": session_id,
        "log_file": log_file,
        "session_folder": session_folder,
        "start_time": datetime.now()
    }
    
    # Send initial message
    status_msg = await update.message.reply_text(
        f"🆔 **Session ID:** `{session_id}`\n"
        f"🔍 Found {len(coupons_data)} coupon(s)\n"
        "Starting test...\n"
        "⏳ Please wait...",
        parse_mode='Markdown'
    )
    
    # Test each coupon
    results = []
    tested = 0
    
    for coupon_data in coupons_data:
        tested += 1
        
        # Update status every 5 coupons
        if tested % 5 == 0 or tested == len(coupons_data):
            active_count = sum(1 for r in results if r['status'] == 'active')
            await status_msg.edit_text(
                f"🆔 **Session:** `{session_id}`\n"
                f"🔍 Testing... {tested}/{len(coupons_data)}\n"
                f"✅ Active: {active_count}\n"
                "⏳ Please wait...",
                parse_mode='Markdown'
            )
        
        # Test the coupon
        result = test_coupon(user_id, session_id, log_file, coupon_data["code"])
        results.append(result)
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(0.1)
    
    # Generate summary
    summary = get_summary_text(results)
    
    # Calculate session duration
    if user_id in user_sessions:
        duration = (datetime.now() - user_sessions[user_id]["start_time"]).total_seconds()
        summary += f"\n⏱️ **Duration:** {duration:.1f} seconds"
    
    # Send summary with download buttons
    await status_msg.edit_text(
        f"🆔 **Session:** `{session_id}`\n\n" + summary + "\n👇 **Download This Session's Coupons:**",
        parse_mode='Markdown',
        reply_markup=get_download_buttons(user_id, session_id)
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks - VERIFY USER AUTHORIZATION."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    # Split callback data using colon separator
    parts = callback_data.split(":")
    
    # Handle clear request
    if parts[0] == "clear":
        requested_user_id = parts[1]
        
        # VERIFICATION: Check if the requesting user matches the user in callback
        if str(user_id) != requested_user_id:
            await query.message.reply_text("❌ Unauthorized access!")
            return
        
        # Clear user data
        user_folder = get_user_folders(user_id)
        if os.path.exists(user_folder):
            import shutil
            shutil.rmtree(user_folder)
            await query.message.reply_text("✅ All your data has been cleared!")
        else:
            await query.message.reply_text("ℹ️ No data found to clear.")
        
        # Update message
        await query.edit_message_text(
            "✅ All your data has been cleared!\n\n"
            "Send coupon codes to start a new session.",
            reply_markup=None
        )
        return
    
    # Handle view session request
    elif parts[0] == "viewsession":
        if len(parts) != 3:
            await query.message.reply_text("❌ Invalid request format.")
            return
        
        requested_user_id = parts[1]
        session_id = parts[2]
        
        # VERIFICATION: Check if the requesting user matches the user in callback
        if str(user_id) != requested_user_id:
            await query.message.reply_text("❌ Unauthorized access! You can only view your own sessions.")
            return
        
        # User verified, show session details
        user_folder = get_user_folders(user_id)
        session_folder = os.path.join(user_folder, f"session_{session_id}")
        
        if not os.path.exists(session_folder):
            await query.message.reply_text("❌ Session folder not found.")
            return
        
        # Count coupons in this session
        coupon_files = []
        total_coupons = 0
        
        for file in os.listdir(session_folder):
            if file.endswith("_rupees.txt"):
                filepath = os.path.join(session_folder, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        coupon_count = len(f.readlines())
                        amount = file.replace("_rupees.txt", "")
                        coupon_files.append((amount, coupon_count))
                        total_coupons += coupon_count
                except:
                    continue
        
        if coupon_files:
            # Create keyboard for downloading session files
            keyboard = []
            
            # Add coupon amount buttons
            for i in range(0, len(coupon_files), 2):
                row = []
                if i < len(coupon_files):
                    amount, count = coupon_files[i]
                    callback_data = f"dwn:{user_id}:{session_id}:{amount}"
                    row.append(InlineKeyboardButton(
                        f"₹{amount} ({count})", 
                        callback_data=callback_data
                    ))
                if i+1 < len(coupon_files):
                    amount, count = coupon_files[i+1]
                    callback_data = f"dwn:{user_id}:{session_id}:{amount}"
                    row.append(InlineKeyboardButton(
                        f"₹{amount} ({count})", 
                        callback_data=callback_data
                    ))
                if row:
                    keyboard.append(row)
            
            # Add session log button
            keyboard.append([
                InlineKeyboardButton(
                    "📄 Session Log", 
                    callback_data=f"log:{user_id}:{session_id}"
                ),
                InlineKeyboardButton(
                    "📊 All Coupons", 
                    callback_data=f"all:{user_id}:{session_id}"
                )
            ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                f"📂 **Session Details**\n\n"
                f"Session ID: `{session_id}`\n"
                f"Total Coupons: {total_coupons}\n"
                f"Available Amounts: {len(coupon_files)}\n\n"
                f"Select what to download:",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        else:
            await query.message.reply_text(f"❌ No coupons found in session {session_id}")
    
    # Handle list sessions request
    elif parts[0] == "listsessions":
        requested_user_id = parts[1]
        
        # VERIFICATION: Check if the requesting user matches the user in callback
        if str(user_id) != requested_user_id:
            await query.message.reply_text("❌ Unauthorized access! You can only view your own sessions.")
            return
        
        await listsessions_command(update, context)
    
    # Handle log download request
    elif parts[0] == "log":
        if len(parts) != 3:
            await query.message.reply_text("❌ Invalid request format.")
            return
        
        requested_user_id = parts[1]
        session_id = parts[2]
        
        # VERIFICATION: Check if the requesting user matches the user in callback
        if str(user_id) != requested_user_id:
            await query.message.reply_text("❌ Unauthorized access! You can only download your own files.")
            return
        
        # User verified, proceed with download
        user_folder = get_user_folders(user_id)
        
        # Send session log file
        log_file = os.path.join(user_folder, f"session_{session_id}", f"session_{session_id}_log.txt")
        
        if os.path.exists(log_file):
            try:
                with open(log_file, 'rb') as f:
                    await query.message.reply_document(
                        document=f,
                        filename=f"session_{session_id}_log.txt",
                        caption=f"📄 Session Log: {session_id}"
                    )
            except Exception as e:
                await query.message.reply_text(f"❌ Error sending file: {e}")
        else:
            await query.message.reply_text("❌ Session log file not found.")
    
    # Handle all coupons download request
    elif parts[0] == "all":
        if len(parts) != 3:
            await query.message.reply_text("❌ Invalid request format.")
            return
        
        requested_user_id = parts[1]
        session_id = parts[2]
        
        # VERIFICATION: Check if the requesting user matches the user in callback
        if str(user_id) != requested_user_id:
            await query.message.reply_text("❌ Unauthorized access! You can only download your own files.")
            return
        
        # User verified, proceed with download
        user_folder = get_user_folders(user_id)
        session_folder = os.path.join(user_folder, f"session_{session_id}")
        
        # Send all active coupons from this session
        all_coupons = []
        if os.path.exists(session_folder):
            for file in sorted(os.listdir(session_folder)):
                if file.endswith("_rupees.txt"):
                    filepath = os.path.join(session_folder, file)
                    try:
                        amount = file.replace("_rupees.txt", "")
                        with open(filepath, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            all_coupons.append(f"=== ₹{amount} Coupons ({len(lines)} total) ===\n")
                            all_coupons.extend(lines)
                            all_coupons.append("\n")
                    except:
                        continue
        
        if all_coupons:
            temp_file = os.path.join(session_folder, f"all_coupons_{session_id}.txt")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.writelines(all_coupons)
            
            try:
                with open(temp_file, 'rb') as f:
                    await query.message.reply_document(
                        document=f,
                        filename=f"session_{session_id}_all_coupons.txt",
                        caption=f"📂 All coupons from Session: {session_id}"
                    )
            except Exception as e:
                await query.message.reply_text(f"❌ Error sending file: {e}")
            
            # Delete temp file
            try:
                os.remove(temp_file)
            except:
                pass
        else:
            await query.message.reply_text("❌ No coupons found in this session.")
    
    # Handle specific amount download request
    elif parts[0] == "dwn":
        if len(parts) != 4:
            await query.message.reply_text("❌ Invalid request format.")
            return
        
        requested_user_id = parts[1]
        session_id = parts[2]
        file_type = parts[3]
        
        # VERIFICATION: Check if the requesting user matches the user in callback
        if str(user_id) != requested_user_id:
            await query.message.reply_text("❌ Unauthorized access! You can only download your own files.")
            return
        
        # User verified, proceed with download
        user_folder = get_user_folders(user_id)
        session_folder = os.path.join(user_folder, f"session_{session_id}")
        
        # Send specific amount file
        filename = os.path.join(session_folder, f"{file_type}_rupees.txt")
        
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    # Count lines
                    f.seek(0)
                    line_count = sum(1 for _ in f)
                    f.seek(0)
                    
                    await query.message.reply_document(
                        document=f,
                        filename=f"{file_type}_rupees_{session_id}.txt",
                        caption=f"💰 ₹{file_type} Coupons ({line_count} coupons)\nSession: {session_id}"
                    )
            except Exception as e:
                await query.message.reply_text(f"❌ Error sending file: {e}")
        else:
            await query.message.reply_text(f"❌ No ₹{file_type} coupons found in this session.")
    
    else:
        await query.message.reply_text("❌ Unknown request type.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    print(f"Update {update} caused error {context.error}")

# ==================== MAIN FUNCTION ====================
def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Create base data directory
    if not os.path.exists(BASE_DATA_DIR):
        os.makedirs(BASE_DATA_DIR)
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("listsessions", listsessions_command))
    
    # Add message handler for coupon codes
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_coupon_message))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the Bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()