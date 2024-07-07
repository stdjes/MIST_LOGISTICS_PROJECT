from datetime import datetime
import random
import string

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['SESSION_TYPE'] = os.getenv("SESSION_TYPE")


bcrypt = Bcrypt(app)
jwt = JWTManager(app)


@app.route('/')
def index():
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        print(f"Received email: {email}")
        print(f"Received password: {password}")

        user = User.query.filter_by(email=email).first()
        session['user_id'] = user.id
        session['email'] = user.email
        session['username'] = user.username
        print(session['user_id'])


        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token, 'message': 'Login successful', 'email': user.email}), 200
        else:
            return jsonify({'message': 'Invalid email or password!'}), 401
    return render_template("login.html")


@app.route("/user/overview", methods=['POST', 'GET'])
def overview():
    email = session.get('email')
    username = session.get('username')
    # print(username)
    return render_template("user/overview.html",email=email,username=username)

@app.route("/user/shipments", methods=['POST', 'GET'])
def shipments():
    email = session.get('email')
    username = session.get('username')
    return render_template("user/shipments.html",email=email,username=username)

@app.route("/user/create_shipment", methods=['POST', 'GET'])
def create_shipment():
    email = session.get('email')
    username = session.get('username')
    user_id = session.get('user_id')

    if request.method == 'POST':
        statuses = ['In Transit', 'Delivered', 'Pending']
        tracking_id_length = 10

        record_date = datetime.now()
        origin = request.form['senderAddress']
        recipient = request.form['receiverName']
        destination = request.form['receiverAddress']
        package_weight = float(request.form['packageWeight'])
        package_type = request.form['packageType']
        estimated_price = float(request.form['estimatedPrice'])
        status = random.choice(statuses)
        tracking_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=tracking_id_length))

        new_shipment = Shipment(
            record_date=record_date,
            origin=origin,
            recipient=recipient,
            destination=destination,
            package_weight=package_weight,
            package_type=package_type,
            estimated_price=estimated_price,
            status=status,
            tracking_id=tracking_id,
            user_id=user_id
        )

        db.session.add(new_shipment)
        db.session.commit()

        return render_template("user/create_shipment.html", email=email, username=username, success_message="Shipment created successfully!")

    return render_template("user/create_shipment.html", email=email, username=username)



@app.route("/user/invoices", methods=['POST', 'GET'])
def invoices():
    email = session.get('email')
    username = session.get('username')
    return render_template("user/invoices.html",email=email,username=username)

@app.route("/user/settings", methods=['POST', 'GET'])
def settings():
    email = session.get('email')
    username = session.get('username')
    return render_template("user/settings.html",email=email,username=username)

@app.route("/user/support", methods=['POST', 'GET'])
def support():
    email = session.get('email')
    username = session.get('username')
    return render_template("user/support.html",email=email,username=username)

@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    tracking_result = None
    if request.method == 'GET':
        package_id = request.args.get('package_id')
        if package_id:
            tracking_result = Shipment.query.filter_by(tracking_id=package_id).first()
    return render_template("trackingpage.html", tracking_result=tracking_result)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
