from flask import Flask, render_template, redirect
from forms.login_form import LoginForm
from data import db_session
from data.users import User
from data.orders import Orders
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def main():
    return render_template('main_page.html')


@app.route('/make_order', methods=['GET', 'POST'])
def make_order():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('make_order.html', title='Авторизация', form=form)


@app.route("/for_admin")
def index():
    db_sess = db_session.create_session()
    orders = db_sess.query(Orders).all()
    return render_template("for_admin.html", orders=orders)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Orders).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            phone=form.phone.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    order = Orders()
    order.positions = 'dkhdfg'
    db_sess = db_session.create_session()
    db_sess.add(order)
    db_sess.commit()
    app.run(port=8080, host='127.0.0.1')
