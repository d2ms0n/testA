from enum import Enum

# Определяем enum для статуса автомобиля
class CarStatus(Enum):
    AVAILABLE = "Доступен"
    SOLD = "Продан"
    IN_REPAIR = "На ремонте"
    BOOKED = "Забронирован"

# Класс для пользователя
class User:
    def __init__(self, name, age, roles):
        self.name = name
        self.age = age
        self.roles = roles

    def display_info(self):
        print(f"Имя: {self.name}")
        print(f"Возраст: {self.age}")
        print("Роли:")
        for role in self.roles:
            print(f"- {role.name}")

# Класс для роли
class Role:
    def __init__(self, name):
        self.name = name

# Создаем конкретные роли
Manager = Role("Менеджер")
Customer = Role("Клиент")

# Функция для создания пользователя через консоль
def create_user():
    name = input("Введите имя: ")
    age = int(input("Введите возраст: "))
    role_names = input("Введите роли (через запятую): ").split(',')
    
    # Преобразуем строки в объекты ролей
    roles = []
    for role_name in role_names:
        role_name = role_name.strip().lower()
        if role_name == "менеджер":
            roles.append(Manager)
        elif role_name == "клиент":
            roles.append(Customer)
            
    return User(name, age, roles)

# Пример использования
if __name__ == "__main__":
    # Создаем пользователя через консоль
    print("Создание нового пользователя:")
    new_user = create_user()
    
    # Выводим информацию о пользователе
    print("\nИнформация о пользователе:")
    new_user.display_info()
    
    # Пример работы с enum
    print("\nДоступные статусы автомобиля:")
    for status in CarStatus:
        print(f"{status.name}: {status.value}")