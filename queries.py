# -*- coding: cp1251 -*-


create_table_Users_sql = """
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                role INTEGER
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

