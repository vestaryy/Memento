from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.users import User
from data.content import Content
from forms.content import ContentForm
from utils.yandex_disk import YandexDisk

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yra_loh_67'
login_manager = LoginManager()
login_manager.init_app(app)

yd = YandexDisk("")

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        memories = db_sess.query(Content).filter(Content.user_id == current_user.id).all()
        for item in memories:
            item.temp_url = yd.get_download_link(item.yandex_path)
    else:
        memories = []
    return render_template('index.html', memories=memories)

@app.route('/add_memory', methods=['GET', 'POST'])
@login_required
def add_memory():
    form = ContentForm()
    if form.validate_on_submit():
        file_data = form.photo.data.read()
        filename = form.photo.data.filename
        
        yandex_path = f"disk:/assistant_app/{current_user.id}/{filename}"
        yd.create_folder(f"disk:/assistant_app/{current_user.id}")
        yd.upload_bytes(yandex_path, file_data)
        
        db_sess = db_session.create_session()
        memory = Content(
            category='photo',
            yandex_path=yandex_path,
            description=form.description.data,
            user_id=current_user.id
        )
        db_sess.add(memory)
        db_sess.commit()
        
        return redirect('/')
    return render_template('add_memory.html', title='Новое воспоминание', form=form)

if __name__ == '__main__':
    db_session.global_init("db/assistant.db")
    app.run(port=8080, host='127.0.0.1')
