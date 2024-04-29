from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite:///data.db"
db = SQLAlchemy(app) 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    pswd = db.Column(db.String(120))

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    pswd = request.form["pswd"]

    user = User(name=name, email=email, pswd=pswd)

    with app.app_context():
        db.session.add(user)
        db.session.commit()
    return redirect(url_for("results"))

@app.route("/results")
def results():
    users = User.query.all()
    return render_template("results.html", users=users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)