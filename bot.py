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
BOT_TOKEN = "8635537345:AAHy2OCc2Fh40eMcPSy3VV5aZXf6x2vL_JQ"
ADMIN_ID = 8366608745
SUPPORT_USERNAME = "RahulMod77"

# Store users who started the bot
started_users = set()  # Sirf user IDs store honge

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ============= MAIN KEYBOARD =============
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    contact_btn = InlineKeyboardButton("📞 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐓𝐎 𝐁𝐔𝐘", url=f"https://t.me/{SUPPORT_USERNAME}")
    keyboard.add(contact_btn)
    return keyboard

# ============= START COMMAND =============
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    # Add user to started_users set
    started_users.add(user_id)
    
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

# ============= ADMIN COMMAND - Sirf users count dikhega =============
@bot.message_handler(commands=['admin'])
def admin_command(message):
    # Check if user is admin
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ **𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐀𝐜𝐜𝐞𝐬𝐬!**", parse_mode='Markdown')
        return
    
    total_users = len(started_users)
    
    admin_msg = f"""
╔══════════════════════════════╗
║      👑 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋 👑      ║
╚══════════════════════════════╝

📊 **𝐓𝐎𝐓𝐀𝐋 𝐔𝐒𝐄𝐑𝐒:** `{total_users}`

👥 **𝐔𝐬𝐞𝐫𝐬 𝐰𝐡𝐨 𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐭𝐡𝐞 𝐛𝐨𝐭**

━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 @RahulModDeveloper
"""
    
    bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')

# ============= HELP COMMAND =============
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📖 **𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔**

/start - Start the bot
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

# ============= FLASK APP =============
@app.route('/')
def home():
    return {
        "status": "APK FUD Bot is Running",
        "version": "V3",
        "total_users": len(started_users)
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
    print("🔥 APK FUD BOT V3 - SIMPLE CONTACT 🔥")
    print("=" * 50)
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print(f"📞 Support: @{SUPPORT_USERNAME}")
    print("💰 Price: ₹500")
    print("=" * 50)
    
    # Start bot polling
    polling_thread = threading.Thread(target=run_bot_polling)
    polling_thread.daemon = True
    polling_thread.start()
    
    print("🚀 Starting Flask Server...")
    app.run(host="0.0.0.0", port=port)
