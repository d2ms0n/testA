import re
from sqlite3 import IntegrityError
from models import User, Role, generate_password_hash, db


    # @classmethod
    # def authenticate(cls, login, password):
    #     try:
    #         user = cls.query.filter_by(login=login).first()
    #         if user and user.check_password(password):
    #             return user, None
    #         return None, "Неверный логин или пароль"
    #     except Exception as e:
    #         return None, f"Ошибка при аутентификации: {str(e)}"

    # @classmethod
    # def create(cls, form_data):
    #     errors = []
        
    #     # Валидация данных
    #     errors += cls._validate_login(form_data.get("login"))
    #     errors += cls._validate_email(form_data.get("email"))
    #     errors += cls._validate_name(form_data.get("name"))
    #     errors += cls._validate_phone(form_data.get("phone"))
    #     errors += cls._validate_password(form_data.get("password"))
        
    #     if errors:
    #         return False, errors

    #     user_data = {
    #         "login": form_data["login"],
    #         "email": form_data["email"],
    #         "name": form_data["name"],
    #         "phone": form_data["phone"],
    #         "password_hash": generate_password_hash(form_data["password"]),
    #         "role": Role.BUYER
    #     }
        
    #     try:
    #         new_user = cls(**user_data)
    #         db.session.add(new_user)
    #         db.session.commit()
    #         return new_user, None
    #     except Exception as ex:
    #         db.session.rollback()
    #         return None, str(ex)

    # @staticmethod
    # def _validate_login(login):
    #     errors = []
    #     if not login:
    #         errors.append("Логин не может быть пустым")
    #     elif len(login) < 4 or len(login) > 30:
    #         errors.append("Логин должен быть от 4 до 30 символов")
    #     elif not re.match(r'^[a-zA-Z0-9_]+$', login):
    #         errors.append("Логин может содержать только буквы, цифры и символ _")
    #     return errors

    # @staticmethod
    # def _validate_email(email):
    #     errors = []
    #     if not email:
    #         errors.append("Email не может быть пустым")
    #     elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}$', email):
    #         errors.append("Неверный формат email")
    #     return errors

    # @staticmethod
    # def _validate_name(name):
    #     errors = []
    #     if name and len(name) > 50:
    #         errors.append("Имя не может превышать 50 символов")
    #     return errors

    # @staticmethod
    # def _validate_phone(phone):
    #     errors = []
    #     if not re.match(r'^\+?[0-9() -]{7,15}$', phone):
    #         errors.append("Неверный формат телефона")
    #     return errors

    # @staticmethod
    # def _validate_password(password):
    #     errors = []
    #     if not password:
    #         errors.append("Пароль не может быть пустым")
    #     elif len(password) < 6:
    #         errors.append("Пароль должен содержать минимум 6 символов")
    #     return errors

    # def __repr__(self):
    #     return f"<User {self.id}, {self.login}, {self.name}, {self.email}, {self.phone}, {self.role}>"

    # def set_password(self, password:

