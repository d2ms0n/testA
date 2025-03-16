from sqlite3 import IntegrityError
from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import Column, Text, CheckConstraint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_manager, login_required, login_user, logout_user, current_user
from models import User, Role, generate_password_hash, app, db
import external as e  # внешние функции









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
                    "login": form_data["login"],
                    "email": form_data["email"],
                    "name": form_data["name"],
                    "phone": form_data["phone"],
                    "password_hash": generate_password_hash(form_data["password"]),
                    "role":Role.BUYER
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

        user = User.query.filter_by(login=login).first()
        #print(user.id)
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