# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required
from . import login_manager

app = Flask(__name__)
db = SQLAlchemy(app)
# 定义 Role 和 User 模型
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	# ...
	# 加入了lazy = 'dynamic'参数，从而禁止自动执行查询。
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	# ...
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User %r>' % self.username

'''
class User(db.Model):
	__tablename__ = 'users'

	password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
	# 验证密码
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
'''
# 加载用户的回调函数
@login_manager.user_loader
def loas_user(user_id):
	return User.query.get(int(user_id))

