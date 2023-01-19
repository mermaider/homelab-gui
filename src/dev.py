from werkzeug.security import generate_password_hash
from models import User
from app import app

pwd = generate_password_hash("pass")
user = User(username="user", password=pwd)
print(user)
with app.app_context():
    user.insert()
