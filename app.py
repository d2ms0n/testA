from sqlite3 import IntegrityError
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user, current_user
from models import User, Role, generate_password_hash, app, db
import external as e  # внешние функции








# Главная страница
@app.route("/")
@app.route("/index")
@login_required
def index():
    
    return render_template("index.html")




# если метод GET отправляет форму
# Если POST проверяет данные и создает нового пользователя с ролью по умолчанию Покупатель
@app.route("/registry", methods=["GET", "POST"])
def registry():

    roles = Role.choices() 

    if request.method == "POST":
        form_data = request.form
        
        # Создание пользователя
        user, errors = User.create(form_data)
        
        if errors:
            for error in errors:
               flash(error)            
            return render_template("registry.html", form_data=form_data, roles=roles )            
        else:
            flash("Пользователь успешно создан", "success")
            return redirect(url_for("login"))

    
    return render_template("registry.html", form_data="", roles=roles)




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



# Редактирование пользователя
@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):

    if not current_user.is_admin:
        flash(f"У вас нет доступа к этой странице", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        form_data = {}
        for key in request.form:
            form_data[key] = request.form.get(key)
        print(f"form{form_data}")
        user, error = User.update(form_data)


        if error:
            flash(f"Ошибка: {error}", "danger")
            return redirect(url_for("update", id=id))
        elif user:
            
            flash(f"Данные пользователя {user.login} обновлены")
            return redirect(url_for("alluser"))
        else:
            flash("Пользователь не найден", "danger")

    user = User.query.get_or_404(id)
    roles = Role.choices()  # список всех доступных ролей
    return render_template('update.html', user=user, roles=roles)




# вывод всех пользователей
@app.route("/alluser")
@login_required
def alluser():

    if not current_user.is_admin:
        flash(f"У вас нет доступа к этой странице", "danger")
        return redirect(url_for("index"))

    users = User.query.all()
    return render_template("alluser.html", users=users)



  


# Удаление (Delete)
# return redirect(request.referrer or url_for('default_route'))
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    if not current_user.is_admin:
        flash(f"У вас нет доступа к этой странице", "danger")
        return redirect(url_for("index"))

    user = User.query.get_or_404(id)

    if user and request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        flash(f"Пользователь {user.login} удален")
        return redirect(url_for("alluser"))

    flash(f"Произошла ошибка")
    return redirect(request.referrer or url_for('alluser'))


if __name__ == "__main__":
    app.run(debug=True)