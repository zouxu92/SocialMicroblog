from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Required
from flask_wtf import Form
# 定义表单类
class NameForm(Form):
	name = StringField('What is your name?', validators=[InputRequired()])
	submit = SubmitField('Submit')