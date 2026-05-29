#!/usr/bin/env python3
# APK FUD BOT - Simple Contact Bot
# Developer: Rahul Mod Developer

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time
import threading
from flask import Flask, jsonify
from datetime import datetime

# 🔑 BOT CONFIG
BOT_TOKEN = "8766471260:AAEzCxeEJTL9l-2JoO09zHpgR-409-j9QTM"
ADMIN_ID = 8366608745
SUPPORT_USERNAME = "RahulMod77"  # Contact username

# Store verified users with timestamp
verified_users = {}  # {user_id: {"date": "2024-01-01", "username": "username"}}
pending_requests = {}  # For future use

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ============= MAIN KEYBOARD (Only Contact Button) =============
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    contact_btn = InlineKeyboardButton("📞 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐓𝐎 𝐁𝐔𝐘", url=f"https://t.me/{SUPPORT_USERNAME}")
    keyboard.add(contact_btn)
    return keyboard

# ============= START COMMAND =============
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if user_id in verified_users:
        welcome_back = """
╔══════════════════════════════╗
║      🔥 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐀𝐂𝐊 🔥      ║
╚══════════════════════════════╝

✅ **𝐘𝐨𝐮 𝐚𝐫𝐞 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐯𝐞𝐫𝐢𝐟𝐢𝐞𝐝!**

📱 **𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀𝐏𝐊 𝐅𝐔𝐃 𝐕𝟐:**
[𝐂𝐋𝐈𝐂𝐊 𝐇𝐄𝐑𝐄 𝐓𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃](https://example.com/apk-fud.apk)

━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 @RahulModDeveloper
"""
        bot.send_message(user_id, welcome_back, parse_mode='Markdown')
        return
    
    welcome_text = """
╔══════════════════════════════╗
║      🔥 𝐀𝐏𝐊 𝐅𝐔𝐃 𝐍𝐄𝐖 𝐔𝐏𝐃𝐀𝐓𝐄 𝐕𝟐 🔥      ║
╚══════════════════════════════╝

◈────────────────────◈
│  📱 𝐀𝐏𝐊 𝐅𝐄𝐀𝐓𝐔𝐑𝐄𝐒   │
◈────────────────────◈

✅ **𝐎𝐍𝐄 𝐂𝐋𝐈𝐂𝐊 𝐈𝐍𝐒𝐓𝐀𝐋𝐋**
❌ **𝐍𝐎 𝐃𝐎𝐔𝐁𝐋𝐄 𝐈𝐍𝐒𝐓𝐀𝐋𝐋**

◈────────────────────◈
│    💰 𝐏𝐑𝐈𝐂𝐄 💰       │
◈────────────────────◈

🔥 **𝐏𝐫𝐢𝐜𝐞: ₹𝟱𝟬𝟬 𝗢𝗻𝗹𝘆**
📆 **𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗨𝗗**
⏰ **𝗩𝗮𝗹𝗶𝗱𝗶𝘁𝘆: 𝟭 𝗠𝗼𝗻𝘁𝗵**

◈────────────────────◈
│   👨‍💻 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑    │
◈────────────────────◈

👑 **𝗥𝗮𝗵𝘂𝗹 𝗠𝗼𝗱 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿**

━━━━━━━━━━━━━━━━━━━━━━━━
💡 **𝐂𝐥𝐢𝐜𝐤 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐓𝐎 𝐁𝐔𝐘 𝐭𝐨 𝐩𝐫𝐨𝐜𝐞𝐞𝐝**
━━━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(user_id, welcome_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

# ============= STATUS COMMAND =============
@bot.message_handler(commands=['status'])
def status_command(message):
    user_id = message.from_user.id
    if user_id in verified_users:
        status_msg = "✅ **𝐀𝐂𝐂𝐄𝐒𝐒 𝐀𝐂𝐓𝐈𝐕𝐄**\n\n[📥 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐀𝐏𝐊](https://example.com/apk-fud.apk)"
    else:
        status_msg = "❌ **𝐍𝐎 𝐀𝐂𝐓𝐈𝐕𝐄 𝐒𝐔𝐁𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍**\n\n💡 𝐓𝐲𝐩𝐞 /start 𝐚𝐧𝐝 𝐜𝐥𝐢𝐜𝐤 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐓𝐎 𝐁𝐔𝐘\n\n💰 **𝐏𝐫𝐢𝐜𝐞: ₹𝟱𝟬𝟬**"
    bot.send_message(user_id, status_msg, parse_mode='Markdown')

# ============= ADMIN COMMAND - Show all user stats =============
@bot.message_handler(commands=['admin'])
def admin_command(message):
    # Check if user is admin
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ **𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐀𝐜𝐜𝐞𝐬𝐬!**\n\nThis command is only for bot admin.", parse_mode='Markdown')
        return
    
    total_users = len(verified_users)
    
    # Calculate today's users (users added today)
    today = datetime.now().strftime("%Y-%m-%d")
    today_users = 0
    recent_users_list = []
    
    for uid, data in verified_users.items():
        if data.get("date") == today:
            today_users += 1
        recent_users_list.append(f"• `{uid}` | @{data.get('username', 'unknown')}")
    
    # Show last 10 users
    last_10 = "\n".join(recent_users_list[-10:]) if recent_users_list else "No users yet"
    
    admin_stats = f"""
╔════════════════════════════════╗
║      👑 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋 👑      ║
╚════════════════════════════════╝

📊 **𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒**
━━━━━━━━━━━━━━━━━━━━━━━━
✅ **𝐓𝐨𝐭𝐚𝐥 𝐕𝐞𝐫𝐢𝐟𝐢𝐞𝐝 𝐔𝐬𝐞𝐫𝐬:** `{total_users}`
📅 **𝐓𝐨𝐝𝐚𝐲'𝐬 𝐔𝐬𝐞𝐫𝐬:** `{today_users}`
💰 **𝐏𝐫𝐢𝐜𝐞:** `₹500`
━━━━━━━━━━━━━━━━━━━━━━━━

👥 **𝐑𝐄𝐂𝐄𝐍𝐓 𝐔𝐒𝐄𝐑𝐒 (𝐋𝐚𝐬𝐭 𝟏𝟎)**
{last_10}

━━━━━━━━━━━━━━━━━━━━━━━━
📌 **𝐀𝐃𝐌𝐈𝐍 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒**
/give @username or id - Give access
/remove @username or id - Remove access
/users - List all users with details
/broadcast - Send message to all
/status - Bot status
━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 @RahulModDeveloper
"""
    
    bot.send_message(ADMIN_ID, admin_stats, parse_mode='Markdown')

# ============= ADMIN PANEL (Old - keeping for compatibility) =============
@bot.message_handler(commands=['panel'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: 
        return
    stats_msg = f"""
👑 **𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋**
━━━━━━━━━━━━━━━━━━
✅ **𝐕𝐞𝐫𝐢𝐟𝐢𝐞𝐝 𝐔𝐬𝐞𝐫𝐬:** {len(verified_users)}

📌 **𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:**
/give @username or user_id - Give access
/remove @username or user_id - Remove access
/users - List all verified users
/broadcast - Send message to all
"""
    bot.send_message(ADMIN_ID, stats_msg, parse_mode='Markdown')

@bot.message_handler(commands=['give'])
def give_access(message):
    if message.from_user.id != ADMIN_ID: 
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /give @username or /give 123456789")
        return
    
    target = parts[1].replace("@", "")
    
    # Check if it's numeric (user_id) or string (username)
    if target.isdigit():
        user_id = int(target)
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Try to get username
        username = "unknown"
        try:
            user_info = bot.get_chat(user_id)
            username = user_info.username or "no_username"
        except:
            pass
        
        verified_users[user_id] = {
            "date": current_date,
            "username": username,
            "user_id": user_id
        }
        bot.reply_to(message, f"✅ Access granted to User ID: `{user_id}`\n📅 Date: {current_date}", parse_mode='Markdown')
        
        # Notify the user
        try:
            bot.send_message(user_id, "✅ **𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐫𝐚𝐧𝐭𝐞𝐝!**\n\n📱 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀𝐏𝐊:\n[𝐂𝐋𝐈𝐂𝐊 𝐇𝐄𝐑𝐄](https://example.com/apk-fud.apk)", parse_mode='Markdown')
        except:
            pass
    else:
        bot.reply_to(message, f"⚠️ To give access by username, first get the user's ID.\n\nOr use: /give user_id\n\nContact @{target} manually.")
    
    # Update admin stats
    admin_command(message)

@bot.message_handler(commands=['remove'])
def remove_access(message):
    if message.from_user.id != ADMIN_ID: 
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /remove @username or /remove user_id")
        return
    
    target = parts[1].replace("@", "")
    
    if target.isdigit():
        user_id = int(target)
        if user_id in verified_users:
            del verified_users[user_id]
            bot.reply_to(message, f"❌ Access removed for User ID: `{user_id}`", parse_mode='Markdown')
        else:
            bot.reply_to(message, f"⚠️ User ID `{user_id}` not found in verified list", parse_mode='Markdown')
    else:
        bot.reply_to(message, "⚠️ Please provide numeric User ID. Use /users to see all verified IDs.")

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id != ADMIN_ID: 
        return
    
    if not verified_users:
        bot.reply_to(message, "📭 No verified users yet.")
        return
    
    user_list = []
    for uid, data in verified_users.items():
        username = data.get('username', 'unknown')
        date = data.get('date', 'unknown')
        user_list.append(f"• `{uid}` | @{username} | 📅 {date}")
    
    users_text = "\n".join(user_list)
    
    # Split if message too long
    if len(users_text) > 4000:
        parts_list = [users_text[i:i+4000] for i in range(0, len(users_text), 4000)]
        for idx, part in enumerate(parts_list):
            bot.reply_to(message, f"📋 **𝐕𝐞𝐫𝐢𝐟𝐢𝐞𝐝 𝐔𝐬𝐞𝐫𝐬 ({len(verified_users)}) - Part {idx+1}:**\n\n{part}", parse_mode='Markdown')
    else:
        bot.reply_to(message, f"📋 **𝐕𝐞𝐫𝐢𝐟𝐢𝐞𝐝 𝐔𝐬𝐞𝐫𝐬 ({len(verified_users)}):**\n\n{users_text}", parse_mode='Markdown')

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != ADMIN_ID: 
        return
    
    msg_text = message.text.replace("/broadcast", "").strip()
    if not msg_text:
        bot.reply_to(message, "⚠️ Usage: /broadcast Your message here")
        return
    
    sent = 0
    failed = 0
    
    for user_id in verified_users:
        try:
            bot.send_message(user_id, f"📢 **𝐀𝐍𝐍𝐎𝐔𝐍𝐂𝐄𝐌𝐄𝐍𝐓**\n\n{msg_text}", parse_mode='Markdown')
            sent += 1
        except:
            failed += 1
        time.sleep(0.1)
    
    bot.reply_to(message, f"✅ Broadcast completed!\n\n📨 Sent: {sent}\n❌ Failed: {failed}")

# ============= HELP COMMAND =============
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📖 **𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔**

/start - Start the bot
/status - Check your access status
/help - Show this help menu

━━━━━━━━━━━━━━━━━━
💰 **𝐏𝐫𝐢𝐜𝐞: ₹𝟱𝟬𝟬**

💡 **𝐇𝐨𝐰 𝐭𝐨 𝐁𝐮𝐲:**
1. Click "CONTACT TO BUY" button
2. Message @RahulMod77
3. Complete payment & get access

━━━━━━━━━━━━━━━━━━
👨‍💻 **Developer:** @RahulModDeveloper
"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# ============= FLASK APP (for Render/Railway) =============
@app.route('/')
def home():
    return {
        "status": "APK FUD Bot is Running",
        "version": "V3",
        "verified_users": len(verified_users),
        "admin_id": ADMIN_ID
    }, 200

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

def run_bot_polling():
    while True:
        try:
            print("🤖 Bot Started with Polling...")
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("🔥 APK FUD BOT V3 - CONTACT ONLY 🔥")
    print("=" * 50)
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print(f"📞 Support: @{SUPPORT_USERNAME}")
    print("💰 Price: ₹500")
    print("=" * 50)
    
    # Start bot polling in background thread
    polling_thread = threading.Thread(target=run_bot_polling)
    polling_thread.daemon = True
    polling_thread.start()
    
    print("🚀 Starting Flask Server...")
    app.run(host="0.0.0.0", port=port)
