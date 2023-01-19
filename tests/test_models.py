from src.models import *
from src.app import app, db
from random import randint

test_user = f"test_user_{randint(0, 10000)}"

# Schema tests

def test_drop_schema():
    with app.app_context():
        db.drop_all()

def test_create_schema():
    with app.app_context():
        db.create_all()

# User tests

def test_create_user():
    user = user_factory.create_user(test_user, "password")
    with app.app_context():
        user.insert()

def test_get_user():
    with app.app_context():
        assert user_factory.find_user(test_user)
        
def test_failed_get_user():
    with app.app_context():
        assert user_factory.find_user(f"fake_{test_user}").first()
        
# # Post tests

# def test_create_post():
#     post = Post(test_user, "post")
#     with app.app_context():
#         post.insert()

# def test_get_user():
#     with app.app_context():
#         post = post_factory.find_posts_by_username(test_user)
#         assert post
