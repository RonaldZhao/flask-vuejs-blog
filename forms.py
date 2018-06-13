from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField,\
    TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    user_name = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    remember_me = BooleanField(label='记住我', default=False)
    submit = SubmitField(label='登录')


class RegisterForm(FlaskForm):
    user_name = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    password_check = PasswordField(label='确认密码', validators=[DataRequired()])
    submit = SubmitField(label='注册')


class PostForm(FlaskForm):
    title = StringField(label='标题', validators=[DataRequired()])
    content = TextAreaField(label='内容', validators=[DataRequired()])
    submit = SubmitField(label='发布')
