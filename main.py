import telebot
from telebot import types

bot = telebot.TeleBot("8701261854:AAFV1jpqsdE0XMKUecqT01jP5I5oINl7sxg")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("➕ أضفني للمجموعة", url="https://t.me/axeror_bot?startgroup=true")
    btn2 = types.InlineKeyboardButton("👨‍💻 المطور", url="https://t.me/ao1x1")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, """
• أهلاً بك عزيزي 👋
• أنا بوت اسمي يوهان 𒀭
• اختصاصي حماية المجموعات 🛡
• أضفني لمجموعتك وارفعني أدمن!
• المطور ↤ @ao1x1
""", reply_markup=markup)

bot.infinity_polling()
