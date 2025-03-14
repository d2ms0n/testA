import bcrypt

def hash_password(password):
 # Преобразуем пароль в байты
 password_bytes = password.encode('utf-8')
 
 # Генерируем соль
 salt = bcrypt.gensalt()
 
 # Создаем хеш
 hashed_password = bcrypt.hashpw(password_bytes, salt)
 
 return hashed_password