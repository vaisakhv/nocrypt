from flask_login import login_required, LoginManager, login_user, current_user, logout_user
from flask import render_template, jsonify, redirect, url_for, flash, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from bleach import clean, sanitizer
from app.views import LoginForm, SignupForm, CreateNoteForm
from app.model import User, create_app, db, Note
from app.security import encrypt, decrypt

# bp = Blueprint('main', __name__)
app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db.init_app(app)
db.create_all()
admin = Admin(app)


def is_auth():
    auth = False
    if current_user.is_authenticated:
        auth = True
    return auth


def get_custom_list():
    return ['h1', 'h3', 'h4', 'h2', 'br', 'p', 'font', 'pre', 'u', 'td', 'tr', 'tbody', 'table', 'div']


@app.route('/check/<username>')
def check(username):
    user = User.find_user_by_username(username=username)
    if user is None:
        return jsonify(False)
    else:
        return jsonify(True)


@login_manager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))


@app.route('/')
def to_home():
    if is_auth():
        next = request.args.get('next')
        return redirect(next or url_for('mynotes'))
    return redirect(url_for('login'), code=302)


@app.route("/join", methods=["GET", "POST"])
def signUp():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        conf_passw = form.confirm_password.data
        existing_user = User.find_by_username(username=username)
        enc_pass = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
        if password == conf_passw and existing_user is None:
            new_user = User(username=username,
                            password=enc_pass)
            new_user.save_to_db()
            return redirect(url_for("login"))
        flash(message='Invalid username or password')
    return render_template('main/index.html', title='noCRYPT', auth=is_auth(), form=form, login=False)


@app.route('/login', methods=["GET", "POST"])
def login():
    if is_auth():
        next = request.args.get('next')
        return redirect(next or url_for('mynotes'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.find_by_username(username=username)
        if user is not None and check_password_hash(user.password, password=password):
            login_user(user)
            # admin.add_view(ModelView(User, db.session))
            # admin.add_view(ModelView(Note, db.session))
            next = request.args.get('next')
            return redirect(next or url_for('mynotes'))
    return render_template('main/index.html', title='noCRYPT', auth=is_auth(), form=form, login=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/create_notes', methods=["GET", "POST"])
@login_required
def create_notes():
    if request.method == 'POST':
        cleaned_data = clean(request.form.get('editordata'),
                             tags=sanitizer.ALLOWED_TAGS + get_custom_list())
        if cleaned_data != '<p>&nbsp;</p>':
            encrypted_data = encrypt(raw=cleaned_data, __key=current_user.password)
            new_data = Note(body=encrypted_data, owner_id=current_user.id, uid=str(uuid4()))
            new_data.save_to_db()
            return redirect(url_for('mynotes'))
    return render_template('main/notes.html', title='noCRYPT', auth=is_auth(), login=True)


@app.route('/mynotes')
@login_required
def mynotes():
    notes = Note.find_by_user_id(current_user.id)
    return render_template('main/mynotes.html', title='noCRYPT', auth=is_auth(), notes=notes, decrypt=decrypt)


@app.route('/edit/<string:uid>', methods=['GET', 'POST'])
@login_required
def edit(uid):
    selected_id = str(uid)
    data = Note.find_by_uid(selected_id)
    if request.method == "POST":
        if data.owner_id == current_user.id:
            cleaned_edit = clean(request.form.get('editordata'),
                                 tags=sanitizer.ALLOWED_TAGS + get_custom_list())
            encrypted_edit = encrypt(raw=cleaned_edit, __key=current_user.password)
            data.body = encrypted_edit
            if len(data.body) >= 1:
                data.save_to_db()
            else:
                data.remove_from_db()
            return redirect(url_for('mynotes'))
            # return render_template('main/display.html', data=data.body, title='noCRYPT')
        flash(message='This is not your note')
        return render_template('main/display.html', data='<h1>Not your note</h1>', title='noCRYPT')
    return render_template('main/display.html', data=data, title='noCRYPT', decrypt=decrypt)


if __name__ == '__main__':
    app.run()
