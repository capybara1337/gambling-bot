import sqlite3
from admin import check_privilege
from sys import maxsize
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

def get_info(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    info = list(cur.execute("SELECT * FROM users where chatid = ?", (id,)))[0]
    print(info)
    data.commit()
    data.close()
    return info

def addnametodb(message, name):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    cur.execute("UPDATE users SET name = ? WHERE chatid = ?", (name, id))  
    data.commit()
    data.close()

def addsurnametodb(message, surname):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    cur.execute("UPDATE users SET surname = ? WHERE chatid = ?", (surname, id))  
    data.commit()
    data.close()
def getleaderboard():
    maxpositions = 8
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    cur.execute("SELECT surname, name FROM users WHERE isadmin = 0 ORDER BY balance DESC")
    ls = cur.fetchmany(maxpositions)
    leaderboard = ''
    try:
        leaderboard += '1. 🥇 ' + str(ls[0][1]) + '\n'
        leaderboard += '2. 🥈 ' + str(ls[1][1]) + '\n'
        leaderboard += '3. 🥉 ' + str(ls[2][1])+ '\n'
        count = 3
        for i in range(3, maxpositions):
            count+=1
            leaderboard += str(count) +'. ' + str(ls[i][1]) + '\n'
    except IndexError:
        pass
    return leaderboard
    data.commit()
    data.close()