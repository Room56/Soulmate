from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
# это нужно для сессионных функций
app.config['SECRET_KEY'] = 'q5rVjWG01Kf4Sdd11tM2XaHaQ'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20), nullable=False)
    Username = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Profiles %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogIn().fromDB(user_id, db)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/personal_account/<user_id>")
def personal_account(user_id):
    user = User.query.where(User.id == user_id).one_or_none()
    return render_template("personal_account.html", User=user)


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if request.form['password'] == request.form['password2']:
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
            return render_template('index.html')
        else:
            flash("Ошибка регистрации", category='error')
            flash('Пароли должны совпадать', category='error')
            return render_template("signup.html")
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
