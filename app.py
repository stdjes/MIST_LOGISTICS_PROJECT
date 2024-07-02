from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "uijdkshkdfljkodlfjldjfldsf"

# Ensure you set the SQLAlchemy Database URI before creating the db instance
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:pokermessiaH307864$@localhost/logistics_db"

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f'<Shipment {self.tracking_id}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    db.create_all()
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match!'}), 400

        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            return jsonify({'message': 'User already exists!'}), 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Registration successful! Please log in.'}), 201
        except Exception as e:
            return jsonify({'message': f'Error registering user: {str(e)}'}), 500
    return render_template('registration.html')
@app.route("/dashboard", methods=['POST','GET'])
def dashboard():
    return  render_template("dashboard.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid email or password!'}), 401
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
