from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "uijdkshkdfljkodlfjldjfldsf"

# Ensure you set the SQLAlchemy Database URI before creating the db instance
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/logistics_db"

db = SQLAlchemy(app)

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Shipment {self.tracking_id}>'

# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/')
def index():
    db.create_all()
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
@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    tracking_result = None
    if request.method == 'GET':
        package_id = request.args.get('package_id')
        if package_id:
            tracking_result = Shipment.query.filter_by(tracking_id=package_id).first()
    return render_template("trackingpage.html", tracking_result=tracking_result)

if __name__ == '__main__':
    app.run(debug=True)
