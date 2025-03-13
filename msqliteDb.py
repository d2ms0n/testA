# -*- coding: cp1251 -*-
import sqlite3
from queries import *


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        try:
            self.cursor.execute(create_table_Users_sql)
            self.connection.commit()
            self.cursor.execute(create_table_Car_sql)
            self.connection.commit()
            self.cursor.execute(create_table_Comments_sql)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблиц: {e}")

#User metod db
#region User metod db
    def add_user(self, user):
        try:
            self.cursor.execute(
                """
                INSERT INTO Users (user_login, user_password, user_token, name, email, phone, role)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (user.user_login, user.user_password, user.user_token, user.name, user.email, user.phone, user.role),
            )
            self.connection.commit()
            print(f"Пользователь {user.name} успешно добавлен")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении пользователя: {e}")

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        user_data = self.cursor.fetchone()

        if user_data:
            return user_data
        return None

    def update_user(self, user):
        try:
            self.cursor.execute(
                """
                 UPDATE users
                SET 
                    user_login = ?,
                    user_password = ?,
                    user_token = ?,
                    name = ?,
                    email = ?,
                    phone = ?,
                    role = ?
                WHERE user_id = ?;
            """,
                (user.user_login, user.user_password, user.user_token, user.name, user.email, user.phone, user.role, user.user_id),
            )
            self.connection.commit()
            print(f"Пользователь {user.name} успешно обновлен")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении пользователя: {e}")

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            self.connection.commit()
            print(f"Пользователь с ID {user_id} удален")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пользователя: {e}")

    def all_user(self):

        self.cursor.execute("SELECT * FROM Users")
        return self.cursor.fetchall()

#endregion

#Car metod db
#region Car metod db
    def add_car(self, car):
        try:
            self.cursor.execute(
                """
                INSERT INTO Car (car_number, model, production_date, warehouse_arrival_date, status, description, manager, buyer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (car.car_number, car.model, car.production_date, car.warehouse_arrival_date, car.status, car.description, car.manager, car.buyer),
            )
            self.connection.commit()
            print(f"Автомобиль {car.model} успешно добавлен")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении Автомобиля: {e}")

    def get_car_by_id(self, car_id):
        self.cursor.execute("SELECT production_date, warehouse_arrival_date, car_id, car_number, model, status, description, manager, buyer FROM Car WHERE car_id = ?", (car_id,))
        car_data = self.cursor.fetchone()
        if car_data:
            return car_data
        return None

    def update_car(self, car):
        try:
            self.cursor.execute(
                """
                 UPDATE Car
                SET 
                    production_date = ?,
                    warehouse_arrival_date = ?,
                    car_number = ?,
                    model = ?,
                    status = ?,
                    description = ?,
                    manager = ?,
                    buyer = ?
                WHERE car_id = ?;
            """,
                (car.production_date, car.warehouse_arrival_date, car.car_number, car.model, car.status, car.description, car.manager, car.buyer, car.car_id ),
            )
            self.connection.commit()
            print(f"Автомобиль {car.model} успешно обновлен")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении пользователя: {e}")

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            self.connection.commit()
            print(f"Пользователь с ID {user_id} удален")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пользователя: {e}")

    def all_user(self):

        self.cursor.execute("SELECT * FROM Users")
        return self.cursor.fetchall()

#endregion









    def close(self):
        self.connection.close()