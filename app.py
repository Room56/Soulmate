from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
# это нужно для сессионных функций
app.config['SECRET_KEY'] = 'q5rVjWG01Kf4Sdd11tM2XaHaQ'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20), nullable=False)
    Username = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description=db.Column(db.Text(), nullable=True)
    age=db.Column(db.String(10),nullable=True)

    def __repr__(self):
        return '<Profiles %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route("/index")
@app.route('/')
def index():
    return render_template("index.html")


#@app.route('/submit_profile',methods=["GET", "POST"])
#def submit_profile():


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form.get("email")).first()
        if user:
            # profile = Profiles.query.where(user.id == Profiles.user_id).first()
            if check_password_hash(user.Password, request.form.get("password")):
                login_user(user)
                # if profile.description == None:
                #     return redirect(url_for("submit_profile"))
                return redirect(url_for("personal_account"))
            else:
                flash('Неверный адрес электронной почты/пароль', category='error')
        else:
            flash('Неверный адрес электронной почты/пароль', category='error')
    return render_template("index.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/personal_account")
@login_required
def personal_account():
    return render_template("personal_account.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if request.form['password'] == request.form['password2']:
            chek_user = User.query.filter_by(
                email=request.form.get("email")).first()
            if chek_user:
                flash("Ошибка регистрации", category='error')
                flash('Пользователь с таким email уже зарегестрирован', category='error')
                return render_template("signup.html")
            username = request.form['username']
            # шифрование паролей чтоб не сглазили
            hash = generate_password_hash(request.form['password'])
            password = hash
            email = request.form['email']
            city = request.form['city']
            user = User(Password=password, email=email)
            db.session.add(user)
            db.session.flush()
            prof = Profiles(Username=username, city=city, user_id=user.id)
            db.session.add(prof)
            db.session.commit()
            # этот флэш и есть сессионная функция
            flash('Регистрация прошла успешно', category='success')
            return redirect(url_for("login"))
        else:
            flash("Ошибка регистрации", category='error')
            flash('Пароли должны совпадать', category='error')
            return render_template("signup.html")
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)