from flask import Flask
from flask.templating import _render
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from flask_marshmallow import Marshmallow
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token,create_access_token
from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from models import User, Product, Store, Payment, PaymentStatus, Request, Dashboard, Report
from flask_mail import Mail, Message
import os 
from flask.views import MethodView



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myduka.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'j2D7Ku4aF8Rne2vdmefam    '  # Change this to a secure secret key
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Change this to your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_'] = ''
app.config['MAIL_USERNAME'] = 'daveroymutisya2@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('Daveroy')

# Initializing Flask-Migrate and other extensions
migrate = Migrate(app, db)
ma = Marshmallow
jwt = JWTManager()
mail = Mail(app)


# Initialize SQLAlchemy
db.init_app(app)
jwt.init_app(app)


# @app.route('/home')
# @app.route('/')
# def home ():
#     return _render.template('index.html')

# # Define superuser route to initialize registration process
# @app.route('/initiate-registration', methods=['POST'])
# def initiate_registration():
#     data = request.json
#     email = data.get('email')

#     # Check if the email belongs to a superuser
#     if email == 'superuser@example.com':  # Change this to your superuser email
#         # Generate token for registration link
#         access_token = create_access_token(identity=email)

#         # Send email with tokenized link for registration
#         msg = Message('Registration Link', sender='admin@example.com', recipients=[email])
#         msg.body = f"Use the following link to register: http://example.com/register?token={access_token}"
#         mail.send(msg)

#         return jsonify({'message': 'Registration link sent successfully'}), 200
#     else:
#         return jsonify({'error': 'Unauthorized'}), 401

# # Define registration route for invitee to register
# @app.route('/register', methods=['POST'])
# def register():
#     token = request.args.get('token')
#     data = request.json
#     email = data.get('email')

#     # Verify token
#     try:
#         decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'])
#         if decoded_token['email'] == email:
#             # Check if user already exists
#             if User.query.filter_by(email=email).first():
#                 return jsonify({'error': 'User already exists'}), 400

#             # Create new user
#             user = User(email=email)

#             # Check if user is an admin
#             if email == 'admin@example.com':  # Change this to your admin email
#                 user.is_admin = True

#             db.session.add(user)
#             db.session.commit()

#             return jsonify({'message': 'User registered successfully'}), 201
#         else:
#             return jsonify({'error': 'Invalid token'}), 401
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


## This if for clerks requesting products to admins
# The get_requests checks if the products exists
@app.route('/products', methods=['GET'])
def get_requests():
    
    # Assuming the clerk has been authenticated
    if current_user.role == 'clerk':
       products = Product.query.all() # this querys from the product tables
       serialized_products = [product.serialize() for product in products]
       return jsonify(serialized_products), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401

   
## This then sends a post request to the request table adding the new request to the table
@app.route('/requests', methods=['POST'])
def add_request():
    if current_user.role == 'clerk':  
        data = request.json
        product_id = data['product_id']
        quantity = data['quantity']
        requester_name = data['requester_name']
        requester_contact = data['requester_contact']
        
        # This checks if the request already exists in the database
        existing_request = Request.query.filter_by(product_id=product_id, 
                                                   quantity=quantity, 
                                                   requester_name=requester_name, 
                                                   requester_contact=requester_contact).first()
        if existing_request:
            return jsonify({'message': 'The request has already been sent'}), 409 
        else:
            new_request = Request(
                product_id=product_id,
                quantity=quantity,
                requester_name=requester_name,
                requester_contact=requester_contact
            )
            db.session.add(new_request)
            db.session.commit()
            return jsonify({'message': 'Request added successfully'}), 201
    else:
        return jsonify({"message": "Unauthorized"}), 401
    
## Route for the store admins 
## Method view has been used to define our get request

class Dashboard(MethodView):
    def get(self):
        # Check if the user is authenticated and has admin role
        if not is_authenticated(request) or not is_admin(request):
            return jsonify({'error': 'Unauthorized access'}), 401
        
        # Retrieve dashboard data from the Dashboard model
        dashboard_data = DashboardModel.query.first()  # Example: Retrieve the first row of dashboard data
        
        if not dashboard_data:
            return jsonify({'error': 'No dashboard data available'}), 404
        
        # Serialize data if needed (convert to JSON-serializable format)
        serialized_dashboard_data = {
            'total_sales': dashboard_data.total_sales,
            'top_products': dashboard_data.top_products,
            'low_stock_items': dashboard_data.low_stock_items
        }
        
        return jsonify(serialized_dashboard_data)


# Route for retrieving detailed reports (store admin only)
class store_admin_Reports(Resource):
    @jwt_required(refresh=True)
    def get(self):
        # Check if the user is authenticated and has the admin role
        if not is_authenticated(request) or not is_admin(request):
            return {'error': 'Unauthorized access. Only store admins are allowed'}, 401

        # Retrieve reports from the database
        reports = Report.query.all()

        # Serialize reports to JSON
        serialized_reports = []
        for report in reports:
            serialized_report = {
                'id': report.id,
                'entry_id': report.entry_id,
                'details': report.details
            }
            serialized_reports.append(serialized_report)

        return jsonify(serialized_reports)



## Route for admins accepting and declining supply requests from clerks
class admin_requests(MethodView):
    def patch(self, request_id):
        # Check if the user is authenticated and has admin role
        if not is_authenticated(request) or not is_admin(request):
            return jsonify({'error': 'Unauthorized access. Only store admins are allowed'}), 401

        # Retrieve the request from the database based on request_id
        request_obj = Request.query.get(request_id)
        
        if not request_obj:
            return jsonify({'error': 'Request not found'}), 404

        # Retrieve the request status from the request body
        status = request.json.get('status')

        # Update the status of the request
        if status in ['Approved', 'Declined']:
            request_obj.status = status
            db.session.commit()  # Commit the changes to the database
            return jsonify({'message': f'Request {request_id} has been {status}'}), 200
        else:
            return jsonify({'error': 'Invalid status. Please provide either "Approved" or "Declined"'}), 400

# Add the route to the Flask application
app.add_url_rule('/requests/<int:request_id>', view_func=ClerkRequestsAPI.as_view('clerk_requests'))
    


## route for payment status
class PaymentAPI(MethodView):
    def patch(self, payment_id):
        # Check if the user is authenticated and has admin role
        if not is_authenticated(request) or not is_admin(request):
            return jsonify({'error': 'Unauthorized access. Only store admins are allowed'}), 401
        
        # Retrieve the payment from the database based on payment_id
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        # Check if the payment is currently not paid
        if payment.status == PaymentStatus.NOT_PAID.value:
            # Update the payment status to paid
            payment.status = PaymentStatus.PAID.value
            db.session.commit()  # Commit the changes to the database
            return jsonify({'message': f'Payment {payment_id} status has been changed to "paid"'}), 200
        else:
            return jsonify({'error': 'Payment is already paid'}), 400

# Add the route to the Flask application
app.add_url_rule('/payments/<int:payment_id>', view_func=PaymentAPI.as_view('payment'))


## route for deleting, deactivating and adding clerks
class ClerkManagementAPI(MethodView):
    def patch(self, clerk_id):
        # Check if the user is authenticated
        if not is_authenticated(request):
            return jsonify({'error': 'Unauthorized access. You need to login to perform this action'}), 401
        
        # Retrieve the current user
        current_user = get_current_user(request)
        
        # Check if the user is a store admin
        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized access. Only store admins are allowed to perform this action'}), 403
        
        # Retrieve the clerk from the database based on clerk_id
        clerk = Clerk.query.get(clerk_id)
        
        if not clerk:
            return jsonify({'error': 'Clerk not found'}), 404
        
        # Check the action to perform (deactivate or delete)
        action = request.json.get('action')
        if action not in ['deactivate', 'delete']:
            return jsonify({'error': 'Invalid action. Please provide either "deactivate" or "delete"'}), 400
        
        # Perform the action
        if action == 'deactivate':
            clerk.is_active = False
            db.session.commit()  # Commit the changes to the database
            return jsonify({'message': f'Clerk {clerk_id} has been deactivated'}), 200
        elif action == 'delete':
            db.session.delete(clerk)
            db.session.commit()  # Commit the changes to the database
            return jsonify({'message': f'Clerk {clerk_id} has been deleted'}), 200

    def post(self):
        # Check if the user is authenticated and is a store admin
        if not is_authenticated(request) or get_current_user(request).role != 'admin':
            return jsonify({'error': 'Unauthorized access. Only store admins are allowed to perform this action'}), 403

        # Retrieve clerk details from the request body
        clerk_data = request.json
        
        # Validate clerk data (ensure all required fields are present)
        if 'name' not in clerk_data or 'username' not in clerk_data or 'email' not in clerk_data or 'password' not in clerk_data:
            return jsonify({'error': 'Incomplete clerk data. Please provide name, username, email, and password'}), 400
        
        # Check if the clerk already exists in the database
        existing_clerk = Clerk.query.filter_by(username=clerk_data['username']).first()
        if existing_clerk:
            return jsonify({'error': 'Clerk with this username already exists'}), 400
        
        # Create a new clerk
        new_clerk = Clerk(name=clerk_data['name'], username=clerk_data['username'], email=clerk_data['email'], password=clerk_data['password'], is_active=True)
        db.session.add(new_clerk)
        db.session.commit()  # Commit the changes to the database
        
        return jsonify({'message': 'New clerk added successfully', 'clerk_id': new_clerk.id}), 201

# Add the route to the Flask application
app.add_url_rule('/clerks/<int:clerk_id>', view_func=ClerkManagementAPI.as_view('clerk_management'))


















if __name__ == '__main__':
    app.run(debug=True)