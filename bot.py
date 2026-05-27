#!/usr/bin/env python3
# APK FUD BOT - With ZapUPI Gateway Integration
# Developer: Rahul Mod Developer

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
import os
import time
import threading
from flask import Flask, request, jsonify
from datetime import datetime

# 🔑 BOT CONFIG
BOT_TOKEN = "8766471260:AAEzCxeEJTL9l-2JoO09zHpgR-409-j9QTM"
ADMIN_ID = 8366608745

# 🔑 ZAPUPI GATEWAY CONFIG
ZAP_KEY = "zape52407ad41fde98699d4c8c9b85d9d7f"  
ZAP_API_URL = "https://pay.zapupi.com/api/create-order"  
WEBHOOK_URL = "https://fub-bot.onrender.com/webhook"  

# 💾 Store user orders
user_orders = {}
verified_users = set()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ============= CREATE ORDER IN ZAPUPI =============
def create_zapupi_order(user_id, user_name, amount=500):
    """Create order in ZapUPI gateway"""
    order_id = f"APK_{user_id}_{int(time.time())}"
    
    # ✅ FIX: Remark में कोई स्पेस या स्पेशल कैरेक्टर नहीं होना चाहिए
    safe_remark = f"APK{user_id}" 

    # ✅ Fixed Payload according to ZapUPI Docs
    payload = {
        "zap_key": ZAP_KEY,
        "order_id": order_id,
        "amount": str(amount),
        "customer_mobile": str(user_id)[:10],  
        "remark": safe_remark,  
        "webhook_url": WEBHOOK_URL,
        "success_url": "https://t.me/Rahul_Mod77_bot" # ✅ आपका बॉट यूज़रनेम लगा दिया है
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"[DEBUG] Creating order for user {user_id}")
        response = requests.post(ZAP_API_URL, json=payload, headers=headers, timeout=30)
        print(f"[DEBUG] Response Status: {response.status_code}")
        print(f"[DEBUG] Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                return {"success": False, "error": f"Invalid API Response: {response.text[:50]}"}
                
            if data.get("status") == "success" or data.get("status") == True:
                payment_link = data.get("payment_url") or data.get("payment_link") or data.get("url")
                return {
                    "success": True,
                    "order_id": order_id,
                    "payment_link": payment_link,
                    "amount": amount
                }
            else:
                return {"success": False, "error": data.get("message", "Unknown API error")}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text[:50]}"}
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"success": False, "error": str(e)}

# ============= VERIFY PAYMENT STATUS =============
def check_payment_status(order_id):
    """Check payment status from ZapUPI"""
    url = "https://pay.zapupi.com/api/check-status"
    payload = {
        "zap_key": ZAP_KEY,
        "order_id": order_id
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get("status") == "Success" or data.get("status") == "success"
        return False
    except:
        return False

# ============= GET MAIN KEYBOARD =============
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buy_btn = InlineKeyboardButton("🛒 𝐁𝐔𝐘 𝐍𝐎𝐖 - ₹𝟱𝟬𝟬", callback_data="buy_now")
    keyboard.add(buy_btn)
    return keyboard

def get_payment_keyboard(order_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    check_btn = InlineKeyboardButton("✅ 𝐂𝐇𝐄𝐂𝐊 𝐏𝐀𝐘𝐌𝐄𝐍𝐓", callback_data=f"check_{order_id}")
    cancel_btn = InlineKeyboardButton("❌ 𝐂𝐀𝐍𝐂𝐄𝐋", callback_data="cancel")
    keyboard.add(check_btn, cancel_btn)
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

🔥 **₹𝟱𝟬𝟬 𝗥𝘀. 𝗢𝗻𝗹𝘆**
📆 **𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗨𝗗**
⏰ **𝗩𝗮𝗹𝗶𝗱𝗶𝘁𝘆: 𝟭 𝗠𝗼𝗻𝘁𝗵**

◈────────────────────◈
│   👨‍💻 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑    │
◈────────────────────◈

👑 **𝗥𝗮𝗵𝘂𝗹 𝗠𝗼𝗱 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿**

━━━━━━━━━━━━━━━━━━━━━━━━
💡 **𝐂𝐥𝐢𝐜𝐤 𝐁𝐔𝐘 𝐍𝐎𝐖 𝐭𝐨 𝐩𝐫𝐨𝐜𝐞𝐞𝐝**
━━━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(user_id, welcome_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

# ============= BUY NOW BUTTON =============
@bot.callback_query_handler(func=lambda call: call.data == "buy_now")
def buy_now_callback(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name or "User"
    
    if user_id in verified_users:
        bot.answer_callback_query(call.id, "✅ You already have access!", show_alert=True)
        return
    
    processing_msg = bot.send_message(
        user_id,
        "🔄 **𝐂𝐫𝐞𝐚𝐭𝐢𝐧𝐠 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐥𝐢𝐧𝐤...**\n\n⏳ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝟓-𝟏𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬",
        parse_mode='Markdown'
    )
    
    order = create_zapupi_order(user_id, user_name, 500)
    
    if order["success"]:
        user_orders[user_id] = {
            "order_id": order["order_id"],
            "payment_link": order["payment_link"],
            "amount": order["amount"],
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        bot.delete_message(user_id, processing_msg.message_id)
        
        payment_text = f"""
╔══════════════════════════════╗
║      💳 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐋𝐈𝐍𝐊 💳      ║
╚══════════════════════════════╝

◈────────────────────◈
│   📝 𝐎𝐑𝐃𝐄𝐑 𝐃𝐄𝐓𝐀𝐈𝐋𝐒   │
◈────────────────────◈

🆔 **𝐎𝐫𝐝𝐞𝐫 𝐈𝐃:** `{order['order_id']}`
💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{order['amount']}
⏰ **𝐓𝐢𝐦𝐞:** {datetime.now().strftime("%I:%M %p")}

━━━━━━━━━━━━━━━━━━━━━━━━
🔗 **𝐂𝐥𝐢𝐜𝐤 𝐭𝐡𝐞 𝐥𝐢𝐧𝐤 𝐭𝐨 𝐩𝐚𝐲:**

{order['payment_link']}

━━━━━━━━━━━━━━━━━━━━━━━━
📌 **𝐈𝐍𝐒𝐓𝐑𝐔𝐂𝐓𝐈𝐎𝐍𝐒:**
1️⃣ 𝐂𝐥𝐢𝐜𝐤 𝐭𝐡𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐥𝐢𝐧𝐤
2️⃣ 𝐂𝐡𝐨𝐨𝐬𝐞 𝐲𝐨𝐮𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐦𝐞𝐭𝐡𝐨𝐝
3️⃣ 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞 𝐭𝐡𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭
4️⃣ **𝐂𝐥𝐢𝐜𝐤 𝐂𝐇𝐄𝐂𝐊 𝐏𝐀𝐘𝐌𝐄𝐍𝐓** 𝐛𝐞𝐥𝐨𝐰

━━━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.send_message(user_id, payment_text, parse_mode='Markdown', reply_markup=get_payment_keyboard(order['order_id']))
        
        admin_msg = f"🆕 **𝐍𝐄𝐖 𝐎𝐑𝐃𝐄𝐑 𝐂𝐑𝐄𝐀𝐓𝐄𝐃**\n\n👤 **𝐔𝐬𝐞𝐫:** {user_name}\n🆔 **𝐔𝐬𝐞𝐫 𝐈𝐃:** `{user_id}`\n🆔 **𝐎𝐫𝐝𝐞𝐫 𝐈𝐃:** `{order['order_id']}`\n💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{order['amount']}"
        bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
        
    else:
        bot.edit_message_text(
            f"❌ **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐜𝐫𝐞𝐚𝐭𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐥𝐢𝐧𝐤!**\n\n💡 **𝐄𝐫𝐫𝐨𝐫:** `{order['error']}`\n\n📞 **𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐀𝐝𝐦𝐢𝐧:** @RahulModDeveloper",
            user_id,
            processing_msg.message_id,
            parse_mode='Markdown'
        )

# ============= CHECK PAYMENT STATUS =============
@bot.callback_query_handler(func=lambda call: call.data.startswith("check_"))
def check_payment_callback(call):
    user_id = call.from_user.id
    order_id = call.data.replace("check_", "")
    
    if user_id not in user_orders:
        bot.answer_callback_query(call.id, "❌ Order not found!", show_alert=True)
        return
    
    order = user_orders[user_id]
    bot.answer_callback_query(call.id, "🔄 Checking payment status...")
    
    checking_msg = bot.send_message(user_id, "🔄 **𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐬𝐭𝐚𝐭𝐮𝐬...**\n\n⏳ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭", parse_mode='Markdown')
    
    is_paid = check_payment_status(order_id)
    
    if is_paid:
        verified_users.add(user_id)
        order["status"] = "completed"
        bot.delete_message(user_id, checking_msg.message_id)
        
        success_msg = """
╔══════════════════════════════╗
║    ✅ 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐕𝐄𝐑𝐈𝐅𝐈𝐄𝐃 ✅    ║
╚══════════════════════════════╝

✅ **𝐘𝐨𝐮𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐢𝐬 𝐯𝐞𝐫𝐢𝐟𝐢𝐞𝐝!**

━━━━━━━━━━━━━━━━━━━━━━━━
📱 **𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐘𝐨𝐮𝐫 𝐀𝐏𝐊 𝐅𝐔𝐃 𝐕𝟐:**

[🔽 **𝐂𝐋𝐈𝐂𝐊 𝐇𝐄𝐑𝐄 𝐓𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃**](https://example.com/apk-fud.apk)

━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐀𝐝𝐦𝐢𝐧:** @RahulModDeveloper
"""
        keyboard = InlineKeyboardMarkup()
        download_btn = InlineKeyboardButton("📥 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐀𝐏𝐊", url="https://example.com/apk-fud.apk")
        keyboard.add(download_btn)
        
        bot.send_message(user_id, success_msg, parse_mode='Markdown', reply_markup=keyboard)
        
        admin_msg = f"✅ **𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄𝐃**\n\n👤 **𝐔𝐬𝐞𝐫:** {call.from_user.first_name}\n🆔 **𝐔𝐬𝐞𝐫 𝐈𝐃:** `{user_id}`\n🆔 **𝐎𝐫𝐝𝐞𝐫:** `{order_id}`\n💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{order['amount']}"
        bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
        
    else:
        bot.edit_message_text(
            f"❌ **𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐍𝐨𝐭 𝐅𝐨𝐮𝐧𝐝 𝐨𝐫 𝐏𝐞𝐧𝐝𝐢𝐧𝐠!**\n\n💡 **𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐨𝐦𝐩𝐥𝐞𝐭𝐞 𝐭𝐡𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐟𝐢𝐫𝐬𝐭**\n\n✅ 𝐀𝐟𝐭𝐞𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭, 𝐜𝐥𝐢𝐜𝐤 𝐂𝐇𝐄𝐂𝐊 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐚𝐠𝐚𝐢𝐧\n\n🆔 **𝐎𝐫𝐝𝐞𝐫 𝐈𝐃:** `{order_id}`",
            user_id,
            checking_msg.message_id,
            parse_mode='Markdown',
            reply_markup=get_payment_keyboard(order_id)
        )

# ============= CANCEL ORDER =============
@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel_callback(call):
    user_id = call.from_user.id
    if user_id in user_orders:
        del user_orders[user_id]
    bot.answer_callback_query(call.id, "❌ Order cancelled!")
    bot.send_message(user_id, "❌ **𝐎𝐫𝐝𝐞𝐫 𝐜𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝!**\n\n💡 𝐓𝐲𝐩𝐞 /start 𝐭𝐨 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧", parse_mode='Markdown')

# ============= WEBHOOK FOR ZAPUPI (AUTO VERIFICATION) =============
@app.route('/webhook', methods=['POST'])
def zapupi_webhook():
    try:
        data = request.json
        print(f"[WEBHOOK] Received: {json.dumps(data, indent=2)}")
        
        order_id = data.get("order_id")
        status = data.get("status")
        utr = data.get("utr")
        amount = data.get("amount")
        
        if status == "Success" and order_id:
            try:
                parts = order_id.split("_")
                user_id = int(parts[1])
            except:
                user_id = None
            
            if user_id:
                verified_users.add(user_id)
                if user_id in user_orders:
                    user_orders[user_id]["status"] = "completed"
                    user_orders[user_id]["utr"] = utr
                
                success_msg = f"✅ **𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃!**\n\n💳 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{amount}\n🆔 **𝐔𝐓𝐑:** `{utr}`\n\n📱 **𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀𝐏𝐊 𝐅𝐔𝐃 𝐕𝟐:**\n[𝐂𝐋𝐈𝐂𝐊 𝐇𝐄𝐑𝐄 𝐓𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃](https://example.com/apk-fud.apk)\n\n👨‍💻 @RahulModDeveloper"
                try:
                    bot.send_message(user_id, success_msg, parse_mode='Markdown')
                except:
                    pass
                
                admin_msg = f"💳 **𝐀𝐔𝐓𝐎 𝐕𝐄𝐑𝐈𝐅𝐈𝐄𝐃 𝐏𝐀𝐘𝐌𝐄𝐍𝐓**\n\n👤 **𝐔𝐬𝐞𝐫 𝐈𝐃:** `{user_id}`\n🆔 **𝐎𝐫𝐝𝐞𝐫:** `{order_id}`\n💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{amount}\n🔢 **𝐔𝐓𝐑:** `{utr}`\n\n✅ **𝐀𝐜𝐜𝐞𝐬𝐬 𝐠𝐫𝐚𝐧𝐭𝐞𝐝 𝐚𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜𝐚𝐥𝐥𝐲**"
                bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"[WEBHOOK ERROR] {e}")
        return jsonify({"status": "error"}), 200

# ============= STATUS COMMAND =============
@bot.message_handler(commands=['status'])
def status_command(message):
    user_id = message.from_user.id
    if user_id in verified_users:
        status_msg = "✅ **𝐀𝐂𝐂𝐄𝐒𝐒 𝐀𝐂𝐓𝐈𝐕𝐄**\n\n[📥 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐀𝐏𝐊](https://example.com/apk-fud.apk)"
    elif user_id in user_orders:
        order = user_orders[user_id]
        status_msg = f"⏳ **𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐏𝐄𝐍𝐃𝐈𝐍𝐆**\n\n🔗 **𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐥𝐢𝐧𝐤:**\n{order['payment_link']}"
    else:
        status_msg = "❌ **𝐍𝐎 𝐀𝐂𝐓𝐈𝐕𝐄 𝐒𝐔𝐁𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍**\n\n💡 𝐓𝐲𝐩𝐞 /start 𝐭𝐨 𝐩𝐮𝐫𝐜𝐡𝐚𝐬𝐞"
    bot.send_message(user_id, status_msg, parse_mode='Markdown')

# ============= ADMIN COMMANDS =============
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    stats_msg = f"👑 **𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋**\n\n✅ **𝐕𝐞𝐫𝐢𝐟𝐢𝐞𝐝 𝐔𝐬𝐞𝐫𝐬:** {len(verified_users)}\n⏳ **𝐏𝐞𝐧𝐝𝐢𝐧𝐠 𝐎𝐫𝐝𝐞𝐫𝐬:** {len(user_orders)}\n\n📌 /give @username\n📌 /remove @username"
    bot.send_message(ADMIN_ID, stats_msg, parse_mode='Markdown')

@bot.message_handler(commands=['give'])
def give_access(message):
    if message.from_user.id != ADMIN_ID: return
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /give @username")
        return
    username = parts[1].replace("@", "")
    verified_users.add(username)
    bot.reply_to(message, f"✅ Access granted to @{username}")

# ============= FLASK APP =============
@app.route('/')
def home():
    return {"status": "APK FUD Bot is Running", "version": "V2"}, 200

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
    print("🔥 APK FUD BOT V2 - WITH ZAPUPI 🔥")
    
    polling_thread = threading.Thread(target=run_bot_polling)
    polling_thread.daemon = True
    polling_thread.start()
    
    print("🚀 Starting Flask Server...")
    app.run(host="0.0.0.0", port=port)
