# -*- coding:utf-8 -*-
from flask import render_template, request, url_for, flash, redirect, Flask
from flask_login import login_user, login_required, current_user
from . import auth
from ..models import User
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from ..email import send_email
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
		db.session.commit()
		# 发送邮件的注册路由
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Accout',
				   'auth/email/confirm', user=user, token=token)
		flash('Aconfirmation email has been sent to you by email.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)

# 确认用户的账号
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))

# 处理程序中过滤未确认的账户
@auth.before_app_request()
def before_request():
	if current_user.is_authenticated() \
		and not current_user.confirmed \
		and request.endpoint[:5] != 'auth.':
		and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))
@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous() or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

# 从新发账户确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account',
			   'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.index'))
