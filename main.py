from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.orders import Orders
from forms.login_form import LoginForm
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.order_form import OrderForm
from forms.form_for_main import To_korzina
from data.category import Tovars

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
d = {1: 0, 2: 0, 3: 0}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def main():
    form = To_korzina()
    d_secc = db_session.create_session()
    food = d_secc.query(Tovars).all()
    if form.validate_on_submit():
        print(d)
        d[2] += 1
    else:
        return render_template('main_page.html', form=form, food=food)


@app.route("/for_admin")
def index():
    print()
    db_sess = db_session.create_session()
    orders = db_sess.query(Orders).all()
    if current_user.is_authenticated and current_user.email == 'admin1@admin.ru':
        return render_template("for_admin.html", orders=orders)
    else:
        return redirect('/')


@app.route("/search_id/<int:i>")
def index1(i):
    print(i)
    d[i] += 1
    return 'Добавлено'
    # db_sess = db_session.create_session()
    # orders = db_sess.query(Orders).all()


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/for_admin")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/make_order', methods=['GET', 'POST'])
def add_news():
    if current_user.is_authenticated:
        form = OrderForm()
        d_secc = db_session.create_session()
        food = d_secc.query(Tovars).all()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            order = Orders()
            order.positions = form.order.data
            current_user.orders.append(order)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/for_admin')
        return render_template('make_order.html', title='Оформление заказа',
                               form=form, d=d, food=food)
    else:
        return redirect('/login')


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')
