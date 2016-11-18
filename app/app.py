# -*- coding:utf-* -*-
from flask_login import UserMixin, login_required
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import os

# 表单
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Required

from flask_sqlalchemy import SQLAlchemy
# 配置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# 设置Flask-WTF
app.config['SECRET_KEY'] = 'hard to guess string' # 保证安全不应该写入这里,写在配置文件中
# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
# 初始化flask_moment --> 本地时间
moment = Moment(app)

# 定义表单类
class NameForm(Form):
	name = StringField('What is your name?', validators=[InputRequired()])
	submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
	# name = None
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'),
						   known = session.get('known', False),current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

# 保护路由，只让认证的用户访问
@app.route('/secret')
@login_required
def secret():
	return 'Only authenticated users are allowed!'

