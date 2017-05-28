from flask import Flask, render_template

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def index():
    return render_template("index.html")
