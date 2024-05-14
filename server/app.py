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
from models import User, Product, Store, Payment, PaymentStatus, Request
from flask_mail import Mail, Message
import os 


@app.route('/products', methods=['GET'])
@jwt_required()  # Ensure authentication is required
def get_products():
    if current_identity.role == 'clerk':  # Assuming role is stored in current_identity
        products = Product.query.all()
        serialized_products = [product.serialize() for product in products]
        return jsonify(serialized_products), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401


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


@app.route('/home')
@app.route('/')
def home ():
    return _render.template('index.html')

# This is to define the different roles
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# This table establishes the many to many relationship between users
user_roles = db.Table('user_roles',
                       
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True))

# Define User model
class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(100), unique=True, nullable=False)
   roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

# Define superuser route to initialize registration process
@app.route('/initiate-registration', methods=['POST'])
def initiate_registration():
    data = request.json
    email = data.get('email')

    # Check if the email belongs to a superuser
    if email == 'superuser@example.com':  # Change this to your superuser email
        # Generate token for registration link
        access_token = create_access_token(identity=email)

        # Send email with tokenized link for registration
        msg = Message('Registration Link', sender='admin@example.com', recipients=[email])
        msg.body = f"Use the following link to register: http://example.com/register?token={access_token}"
        mail.send(msg)

        return jsonify({'message': 'Registration link sent successfully'}), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 401

# Define registration route for invitee to register
@app.route('/register', methods=['POST'])
def register():
    token = request.args.get('token')
    data = request.json
    email = data.get('email')

    # Verify token
    try:
        decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'])
        if decoded_token['email'] == email:
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                return jsonify({'error': 'User already exists'}), 400

            # Create new user
            user = User(email=email)

            # Check if user is an admin
            if email == 'admin@example.com':  # Change this to your admin email
                user.is_admin = True

            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'User registered successfully'}), 201
        else:
            return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# # This route checks if the user is a merchant
# @app.route('/merchant-panel', methods=['GET'])
# @jwt_required()
# def merchant_panel():
#     current_user_email = get_jwt_identity()
#     user = User.query.filter_by(email=current_user_email).first()
#     if user and 'merchant' in [role.name for role in user.roles]:
#         return jsonify({'message': 'Welcome to the merchant panel!'}), 200
#     else:
#         return jsonify({'error': 'Unauthorized'}), 401
    

# # This route checks if the user is an admin
# @app.route('/admin-panel', methods=['GET'])
# @jwt_required()
# def admin_panel():
#     current_user_email = get_jwt_identity()
#     user = User.query.filter_by(email=current_user_email).first()
#     if user and 'admin' in [role.name for role in user.roles]:
#         return jsonify({'message': 'Welcome to the admin panel!'}), 200
#     else:
#         return jsonify({'error': 'Unauthorized'}), 401
    

# # This route checks if the user is an clerk
# @app.route('/clerk-panel', methods=['GET'])
# @jwt_required()
# def clerk_panel():
#     current_user_email = get_jwt_identity()
#     user = User.query.filter_by(email=current_user_email).first()
#     if user and 'clerk' in [role.name for role in user.roles]:
#         return jsonify({'message': 'Welcome to the clerk panel!'}), 200
#     else:
#         return jsonify({'error': 'Unauthorized'}), 401
    



@app.route('/products', methods=['GET'])
@jwt_required()  # Ensure authentication is required
def get_products():
    if current_identity.role == 'clerk':  # Assuming role is stored in current_identity
        products = Product.query.all()
        serialized_products = [product.serialize() for product in products]
        return jsonify(serialized_products), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401
    

@app.route('/request', methods =['GET'])
@jwt_required()
def get_request():
    if current_identity.role == 'clerk':
    request = Request.query.all()





if __name__ == '__main__':
    app.run(debug=True)