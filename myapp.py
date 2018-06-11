import os

from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required,\
    logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_bootstrap import Bootstrap

from forms import LoginForm, RegisterForm


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from models import User

login_manager = LoginManager()
# login_manager.session_protection = 'strong'
# login_manager.login_view = 'login'
login_manager.init_app(app=app)
bootstrap = Bootstrap(app)


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('此用户不存在!')
        elif check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return render_template('index.html', current_user=current_user)
        else:
            flash('密码错误!')
    # return render_template('login_or_register.html', form=form)
    return render_template('form.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录.')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('此用户已存在!')
            # return render_template('login_or_register.html', form=form)
            return render_template('form.html', form=form)
        elif form.password.data != form.password_check.data:
            flash('两次输入密码不一致!')
            # return render_template('login_or_register.html', form=form)
            return render_template('form.html', form=form)
        else:
            user = User(form.username.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('注册成功, 请登录!')
            return redirect(url_for('login'))
    # return render_template('login_or_register.html', form=form)
    return render_template('form.html', form=form)
