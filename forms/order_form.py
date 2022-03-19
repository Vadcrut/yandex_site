from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    order = StringField('Шаурма', validators=[DataRequired()])
    submit = SubmitField('Применить')
