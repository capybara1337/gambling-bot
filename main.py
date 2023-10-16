import telebot
import sqlite3
from telebot import types
from config import token

bot = telebot.TeleBot(token)
bal = 1000
lend_limit = 1000
bar = []
@bot.message_handler(commands=['start']) # обработка команды start
def main(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    global bal
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        chatid integer,
        balance integer,
        lend_cash integer,
        winrate float
    )""")
    cur.execute("INSERT INTO users(chatid, balance, lend_cash, winrate) SELECT ?, ?, 0, 0 WHERE NOT EXISTS (SELECT chatid FROM users WHERE chatid = ?)" , (id, bal, id))
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    data.commit()
    data.close()
    markup=types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Взять деньги в долг', callback_data = '+lend_cash'))
    markup.row(types.InlineKeyboardButton('Заказать напиток', callback_data='bar'))
    markup.add(types.InlineKeyboardButton('Игры', callback_data='games'))
    bot.send_message(message.chat.id, """Ваши данные были занесены в систему, прошу нажмите на одну из кнопок!
Либо напишите /help для дополнительной информации""",reply_markup = markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_start(callback):
    bot.send_message(callback.message.chat.id, 'тест')
    if callback.data == '+lend_cash':
        bot.send_message(callback.message.chat.id, 'Введите сумму, которую вы хотите взять в долг (до 1000)')
        bot.register_next_step_handler(callback.message, addlend)
    if callback.data == 'bar':
        pass
    if callback.data == 'games':
        pass
def addlend(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Взять деньги в долг', callback_data='+lend_cash'))
    markup.row(types.InlineKeyboardButton('Заказать напиток', callback_data='bar'))
    markup.add(types.InlineKeyboardButton('Игры', callback_data='games'))
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Впишите число")
        bot.register_next_step_handler(message, addlend)
        return
    cur.execute("SELECT lend_cash FROM users WHERE chatid = ?", (id,))
    ls = list(cur.fetchone())
    cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
    ball = list(cur.fetchone())
    if lend_limit >= ls[0] + amount > 0:
        cur.execute("UPDATE users SET lend_cash = ? WHERE chatid = ?", (ls[0] + amount, id))
        cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (ball[0] + amount, id))
        cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
        answ = list(cur.fetchone())
        bot.send_message(message.chat.id, f"ваш баланс: {answ[0]}", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Вы ввели неверное число', reply_markup=markup)
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    data.commit()
    data.close()

# @bot.message_handler(commands=['add'])
# def add_lend(message):
#     data = sqlite3.connect('baseddata.db')
#     cur = data.cursor()
#     id = message.chat.id
#     bal = 1600
#     print(id)
#     cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (bal, id))
#     cur.execute("SELECT * FROM users")
#     print(cur.fetchall())
#     data.commit()
#     data.close()


#@bot.message_handler(commands=['bank'])
#def late(message):
   # markup = telebot.types.InlineKeyboardMarkup()
   # markup.row(types.InlineKeyboardButton('Взять денег', callback_data='+money'))
   # markup.row(types.InlineKeyboardButton('ОТДАТЬ ДЕНЬГИ НА БЛАГОТВОРИТЕЛЬНОСТЬ', callback_data='-money'))
    #bot.send_message(message.chat.id, str(b_dep), reply_markup=markup)

#@bot.message_handler(commands=['bar'])
#def bar(message):
   # bot.send_message(message.chat.id, "Выберите напитки из списка:", parse_mode="html")
    #print(message.text)


bot.polling(none_stop=True)
