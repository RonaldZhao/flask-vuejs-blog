from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    remember_me = BooleanField(label='记住我', default=False)
    submit = SubmitField(label='登录')


class RegisterForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    password_check = PasswordField(label='确认密码', validators=[DataRequired()])
    submit = SubmitField(label='注册')
