from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from flask import Flask
from .. import db
from ..models import User
from flask_login import login_required

app = Flask(__name__)
'''
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))
    return render_template('templates/index.html',
                         form=form, name=session.get('name'),
                         known=session.get('known', False),
                         current_time=datetime.utcnow())
'''
# 保护路由，只让认证的用户访问
@app.route('/secret')
@login_required
def secret():
	return 'Only authenticated users are allowed!'


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

