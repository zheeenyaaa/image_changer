from telebot import TeleBot, types

bot = TeleBot("8393109659:AAGHCUHAPGUHGm917epEtRaR7h7_C8AKHP8")  # вставьте токен вашего бота

@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_info = types.WebAppInfo("https://qtklah-178-157-188-6.ru.tuna.am/")
    btn = types.KeyboardButton("Открыть Mini App", web_app=web_info)
    markup.add(btn)

    bot.send_message(msg.chat.id, "Нажми кнопку ниже — откроется Mini App:", reply_markup=markup)

bot.infinity_polling()
