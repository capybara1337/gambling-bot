from config import admins
from sys import maxsize

def check_privilege(chat_id):
    if str(chat_id) in admins:
        print('lf')
        return maxsize, 1
    else:
        return 600, 0