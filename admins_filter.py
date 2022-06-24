#получаем список админов 2 способ, мой

from create import conn, cur, OWNER_ID, BOT_ID

# добавляем в список по умолчанию владельца и бота
DEFAULT_LIST = [OWNER_ID, BOT_ID] 
ADMINS_LIST = [] 
def moderators():
# удаляем старый список админов
    ADMINS_LIST.clear()
# добавляем в список ADMINS_LIST список DEFAULT_LIST  
    ADMINS_LIST.extend(DEFAULT_LIST)
    cur = conn.cursor()
    cur.execute(f"SELECT user_id FROM users WHERE admin = 'True'")
    result = cur.fetchall()# получаем id пользователей с правом доступа из базы    
    conn.commit()    
    # создаём ADMINS_LIST и вносим сразу OWNER_ID и BOT_ID в список админов       
    for q in result:
       w = q[0] # здесь мы избавляемся от запятой        
       ADMINS_LIST.append(w)
   




    

