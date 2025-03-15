from sqlite3 import IntegrityError
from sqlalchemy import Column, Text, CheckConstraint
from sqlalchemy.orm import Session
import external as e  # внешние функции
from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_jwt_extended import (
#     JWTManager,
#     create_access_token,
#     jwt_required,
#     get_jwt_identity
# )


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


# Определение модели
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(80), unique=True, nullable=False)
    user_password = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    role = Column(
        Text,
        CheckConstraint("role IN ('Администратор', 'Менеджер', 'Покупатель')"),
        nullable=True,
    )
    password_hash = db.Column(db.String(128))
    
    def __repr__(self):
        return f"<User {self.user_id},{self.user_login},{self.name},{self.email},{self.phone},{self.role},>"

    # created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        print(self.user_password , password)
        return check_password_hash(self.user_password, password)
    
    def get_id(self):
        return str(self.user_id)

    # def __repr__(self):
    #     return f"<User {self.name}>"


# Создание базы данных (альтернативный способ для Flask 2.3.0)
with app.app_context():
    db.create_all()


# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


@app.route("/registry", methods=["GET", "POST"])
def registry():
    if request.method == "POST":
        if request.method == "POST":
            try:
                form_data = request.form

                # Валидация данных
                errors = e.validate_form_data(form_data)
                if errors:
                    flash("\n".join(errors), "error")
                    return render_template("registry.html")

                # Подготовка данных
                user_data = {
                    "user_login": form_data["login"],
                    "email": form_data["email"],
                    "name": form_data["name"],
                    "phone": form_data["phone"],
                    "user_password": generate_password_hash(form_data["password"]),
                }

                # Создание пользователя
                new_user = User(**user_data)
                db.session.add(new_user)
                db.session.commit()
                flash("Пользователь успешно создан", "success")
                return redirect(url_for("login"))
            except IntegrityError as ex:
               # Откат транзакции
                db.session.rollback()
    
                # Обработка ошибки
                print(f"Ошибка целостности: {str(ex)}")
                flash("Пользователь с таким логином или email уже существует", "error")
                return render_template("registry.html")

            except Exception as ex:
                db.session.rollback()
                print(f"Произошла ошибка при создании пользователя: {str(ex)}")
                flash(f"Произошла ошибка при создании пользователя", "error")
                return render_template("registry.html")
    return render_template("registry.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        flash("Вы уже авторизованны")
        return redirect(url_for("index"))

    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        user = User.query.filter_by(user_login=login).first()
        print(user.user_id)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Неверный email или пароль", "danger")

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 





# Главная
@app.route("/")
@app.route("/index")
@login_required
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

# вывод всех пользователей
@app.route("/alluser")
@login_required
def alluser():
    users = User.query.all()
    return render_template("alluser.html", users=users)


# Обновление (Update)
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":
        user.name = request.form["name"]
        user.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("update.html", user=user)


# Удаление (Delete)
# return redirect(request.referrer or url_for('default_route'))
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("delete.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)