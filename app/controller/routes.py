from flask_login import login_required, LoginManager, login_user, current_user, logout_user
from app.model import User, create_app, db, Note
from flask import render_template, jsonify, redirect, url_for, flash, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
import bleach
from app.views import LoginForm, SignupForm, CreateNoteForm

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
    print('redirecting to ', url_for('login'))
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
        print(username, password, enc_pass)
        try:
            print(existing_user.id)
        except Exception as e:
            print(str(e))
        if password == conf_passw and existing_user is None:
            new_user = User(username=username,
                            password=enc_pass)
            new_user.save_to_db()
            print('user created')
            return redirect(url_for("login"))
        flash(message='Invalid username or password')
    return render_template('main/index.html', title='noCRYPT', auth=is_auth(), form=form, login=False)


@app.route('/login', methods=["GET", "POST"])
def login():
    print(is_auth())
    form = LoginForm()
    print(form.errors)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.find_by_username(username=username)
        if user is not None and check_password_hash(user.password, password=password):
            login_user(user)
            admin.add_view(ModelView(User, db.session))
            admin.add_view(ModelView(Note, db.session))
            next = request.args.get('next')
            return redirect(next or url_for('notes'))
    return render_template('main/index.html', title='noCRYPT', auth=is_auth(), form=form, login=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/notes', methods=["GET", "POST"])
@login_required
def notes():
    if request.method == 'POST':
        print(current_user.id)
        cleaned_data = bleach.clean(request.form.get('editordata'),
                                    tags=bleach.sanitizer.ALLOWED_TAGS + ['h1', 'h3', 'h4', 'h2', 'br', 'img'])
        print(cleaned_data)
        new_data = Note(body=cleaned_data, owner_id=current_user.id)
        new_data.save_to_db()
        return "posted"
    return render_template('main/notes.html', title='noCRYPT', auth=is_auth(), login=True)
# make a screen to display notes from the user/like search reseult in med360
# make a function for giving base64 id
# streamline everything


@app.route('/display/<int:id>', methods=['GET', 'POST'])
def display(id):
    data = Note.find_by_id(id)
    print(data.body)
    if request.method == "POST":
        print('in post')
        data.body = bleach.clean(request.form.get('editordata'),
                                 tags=bleach.sanitizer.ALLOWED_TAGS + ['h1', 'h3', 'h4', 'h2', 'br', 'img'])
        print('edit')
        print(data.body)
        data.save_to_db()
        return render_template('display.html', data=data.body)
    return render_template('display.html', data=data.body)
    # return render_template('display.html', data=data.body)


if __name__ == '__main__':
    app.run()
