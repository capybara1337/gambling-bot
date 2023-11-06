import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import token
import db_manager as db
BANK = 10000
bot = telebot.TeleBot(token)

bar = {'ягерьбомба' : 300, 'водка' : 100}

def main_menu(message: telebot.types.Message):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Взять деньги в долг💸', callback_data='lend_cash'))
    markup.row(InlineKeyboardButton('Заказать напиток🍸', callback_data='bar'))
    markup.add(InlineKeyboardButton('Перевод денег за границу💱', callback_data='transaction'))
    markup.add(InlineKeyboardButton('Таблица лидеров🏅', callback_data='leaderboard'))
    markup.add(InlineKeyboardButton('Поздравить Влада с днём рождения🎉', callback_data='congratulations'))
    markup.add(InlineKeyboardButton('Изменить фамилию и имя✍️', callback_data='change_user'))
    bot.send_message(message.chat.id, f'Ваши имя и фамилия: {db.get_info(message)[0]} {db.get_info(message)[1]} \nВаш баланс💰: {db.get_info(message)[3]} \nВыберете действие:', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    db.create(message)
    bot.send_message(message.chat.id, 'привет, пожалуйста введи своё имя и фамилию, через пробел🥺 ')
    bot.register_next_step_handler(message, user_name)
    #main_menu(message)

def user_name(message):
    try:
        name = message.text.split(' ')
        db.addnametodb(message, name)
    except IndexError:
        bot.send_message(message.chat.id, 'Введите корректные данные, ИМЯ пробел ФАМИЛИЯ')
        bot.register_next_step_handler(message, user_name)
        return
    bot.send_message(message.chat.id, 'поздравляю! ты теперь официальный гость влада козлова🤩')
    main_menu(message)

@bot.callback_query_handler(func=lambda callback: True)
def callback_start(callback: telebot.types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.id, reply_markup=None)
    # print(callback)
    # bot.edit_message_text(text= ,chat_id=callback.message.chat.id, message_id=callback.message.id, reply_markup=)
    bot.send_message(callback.message.chat.id, 'тест')
    if callback.data == 'lend_cash':
        bot.send_message(callback.message.chat.id, 'Введите сумму, которую вы хотите взять в долг' + '\n' +
                         'Комиссия составляет 3%, то есть взяв 100, придется вернуть 103')
        bot.send_message(callback.message.chat.id, f'Ваш кредитный лимит: {1000 - db.get_info(callback.message)[3]} \nВведите сумму, которую хотите взять в долг:')
        bot.register_next_step_handler(callback.message, addlend)
    if callback.data == 'bar':
        count = 0
        s = ''
        for i in bar.items():
            count+=1
            s += str(count) + '. ' + i[0]+ ': ' + str(i[1]) + '💵\n'
        bot.send_message(callback.message.chat.id, s + 'Напишите наименование напитка, который вы хотите заказать🍹:')
        bot.register_next_step_handler(callback.message, bar_purchase)
    if callback.data == 'canceled':
        bot.send_message(callback.message.chat.id, 'Покупка отменена')
        main_menu(callback.message)
    if callback.data in bar.keys():
        db.buy_bar(callback.message, callback.data, bar)
        print(callback.data)
        bot.send_message(callback.message.chat.id, 'Покупка прошла успешно! Заказ отправлен бармену ✅')
        # Добавить отправку сообщения с заказом бармену :3
        # bot.send_message(тут id бармена, 'Заказ: '+ callback.data + ' ' + db.get_info(message)[0] + db.get_info(message)[1])
        main_menu(callback.message)
    if callback.data == 'leaderboard':
        lb = db.getleaderboard()
        bot.send_message(callback.message.chat.id, lb)
        main_menu(callback.message)
    if callback.data == 'congratulations':
        # bot.send_message(тут id влада козлова, 'Поздравление от' + db.get_info(message)[0] + db.get_info(message)[1])
        pass
    if callback.data == 'change_user':
        bot.send_message(callback.message.chat.id, 'Пожалуйста введи своё имя и фамилию, через пробел🥺')
        bot.register_next_step_handler(callback.message, change_user_name)

def change_user_name(message):
    try:
        name = message.text.split(' ')
        db.addnametodb(message, name)
    except IndexError:
        bot.send_message(message.chat.id, 'Введите корректные данные, ИМЯ пробел ФАМИЛИЯ')
        bot.register_next_step_handler(message, user_name)
        return
    bot.send_message(message.chat.id, 'Данные изменены успешно')
    main_menu(message)

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

def bar_purchase(message: telebot.types.Message):
    id = message.chat.id
    name = message.text.strip()
    print(name)
    if name in bar.keys():
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('Купить🫰', callback_data=name))
        markup.row(InlineKeyboardButton('Бросаю пить❤️‍🩹', callback_data='canceled'))
        bot.send_message(message.chat.id, f'Ваш напиток : {message.text}', reply_markup=markup)  
    else:
        bot.send_message(message.chat.id, 'Введите корректное название напитка')
        bot.register_next_step_handler(message, bar_purchase)
bot.polling()