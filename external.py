import re


def validate_form_data(form_data):
    errors = []
    
    if not form_data['login']:
        errors.append('Логин не может быть пустым')
        
    if not form_data['email'] or not re.match(r'[^@]+@[^@]+\.[^@]+', form_data['email']):
        errors.append('Некорректный email')
        
    if not form_data['password'] or len(form_data['password']) < 6:
        errors.append('Пароль должен быть минимум 6 символов')
        
    return errors