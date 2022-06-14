#получаем список админов 2 способ, мой

from create_bot import conn, cur
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from create_bot import OWNER_ID, BOT_ID


def moderators():
    print('Админ следит за чатом!')
    cur = conn.cursor()
    cur.execute(f"SELECT user_id FROM users WHERE admin = 'True'")
    result = cur.fetchall()# получаем id пользователей с правом доступа из базы    
    conn.commit()    
    # создаём ADMINS_LIST и вносим сразу OWNER_ID и BOT_ID в список админов
    ADMINS_LIST = [OWNER_ID, BOT_ID]    
    for q in result:
       w = q[0] # здесь мы избавляемся от запятой        
       ADMINS_LIST.append(w)
    print(ADMINS_LIST)



def main():
    print(moderators())
    
if __name__ == '__main__':
    main() 
