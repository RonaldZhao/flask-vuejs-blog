import os

from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown

from forms import LoginForm, RegisterForm, PostForm


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config.from_pyfile('config.py')
bootstrap = Bootstrap(app)
Markdown(app)
db = SQLAlchemy(app)

from models import User, Post

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(-Post.post_time).all()  # 查询所有已发布文章并根据发布时间逆序排列
    return render_template('index.html', posts=posts, posts_len=len(posts))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # 如果用户已登录则直接跳转到首页
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('此用户不存在!')
        elif check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('密码错误!')
    return render_template('form.html', form=form)


@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        flash('请先登录!')
        return redirect(url_for('login'))
    logout_user()
    flash('你已退出登录.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # 如果用户已登录则直接跳转到首页
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('此用户已存在!')
            return render_template('form.html', form=form)
        elif form.password.data != form.password_check.data:
            flash('两次输入密码不一致!')
            return render_template('form.html', form=form)
        else:
            user = User(form.username.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('注册成功, 请登录!')
            return redirect(url_for('login'))
    return render_template('form.html', form=form)


@app.route('/post', methods=['GET', 'POST'])
def post():
    if not current_user.is_authenticated:
        flash('请先登录!')
        return redirect(url_for('login'))
    form = PostForm()
    if form.validate_on_submit():
        # TODO: 文章名过长时的错误提示
        post = Post(form.title.data, form.content.data)
        post.author = current_user
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post.html', form=form)


@app.route('/posts/<int:post_id>')
def posts(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return redirect(url_for('index'))
    return render_template('page.html', post=post)
