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
from data.korzina import Korzina
import datetime
from API import get_picture

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
d = {}
mashtab = (0.001, 0.001)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def main():
    form = To_korzina()
    d_secc = db_session.create_session()
    food = d_secc.query(Tovars).all()
    address = 'Кострома, ул.Сусанина 10'
    get_picture.do(address, mashtab)
    if form.validate_on_submit():
        print(d)
        d[2] += 1
    else:
        return render_template('main_page.html', form=form, food=food)


@app.route("/for_admin")
def index():
    db_sess = db_session.create_session()
    orders = db_sess.query(Orders).all()
    if current_user.is_authenticated and current_user.email == 'admin1@admin.ru':
        return render_template("for_admin.html", orders=orders)
    else:
        return redirect('/')


@app.route("/search_id/<int:i>")
def index1(i):
    db_sess = db_session.create_session()
    a = db_sess.query(Korzina).all()
    f = False
    for item in a:
        if item.user_id == current_user.id:
            if item.tovar_id == i:
                f = True
                item.amount += 1
                db_sess.merge(item)
                db_sess.commit()
    if not f:
        form1 = Korzina()
        form1.user_id = current_user.id
        form1.tovar_id = i
        form1.amount = 1
        db_sess.add(form1)
        db_sess.commit()
    return 'Добавлено'


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
    form = OrderForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        order = Orders()
        order.user_id = current_user.id
        a = datetime.datetime.now()
        b = a + datetime.timedelta(minutes=30)
        order.created_date = a
        order.bringing_time = b
        db_sess.add(order)
        db_sess.commit()
    if current_user.is_authenticated:
        a = db_sess.query(Korzina).all()
        sl = {}
        for item in a:
            if item.user_id == current_user.id and item.amount != 0:
                goods = db_sess.query(Tovars).filter(Tovars.id == item.tovar_id)
                sl[item] = goods
        return render_template('make_order.html', form=form, sl=sl)
    else:
        return redirect('/login')


@app.route('/add_tovar/<int:i>')
def add(i):
    db_sess = db_session.create_session()
    a = db_sess.query(Korzina).all()
    for item in a:
        if item.user_id == current_user.id:
            if item.tovar_id == i:
                s = item.amount
                db_sess.delete(item)
                form1 = Korzina()
                form1.user_id = current_user.id
                form1.tovar_id = i
                form1.amount = s + 1
                db_sess.add(form1)
                db_sess.commit()
    return render_template('success_page.html')


@app.route('/remove_tovar/<int:i>')
def remove(i):
    db_sess = db_session.create_session()
    a = db_sess.query(Korzina).all()
    for item in a:
        if item.user_id == current_user.id:
            if item.tovar_id == i:
                s = item.amount
                db_sess.delete(item)
                form1 = Korzina()
                form1.user_id = current_user.id
                form1.tovar_id = i
                form1.amount = s - 1
                db_sess.add(form1)
                db_sess.commit()
    return render_template('success_page.html')


@app.route('/make_less')
def make_less():
    global mashtab
    x, y = mashtab[0], mashtab[1]
    mashtab = x / 2, y / 2
    return 'done'

@app.route('/make_more')
def make_more():
    global mashtab
    x, y = mashtab[0], mashtab[1]
    mashtab = x * 2, y * 2
    return 'done'


if __name__ == '__main__':
    address = 'Кострома, ул.Сусанина 10'
    get_picture.do(address, mashtab)
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')
