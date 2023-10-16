import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import token
import db_manager as db

bot = telebot.TeleBot(token)


def main_menu(message: telebot.types.Message):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Взять деньги в долг', callback_data='lend_cash'))
    markup.row(InlineKeyboardButton('Заказать напиток', callback_data='bar'))
    markup.add(InlineKeyboardButton('Игры', callback_data='games'))
    bot.send_message(message.chat.id, f'Ваш баланс: {db.get_info(message)[1]} \nВыберете действие:', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    db.create(message)
    main_menu(message)

    
@bot.callback_query_handler(func=lambda callback: True)
def callback_start(callback: telebot.types.CallbackQuery):
    # print(callback)
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.id, reply_markup=None)
    # bot.edit_message_text(text= ,chat_id=callback.message.chat.id, message_id=callback.message.id, reply_markup=)
    bot.send_message(callback.message.chat.id, 'тест')
    if callback.data == 'lend_cash':
        bot.send_message(callback.message.chat.id, f'Ваш кредитный лимит: {1000 - db.get_info(callback.message)[2]} \nВведите сумму, которую хотите взять в долг:')
        bot.register_next_step_handler(callback.message, addlend)
    if callback.data == 'bar':
        pass
    if callback.data == 'games':
        pass

def addlend(message: telebot.types.Message):
    try:
        amount = int(message.text.strip())
        if amount < 0: raise ValueError
        db.lend(message, amount)
    except ValueError:
        bot.send_message(message.chat.id, "Введено неверное число")
        bot.register_next_step_handler(message, addlend)
        return
    main_menu(message)




bot.polling()