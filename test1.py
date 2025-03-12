from dataclasses import dataclass
import sqlite3
from test2 import Optional

#3546365
@dataclass
class User:
        
        id: Optional[int] = None
        name: str ="" 
        email: str= ""
        age: Optional[int] = None

    


# Создаем класс для работы с базой данных
class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            )
        ''')
        self.connection.commit()
    
    def add_user(self, user):
        try:
            self.cursor.execute('''
                INSERT INTO Users (name, email, age)
                VALUES (?, ?, ?)
            ''', (user.name, user.email, user.age))
            self.connection.commit()
            print(f"Пользователь {user.name} успешно добавлен")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении пользователя: {e}")
    
    def get_user_by_id(self, user_id):
        self.cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
        user_data = self.cursor.fetchone()

        print(user_data[1])


        if user_data:
            return User(*user_data)
        return None
    
    def update_user(self, user):
        try:
            self.cursor.execute('''
                UPDATE Users 
                SET name = ?, email = ?, age = ?
                WHERE id = ?
            ''', (user.name, user.email, user.age, user.id))
            self.connection.commit()
            print(f"Пользователь {user.name} успешно обновлен")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении пользователя: {e}")
    
    def delete_user(self, user_id):
        try:
            self.cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
            self.connection.commit()
            print(f"Пользователь с ID {user_id} удален")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пользователя: {e}")

    def all_user(self):

        self.cursor.execute('SELECT * FROM Users')
        users = self.cursor.fetchall()

        for user in users:
            print(user)


    def close(self):
        self.connection.close()

# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр базы данных
    db = Database('users.db')
    
    # Создаем нового пользователя
    new_user = User(
        name="ИванПетров",
        age=35,
        email="ivan.petrov@example.com",
    )
    
    # Добавляем пользователя в базу
    db.add_user(new_user)
    
    # Получаем пользователя по ID
    user = db.get_user_by_id(2)
    if user:
        print(f"Получен пользователь: {user.name}")
    
    # Обновляем данные пользователя
    user.age = 26
    db.update_user(user)
    
    # Удаляем пользователя
    db.delete_user(1)

    db.all_user()
    
    # Закрываем соединение
    db.close()



#
#

#  git remote add origin https://github.com/d2ms0n/testA.git
#git remote set-url origin https://github.com/d2ms0n/testA.git


