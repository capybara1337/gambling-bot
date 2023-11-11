import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import token, admins
import db_manager as db
bot = telebot.TeleBot(token)
bar = {'Лонг-айленд' : 500, 'Текила санрайз' : 350, 'Мартини фиеро' : 250, 'Ром кола' : 250, 
       'Виски кола' : 250, 'Отвертка' : 200, 'Джин тоник' : 250, 'Дайкири' : 350, 'Северное сияние' : 300}

events = {'Заказное убийство' : 1500, 'Кокаиновая фотосессия' : 1000, 
          'Поздравление Стаса' : 1000, 'Кастомный коктейль' : 1000,
          'Попробуй проглоти' : 1000, 'Кальян' : 500}

def main_menu(message: telebot.types.Message):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Заказать напиток🍸', callback_data='bar'))
    markup.row(InlineKeyboardButton('Отправить деньги📩', callback_data='send_cash'))
    markup.add(InlineKeyboardButton('Таблица лидеров🏅', callback_data='leaderboard'))
    markup.add(InlineKeyboardButton('Поздравить Влада с днём рождения🎉', callback_data='congratulations'))
    markup.add(InlineKeyboardButton('Изменить фамилию и имя✍️', callback_data='change_user'))
    markup.add(InlineKeyboardButton('Меню ивентов🥳', callback_data='event_menu'))
    if db.get_info(message)[5] == 1:
        markup.add(InlineKeyboardButton('Вывести всех пользователей💻', callback_data='admin_butt'))
    bot.send_message(message.chat.id, f'Ваши имя и фамилия: {db.get_info(message)[0]} {db.get_info(message)[1]} \nВаш баланс💰: {db.get_info(message)[3]} 💵стасиков \nВыберете действие:', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    db.create(message)
    bot.send_message(message.chat.id, 'Привет, пожалуйста введи своё имя и фамилию, через пробел🥺 ')
    bot.register_next_step_handler(message, user_name)
    #main_menu(message)

def user_name(message):
    try:
        name = message.text
        if name == None:
            raise IndexError
        name = name.split(' ')
        db.addnametodb(message, name)
    except IndexError:
        bot.send_message(message.chat.id, 'Введите корректные данные, ИМЯ пробел ФАМИЛИЯ')
        bot.register_next_step_handler(message, user_name)
        return
    bot.send_message(message.chat.id, 'Поздравляю! ты теперь официальный гость Влада Козлова🤩')
    db.Printalluser()
    main_menu(message)

def check_person(message: telebot.types.Message):
    # print(tuple(message.text.split()[1:2]))
    try:
        names = db.get_names(message)
        ind = int(message.text[1:])
        if ind in range(len(names) + 1):
        # if tuple(message.text.split()) in db.get_names(message):
            bot.send_message(message.chat.id, 'Введите сумму стасиков, которую хотите отправить! (коммисия 3%)')
            bot.register_next_step_handler(message, send_cash, db.get_chat_id(names[ind-1]))
        else:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, 'Проверьте корректность введённых данных!')
        bot.send_message(message.chat.id, 'Выберете гостя, которому хотите отправить стасики! (коммисия 3%)')
        members = db.get_names(message)
        members_out = ''
        count = 1
        for i in members:
            members_out += f'/{count} {i[0]} {i[1]} \n'
            count += 1
        bot.send_message(message.chat.id, members_out)
        bot.register_next_step_handler(message, check_person)

def send_cash(message: telebot.types.Message, id: int):
    try:
        if db.check_wealth(message) == 1:
            db.withdraw_money(message, id)
            bot.send_message(message.chat.id, 'Стасики отправлены!')
            main_menu(message)
        elif db.check_wealth(message) == -1:
            bot.send_message(message.chat.id, 'На Вашем балансе недостаточно стасиков!')
            bot.send_message(message.chat.id, 'Введите сумму стасиков, которую хотите отправить! (коммисия 3%)')
            bot.register_next_step_handler(message, send_cash, id)
        else: raise Exception
    except:
        bot.send_message(message.chat.id, 'Введенны неверные данные!')
        bot.send_message(message.chat.id, 'Введите сумму стасиков, которую хотите отправить! (коммисия 3%)')
        bot.register_next_step_handler(message, send_cash, id)

@bot.callback_query_handler(func=lambda callback: True)
def callback_start(callback: telebot.types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.id, reply_markup=None)
    # print(callback)
    # bot.edit_message_text(text= ,chat_id=callback.message.chat.id, message_id=callback.message.id, reply_markup=)
    if callback.data == 'bar':
        markup = InlineKeyboardMarkup()
        for i in bar.items():
            markup.add(InlineKeyboardButton(i[0] + ' | ' + str(i[1]), callback_data=i[0]))
        markup.add(InlineKeyboardButton('Вернуться в меню🔙', callback_data='canceled'))
        bot.send_message(callback.message.chat.id,'Напишите наименование напитка, который вы хотите заказать🍹:', reply_markup=markup)

    if callback.data in bar.keys():
        try:
            db.buy_bar(callback.message, callback.data, bar)
            bot.send_message(callback.message.chat.id, 'Покупка прошла успешно! Заказ отправлен бармену ✅')
        except ValueError:
            bot.send_message(callback.message.chat.id, 'Покупка отменена, недостаточно стасиков❌')
        # Добавить отправку сообщения с заказом бармену :3
        bot.send_message('338011074', 'Заказ: '+ callback.data + ' ' + db.get_info(callback.message)[0] + db.get_info(callback.message)[1])
        bot.send_message('442164116', 'Заказ: '+ callback.data + ' ' + db.get_info(callback.message)[0] + db.get_info(callback.message)[1])
        bot.send_message('874896474', 'Заказ: '+ callback.data + ' ' + db.get_info(callback.message)[0] + db.get_info(callback.message)[1])
        main_menu(callback.message)

    if callback.data == 'leaderboard':
        lb = db.getleaderboard()
        if lb == '':
            bot.send_message(callback.message.chat.id, 'Гостей ещё нет')
        else:
            bot.send_message(callback.message.chat.id, lb)
        main_menu(callback.message)

    if callback.data == 'congratulations':
        bot.send_message('1988704372', 'Поздравление от: ' + db.get_info(callback.message)[0] + ' ' + db.get_info(callback.message)[1] + '!!!🎊')
        main_menu(callback.message)

    if callback.data == 'change_user':
        bot.send_message(callback.message.chat.id, 'Пожалуйста введи своё имя и фамилию, через пробел🥺')
        bot.register_next_step_handler(callback.message, change_user_name)

    if callback.data == 'event_menu':
        markup = InlineKeyboardMarkup()
        for i in events.items():
            markup.add(InlineKeyboardButton(i[0] + ' | ' + str(i[1]), callback_data=i[0]))
        markup.add(InlineKeyboardButton('Вернуться в меню🔙', callback_data='canceled'))
        bot.send_message(callback.message.chat.id, 'Выбери ивент, который ты хочешь заказать: ', reply_markup=markup)

    if callback.data in events.keys():
        try:
            db.buy_event(callback.message, callback.data, events)     
            bot.send_message(callback.message.chat.id, 'Ивент ' + callback.data + ' приобретен!')
            for i in admins:
                bot.send_message('854453212',  db.get_info(callback.message)[0] + ' ' + db.get_info(callback.message)[1] + ' купил(-а) ивент ' + callback.data)
        except ValueError:
            bot.send_message(callback.message.chat.id, 'Покупка отменена, недостаточно стасиков❌')
        main_menu(callback.message)

    if callback.data == 'send_cash':
        members = db.get_names(callback.message)
        members_out = ''
        count = 1
        for i in members:
            members_out += f'/{count} {i[0]} {i[1]} \n'
            count += 1
        bot.send_message(callback.message.chat.id, 'Выберете гостя, которому хотите отправить деньги! (коммисия 3%)')
        bot.send_message(callback.message.chat.id, members_out)
        bot.register_next_step_handler(callback.message, check_person)

    if callback.data == 'admin_butt':
        bot.send_message(callback.message.chat.id, db.getallusers())
        main_menu(callback.message)

    if callback.data == 'canceled':
        bot.edit_message_text('Действие отменено!', callback.message.chat.id, callback.message.id)
        main_menu(callback.message)

def change_user_name(message):
    try:
        name = message.text
        if name == None:
            raise IndexError
        name = name.split(' ')
        db.addnametodb(message, name)
    except IndexError:
        bot.send_message(message.chat.id, 'Введите корректные данные, ИМЯ пробел ФАМИЛИЯ')
        bot.register_next_step_handler(message, change_user_name)
        return
    bot.send_message(message.chat.id, 'Данные изменены успешно')
    main_menu(message)

bot.polling()