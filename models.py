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