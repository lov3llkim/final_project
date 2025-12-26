from telebot import TeleBot, types
import sqlite3
from logic import DB_Manager
from config import *




TOKEN = "8585966889:AAEiqYaqx59IMToLIu7rTJasLU-LcrjQsxk"      

bot = TeleBot(TOKEN)
db = DB_Manager(DATABASE)

@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    
    questions = db.select_data("SELECT question FROM faq ORDER BY id")

    # Добавляем кнопки с вопросами
    for i in range(0, len(questions), 2):
        if i + 1 < len(questions):
            markup.add(
                types.KeyboardButton(questions[i][0]),
                types.KeyboardButton(questions[i + 1][0])
            )
        else:
            markup.add(types.KeyboardButton(questions[i][0]))

    # Добавляем кнопку для связи с оператором
    markup.add(types.KeyboardButton("Связаться с оператором"))

    welcome_text = (
        "Здравствуйте! 👋\n"
        "Я бот поддержки магазина.\n\n"
        "Вы можете:\n"
        "• выбрать один из частых вопросов ниже\n"
        "• написать свой вопрос текстом\n\n"
        "Чем могу помочь сегодня?"
    )

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


@bot.message_handler(commands=['faq', 'questions'])
def show_all_questions(message):
    """Показать список всех доступных вопросов"""
    questions = db.select_data("SELECT question FROM faq ORDER BY id")
    
    if questions:
        text = "📋 Доступные вопросы:\n\n"
        for q in questions:
            text += f"• {q[0]}\n"
        text += "\nПросто напишите любой из них или выберите из кнопок!"
    else:
        text = "⚠️ В базе пока нет вопросов"

    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_text = message.text.strip()

    # Пытаемся найти точный ответ по вопросу
    result = db.select_data(
        "SELECT answer FROM faq WHERE question = ?",
        (user_text,)
    )

    if result:
        bot.send_message(message.chat.id, result[0][0])
    else:
        # Если ничего не нашли — вежливый ответ
        if "оператор" in user_text.lower() or "помощь" in user_text.lower():
            bot.send_message(
                message.chat.id,
                "Сейчас передам ваш запрос оператору.\n"
                "Пожалуйста, подождите 1–5 минут, вам ответят 👨‍💻"
            )
        else:
            bot.send_message(
                message.chat.id,
                "😔 К сожалению, я не нашёл точного ответа на ваш вопрос.\n\n"
                "Попробуйте выбрать вопрос из предложенных кнопок\n"
                "или напишите «Связаться с оператором»"
            )
# Запуск
if __name__ == '__main__':
    bot.infinity_polling()
