from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/personal_account/<user_id>")
def personal_account(user_id):
    user = User.query.order_by(User.id==user_id).one_or_none()
    return render_template("personal_account.html",User=user)


@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        city = request.form['city']
        user=User(Username=username,Password=password,city=city,email=email)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/personal_account/<user_id>')
        except:
            return "Ошибка регистрации"
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)