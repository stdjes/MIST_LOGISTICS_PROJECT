from flask import Blueprint, render_template, request, session,make_response
from MIST_LOGISTICS_PROJECT.app.model.models import db, Shipment
from datetime import datetime
import random
import string



# Configure path to wkhtmltopdf executable


shipment_bp = Blueprint("user", __name__)


@shipment_bp.route("/user/overview", methods=['POST', 'GET'])
def overview():
    email = session.get('email')
    username = session.get('username')
    user_id = session.get('user_id')

    shipments = Shipment.query.filter_by(user_id=user_id).all()

    return render_template("user/overview.html",email=email,username=username,shipments=shipments)


@shipment_bp.route("/user/shipments", methods=['POST', 'GET'])
def shipments():
    email = session.get('email')
    username = session.get('username')
    user_id = session.get('user_id')

    shipments = Shipment.query.filter_by(user_id=user_id).all()

    # Pass the shipments data to the template
    return render_template("user/shipments.html", email=email, username=username, shipments=shipments)

@shipment_bp.route("/user/create_shipment", methods=['POST', 'GET'])
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



# @shipment_bp.route("/user/invoices", methods=['POST', 'GET'])
# def invoices():
#     email = session.get('email')
#     username = session.get('username')
#     return render_template("user/invoices.html",email=email,username=username)


@shipment_bp.route("/user/invoices", methods=['POST', 'GET'])
def invoices():
    email = session.get('email')
    username = session.get('username')
    user_id = session.get('user_id')

    # Query shipments from the database
    shipments = Shipment.query.filter_by(user_id=user_id).all()

    return render_template("user/invoices.html", email=email, username=username, shipments=shipments)


@shipment_bp.route("/user/invoice/<int:shipment_id>")
def view_invoice(shipment_id):
    shipment = Shipment.query.get_or_404(shipment_id)
    return render_template("user/invoice_template.html", shipment=shipment)

@shipment_bp.route("/user/invoice", methods=['POST', 'GET'])
def invoice_templates():
    email = session.get('email')
    username = session.get('username')

    user_id = session.get('user_id')

    shipments = Shipment.query.filter_by(user_id=user_id).all()
    return render_template("user/invoice_template.html",email=email,username=username,shipments=shipments)


@shipment_bp.route('/tracking', methods=['GET', 'POST'])
def tracking():
    tracking_result = None
    if request.method == 'GET':
        package_id = request.args.get('package_id')
        if package_id:
            tracking_result = Shipment.query.filter_by(tracking_id=package_id).first()
    return render_template("trackingpage.html", tracking_result=tracking_result)


