# data_classes.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    age: Optional[int] = None
    
    def __post_init__(self):
        # Простая валидация данных
        if self.email and not self.is_valid_email(self.email):
            raise ValueError("Неверный формат email")
        
        if self.age and not (18 <= self.age <= 100):
            raise ValueError("Возраст должен быть от 18 до 100 лет")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        # Простая проверка email
        return "@" in email and len(email) > 5

    def __str__(self):
        return f"Пользователь: {self.username}\nEmail: {self.email}\nВозраст: {self.age}"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__dict__:
                setattr(self, key, value)

# Пример использования
if __name__ == "__main__":
    # Создание нового пользователя
    new_user = User(
        username="ИванПетров",
        email="ivan.petrov@example.com",
        age=25
    )
    
    print(new_user)
    
    # Обновление данных
    new_user.update(email="new.email@example.com", age=26)
    print(new_user)
    
    # Попытка создать пользователя с некорректными данными
    try:
        invalid_user = User(
            username="Invalid",
            email="wrong_email",
            age=15
        )
    except ValueError as e:
        print(f"Ошибка создания пользователя: {e}")