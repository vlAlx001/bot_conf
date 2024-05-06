import asyncio
import json

from bot_init import bot_key, load_user, bot_all_key, bot_dir


load_user = {
    'admin': 12,
    'analitic': [123, 235, 3465, 4576, 567, 333],
    'resp': [2134, 3465, 34576, 5678, 555, 4567]
}

B = 5552457

def get_reg(A: int) -> str | bool:
    if load_user['admin'] == A: return 'admin'
    if B in load_user['analitic']: return 'analitic'
    if B in load_user['resp']: return 'resp'
    return False

def set_reg(A: int, status):
    global load_user
    B = load_user[status]
    B.append(A)
    load_user[status] = B
    try:
        with open(f'user.json', 'w') as f:
            json.dump(load_user, f)
    except Exception as e:
        logging.error('Файл user.json был заблокмрован', exc_info=True)

C = get_reg(B)
print(C)

print(load_user)
set_reg(B, 'analitic')

print(load_user)

