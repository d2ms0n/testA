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
                role TEXT CHECK(role IN ('�������������', '��������', '����������')) NOT NULL
            )
"""

create_table_Car_sql = """

CREATE TABLE IF NOT EXISTS Car (
 car_id INTEGER PRIMARY KEY AUTOINCREMENT, -- ���������� �������������
 car_number TEXT UNIQUE, -- ����� ����������
 model TEXT NOT NULL, -- ������ ����������
 production_date DATE NOT NULL, -- ���� ������������
 warehouse_arrival_date DATE NOT NULL, -- ���� ����������� �� �����
 status TEXT CHECK(status IN ('���������������� �� �����', '�� ������', '�������')) NOT NULL, -- ������
 description TEXT, -- ��������
 manager INTEGER, -- ������������� ��������
 buyer INTEGER -- ����������
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