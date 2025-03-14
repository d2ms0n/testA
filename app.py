from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Инициализация приложения
app = Flask(__name__, template_folder='html')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Определение модели
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.name}>"

# Создание базы данных (альтернативный способ для Flask 2.3.0)
with app.app_context():
    db.create_all()

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