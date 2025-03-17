import re
from sqlite3 import IntegrityError
from models import User, Role, generate_password_hash, db

