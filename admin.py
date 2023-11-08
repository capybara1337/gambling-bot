from config import admins
from sys import maxsize

def check_privilege(chat_id):
    print(admins, chat_id)
    print(True if chat_id in admins else False)
    if chat_id in admins:
        return float(maxsize), 1
    else:
        return 1000.0, 0