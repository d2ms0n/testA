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

