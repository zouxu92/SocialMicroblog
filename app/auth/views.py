# -*- coding:utf-8 -*-
from flask import render_template, request, url_for, flash, redirect, Flask
from flask_login import login_user, login_required
from . import auth
from ..models import User
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)
# 用户登录
@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)

# 退出路由
@auth.route('/logout')
@login_required
def logout():
	login_required()
	flash("You have been logged out.")
	return redirect(url_for('main.index'))

# 用户注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		flash('You can now login.')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)

