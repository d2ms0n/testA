import re
from enum import Enum
from flask import Flask
from flask_login import LoginManager, UserMixin
from datetime import date, datetime
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
			"role": form_data["role"],
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
		print(f"len!={len(login)}")
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
		elif len(password) < 6:
			errors.append("Пароль должен содержать минимум 6 символов")
		return errors

	@staticmethod
	def _validate_role(role):
		print(role, Role)
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
	production_date = db.Column(db.Date, nullable=True)
	warehouse_date = db.Column(db.Date, nullable=True)
	status = db.Column(db.Enum(Status), nullable=False)
	description = db.Column(db.Text)
	manager_id = db.Column(db.Integer, nullable=True)
	buyer_id = db.Column(db.Integer, nullable=True)


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
		new_car = cls(**form_data)

		# Добавление в сессию и сохранение
		try:
			db.session.add(new_car)
			db.session.commit()
			return new_car, None

		except Exception as ex:
			db.session.rollback()
			return None, str(ex)




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
		# if not isinstance(production_date, date):
		#     errors.append("Дата производства должна быть объектом datetime.date")
		if production_date > date.today():
			errors.append("Дата производства не может быть в будущем")
		return errors

	@staticmethod
	def _validate_warehouse_date(warehouse_date):
		if warehouse_date:
			errors = []
			# if not isinstance(warehouse_date, date):
			#     errors.append("Дата поступления на склад должна быть объектом datetime.date")
			if warehouse_date > date.today():
				errors.append("Дата поступления на склад не может быть в будущем")
		return errors

	@staticmethod
	def _validate_status(status):
		errors = []
		if not isinstance(status, Status):
			errors.append("Неверно указан статус автомобиля")
		return errors

	def __repr__(self):
		return (
			f"<Cars(id={self.id}, car_number='{self.car_number}', model='{self.model}', "
			f"production_date={self.production_date}, warehouse_date={self.warehouse_date}, "
			f"status={self.status}, description='{self.description}', "
			f"manager_id={self.manager_id}, buyer_id={self.buyer_id})>"
		)


def str_to_datetime(str):

	try:
		return datetime.strptime(str, "%Y-%m-%d").date()

	except ValueError as ex:
		print(f"Ошибка при конвертации даты: {ex}")
		return None


if __name__ == "__main__":

	with app.app_context():
		db.create_all()

		form_data = {
			"car_number": "А123АА77",
			"model": "Toyota Camry",
			"production_date": str_to_datetime("2023-01-01"),
			"warehouse_date": str_to_datetime("2023-02-01"),
			"status": Status.SALE,  # Значение из вашего Enum Status
			"description": "Автомобиль в отличном состоянии",
			"manager_id": 1,
			"buyer_id": None,
		}
		cars, errors = Cars.create(form_data)
		print(f"cars-{cars}...erors-{errors}")

		# 'manager_id': 1,
		# 'buyer_id': None  # Можно оставить None, если покупатель еще не определен