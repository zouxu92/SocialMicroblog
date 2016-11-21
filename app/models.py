# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db
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

	# 确认用户账户
	confirmed = db.Column(db.Boolean, default=False)
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dump({'confirm':self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

# 加载用户的回调函数
@login_manager.user_loader
def loas_user(user_id):
	return User.query.get(int(user_id))


