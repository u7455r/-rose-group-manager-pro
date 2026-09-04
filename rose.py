import os
import random
import re
import time
import telebot
from telebot import types
from keep_alive import keep_alive

# আপনার নতুন এপিআই টোকেন
BOT_TOKEN = "8886219226:AAHAk9py2IIsXQZKF3X6CwyKWswQalJpZdM"
bot = telebot.TeleBot(BOT_TOKEN)

# Force Subscribe এর চ্যানেল/গ্রুপ তথ্য
REQ_CHANNEL = "@rafimhossen3"
REQ_CHANNEL_LINK = "https://t.me/rafimhossen3"
REQ_GROUP_LINK = "https://t.me/+M2fdG9hbU3tlOGQ1"

REACTIONS = ["🔥", "👍", "❤️", "🎉", "⚡", "👏"]
USER_WARNS = {}
GROUP_FILTERS = {}

def is_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(REQ_CHANNEL, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception:
        return True

def get_join_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_chan = types.InlineKeyboardButton("📢 ১. চ্যানেলে জয়েন করুন", url=REQ_CHANNEL_LINK)
    btn_grp = types.InlineKeyboardButton("👥 ২. গ্রুপে জয়েন করুন", url=REQ_GROUP_LINK)
    btn_check = types.InlineKeyboardButton("✅ জয়েন করেছি (Verify)", callback_data="check_sub")
    markup.add(btn_chan, btn_grp, btn_check)
    return markup

def is_group_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['creator', 'administrator']
    except Exception:
        return False

def get_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🔄 রিস্টার্ট (/start)"))
    markup.add(types.KeyboardButton("📖 কমান্ড লিস্ট"), types.KeyboardButton("👤 আমার তথ্য (/id)"))
    markup.add(types.KeyboardButton("🛡️ অ্যাডমিন লিস্ট (/admins)"), types.KeyboardButton("📜 রুলস"))
    markup.add(types.KeyboardButton("➕ গ্রুপে এড করুন"), types.KeyboardButton("📢 চ্যানেলে এড করুন"))
    return markup

MODULE_BTNS = [
    "Admin", "Antiflood", "AntiRaid", "Approval", "Bans", "Blocklists",
    "CAPTCHA", "Clean Comma", "Clean Service", "Connections", "Disabling",
    "Federations", "Filters", "Formatting", "Greetings", "Import/Export",
    "Languages", "Locks", "Log Channels", "Misc", "Notes", "Pin",
    "Privacy", "Purges", "Reports", "Rules", "Topics"
]

def get_rose_help_menu():
    markup = types.InlineKeyboardMarkup(row_width=3)
    btns = [types.InlineKeyboardButton(name, callback_data=f"h_{name.lower().replace(' ', '')[:8]}") for name in MODULE_BTNS]
    markup.add(*btns)
    markup.row(types.InlineKeyboardButton("Warnings", callback_data="h_warn"), types.InlineKeyboardButton("⭐ Custom Instances", callback_data="h_cust"))
    markup.row(types.InlineKeyboardButton("👨‍💻 Connect Admin (@rafimhossen)", url="https://t.me/rafimhossen"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ ধন্যবাদ! আপনার ভেরিফিকেশন সফল হয়েছে।", show_alert=True)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        send_welcome(call.message, call.from_user)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো চ্যানেলে জয়েন করেননি! আগে জয়েন করে আবার চাপুন।", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("h_") or call.data == "back_menu")
def handle_help_callbacks(call):
    if call.data == "back_menu":
        bot.edit_message_text("নিচের মডিউলগুলোতে চাপ দিয়ে বিস্তারিত জানুন:\nAll commands: `/` `!`", call.message.chat.id, call.message.message_id, reply_markup=get_rose_help_menu())
    else:
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu"), types.InlineKeyboardButton("👨‍💻 Connect Admin", url="https://t.me/rafimhossen"))
        bot.edit_message_text("📌 **মডিউল বিবরণ:**\n\nগ্রুপের মডারেশন, ফিল্টার ও অ্যাডমিন সুরক্ষা সক্রিয় রয়েছে।", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

def send_welcome(message, user=None):
    u = user if user else message.from_user
    text = (
        f"🔄 বট সফলভাবে চালু হয়েছে!\n\n"
        f"হ্যালো **{u.first_name}**! 👋\n\n"
        "আমি আপনার ফ্রি গ্রুপ ম্যানেজমেন্ট ও অটোমেশন বট।\n"
        "গ্রুপ পরিচালনা, পিন মেসেজ, অ্যান্টি-স্প্যাম লিংক ব্লকার ও চ্যানেল অটো-রিয়্যাকশনের জন্য আমাকে গ্রুপে যুক্ত করুন।"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_reply_keyboard(), parse_mode='Markdown')
    bot.send_message(
        message.chat.id, 
        "নিচের মডিউলগুলোতে চাপ দিয়ে বিস্তারিত কমান্ড জেনে নিন:\n\nAll commands can be used with the following: `/` `!`", 
        reply_markup=get_rose_help_menu()
    )

@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == 'private':
        if not is_subscribed(message.from_user.id):
            bot.send_message(
                message.chat.id,
                f"⚠️ **বট ব্যবহার করতে হলে আপনাকে অবশ্যই আমাদের চ্যানেল ও গ্রুপে যুক্ত হতে হবে!**\n\nনিচের লিঙ্কগুলো থেকে জয়েন করে **Verify** বাটনে চাপ দিন:",
                reply_markup=get_join_markup(),
                parse_mode='Markdown'
            )
            return
        send_welcome(message)
    else:
        bot.reply_to(message, "✅ বট সক্রিয় রয়েছে! কমান্ড দেখতে /help লিখুন।")

@bot.message_handler(func=lambda msg: msg.text in [
    "🔄 রিস্টার্ট (/start)", "📖 কমান্ড লিস্ট", "👤 আমার তথ্য (/id)", "🛡️ অ্যাডমিন লিস্ট (/admins)", "📜 রুলস", "➕ গ্রুপে এড করুন", "📢 চ্যানেলে এড করুন"
])
def reply_buttons_handler(message):
    if message.chat.type == 'private' and not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "⚠️ অনুগ্রহ করে আগে আমাদের চ্যানেল ও গ্রুপে জয়েন করুন!", reply_markup=get_join_markup())
        return
        
    bot_info = bot.get_me()
    if message.text == "🔄 রিস্টার্ট (/start)":
        send_welcome(message)
    elif message.text == "📖 কমান্ড লিস্ট":
        bot.send_message(message.chat.id, "নিচের মডিউলগুলোতে চাপ দিয়ে কমান্ড জেনে নিন:", reply_markup=get_rose_help_menu())
    elif message.text == "👤 আমার তথ্য (/id)":
        user = message.from_user
        info = (
            f"👤 **আপনার প্রোফাইল তথ্য:**\n"
            f"• নাম: {user.first_name}\n"
            f"• ইউজারনেম: @{user.username or 'নাই'}\n"
            f"• টেলিগ্রাম আইডি: `{user.id}`"
        )
        bot.send_message(message.chat.id, info, parse_mode='Markdown')
    elif message.text == "🛡️ অ্যাডমিন লিস্ট (/admins)":
        bot.send_message(message.chat.id, "গ্রুপে গিয়ে `/admins` কমান্ড দিলে অ্যাডমিন তালিকা দেখতে পাবেন।")
    elif message.text == "📜 রুলস":
        bot.send_message(message.chat.id, "📜 গ্রুপে কোনো লিঙ্ক শেয়ার ও স্প্যামিং সম্পূর্ণ নিষিদ্ধ।")
    elif message.text == "➕ গ্রুপে এড করুন":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{bot_info.username}?startgroup=true"))
        bot.send_message(message.chat.id, "গ্রুপে এড করতে নিচের বাটনে চাপ দিন:", reply_markup=markup)
    elif message.text == "📢 চ্যানেলে এড করুন":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Add to Channel", url=f"https://t.me/{bot_info.username}?startchannel=true"))
        bot.send_message(message.chat.id, "চ্যানেলে এডমিন করতে নিচের বাটনে চাপ দিন:", reply_markup=markup)

@bot.message_handler(commands=['pin', 'warn', 'ban', 'purge', 'kick', 'mute'])
def handle_admin_commands(message):
    if message.chat.type == 'private':
        return
    
    is_anon = message.sender_chat and message.sender_chat.id == message.chat.id
    is_user_admin = is_anon or (message.from_user and is_group_admin(message.chat.id, message.from_user.id))

    if not is_user_admin:
        bot.reply_to(message, "❌ এই কমান্ডটি শুধুমাত্র গ্রুপের অ্যাডমিনগণ ব্যবহার করতে পারবেন!")
        return

    text_clean = message.text.split()[0].split('@')[0].replace('/', '')
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Click to prove admin", callback_data=f"prov_{text_clean}_{message.message_id}"))
    
    bot.reply_to(
        message, 
        "It looks like you're anonymous.\nTap this button to confirm your identity.", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("prov_"))
def verify_and_execute_admin(call):
    data_parts = call.data.split("_")
    cmd = data_parts[1]
    
    if not is_group_admin(call.message.chat.id, call.from_user.id):
        bot.answer_callback_query(call.id, "❌ আপনি এই গ্রুপের অ্যাডমিন নন!", show_alert=True)
        return

    bot.answer_callback_query(call.id, "✅ অ্যাডমিন ভেরিফাই হয়েছে!")
    
    try:
        orig_msg = call.message.reply_to_message
        chat_id = call.message.chat.id

        if cmd == 'pin':
            if orig_msg:
                bot.pin_chat_message(chat_id, orig_msg.message_id)
                bot.edit_message_text("📌 মেসেজটি সফলভাবে পিন করা হয়েছে!", chat_id, call.message.message_id)
            else:
                bot.edit_message_text("⚠️ পিন করার জন্য মেসেজে রিপ্লাই দেওয়া হয়নি।", chat_id, call.message.message_id)

        elif cmd == 'warn':
            if orig_msg and orig_msg.from_user:
                target = orig_msg.from_user
                key = f"{chat_id}_{target.id}"
                USER_WARNS[key] = USER_WARNS.get(key, 0) + 1
                curr = USER_WARNS[key]
                if curr >= 3:
                    bot.restrict_chat_member(chat_id, target.id, permissions=types.ChatPermissions(can_send_messages=False))
                    bot.edit_message_text(f"🚫 [{target.first_name}](tg://user?id={target.id}) ৩ বার সতর্ক পেয়ে মিউট হয়েছেন!", chat_id, call.message.message_id, parse_mode='Markdown')
                    USER_WARNS[key] = 0
                else:
                    bot.edit_message_text(f"⚠️ [{target.first_name}](tg://user?id={target.id}) সতর্কবার্তা: **{curr}/3**", chat_id, call.message.message_id, parse_mode='Markdown')
            else:
                bot.edit_message_text("⚠️ সতর্ক করতে ইউজারের মেসেজে রিপ্লাই দিন।", chat_id, call.message.message_id)

        elif cmd == 'ban':
            if orig_msg and orig_msg.from_user:
                bot.ban_chat_member(chat_id, orig_msg.from_user.id)
                bot.edit_message_text("🚫 সদস্যকে স্থায়ীভাবে ব্যান করা হয়েছে।", chat_id, call.message.message_id)
            else:
                bot.edit_message_text("⚠️ ব্যান করতে ইউজারের মেসেজে রিপ্লাই দিন।", chat_id, call.message.message_id)

        elif cmd == 'purge':
            if orig_msg:
                start_id = orig_msg.message_id
                end_id = call.message.message_id
                for mid in range(start_id, end_id + 1):
                    try:
                        bot.delete_message(chat_id, mid)
                    except Exception:
                        pass
            else:
                bot.edit_message_text("⚠️ যেখান থেকে মুছবেন রিপ্লাই দিন।", chat_id, call.message.message_id)

    except Exception as e:
        bot.answer_callback_query(call.id, f"ত্রুটি: {e}", show_alert=True)

@bot.message_handler(commands=['addfilter'])
def add_filter(message):
    if message.chat.type == 'private' or not is_group_admin(message.chat.id, message.from_user.id):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ নিয়ম: `/addfilter শব্দ | উত্তর`", parse_mode='Markdown')
        return
    content = parts[1].split('|')
    if len(content) < 2:
        bot.reply_to(message, "⚠️ সঠিক ফরম্যাট: `/addfilter শব্দ | উত্তর`", parse_mode='Markdown')
        return
    kw = content[0].strip().lower()
    ans = content[1].strip()
    if message.chat.id not in GROUP_FILTERS:
        GROUP_FILTERS[message.chat.id] = {}
    GROUP_FILTERS[message.chat.id][kw] = ans
    bot.reply_to(message, f"🎯 ফিল্টার সেট হয়েছে: `{kw}`", parse_mode='Markdown')

@bot.message_handler(commands=['filters'])
def list_filters(message):
    if message.chat.type == 'private':
        return
    filters = GROUP_FILTERS.get(message.chat.id, {})
    if not filters:
        bot.reply_to(message, "📂 এই গ্রুপে কোনো কাস্টম ফিল্টার নেই।")
        return
    txt = "📋 **গ্রুপের ফিল্টার তালিকা:**\n\n"
    for kw in filters.keys():
        txt += f"• `{kw}`\n"
    bot.reply_to(message, txt, parse_mode='Markdown')

@bot.message_handler(commands=['rules'])
def send_rules(message):
    bot.reply_to(message, "📜 **গ্রুপের নিয়মাবলী:**\n\n১. স্প্যাম মেসেজ ও লিঙ্ক সম্পূর্ণ নিষেধ।\n২. গ্রুপের নিয়ম মেনে চলুন।")

@bot.message_handler(func=lambda msg: msg.chat.type in ['group', 'supergroup'])
def group_filters_and_links(message):
    if not message.text:
        return
    is_admin = is_group_admin(message.chat.id, message.from_user.id) if message.from_user else False
    
    if re.search(r'(https?://[^\s]+|t\.me/[^\s]+|telegram\.me/[^\s]+)', message.text):
        if not is_admin:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, f"⚠️ [{message.from_user.first_name}](tg://user?id={message.from_user.id}), গ্রুপে লিঙ্ক শেয়ার নিষিদ্ধ!", parse_mode='Markdown')
            except Exception:
                pass
            return

    chat_filters = GROUP_FILTERS.get(message.chat.id, {})
    text_lower = message.text.lower()
    for kw, resp in chat_filters.items():
        if kw in text_lower:
            bot.reply_to(message, resp)
            break

if __name__ == '__main__':
    keep_alive()
    try:
        bot.delete_webhook(drop_pending_updates=True)
        time.sleep(1)
    except Exception:
        pass
    print("Final Rose Bot with Force-Sub, Filters & Admin Verify is running!")
    bot.infinity_polling(skip_pending=True)
