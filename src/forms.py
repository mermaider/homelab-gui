from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("User Name: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Submit!")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit!")