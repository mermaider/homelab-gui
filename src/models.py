try:
    from src.app import db, login_manager, app
except ImportError:
    from app import db, login_manager, app

from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey, DateTime, Column, String


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def insert(self):
        db.session.add(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Probably should be mapping to user_id not user_username
    username = db.Column(db.String,  ForeignKey(User.username), nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return f"{self.id}, {self.username}, {self.title},  {self.content}"
    

class UserFactory:
    def find_user(self, username:str) -> User:
        users = User.query
        return users.filter(User.username==username)

    def get(self, user_id:str) -> User:
        users = User.query
        return users.filter(User.id==user_id)

    def create_user(self, username: str, password: str) -> User:
        password_hash = generate_password_hash(password)
        kwargs = dict(username=username, password_hash=password_hash)
        return User(**kwargs)


class PostFactory:
    def get(self, post_id):
        posts = Post.query
        return posts.filter(Post.id==post_id).first()

    def find_posts_by_username(self, username: str) -> Post:
        return Post.query.filter(Post.username==username)

    def create_post(self, username: str, title:str, content:str)-> Post:
        kwargs = dict(username=username, title=title, content=content)
        print(kwargs)
        return Post(**kwargs)


user_factory = UserFactory()
post_factory = PostFactory()

if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = user_factory.create_user("user", "pass")
        user.insert()
        for i in range(5):
            post = post_factory.create_post(user.username, f"title {i}", f"message_text #{i}")
            post.insert()
            print(f"inserted {post}")

    print("Done!")
