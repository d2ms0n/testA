from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from msqliteDb import *


@dataclass
class User:

    user_id: Optional[int] = None
    user_login: str =""
    user_password: str=""
    user_token: Optional[str] = None
    name: str = ""
    email: str = ""
    phone: str = ""
    role: Optional[str] = None


@dataclass
class Car:
    production_date: datetime
    warehouse_arrival_date: datetime
    car_id: Optional[int] = None
    car_number: str = ""
    model: str = ""
    status: str = ""
    description: str = ""
    manager: Optional[int] = None
    buyer: Optional[int] = None


class Comments:

    com_id: Optional[int] = None
    car_id: Optional[int] = None
    autor_id: Optional[int] = None
    autor_name: Optional[str] = ""
    coment_data: datetime
    text: str = ""


# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр базы данных
    db = Database("cars.db")

    time_now = datetime.now()
    new_car = Car(

        car_number = "qwe-123",
        model = "taz",
        production_date = datetime.strptime("22-05-2017 12:30", "%d-%m-%Y %H:%M"),
        warehouse_arrival_date = time_now.strftime("%Y-%m-%d %H:%M"),
        status = "На складе",
        description = "ghjgjh",
        manager = 1
        )

    #db.add_car(new_car)
car = Car(*db.get_car_by_id(1))
if car:
    print(f"Получен автомобиль: {car}")
    time_now = datetime.now()
    car.warehouse_arrival_date = time_now.strftime("%Y-%m-%d %H:%M")
    db.update_car(car)

    # # Создаем нового пользователя
    # new_user = User(

    #     user_login="123",
    #     user_password="123",
    #     name="n123",
    #     email="1@mail",
    #     phone="123456789",
    #     role="Администратор"
    #     )

    # # Добавляем пользователя в базу
    # db.add_user(new_user)

    # # Получаем пользователя по ID
    # user = User(*db.get_user_by_id(2))
    # if user:
    #    print(f"Получен пользователь: {user}")

    # # Обновляем данные пользователя
    # user.name = "q123"
    # db.update_user(user)

    # # Удаляем пользователя
    # db.delete_user(1)

    # print(db.all_user())

    # Закрываем соединение
db.close()



#  git remote add origin https://github.com/d2ms0n/testA.git
# git remote set-url origin https://github.com/d2ms0n/testA.git

# from enum import Enum
# from datetime import datetime
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from app import db

# # Определение ролей через Enum для лучшей типизации
# class Role(Enum):
#     ADMIN = "Администратор"
#     MANAGER = "Менеджер"
#     BUYER = "Покупатель"

# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     login = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(80), unique=True, nullable=False)
#     name = db.Column(db.String(80))
#     phone = db.Column(db.String(30))
#     role = db.Column(db.Enum(Role), nullable=True)
#     password_hash = db.Column(db.String(128))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def __repr__(self):
#         return f"<User {self.id}, {self.login}, {self.name}, {self.email}, {self.phone}, {self.role}>"

#     def set_password(self, password: str) -> None:
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password: str) -> bool:
#         return check_password_hash(self.password_hash, password)

#     def get_id(self) -> str:
#         return str(self.id)

#     @property
#     def is_admin(self) -> bool:
#         return self.role == Role.ADMIN

#     @property
#     def is_manager(self) -> bool:
#         return self.role == Role.MANAGER

#     @property
#     def is_buyer(self) -> bool:
#         return self.role == Role.BUYER
