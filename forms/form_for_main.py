from flask_wtf import FlaskForm
from wtforms import SubmitField


class To_korzina(FlaskForm):
    submit = SubmitField('В корзину')
