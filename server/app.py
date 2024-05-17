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



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myduka.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'j2D7Ku4aF8Rne2vdmefam    '  # Change this to a secure secret key
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Change this to your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_']
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

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

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



















if __name__ == '__main__':
    app.run(debug=True)