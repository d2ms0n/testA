from sqlite3 import IntegrityError
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user, current_user
from models import User, Role, generate_password_hash, app, db
import external as e  # внешние функции








# если метод GET отправляет форму
# Если POST проверяет данные и создает нового пользователя с ролью по умолчанию Покупатель
@app.route("/registry", methods=["GET", "POST"])
def registry():
    if request.method == "POST":
        form_data = request.form
        
        # Создание пользователя
        user, errors = User.create(form_data)
        
        if errors:
            for error in errors:
               flash(error)            
            return render_template("registry.html")            
        else:
            flash("Пользователь успешно создан", "success")
            return redirect(url_for("login"))

    return render_template("registry.html")




# если метод GET отправляет форму
# Если POST проверяет данные  и меня статус текущего пользователя на Залогинен
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Вы уже авторизованы")
        return redirect(url_for("index"))

    if request.method == "POST":

        login = request.form.get("login")
        password = request.form.get("password")

        user, error = User.authenticate(login, password)

        if error:
            flash(f"Ошибка: {error}", "danger")
            return render_template("login.html")
        elif user:
            session.pop('_flashes', None)
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Пользователь не найден", "danger")
            
    return render_template("login.html")


#Пользователь разлогинен
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 





# Главная страница
@app.route("/")
@app.route("/index")
@login_required
def index():
    
    return render_template("index.html")




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
        return redirect(url_for("alluser"))

    roles = Role.choices()  # список всех доступных ролей
    print(roles)
    return render_template('update.html', user=user, roles=roles)

  


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