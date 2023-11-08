from config import admins
from sys import maxsize

def check_privilege(chat_id):
    if str(chat_id) in admins:
        return float(maxsize), 1
    else:
        return 1000.0, 0