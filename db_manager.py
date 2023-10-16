import sqlite3

base_balance = 1000
lend_limit = 1000

def create(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        chatid integer,
        balance integer,
        lent_cash integer,
        winrate float
    )""")
    cur.execute("INSERT INTO users(chatid, balance, lent_cash, winrate) SELECT ?, ?, 0, 0 WHERE NOT EXISTS (SELECT chatid FROM users WHERE chatid = ?)" , (id, base_balance, id))
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    data.commit()
    data.close()

def get_info(message):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id
    info = list(cur.execute("SELECT * FROM users where chatid = ?", (id,)))[0]
    data.commit()
    data.close()
    return info

def lend(message, amount):
    data = sqlite3.connect('baseddata.db')
    cur = data.cursor()
    id = message.chat.id

    cur.execute("SELECT lent_cash FROM users WHERE chatid = ?", (id,))
    user_lent_cash = cur.fetchone()[0]
    cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
    user_balance = cur.fetchone()[0]
    if lend_limit >= user_lent_cash + amount:
        cur.execute("UPDATE users SET lent_cash = ? WHERE chatid = ?", (user_lent_cash + amount, id))
        cur.execute("UPDATE users SET balance = ? WHERE chatid = ?", (user_balance + amount, id))
        cur.execute("SELECT balance FROM users WHERE chatid = ?", (id,))
    else:
        raise ValueError
    data.commit()
    data.close()

