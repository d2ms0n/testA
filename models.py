import re
from enum import Enum
from flask import Flask, flash
from flask_login import LoginManager, UserMixin
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
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



# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Role(Enum):
	BUYER = "Покупатель"
	MANAGER = "Менеджер"
	ADMIN = "Администратор"

	@classmethod
	def choices(cls):
		return [(role.name, role.value) for role in cls]


class Status(Enum):

	ZAKAZ = "Под заказ"
	TOWRH = "Транспортируется на склад"
	SALE = "Продается"
	SOLD = "Продано"

	@classmethod
	def choices(cls):
		return [(status.name, status.value) for status in cls]




class User(UserMixin, db.Model):
	__tablename__ = "users"

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

		# Валидация данных
		errors += cls._validate_login(form_data.get("login"))
		errors += cls._validate_email(form_data.get("email"))
		errors += cls._validate_name(form_data.get("name"))
		errors += cls._validate_phone(form_data.get("phone"))
		errors += cls._validate_password(form_data.get("password"))

		if errors:
			return False, errors

		user_data = {
			"login": form_data["login"],
			"email": form_data["email"],
			"name": form_data["name"],
			"phone": form_data["phone"],
			"password_hash": generate_password_hash(form_data["password"]),
			"role": Role.BUYER,
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

	@classmethod
	def update(cls, form_data):

		errors = []

		# Валидация данных
		errors += cls._validate_id(form_data.get("id"))
		errors += cls._validate_login(form_data.get("login"))
		errors += cls._validate_email(form_data.get("email"))
		errors += cls._validate_name(form_data.get("name"))
		errors += cls._validate_phone(form_data.get("phone"))
		errors += cls._validate_role(form_data.get("role"))

		if errors:
			return False, errors

		user_data = {
			"id": form_data["id"],
			"login": form_data["login"],
			"email": form_data["email"],
			"name": form_data["name"],
			"phone": form_data["phone"],
			"role": form_data["role"]
		}

		if form_data.get("password"):
			user_data["password_hash"] = generate_password_hash(form_data["password"])

		try:
			# Обновление пользователя
			user = cls.query.get(
				form_data["id"]
			)  # Предполагаем, что есть ID пользователя
			for key, value in user_data.items():
				setattr(user, key, value)
			db.session.commit()
			return user, None
		except Exception as ex:
			db.session.rollback()
			return None, str(ex)


	@classmethod
	def get_admins_and_managers(cls):
		users = cls.query.filter(cls.role.in_([Role.ADMIN, Role.MANAGER])).all()
		return users


	@staticmethod
	def _validate_id(id_value):
		errors = []
		if not id_value:
			errors.append("Внутреняя ошибка 1")
		elif not isinstance(id_value, int) and not id_value.isdigit():
			errors.append("Внутреняя ошибка 2")
		elif int(id_value) <= 0:
			errors.append("Внутреняя ошибка 3")
		return errors

	@staticmethod
	def _validate_login(login):
		errors = []
		if not login:
			errors.append("Логин не может быть пустым")
		elif len(login) < 4 or len(login) > 30:
			errors.append("Логин должен быть от 4 до 30 символов")
		elif not re.match(r"^[a-zA-Z0-9_]+$", login):
			errors.append("Логин может содержать только буквы, цифры и символ _")
		return errors

	@staticmethod
	def _validate_email(email):
		errors = []
		if not email:
			errors.append("Email не может быть пустым")
		elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}$", email):
			errors.append("Неверный формат email")
		return errors

	@staticmethod
	def _validate_name(name):
		errors = []
		if name and len(name) > 50:
			errors.append("Имя не может превышать 50 символов")
		return errors

	@staticmethod
	def _validate_phone(phone):
		errors = []
		if not re.match(r"^\+?[0-9() -]{7,15}$", phone):
			errors.append("Неверный формат телефона")
		return errors

	@staticmethod
	def _validate_password(password):
		errors = []
		if not password:
			errors.append("Пароль не может быть пустым")
		elif len(password) < 4:
			errors.append("Пароль должен содержать минимум 4 символа")
		return errors

	@staticmethod
	def _validate_role(role):
		errors = []
		# Проверяем, что роль является допустимым значением из перечисления Role
		if role not in [role.name for role in Role]:

			errors.append("Некорректная роль пользователя")
		return errors

	def __repr__(self):
		return f"<User {self.id}, {self.login}, {self.name}, {self.email}, {self.phone}, {self.role}>"

	def set_password(self, password: str) -> None:
		self.password_hash = generate_password_hash(password)

	def check_password(self, password: str) -> bool:
		return check_password_hash(self.password_hash, password)

	def get_id(self) -> str:
		return str(self.id)

	# Запрос для получения всех менеджеров и администраторов
	@staticmethod
	def get_managers_and_buers():
		managers = []
		buers = []
		users = User.query.all()
		for user in users:
			if user.role == Role.ADMIN or user.role == Role.MANAGER:
				managers.append({'id': user.id, 'name': user.name})
			elif user.role == Role.BUYER:
				buers.append({'id': user.id, 'name': user.name})				
		return managers, buers

	@property
	def is_admin(self) -> bool:
		return self.role == Role.ADMIN

	@property
	def is_manager(self) -> bool:
		return self.role == Role.MANAGER

	@property
	def is_buyer(self) -> bool:
		return self.role == Role.BUYER


class Cars(db.Model):
	__tablename__ = "cars"

	id = db.Column(db.Integer, primary_key=True)
	car_number = db.Column(db.String(30), unique=True, nullable=False)
	model = db.Column(db.String(50), nullable=False)
	production_date = db.Column(db.Date, nullable=False)
	warehouse_date = db.Column(db.Date, nullable=True)
	data_sale = db.Column(db.Date, nullable=True)
	status = db.Column(db.Enum(Status), nullable=False)
	description = db.Column(db.Text)
	manager_id = db.Column(db.Integer, nullable=True)
	manager_name = db.Column(db.String(50), nullable=True)
	buyer_id = db.Column(db.Integer, nullable=True)
	buyer_name = db.Column(db.String(50), nullable=True)


# Добавление автомобиля
	@classmethod
	def create(cls, form_data):

		errors = []
		errors += cls._validate_car_number(form_data.get("car_number"))
		errors += cls._validate_model(form_data.get("model"))
		errors += cls._validate_production_date(form_data.get("production_date"))
		errors += cls._validate_warehouse_date(form_data.get("warehouse_date"))
		errors += cls._validate_status(form_data.get("status"))

		if errors:
			return False, errors


		# Создание нового объекта
		manager_name = get_user_name(form_data.get("manager_id"))
		buyer_name = get_user_name(form_data.get("buyer_id"))

		data_car = {
			"car_number": form_data["car_number"],
			"model": form_data["model"],
			"production_date": str_to_datetime(form_data["production_date"]),
			"warehouse_date": str_to_datetime(form_data["warehouse_date"]),
			"status": form_data["status"],
			"description": form_data["description"],
			"manager_id": form_data["manager_id"],
			"manager_name":manager_name,
			"buyer_id": form_data["buyer_id"],
			"buyer_name":buyer_name
		}

		# Добавление в сессию и сохранение
		try:
			new_car = cls(**data_car)
			db.session.add(new_car)
			db.session.commit()
			return new_car, None

		except Exception as ex:
			db.session.rollback()
			return None, str(ex)


	

# Обновление автомобиля
	@classmethod  
	def update(cls, form_data):

		data_sale = None
		errors = []
		errors += cls._validate_car_number(form_data.get("car_number"))
		errors += cls._validate_model(form_data.get("model"))
		errors += cls._validate_production_date(form_data.get("production_date"))
		errors += cls._validate_warehouse_date(form_data.get("warehouse_date"))
		errors += cls._validate_status(form_data.get("status"))

		if errors:
			return False, errors


		manager_name = get_user_name(form_data.get("manager_id"))
		buyer_name = get_user_name(form_data.get("buyer_id"))


		if form_data.get("status") == "SOLD":

			format_time = datetime.now().strftime("%Y-%m-%d") 
			admins = User.get_admins_and_managers()
			for admin in admins:
				msg_data = {
					"user_id":admin.id,
					"text": f"Продан автомобиль {form_data["model"]}, номер {form_data["car_number"]},покупатель {buyer_name}, дата продажи {format_time}"					
					}

				Message.create(msg_data)
			data_sale = datetime.now()

			

		data_car = {
			"car_number": form_data["car_number"],
			"model": form_data["model"],
			"production_date": str_to_datetime(form_data["production_date"]),
			"warehouse_date": str_to_datetime(form_data["warehouse_date"]),
			"data_sale":data_sale,
			"status": form_data["status"],
			"description": form_data["description"],
			"manager_id": form_data["manager_id"],
			"manager_name":manager_name,
			"buyer_id": form_data["buyer_id"],
			"buyer_name":buyer_name
		}

		try:
			
			car = cls.query.get(form_data["id"]) 

			for key, value in data_car.items():
				setattr(car, key, value)
			db.session.commit()
			return car, None
		except Exception as ex:
			db.session.rollback()
			return None, str(ex)


#получить список автомобилей покупателя по его ид
	@classmethod 
	def get_car_from_buyerid(cls, buyer_id):
		return cls.query.filter_by(buyer_id=buyer_id).all()

#Статистика авто
#Количество проданных автомобилей
	@classmethod
	def get_sold_cars_count(cls):
		return cls.query.filter_by(status=Status.SOLD.name).count()

#Среднее время продажи автомобиля
	@classmethod
	def get_average_sale_time(cls):
		
		sold_cars = cls.query.filter(
			cls.status == Status.SOLD,
			cls.warehouse_date != None,
			cls.data_sale != None
		).all()

		if not sold_cars:
			return None

		total_days = 0
		for car in sold_cars:
			total_days += (car.data_sale - car.warehouse_date).days

		average_days = total_days / len(sold_cars)
		return round(average_days) 


#Статистика по моделям автомобилей
	@classmethod
	def get_model_statistics(cls):
	
		# Получаем базовую статистику
		result = db.session.query(
			cls.model,
			db.func.count(cls.id).label('total'),
			db.func.sum(db.case((cls.status == Status.SALE.name, 1), else_=0)).label('sale'),
			db.func.sum(db.case((cls.status == Status.ZAKAZ.name, 1), else_=0)).label('zakaz'),
			db.func.sum(db.case((cls.status == Status.TOWRH.name, 1), else_=0)).label('towrh'),
			db.func.sum(db.case((cls.status == Status.SOLD.name, 1), else_=0)).label('sold')
		).group_by(cls.model).all()

		# Форматируем результат
		stats = {
			row.model: {
				"total": row.total,
				"sale": row.sale,
				"zakaz": row.zakaz,
				"towrh": row.towrh,
				"sold": row.sold
			}
			for row in result
		}
		return stats




#Полная статистика
	@classmethod
	def get_full_statistics(cls):
		
		return {
			"sold_cars_count": cls.get_sold_cars_count(),
			"average_sale_time": cls.get_average_sale_time(),
			"model_statistics": cls.get_model_statistics()
		}


#Валидация полученных данных
	@staticmethod
	def _validate_car_number(car_number):
		errors = []
		if not car_number:
			errors.append("Номер автомобиля обязателен")
		if len(car_number) > 30:
			errors.append("Номер автомобиля не может превышать 30 символовн")
		return errors

	@staticmethod
	def _validate_model(model):
		errors = []
		if not model:
			errors.append("Модель автомобиля обязательна")
		if len(model) > 50:
			errors.append("Модель не может превышать 50 символов")
		return errors

	@staticmethod
	def _validate_production_date(production_date):
		errors = []

		if str_to_datetime(production_date) > date.today():
			errors.append("Дата производства не может быть в будущем")
		return errors

	@staticmethod
	def _validate_warehouse_date(warehouse_date):
		errors = []

		if warehouse_date == "":
			return errors

		if str_to_datetime(warehouse_date) > date.today():
			errors.append("Дата поступления на склад не может быть в будущем")
		return errors

	@staticmethod
	def _validate_status(status):
		errors = []

		if status not in [status.name for status in Status]:
			errors.append("Неверно указан статус автомобиля")
		return errors


	def __repr__(self):
		return (
			f"<Cars(id={self.id}, car_number='{self.car_number}', model='{self.model}', "
			f"production_date={self.production_date}, warehouse_date={self.warehouse_date}, "
			f"status={self.status}, description='{self.description}', "
			f"manager_id={self.manager_id}, buyer_id={self.buyer_id})>"
		)



class Comment(db.Model):
	__tablename__ = "comment"

	id = db.Column(db.Integer, primary_key=True)
	autor_id = db.Column(db.Integer, nullable=False)
	autor_name = db.Column(db.String(40), nullable=False)
	car_id = db.Column(db.Integer, nullable=True)
	text = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	
	@classmethod 
	def create(cls, form_data):
	
		errors = []
		errors += cls._validate_autor_id(form_data.get("autor_id"))
		errors += cls._validate_car_id(form_data.get("car_id"))
		errors += cls._validate_text(form_data.get("text"))

		if errors:
			return False, errors

		autor_name = get_user_name(form_data.get("autor_id"))
		
		data_comment = {
			"autor_id": form_data["autor_id"],
			"autor_name": autor_name,
			"car_id": form_data["car_id"],
			"text": form_data["text"],
			"created_at": datetime.utcnow()
		}

		# Добавление в сессию и сохранение
		try:
			new_comment = cls(**data_comment)
			db.session.add(new_comment)
			db.session.commit()
			return new_comment, None

		except Exception as ex:
			db.session.rollback()
			return None, str(ex)

	# Валидация autor_id
	@staticmethod
	def _validate_autor_id(autor_id):
		errors = []
		if not autor_id:
			errors.append("ID автора не указан")
		elif not autor_id.isdigit():
			errors.append("ID автомобиля должен быть числом")
		return errors	

	# Валидация car_id
	@staticmethod
	def _validate_car_id(car_id):
		errors = []
		if not car_id:
			errors.append("ID автора не указан")
		elif not car_id.isdigit():
			errors.append("ID автомобиля должен быть числом")
		return errors
	
	#Валидация text
	@staticmethod
	def _validate_text(text):
		errors = []
		if not text:
			errors.append("Текст комментария обязателен")
		return errors 
	
	def __repr__(self):
		return f"<Comment {self.id}, {self.autor_id}, {self.autor_name}, {self.car_id}, {self.text}, {self.created_at}>"
	



class Message(db.Model):
	__tablename__ = "message"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	text = db.Column(db.Text, nullable=False)

	
	@classmethod 
	def create(cls, msg_data):
	
		try:
			new_msg = cls(**msg_data)
			db.session.add(new_msg)
			db.session.commit()
			return new_msg, None

		except Exception as ex:
			db.session.rollback()
			return None, str(ex)


	@classmethod
	def show_and_delete_by_user(cls, user_id):
		"""
		Выводит все сообщения для пользователя и удаляет их из базы	
		:param user_id: ID пользователя
		:return: (True, ошибка)
		"""

		try:
			# Получаем все сообщения пользователя
			messages = cls.query.filter_by(user_id=user_id).all()

			if not messages:
				return
		
		# Показываем каждое сообщение в flash
			for msg in messages:
				flash(msg.text)

			# Удаляем сообщения
			cls.query.filter(cls.user_id == user_id).delete()
			db.session.commit()			
			return
	
		except Exception as ex:
			# Откатываем транзакцию при ошибке
			db.session.rollback()
			return str(ex)

	
	def __repr__(self):
		return f"<Message {self.id}, {self.user_id}, {self.text}>"
	




#Общие функции

#Строку в datetime
def str_to_datetime(str):


	try:
		return datetime.strptime(str, "%Y-%m-%d").date()

	except ValueError as ex:
		#print(f"Ошибка при конвертации даты: {ex}")
		return None


#Возвращает ищет юсера по ид и возвращает user.name 
def get_user_name(manager_id):

	try:
		# Проверяем, что ID существует и является положительным числом
		if manager_id is not None and int(manager_id) >= 0:
			user=User.query.get(int(manager_id))
			return user.name
		return ""
	
	except ValueError:
		# Если ID не может быть преобразован в целое число
		return ""





def find_and_add_comment(cars):

	"""
	Добавляет к каждому автомобилю список комментариев
	
	:param cars: список автомобилей
	:return: список автомобилей с комментариями
	"""

	cars_and_comment = []
	
	for car in cars:

		# Получаем комментарии для текущего автомобиля
		comments = Comment.query\
			.filter_by(car_id=car.id)\
			.order_by(Comment.created_at.desc())\
			.all()
			
		# Форматируем даты комментариев
		formatted_comments = [
			{
				"autor_id": comment.autor_id,
				"autor_name": comment.autor_name,
				"car_id": comment.car_id,
				"text": comment.text,
				"created_at": comment.created_at.strftime('%Y-%m-%d %H:%M')                
			}
			for comment in comments
		]
		
		cars_and_comment.append({"car": car,
			"comments": formatted_comments
		})
	
	return cars_and_comment



def find_db_cars(form_data):
	"""
	Поиск автомобилей по заданным параметрам    
	:param form_data: словарь с данными для поиска
	:return: список найденных автомобилей
	"""
	
	# Маппинг полей для поиска
	search_fields = {
		"car_number": Cars.car_number,
		"model": Cars.model,
		"status": Cars.status,
		"production_date": Cars.production_date,
		"warehouse_date": Cars.warehouse_date,
		"manager_name": Cars.manager_name,
		"buyer_name": Cars.buyer_name
	}
	
	# Подготовка данных для поиска
	data_car = {
		key: value 
		for key, value in form_data.items() 
		if value and key in search_fields
	}
	
	# Базовый запрос
	query = Cars.query
	
	# Применение фильтров
	for key, value in data_car.items():
		if key in ["car_number", "model", "manager_name", "buyer_name"]:
			# Для текстовых полей используем нечувствительный поиск
			query = query.filter(
				func.lower(search_fields[key]).like(f'%{value.lower()}%')
			)
		elif key in ["production_date", "warehouse_date"]:
			# Для дат используем точное сравнение
			query = query.filter(search_fields[key] == value)
		else:
			# Для остальных полей (статус)
			query = query.filter(search_fields[key] == value)
	
	# Отладка запроса (можно раскомментировать при необходимости)
	# compiled = query.statement.compile()
	# print("SQL Query:")
	# print(compiled)
	# print("Параметры:")
	# print(compiled.params)
	
	return query.all()


