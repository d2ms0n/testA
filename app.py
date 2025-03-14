import external as e #внешние функции
from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS
from datetime import datetime
# from flask_jwt_extended import (
#     JWTManager, 
#     create_access_token,
#     jwt_required,
#     get_jwt_identity
# )





# Инициализация приложения
app = Flask(__name__, template_folder='html')
app.secret_key = 'your-secret-key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Замените на свой секретный ключ
#jwt = JWTManager(app)
#CORS(app)



db = SQLAlchemy(app)

# Определение модели
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user_pwd = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.name}>"

# Создание базы данных (альтернативный способ для Flask 2.3.0)
with app.app_context():
    db.create_all()




@app.route('/registry', methods=['GET', 'POST'])
def registry():
    if request.method == 'POST':
        name = request.form['name']
        password = e.hash_password(request.form['password'])
        print(name, password)
        new_user = User(name=name, user_pwd=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Успешная регистрация!')
        return redirect(url_for('login'))
    
    return render_template('registry.html')




@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        return "y loginnet"
    elif request.method == 'GET': 
        return render_template('login.html')



    # username = request.json.get('username', None)
    # password = request.json.get('password', None)
    
    # # Простая проверка пользователя (в реальном проекте используйте хеширование паролей)
    # if username != 'test' or password != 'test':
    #     return jsonify({"msg": "Bad username or password"}), 401

    # # Создаем токен
    # access_token = create_access_token(identity=username)
    # return jsonify(access_token=access_token), 200




# Создание (Create)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('create.html')

# Чтение (Read)
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Обновление (Update)
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('update.html', user=user)

# Удаление (Delete)
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('delete.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)