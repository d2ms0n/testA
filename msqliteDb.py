# -*- coding: cp1251 -*-
import email
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
                UPDATE Users 
                SET name = ?, email = ?, age = ?
                WHERE id = ?
            """,
                (user.name, user.email, user.age, user.id),
            )
            self.connection.commit()
            print(f"Пользователь {user.name} успешно обновлен")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении пользователя: {e}")

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
            self.connection.commit()
            print(f"Пользователь с ID {user_id} удален")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пользователя: {e}")

    def all_user(self):

        self.cursor.execute("SELECT * FROM Users")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()