import re
from enum import Enum
from flask import Flask
from flask_login import LoginManager, UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash



# Инициализация приложения
app = Flask(__name__, template_folder="html")
app.secret_key = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста, войдите в систему"
login_manager.login_message_category = "info"

with app.app_context():
    db.create_all()

# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


class Role(Enum):
    ADMIN = "Администратор"
    MANAGER = "Менеджер"
    BUYER = "Покупатель"

    @classmethod
    def choices(cls):
        return [(role.name, role.value) for role in cls]

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(30))
    role = db.Column(db.Enum(Role), nullable=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def authenticate(cls, login, password):
        try:
            user = cls.query.filter_by(login=login).first()
            if user and user.check_password(password):
                return user, None
            return None, "Неверный логин или пароль"
        except Exception as e:
            return None, f"Ошибка при аутентификации: {str(e)}"

    @classmethod
    def create(cls, form_data):     
            
        errors = []
    
        # Валидация логина
        if not form_data["login"]:
            errors.append("Логин не может быть пустым")
        elif len(form_data["login"]) < 4 or len(form_data["login"]) > 30:
            errors.append("Логин должен быть от 4 до 20 символов")
        elif not re.match(r'^[a-zA-Z0-9_]+$', form_data["login"]):
            errors.append("Логин может содержать только буквы, цифры и символ _")
    
        # Валидация email
        if not form_data["email"]:
            errors.append("Email не может быть пустым")
        elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}$', form_data["email"]):
            errors.append("Неверный формат email")
    
        # Валидация имени
        if len(form_data["name"]) > 50:
            errors.append("Имя не может превышать 50 символов")
    
        # Валидация телефона
        if not re.match(r'^\+?[0-9() -]{7,15}$', form_data["phone"]):
            errors.append("Неверный формат телефона")
    
        # Валидация пароля
        if len(form_data["password"]) < 6:
            errors.append("Пароль должен содержать минимум 6 символов")
    
        # Если есть ошибки, возвращаем их
        if errors:
                return False, errors

        user_data = {
            "login": form_data["login"],
            "email": form_data["email"],
            "name": form_data["name"],
            "phone": form_data["phone"],
            "password_hash": generate_password_hash(form_data["password"]),
            "role": Role.BUYER
        }
        try:
            # Создание пользователя
            new_user = cls(**user_data)
            db.session.add(new_user)
            db.session.commit()
            return new_user, None
        except Exception as ex:
            db.session.rollback()
            return None, str(ex)
    
    def __repr__(self):
        return f"<User {self.id}, {self.login}, {self.name}, {self.email}, {self.phone}, {self.role}>"

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        return str(self.id)

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    @property
    def is_manager(self) -> bool:
        return self.role == Role.MANAGER

    @property
    def is_buyer(self) -> bool:
        return self.role == Role.BUYER