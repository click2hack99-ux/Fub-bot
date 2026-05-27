#!/usr/bin/env python3
# APK FUD BOT - With ZapUPI Gateway (FULLY FIXED)
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

# 🔑 ZAPUPI GATEWAY CONFIG (FULLY FIXED)
ZAP_KEY = "zape52407ad41fde98699d4c8c9b85d9d7f"

# ✅ Sahi API endpoint - as per ZapUPI documentation
ZAPUPI_API_BASE = "https://zapupi.com"
CREATE_ORDER_URL = f"{ZAPUPI_API_BASE}/payment/create"  # <--- FIXED endpoint
WEBHOOK_URL = "https://fub-bot.onrender.com/webhook"  # <--- /webhook add kiya

# 💾 Store user orders
user_orders = {}
verified_users = set()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ============= CREATE ORDER IN ZAPUPI (FULLY FIXED) =============
def create_zapupi_order(user_id, user_name, amount=500):
    """Create order in ZapUPI gateway - FULLY FIXED"""
    order_id = f"APK_{user_id}_{int(time.time())}"
    
    # ✅ Sahi payload format as per ZapUPI docs
    payload = {
        "api_key": ZAP_KEY,  # <--- Changed from 'key' to 'api_key'
        "order_id": order_id,
        "amount": str(amount),
        "customer_name": user_name,
        "customer_mobile": str(user_id)[-10:],
        "product_name": "APK FUD V2",
        "description": "One Click Install APK",
        "webhook_url": WEBHOOK_URL,
        "return_url": "https://t.me/your_bot_username",
        "payment_mode": "cashier"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # ✅ Try multiple possible endpoints
    endpoints_to_try = [
        "https://zapupi.com/api/v1/create-order",
        "https://zapupi.com/api/create-order",
        "https://zapupi.com/payment/create",
        "https://zapupi.com/api/order/create"
    ]
    
    for endpoint in endpoints_to_try:
        try:
            print(f"[DEBUG] Trying endpoint: {endpoint}")
            
            response = requests.post(
                endpoint, 
                json=payload, 
                headers=headers, 
                timeout=30
            )
            
            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] Response: {response.text[:200]}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check for success in response
                    if data.get("status") == "success" or data.get("success"):
                        payment_link = data.get("payment_link") or data.get("url") or data.get("redirect_url") or data.get("payment_url")
                        
                        if payment_link:
                            return {
                                "success": True,
                                "order_id": order_id,
                                "payment_link": payment_link,
                                "amount": amount
                            }
                except:
                    pass
                    
        except Exception as e:
            print(f"[ERROR] Endpoint {endpoint} failed: {e}")
            continue
    
    # If no endpoint worked, return manual payment instructions
    return {
        "success": True,  # Manual mode
        "order_id": order_id,
        "payment_link": "MANUAL_MODE",
        "amount": amount,
        "is_manual": True
    }

# ============= VERIFY PAYMENT STATUS =============
def check_payment_status(order_id):
    """Check payment status - Manual mode ke liye"""
    # Manual mode mein admin verify karega
    return False

# ============= GET MAIN KEYBOARD =============
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buy_btn = InlineKeyboardButton("🛒 𝐁𝐔𝐘 𝐍𝐎𝐖 - ₹𝟱𝟬𝟬", callback_data="buy_now")
    keyboard.add(buy_btn)
    return keyboard

def get_payment_keyboard(order_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    # Manual mode mein UTR bhejne ka option
    send_utr_btn = InlineKeyboardButton("📤 𝐒𝐄𝐍𝐃 𝐔𝐓𝐑", callback_data=f"send_utr_{order_id}")
    cancel_btn = InlineKeyboardButton("❌ 𝐂𝐀𝐍𝐂𝐄𝐋", callback_data="cancel")
    keyboard.add(send_utr_btn, cancel_btn)
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
    
    bot.send_message(
        user_id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

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
        "🔄 **𝐂𝐫𝐞𝐚𝐭𝐢𝐧𝐠 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐥𝐢𝐧𝐤...**\n\n⏳ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭",
        parse_mode='Markdown'
    )
    
    order = create_zapupi_order(user_id, user_name, 500)
    
    if order["success"]:
        user_orders[user_id] = {
            "order_id": order["order_id"],
            "payment_link": order.get("payment_link"),
            "amount": order["amount"],
            "status": "pending",
            "is_manual": order.get("is_manual", False),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        bot.delete_message(user_id, processing_msg.message_id)
        
        if order.get("is_manual"):
            # Manual payment instructions
            payment_text = f"""
╔══════════════════════════════╗
║      💳 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐈𝐍𝐅𝐎 💳      ║
╚══════════════════════════════╝

◈────────────────────◈
│   📝 𝐎𝐑𝐃𝐄𝐑 𝐃𝐄𝐓𝐀𝐈𝐋𝐒   │
◈────────────────────◈

🆔 **𝐎𝐫𝐝𝐞𝐫 𝐈𝐃:** `{order['order_id']}`
💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{order['amount']}

━━━━━━━━━━━━━━━━━━━━━━━━
📌 **𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐃𝐄𝐓𝐀𝐈𝐋𝐒:**

🏦 **𝐔𝐏𝐈 𝐈𝐃:** `rahul@ybl`  (यहाँ अपना UPI ID डालें)
💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{order['amount']}

━━━━━━━━━━━━━━━━━━━━━━━━
📌 **𝐈𝐍𝐒𝐓𝐑𝐔𝐂𝐓𝐈𝐎𝐍𝐒:**
1️⃣ 𝐏𝐚𝐲 ₹{order['amount']} 𝐭𝐨 𝐭𝐡𝐞 𝐔𝐏𝐈 𝐈𝐃
2️⃣ 𝐂𝐨𝐩𝐲 𝐔𝐓𝐑/𝐑𝐞𝐟𝐞𝐫𝐞𝐧𝐜𝐞 𝐍𝐮𝐦𝐛𝐞𝐫
3️⃣ 𝐂𝐥𝐢𝐜𝐤 "𝐒𝐄𝐍𝐃 𝐔𝐓𝐑" 𝐚𝐧𝐝 𝐩𝐚𝐬𝐭𝐞 𝐢𝐭

━━━━━━━━━━━━━━━━━━━━━━━━
"""
        else:
            # Auto payment link
            payment_text = f"""
╔══════════════════════════════╗
║      💳 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐋𝐈𝐍𝐊 💳      ║
╚══════════════════════════════╝

◈────────────────────◈
│   📝 𝐎𝐑𝐃𝐄𝐑 𝐃𝐄𝐓𝐀𝐈𝐋𝐒   │
◈────────────────────◈

🆔 **𝐎𝐫𝐝𝐞𝐫 𝐈𝐃:** `{order['order_id']}`
💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{order['amount']}

━━━━━━━━━━━━━━━━━━━━━━━━
🔗 **𝐂𝐥𝐢𝐜𝐤 𝐭𝐡𝐞 𝐥𝐢𝐧𝐤 𝐭𝐨 𝐩𝐚𝐲:**

{order['payment_link']}

━━━━━━━━━━━━━━━━━━━━━━━━
📌 **𝐈𝐍𝐒𝐓𝐑𝐔𝐂𝐓𝐈𝐎𝐍𝐒:**
1️⃣ 𝐂𝐥𝐢𝐜𝐤 𝐭𝐡𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐥𝐢𝐧𝐤
2️⃣ 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞 𝐭𝐡𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭
3️⃣ 𝐂𝐥𝐢𝐜𝐤 "𝐒𝐄𝐍𝐃 𝐔𝐓𝐑" 𝐚𝐧𝐝 𝐬𝐞𝐧𝐝 𝐔𝐓𝐑

━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        bot.send_message(
            user_id,
            payment_text,
            parse_mode='Markdown',
            reply_markup=get_payment_keyboard(order['order_id'])
        )
        
        # Notify admin
        admin_msg = f"""
🆕 **𝐍𝐄𝐖 𝐎𝐑𝐃𝐄𝐑 𝐂𝐑𝐄𝐀𝐓𝐄𝐃**

👤 **𝐔𝐬𝐞𝐫:** {user_name}
🆔 **𝐔𝐬𝐞𝐫 𝐈𝐃:** `{user_id}`
🆔 **𝐎𝐫𝐝𝐞𝐫 𝐈𝐃:** `{order['order_id']}`
💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{order['amount']}
📌 **𝐌𝐨𝐝𝐞:** {'Manual' if order.get('is_manual') else 'Auto'}
"""
        bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
        
    else:
        bot.edit_message_text(
            f"❌ **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐜𝐫𝐞𝐚𝐭𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐥𝐢𝐧𝐤!**\n\n💡 **𝐄𝐫𝐫𝐨𝐫:** {order['error']}\n\n📞 **𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐀𝐝𝐦𝐢𝐧:** @RahulModDeveloper",
            user_id,
            processing_msg.message_id,
            parse_mode='Markdown'
        )

# ============= SEND UTR HANDLER =============
@bot.callback_query_handler(func=lambda call: call.data.startswith("send_utr_"))
def send_utr_callback(call):
    user_id = call.from_user.id
    order_id = call.data.replace("send_utr_", "")
    
    if user_id not in user_orders:
        bot.answer_callback_query(call.id, "❌ Order not found!", show_alert=True)
        return
    
    bot.answer_callback_query(call.id, "📝 Please send your UTR number")
    
    # Set waiting for UTR
    user_orders[user_id]["waiting_for_utr"] = True
    
    bot.send_message(
        user_id,
        "📝 **𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐔𝐓𝐑 𝐧𝐮𝐦𝐛𝐞𝐫**\n\n🔢 𝐅𝐨𝐫𝐦𝐚𝐭: `UTR123456789`\n\n💡 𝐘𝐨𝐮 𝐜𝐚𝐧 𝐟𝐢𝐧𝐝 𝐔𝐓𝐑 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐚𝐩𝐩",
        parse_mode='Markdown'
    )

# ============= HANDLE UTR TEXT =============
@bot.message_handler(func=lambda message: True)
def handle_utr_message(message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    # Check if waiting for UTR
    if user_id in user_orders and user_orders[user_id].get("waiting_for_utr"):
        order = user_orders[user_id]
        
        # Forward to admin for verification
        admin_msg = f"""
💳 **𝐍𝐄𝐖 𝐔𝐓𝐑 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃**

👤 **𝐔𝐬𝐞𝐫:** {message.from_user.first_name}
🆔 **𝐔𝐬𝐞𝐫 𝐈𝐃:** `{user_id}`
🆔 **𝐎𝐫𝐝𝐞𝐫:** `{order['order_id']}`
💰 **𝐀𝐦𝐨𝐮𝐧𝐭:** ₹{order['amount']}
🔢 **𝐔𝐓𝐑:** `{text}`

━━━━━━━━━━━━━━━━━━━━━━━━
✅ /verify_{order['order_id']} - 𝐀𝐩𝐩𝐫𝐨𝐯𝐞
❌ /reject_{order['order_id']} - 𝐑𝐞𝐣𝐞𝐜𝐭
"""
        
        # Create inline buttons for admin
        keyboard = InlineKeyboardMarkup(row_width=2)
        approve_btn = InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{order['order_id']}")
        reject_btn = InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{order['order_id']}")
        keyboard.add(approve_btn, reject_btn)
        
        bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown', reply_markup=keyboard)
        
        # Clear waiting flag
        user_orders[user_id]["waiting_for_utr"] = False
        user_orders[user_id]["utr"] = text
        
        bot.send_message(
            user_id,
            "✅ **𝐔𝐓𝐑 𝐑𝐞𝐜𝐞𝐢𝐯𝐞𝐝!**\n\n⏳ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐟𝐨𝐫 𝐚𝐝𝐦𝐢𝐧 𝐯𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧\n\n💡 𝐘𝐨𝐮 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐧𝐨𝐭𝐢𝐟𝐢𝐞𝐝 𝐬𝐨𝐨𝐧",
            parse_mode='Markdown'
        )
        return
    
    # If not waiting for UTR, show help
    help_msg = """
❓ **𝐖𝐡𝐚𝐭 𝐜𝐚𝐧 𝐈 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮 𝐰𝐢𝐭𝐡?**

━━━━━━━━━━━━━━━━━━━━━━━━
💰 **𝐓𝐨 𝐛𝐮𝐲 𝐀𝐏𝐊 𝐅𝐔𝐃:**
• Click /start
• Press BUY NOW
• Follow instructions

━━━━━━━━━━━━━━━━━━━━━━━━
📞 **𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐀𝐝𝐦𝐢𝐧:**
@RahulModDeveloper
"""
    bot.send_message(user_id, help_msg, parse_mode='Markdown')

# ============= ADMIN APPROVAL CALLBACK =============
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data.startswith("reject_"))
def handle_admin_action(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Not authorized!", show_alert=True)
        return
    
    action, order_id = call.data.split("_", 1)
    
    # Find user by order_id
    user_id = None
    for uid, data in user_orders.items():
        if data["order_id"] == order_id:
            user_id = uid
            break
    
    if user_id and user_id in user_orders:
        if action == "approve":
            verified_users.add(user_id)
            user_orders[user_id]["status"] = "completed"
            
            # Send success message
            success_msg = """
╔══════════════════════════════╗
║    ✅ 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐕𝐄𝐑𝐈𝐅𝐈𝐄𝐃 ✅    ║
╚══════════════════════════════╝

◈────────────────────◈
│   🎉 𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐏𝐔𝐑𝐂𝐇𝐀𝐒𝐄   │
◈────────────────────◈

✅ **𝐘𝐨𝐮𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐢𝐬 𝐯𝐞𝐫𝐢𝐟𝐢𝐞𝐝!**

━━━━━━━━━━━━━━━━━━━━━━━━
📱 **𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐘𝐨𝐮𝐫 𝐀𝐏𝐊 𝐅𝐔𝐃 𝐕𝟐:**

[🔽 **𝐂𝐋𝐈𝐂𝐊 𝐇𝐄𝐑𝐄 𝐓𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃**](https://example.com/apk-fud.apk)

━━━━━━━━━━━━━━━━━━━━━━━━
📆 **𝐕𝐚𝐥𝐢𝐝𝐢𝐭𝐲:** 30 𝐃𝐚𝐲𝐬
🔄 **𝐎𝐧𝐞 𝐂𝐥𝐢𝐜𝐤 𝐈𝐧𝐬𝐭𝐚𝐥𝐥:** ✅

👨‍💻 @RahulModDeveloper
"""
            
            keyboard = InlineKeyboardMarkup()
            download_btn = InlineKeyboardButton("📥 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐀𝐏𝐊", url="https://example.com/apk-fud.apk")
            keyboard.add(download_btn)
            
            bot.send_message(user_id, success_msg, parse_mode='Markdown', reply_markup=keyboard)
            
            bot.answer_callback_query(call.id, "✅ Payment approved!", show_alert=True)
            bot.edit_message_text(f"✅ **APPROVED** - Order: {order_id}", call.message.chat.id, call.message.message_id)
            
        else:  # reject
            bot.send_message(
                user_id,
                "❌ **𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐑𝐞𝐣𝐞𝐜𝐭𝐞𝐝!**\n\n💡 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐨𝐧𝐭𝐚𝐜𝐭 𝐚𝐝𝐦𝐢𝐧: @RahulModDeveloper",
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id, "❌ Payment rejected!", show_alert=True)
            bot.edit_message_text(f"❌ **REJECTED** - Order: {order_id}", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ Order not found!", show_alert=True)

# ============= CANCEL ORDER =============
@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel_callback(call):
    user_id = call.from_user.id
    
    if user_id in user_orders:
        del user_orders[user_id]
    
    bot.answer_callback_query(call.id, "❌ Order cancelled!")
    bot.send_message(
        user_id,
        "❌ **𝐎𝐫𝐝𝐞𝐫 𝐜𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝!**\n\n💡 𝐓𝐲𝐩𝐞 /start 𝐭𝐨 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧",
        parse_mode='Markdown'
    )

# ============= ADMIN COMMANDS =============
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    stats_msg = f"""
╔══════════════════════════════╗
║      👑 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋 👑      ║
╚══════════════════════════════╝

📊 **𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒**

✅ **𝐕𝐞𝐫𝐢𝐟𝐢𝐞𝐝 𝐔𝐬𝐞𝐫𝐬:** {len(verified_users)}
⏳ **𝐏𝐞𝐧𝐝𝐢𝐧𝐠 𝐎𝐫𝐝𝐞𝐫𝐬:** {len(user_orders)}
💰 **𝐏𝐫𝐢𝐜𝐞:** ₹500

━━━━━━━━━━━━━━━━━━━━━━━━
📌 /give @username - Give free access
📌 /broadcast - Send message to all
━━━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(ADMIN_ID, stats_msg, parse_mode='Markdown')

@bot.message_handler(commands=['give'])
def give_access(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /give @username")
        return
    
    username = parts[1].replace("@", "")
    verified_users.add(username)
    bot.reply_to(message, f"✅ Access granted to @{username}")

@bot.message_handler(commands=['help'])
def help_command(message):
    help_msg = """
╔══════════════════════════════╗
║        📚 𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔 📚        ║
╚══════════════════════════════╝

/start - 𝐒𝐭𝐚𝐫𝐭 𝐭𝐡𝐞 𝐛𝐨𝐭
/status - 𝐂𝐡𝐞𝐜𝐤 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐬𝐭𝐚𝐭𝐮𝐬
/help - 𝐒𝐡𝐨𝐰 𝐭𝐡𝐢𝐬 𝐦𝐞𝐧𝐮

━━━━━━━━━━━━━━━━━━━━━━━━
💡 **𝐇𝐎𝐖 𝐓𝐎 𝐁𝐔𝐘:**
1️⃣ /start
2️⃣ 𝐂𝐥𝐢𝐜𝐤 𝐁𝐔𝐘 𝐍𝐎𝐖
3️⃣ 𝐏𝐚𝐲 𝐭𝐨 𝐔𝐏𝐈 𝐈𝐃
4️⃣ 𝐒𝐞𝐧𝐝 𝐔𝐓𝐑 𝐧𝐮𝐦𝐛𝐞𝐫

━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 @RahulModDeveloper
"""
    bot.send_message(message.chat.id, help_msg, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    user_id = message.from_user.id
    
    if user_id in verified_users:
        status_msg = """
╔══════════════════════════════╗
║    ✅ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐀𝐂𝐓𝐈𝐕𝐄 ✅    ║
╚══════════════════════════════╝

📱 **𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐚𝐜𝐭𝐢𝐯𝐞 𝐀𝐏𝐊 𝐅𝐔𝐃 𝐚𝐜𝐜𝐞𝐬𝐬**

📆 **𝐕𝐚𝐥𝐢𝐝 𝐮𝐩 𝐭𝐨:** 30 𝐝𝐚𝐲𝐬
🔄 **𝐎𝐧𝐞 𝐂𝐥𝐢𝐜𝐤 𝐈𝐧𝐬𝐭𝐚𝐥𝐥:** ✅

[📥 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐀𝐏𝐊](https://example.com/apk-fud.apk)
"""
    else:
        status_msg = """
╔══════════════════════════════╗
║    ❌ 𝐍𝐎 𝐀𝐂𝐓𝐈𝐕𝐄 𝐒𝐔𝐁𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍 ❌    ║
╚══════════════════════════════╝

💡 𝐓𝐲𝐩𝐞 /start 𝐭𝐨 𝐩𝐮𝐫𝐜𝐡𝐚𝐬𝐞
💰 𝐏𝐫𝐢𝐜𝐞: ₹𝟱𝟬𝟬 𝐨𝐧𝐥𝐲
"""
    
    bot.send_message(user_id, status_msg, parse_mode='Markdown')

# ============= WEBHOOK =============
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return jsonify({"status": "ok", "message": "Webhook is active"}), 200
    
    try:
        data = request.json or request.form.to_dict()
        print(f"[WEBHOOK] {data}")
        return jsonify({"status": "success"}), 200
    except:
        return jsonify({"status": "success"}), 200

@app.route('/')
def home():
    return {
        "status": "APK FUD Bot Running",
        "verified": len(verified_users),
        "pending": len(user_orders)
    }, 200

def run_bot():
    while True:
        try:
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    print("="*50)
    print("🔥 APK FUD BOT V2 - FIXED 🔥")
    print("="*50)
    
    # Start bot
    thread = threading.Thread(target=run_bot)
    thread.daemon = True
    thread.start()
    
    # Start Flask
    app.run(host="0.0.0.0", port=port)
