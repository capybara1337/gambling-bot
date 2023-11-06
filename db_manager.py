import sqlite3
from admin import check_privilege
def create(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id   
    balance = check_privilege(id)
    print(balance)
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        name tinytext,
        surname tinytext,
        chatid integer,
        balance integer,
        lent_cash integer,
        isadmin bit
    )""")
    cur.execute("INSERT INTO users(name, surname, chatid, balance, lent_cash, isadmin) SELECT 0, 0, ?, ?, 0, ? WHERE NOT EXISTS (SELECT chatid FROM users WHERE chatid = ?)" , (id, balance[0], balance[1], id))
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    data.commit()
    data.close()

def buy_event(message, event: str, events : dict):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    price = events.get(event)
    cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
    balance = cur.fetchone()[0]
    print(balance)
    print(price)
    cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (balance - price, id))
    data.commit()
    data.close()

def buy_bar(message, name : str, bar : dict):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    price = bar.get(name)
    cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
    balance = cur.fetchone()[0]
    print(balance)
    print(price)
    cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (balance - price, id))
    data.commit()
    data.close()

def get_info(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    info = list(cur.execute("SELECT * FROM users WHERE chatid = ?", (id,)))[0]
    print(info)
    data.commit()
    data.close()
    return info

def addnametodb(message, name : list[str]):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    cur.execute("UPDATE users SET name = ?, surname = ? WHERE chatid = ?", (name[0], name[1], id))  
    data.commit()
    data.close()

def getusersnames():
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    cur.execute("SELECT name, surname FROM users")
    s = cur.fetchall()
    print(s)
    data.commit()
    data.close()
    return s

def get_names(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    cur.execute("SELECT name, surname FROM users WHERE chatid != ?", (id,))
    ls = cur.fetchall()
    print(ls)
    data.commit()
    data.close()
    return ls

def check_wealth(message):
    try:
        cash = int(message.text)
        if cash <= 0: raise ValueError
        data = sqlite3.connect('baseddata.db')
        cur = data.cursor()
        id = message.chat.id
        cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
        balance = cur.fetchone()[0]
        if balance - cash * 1.03 >= 0:
            data.commit()
            data.close()
            return 1
        else:
            data.commit()
            data.close()
            return -1
    except ValueError:
        return 0
    
def withdraw_money(message, id):
    cash = int(message.text) 
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    cur.execute("SELECT balance FROM users WHERE chatid = ?", (message.chat.id,))
    balance = cur.fetchone()[0]
    cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (balance - cash * 1.03, message.chat.id,))

    cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
    balance = cur.fetchone()[0]
    cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (balance + cash, id,))
    data.commit()
    data.close()

def get_chat_id(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    name, surname = message[0], message[1]
    cur.execute("SELECT chatid FROM users where name = ? AND surname = ?", (name, surname,))
    id = cur.fetchone()[0]
    data.commit()
    data.close()
    return id

def getleaderboard():
    maxpositions = 10
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    cur_positions = cur.fetchone()[0]
    print(cur_positions)
    cur.execute("SELECT surname, name, balance FROM users WHERE isadmin = 0 ORDER BY balance DESC")
    if 0 < cur_positions <= maxpositions:
        ls = cur.fetchmany(cur_positions)
    elif cur_positions > maxpositions:
        ls = cur.fetchmany(maxpositions)
    else:
        leaderboard = 'В базе данных нет данных'
        return leaderboard
    leaderboard = ''
    try:
        if cur_positions == 1:
            leaderboard += '1. 🥇 ' + str(ls[0][0]) + ' ' + str(ls[0][1]) + ':   ' + str(ls[0][2]) + ' 💵 \n'
            return leaderboard
        elif cur_positions == 2:
            leaderboard += '1. 🥇 ' + str(ls[0][0]) + ' ' + str(ls[0][1]) + ':   ' + str(ls[0][2]) + ' 💵 \n'
            leaderboard += '2. 🥈 ' + str(ls[1][0]) + ' ' + str(ls[1][1]) + ':   ' + str(ls[1][2]) + ' 💵 \n'
            return leaderboard
        elif cur_positions >= 3:
            leaderboard += '1. 🥇 ' + str(ls[0][0]) + ' ' + str(ls[0][1]) + ':   ' + str(ls[0][2]) + ' 💵 \n'
            leaderboard += '2. 🥈 ' + str(ls[1][0]) + ' ' + str(ls[1][1]) + ':   ' + str(ls[1][2]) + ' 💵 \n'
            leaderboard += '3. 🥉 ' + str(ls[2][0]) + ' ' + str(ls[2][1]) + ':   ' + str(ls[2][2]) + ' 💵 \n'
            return leaderboard
        for i in range(3, maxpositions):
            leaderboard += str(i) +'. ' + str(ls[i][0]) + ' ' + str(ls[i][1]) + ':   ' + str(ls[i][2]) + ' 💵 \n'
    except IndexError:
        pass
    data.commit()
    data.close()
    return leaderboard
# data = sqlite3.connect('baseddata.db')
# cur = data.cursor()
# cur.execute("SELECT * FROM users")
# print(cur.fetchall())
# data.commit()
# data.close()