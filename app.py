from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from msqliteDb import *



@dataclass
class User:
        
        user_id: Optional[int] = None
        name: str ="" 
        email: str= ""
        phone: str=""
        role: Optional[int] = None

class Car:
        car_id: Optional[int] = None
        car_number: str= ""
        model: str = "" 
        production_date: datetime
        warehouse_arrival_date: datetime
        status: str=""
        description: str=""
        manager:Optional[int] = None
        buyer:Optional[int] = None



# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр базы данных
    db = Database('cars.db')
    
    # # Создаем нового пользователя
    # new_user = User(
    #     name="ИванПетров",
    #     age=35,
    #     email="ivan.petrov@example.com",
    # )
    
    # Добавляем пользователя в базу
    #db.add_user(new_user)
    
    # Получаем пользователя по ID
    #user = User(*db.get_user_by_id(2))
    #if user:
    #    print(f"Получен пользователь: {user.name}")
    
    # Обновляем данные пользователя
    #user.age = 26
    #db.update_user(user)
    
    # Удаляем пользователя
    #db.delete_user(1)

    #print(db.all_user())
    
    # Закрываем соединение
    db.close()



#
#

#  git remote add origin https://github.com/d2ms0n/testA.git
#git remote set-url origin https://github.com/d2ms0n/testA.git


