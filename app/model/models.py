from datetime import datetime
from MIST_LOGISTICS_PROJECT.app.app import db,bcrypt


# Models



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)



class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime, default=datetime.utcnow)
    tracking_id = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    origin = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    package_weight = db.Column(db.Float, nullable=False)
    package_type = db.Column(db.String(255), nullable=False)
    estimated_price = db.Column(db.Float, nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

