import telebot
from telebot import types
import yt_dlp
import os

bot = telebot.TeleBot("8701261854:AAGk_EGJTpKctYPaluNSO6QxE76TLogadR8")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("➕ أضفني للمجموعة", url="https://t.me/axeror_bot?startgroup=true")
    btn2 = types.InlineKeyboardButton("👨‍💻 المطور", url="https://t.me/ao1x1")
    markup.add(btn1, btn2)
    bot.send_photo(message.chat.id,
        photo="https://i.ibb.co/tpfCthtk/image.jpg",
        caption="""
• أهلاً بك عزيزي 👋
• أنا بوت اسمي يوهان 𒀭
• اختصاصي حماية المجموعات 🛡
• أضفني لمجموعتك وارفعني أدمن!
• المطور ↤ @ao1x1
""", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """
📋 قائمة الأوامر:

/start - بدء البوت 🤖
/help - قائمة الأوامر 📋
/يوت - تحميل أغنية 🎵
""")

@bot.message_handler(commands=['يوت'])
def music(message):
    query = message.text.replace('/يوت', '').strip()
    if not query:
        bot.reply_to(message, "اكتب اسم الأغنية!\nمثال: /يوت لحن قمر")
        return
    msg = bot.reply_to(message, "• جاري التحميل ...")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'song.%(ext)s',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            filename = ydl.prepare_filename(info['entries'][0])
        with open(filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)
        os.remove(filename)
    except:
        bot.reply_to(message, "حدث خطأ! جرب مرة ثانية 🎵")

bot.infinity_polling()
