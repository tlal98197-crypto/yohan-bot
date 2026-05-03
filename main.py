import telebot
from telebot import types

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
""")

bot.infinity_polling()
from youtubesearchpython import VideosSearch

@bot.message_handler(commands=['موسيقى'])
def music(message):
    query = message.text.replace('/موسيقى', '').strip()
    if not query:
        bot.reply_to(message, "اكتب اسم الأغنية بعد الأمر!\nمثال: /موسيقى عمر خيرة")
        return
    search = VideosSearch(query, limit=1)
    result = search.result()['result']
    if result:
        video = result[0]
        bot.reply_to(message, f"🎵 {video['title']}\n{video['link']}")
    else:
        bot.reply_to(message, "ما لقيت نتائج! جرب اسم ثاني 🎵")
