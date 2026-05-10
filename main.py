import os
import telebot
import yt_dlp
import sqlite3
from telebot import types
import logging

# --- الإعدادات الأساسية ---
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 123456789  # استبدل هذا برقم الـ ID الخاص بك (يمكنك الحصول عليه من @userinfobot)
bot = telebot.TeleBot(TOKEN)

# إعداد قاعدة البيانات لحفظ المستخدمين (لعمل الإذاعة لاحقاً)
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)')
conn.commit()

# --- وظائف مساعدة ---
def add_user(user_id):
    cursor.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (user_id,))
    conn.commit()

def get_all_users():
    cursor.execute('SELECT id FROM users')
    return cursor.fetchall()

# --- لوحة المفاتيح الاحترافية ---
def main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("طريقة الاستخدام 📖", callback_data="help"),
        types.InlineKeyboardButton("المطور 👨‍💻", url="https://t.me/axeror"), # استبدل بيوزرك
        types.InlineKeyboardButton("إحصائيات البوت 📊", callback_data="stats")
    )
    return markup

# --- معالجة الأوامر ---
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id)
    welcome_text = (
        f"مرحباً بك {message.from_user.first_name} في **Axeror Downloader** 📥\n\n"
        "أرسل رابط الفيديو من (YouTube, TikTok, Instagram, FB) وسأقوم بتحميله فوراً بأعلى جودة."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_markup())

# --- نظام الإذاعة (للآدمن فقط) ---
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "أرسل الرسالة التي تريد إذاعتها للكل (نص، صورة، فيديو)...")
        bot.register_next_step_handler(msg, send_broadcast)

def send_broadcast(message):
    users = get_all_users()
    count = 0
    for user in users:
        try:
            bot.copy_message(user[0], message.chat.id, message.message_id)
            count += 1
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ تم إرسال الرسالة إلى {count} مستخدم.")

# --- المعالج الرئيسي للتحميل ---
@bot.message_handler(func=lambda message: True)
def handle_links(message):
    url = message.text
    if "http" not in url:
        return

    wait_msg = bot.reply_to(message, "⏳ جاري استخراج الفيديو، انتظر ثانية...")

    # إعدادات yt-dlp الذكية
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cachedir': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail')

            # إرسال الفيديو كملف فيديو وليس مجرد رابط
            bot.send_video(
                message.chat.id, 
                video_url, 
                caption=f"✅ **تم التحميل بنجاح**\n\n🎬: {title}\n🆔: @axeror_bot",
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, wait_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ عذراً، لا يمكنني تحميل هذا الرابط حالياً.\nالسبب: {str(e)[:50]}...", message.chat.id, wait_msg.message_id)

# --- معالجة الضغط على الأزرار ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "stats":
        users_count = len(get_all_users())
        bot.answer_callback_query(call.id, f"عدد مستخدمي البوت الحالي: {users_count}", show_alert=True)
    elif call.data == "help":
        bot.send_message(call.message.chat.id, "فقط قم بنسخ رابط الفيديو ولصقه هنا، وسيتكفل البوت بالباقي!")

if __name__ == "__main__":
    print("Axeror Bot is Online!")
    bot.infinity_polling()
    
