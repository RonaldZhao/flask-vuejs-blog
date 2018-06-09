from flask import render_template

from app import app
from forms import LoginForm


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
