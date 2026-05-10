import os
import telebot
import yt_dlp
from flask import Flask
from threading import Thread

# --- إعداد خادم وهمي لإبقاء البوت حياً على Render ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    # Render يعطي بورت تلقائي، يجب أن يستمع البوت له
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- كود البوت الأساسي ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! البوت يعمل الآن بنجاح على سيرفرات Render 🚀")

@bot.message_handler(func=lambda message: True)
def download(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "جاري التحميل... ⏳")
        try:
            with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                bot.send_video(message.chat.id, info['url'], caption="تم التحميل بواسطة @axeror_bot")
                bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"خطأ: {str(e)[:50]}", message.chat.id, msg.message_id)

# --- التشغيل النهائي ---
if __name__ == "__main__":
    keep_alive()  # تشغيل الخادم الوهمي في الخلفية
    print("البوت بدأ بالعمل...")
    bot.infinity_p
    olling()
