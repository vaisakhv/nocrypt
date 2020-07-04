from flask_login import (
    login_required, LoginManager, login_user, current_user, logout_user
)
from app.model import (
    User, Note, create_app, db
)
from flask import (
    Blueprint, render_template, jsonify, redirect, url_for, flash
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from views import LoginForm, SignupForm

# bp = Blueprint('main', __name__)
app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db.create_all()

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


@app.route('/', methods=["GET", "POST"])
def login():
    print("in login")
    print(is_auth())
    form = LoginForm()
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.find_by_username(username=username)
        if user is not None and check_password_hash(user.password, password=password):
            login_user(user)
            print('logged in')
            # return render_template(url_for('index'), auth=is_auth())
            return "logged in"
    return render_template('main/index.html', title='noCRYPT', auth=is_auth(), form=form, login=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.init_app(app)
    app.run()
