from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/text')
def text():
    return render_template("text.html")

@app.route('/login')
def login():
    return render_template("login.html")