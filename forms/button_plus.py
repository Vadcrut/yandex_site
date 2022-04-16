from flask_wtf import FlaskForm
from wtforms import SubmitField


class Button_plus(FlaskForm):
    submit = SubmitField('+')
