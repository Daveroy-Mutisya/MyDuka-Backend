from flask import Flask, request, jsonify, abort
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
import os
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myduka.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Change this to a secure secret key
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change this to your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize Flask extensions
db.init_app(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)z








# # Route to initiate registration process for inviting admins
# @app.route('/invite-admin', methods=['POST'])
# def invite_admin():
#     data = request.json
#     email = data.get('email')

#     # Check if the email belongs to the merchant (superuser)
#     if email == 'myduka7@gmail.com':  # Change this to your superuser email
#         # Generate access token for registration link
#         access_token = create_access_token(identity=email)

#         # Send email with tokenized link for registration
#         msg = Message('Admin Registration Link', sender='admin@example.com', recipients=[email])
#         msg.body = f"Use the following link to register as an admin: http://example.com/register-admin?token={access_token}"
#         mail.send(msg)

#         return jsonify({'message': 'Registration link sent successfully'}), 200
#     else:
#         return jsonify({'error': 'Unauthorized'}), 401


# # Route for registering admins using the tokenized link
# @app.route('/register-admin', methods=['POST'])
# def register_admin():
#     token = request.args.get('token')
#     data = request.json
#     email = data.get('email')

#     # Verify token
#     try:
#         decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'])
#         if decoded_token['identity'] == email:
#             # Check if user already exists
#             if User.query.filter_by(email=email).first():
#                 return jsonify({'error': 'User already exists'}), 400

#             # Create new user
#             new_admin = User(email=email, role='admin')

#             db.session.add(new_admin)
#             db.session.commit()

#             return jsonify({'message': 'Admin registered successfully'}), 201
#         else:
#             return jsonify({'error': 'Invalid token'}), 401
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# # Route for deactivating or deleting admin accounts
# @app.route('/admin/<int:id>', methods=['DELETE'])
# @jwt_required()  # Requires authentication
# def delete_admin(id):
#     current_user = get_jwt_identity()
#     if current_user['role'] != 'merchant':
#         return jsonify({'error': 'Unauthorized'}), 401

#     admin = User.query.get(id)
#     if not admin:
#         return jsonify({'error': 'Admin not found'}), 404

#     # Deactivate or delete admin account
#     # Example: admin.active = False or db.session.delete(admin)
#     # You can implement your own logic here

#     db.session.commit()

#     return jsonify({'message': 'Admin account deactivated or deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
