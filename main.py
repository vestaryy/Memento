from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import flash
from data import db_session
from data.users import User
from data.content import Content
from forms.content import ContentForm
from utils.yandex_disk import YandexDisk
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yra_loh_67'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста, авторизуйтесь"

yd = YandexDisk("")





@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash('Пользователь с такой почтой уже существует', 'danger')
            return render_template('register.html', title='Регистрация', form=form)
        
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash('Вы успешно зарегистрировались!', 'success') 
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', title='Авторизация', form=form)



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
        
    db_sess = db_session.create_session()
    memories = db_sess.query(Content).filter(Content.user_id == current_user.id).order_by(Content.created_date.desc()).all()
    
    for item in memories:
        item.temp_url = yd.get_download_link(item.yandex_path)
    db_sess.close()
    return render_template('index.html', memories=memories)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_memory', methods=['GET', 'POST'])
@login_required
def add_memory():
    form = ContentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        
        f = form.photo.data
        file_bytes = f.read()
        
        yd.create_folder("disk:/assistant_app")
        
        user_folder = f"disk:/assistant_app/{current_user.id}"
        yd.create_folder(user_folder)
        
        path_on_disk = f"{user_folder}/{f.filename}"
        
        if yd.upload_bytes(path_on_disk, file_bytes):
            new_content = Content(
                description=form.description.data,
                yandex_path=path_on_disk,
                user_id=current_user.id
            )
            db_sess.add(new_content)
            db_sess.commit()
            db_sess.close()
            return redirect('/')

    return render_template('add_memory.html', title='Новое воспоминание', form=form)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.create_session().close()


if __name__ == '__main__':
    db_session.global_init("db/assistant.db")
    app.run(port=8080, host='127.0.0.1')
