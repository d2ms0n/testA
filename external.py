import re
from sqlite3 import IntegrityError
from models import User, Role, generate_password_hash, db


def validate_form_data(form_data):
    errors = []
    
    if not form_data['login']:
        errors.append('Логин не может быть пустым')
        
    if not form_data['email'] or not re.match(r'[^@]+@[^@]+\.[^@]+', form_data['email']):
        errors.append('Некорректный email')
        
    if not form_data['password'] or len(form_data['password']) < 6:
        errors.append('Пароль должен быть минимум 6 символов')
        
    return errors


# Функция для создания пользователя
def create_user(form_data):
    try:
        # Подготовка данных
        user_data = {
            "login": form_data["login"],
            "email": form_data["email"],
            "name": form_data["name"],
            "phone": form_data["phone"],
            "password_hash": generate_password_hash(form_data["password"]),
            "role": Role.BUYER
        }

        # Создание пользователя
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return True, None
    
    except IntegrityError as ex:
        db.session.rollback()
        return False, "Пользователь с таким логином или email уже существует"
    
    except Exception as ex:
        db.session.rollback()
        return False, f"Произошла ошибка при создании пользователя: {str(ex)}"





# Функция для аутентификации пользователя
def authenticate_user(login, password):
    user = User.query.filter_by(login=login).first()
    if user and user.check_password(password):
        return user
    return None


