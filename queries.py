# -*- coding: cp1251 -*-


create_table_Users_sql = """
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                user_login TEXT NOT NULL,
                user_password TEXT NOT NULL,
                user_token TEXT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                role TEXT CHECK(role IN ('Администратор', 'Менеджер', 'Покупатель')) NOT NULL
            )
"""

create_table_Car_sql = """

CREATE TABLE IF NOT EXISTS Car (
 car_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор
 car_number TEXT UNIQUE, -- Номер автомобиля
 model TEXT NOT NULL, -- Модель автомобиля
 production_date DATE NOT NULL, -- Дата производства
 warehouse_arrival_date DATE NOT NULL, -- Дата поступления на склад
 status TEXT CHECK(status IN ('Транспортируется на склад', 'На складе', 'Продано')) NOT NULL, -- Статус
 description TEXT, -- Описание
 manager INTEGER, -- Ответственный менеджер
 buyer INTEGER -- Покупатель
);

"""

create_table_Comments_sql = """
            CREATE TABLE IF NOT EXISTS Comments (
                com_id INTEGER PRIMARY KEY,
                car_id INTEGER NOT NULL,
                autor_id INTEGER,
                autor_name TEXT,
                coment_data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                text TEXT NOT NULL
            )
"""