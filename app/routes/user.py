from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_jwt_extended import create_access_token
from MIST_LOGISTICS_PROJECT.app.model.models import db, User

user_bp = Blueprint("user", __name__)

@user_bp.route('/')
def index():
    return render_template("index.html")

@user_bp.route('/register', methods=['GET', 'POST'])
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

@user_bp.route('/login', methods=['POST', 'GET'])
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




@user_bp.route("/user/settings", methods=['POST', 'GET'])
def settings():
    email = session.get('email')
    username = session.get('username')
    return render_template("user/settings.html",email=email,username=username)

@user_bp.route("/user/support", methods=['POST', 'GET'])
def support():
    email = session.get('email')
    username = session.get('username')
    return render_template("user/support.html",email=email,username=username)

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('user_blueprint.login'))
