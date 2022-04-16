from flask_wtf import FlaskForm
from wtforms import SubmitField


class OrderForm(FlaskForm):
    submit = SubmitField('Применить')
