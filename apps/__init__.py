from flask import Flask, render_template, session, request, url_for, redirect
from apps.database import db_session
from apps.models import User

app = Flask(__name__)
app.secret_key = b'^\xe7\xdek\xb9i\x8d\xea]\x8f3KB*\x1f\xc0\x05\xfa\xd5\x86\xc3\x90\xff6'

userlist = list()

for u in User.query.all():
    userlist.append(str(u))

def confirmLogin():
    try:
        if session["user"] in userlist:
            return True
        else:
            return False
    except:
        return False

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def index():
    return render_template("index.html", login=confirmLogin())

@app.route("/login", methods=['GET', 'POST'])
def login():
    if confirmLogin() == True:
        return redirect(url_for('index'))
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        user = "<User {0}, {1}>".format(id, pw)
        if user in userlist:
            session["user"] = user
            return redirect(url_for('index'))
        else:
            return render_template("login.html", login=confirmLogin())
    return render_template("login.html", login=confirmLogin())

@app.route("/logout")
def logout():
    if confirmLogin() == True:
        session.pop("user", None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
