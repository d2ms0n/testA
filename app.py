from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc
from models import Cars, Comment, Status, Role, User, app, db, find_and_add_comment
from jinja2 import Environment, FileSystemLoader








# Главная страница
@app.route("/")
@app.route("/index")
@login_required
def index():
	
	cars = db.session.query(Cars).order_by(desc(Cars.id)).limit(3).all()
	cars_and_comment= (find_and_add_comment(cars))
	return render_template("index.html", cars_and_comment=cars_and_comment)


#User endpoint
#region User 

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
			return redirect(url_for("index"))

	
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
@app.route("/user_update/<int:id>", methods=["GET", "POST"])
@login_required
def user_update(id):

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
			return redirect(url_for("user_update", id=id))
		elif user:
			
			flash(f"Данные пользователя {user.login} обновлены")
			return redirect(url_for("alluser"))
		else:
			flash("Пользователь не найден", "danger")

	user = User.query.get_or_404(id)
	roles = Role.choices()  # список всех доступных ролей
	return render_template('user_update.html', user=user, roles=roles)




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
@app.route("/user_delete/<int:id>", methods=["POST"])
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

#endregion


#Cars endpoint
#region Cars


# если метод GET отправляет форму
# Если POST проверяет данные и создает нового 
@app.route("/add_car", methods=["GET", "POST"])
@login_required
def add_car():

	if not (current_user.is_admin or current_user.is_manager):
		flash(f"У вас нет доступа к этой странице", "danger")
		return redirect(url_for("index"))

	status = Status.choices() 
	managers, buers = User.get_managers_and_buers()

	if request.method == "POST":

		form_data = request.form	
		cars, errors = Cars.create(form_data)	
		if errors:
			for error in errors:
				flash(error)            
			return render_template("add_car.html", form_data=form_data, status=status, managers=managers, buers=buers )            
		else:
			flash("Автомобиль успешно создан", "success")
			return redirect(url_for("all_cars"))


	return render_template("add_car.html", form_data="", status=status, managers=managers, buers=buers )



# Редактирование пользователя
@app.route("/update_car/<int:id>", methods=["GET", "POST"])
@login_required
def update_car(id):

	if not (current_user.is_admin or current_user.is_manager):
		flash(f"У вас нет доступа к этой странице", "danger")
		return redirect(url_for("index"))

	status = Status.choices() 
	managers, buers = User.get_managers_and_buers()

	if request.method == "POST":

		form_data = request.form
		car, error = Cars.update(form_data)

		if error:
			flash(f"Ошибка: {error}", "danger")
			return render_template('update_car.html', form_data=form_data , status=status, managers=managers, buers=buers)
		elif car:			
			flash(f"Данные автомобиля {car.model} обновлены")
			return redirect(url_for("all_cars"))
		else:
			flash("Автомобиль не найден", "danger")
			return redirect(url_for("all_cars"))

	form_data = Cars.query.get_or_404(id)
	return render_template('update_car.html', form_data=form_data , status=status, managers=managers, buers=buers)


# вывод всех автомобилей
@app.route("/all_cars")
@login_required
def all_cars():

	if not (current_user.is_admin or current_user.is_manager):
		flash(f"У вас нет доступа к этой странице", "danger")
		return redirect(url_for("index"))

	cars = Cars.query.all()
	return render_template("all_cars.html", cars=cars)



# Удаление (Delete)
@app.route("/car_delete/<int:id>", methods=["POST"])
@login_required
def car_delete(id):

	if not current_user.is_admin:
		flash(f"У вас нет доступа к этой странице", "danger")
		return redirect(url_for("index"))

	car = Cars.query.get_or_404(id)

	if car and request.method == "POST":
		db.session.delete(car)
		db.session.commit()
		flash(f"Автомобиль {car.model} удален")
		return redirect(url_for("all_cars"))

	flash(f"Произошла ошибка")
	return redirect(request.referrer or url_for('all_cars'))


#endregion


#Comment endpoint
#region Comment

@app.route("/add_comment", methods=["POST"])
@login_required
def add_comment():
	
	form_data = request.form	
	comment, errors = Comment.create(form_data)	
	if errors:
		for error in errors:
			flash(error)              
	else:
		flash("Комментарий успешно создан", "success")
		
	return redirect(request.referrer or url_for('index'))


	

#endregion



@app.route("/mycars", methods=["GET"])
@login_required
def mycars():

	cars = Cars.get_car_from_buyerid(current_user.id)
	if cars:
		cars_and_comment = find_and_add_comment(cars)
		return render_template("index.html", cars_and_comment=cars_and_comment)
	else:
		flash("У вас нет купленных автомобилей")
		return redirect(url_for("index"))






if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run(debug=True)