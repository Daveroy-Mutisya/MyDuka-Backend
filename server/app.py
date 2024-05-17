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


# Helper function to get the current user
def get_current_user():
    current_username = "Merchant"  # Assuming "Merchant" is the current user
    return User.query.filter_by(username=current_username).first()

# Helper function to check if a user is a superuser
def is_superuser(user):
    return user.username == "Merchant"  # Assuming "Merchant" is the superuser

# Class to handle admin-related operations
class AdminHandler:
    @staticmethod
    @app.route('/admins', methods=['POST'])
    @jwt_required()  # Requires JWT authentication
    def create_admin():
        current_user = get_current_user()
        if not current_user or not is_superuser(current_user):
            abort(403, description="Access denied. Superuser only.")
        
        data = request.get_json()

        if not data or not all(k in data for k in ('name', 'username', 'email', 'password')):
            return jsonify({"message": "Invalid input"}), 400

        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        role = 'admin'
        image = data.get('image', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            new_admin = User(name=name, username=username, email=email, password=hashed_password, role=role, image=image)
            db.session.add(new_admin)
            db.session.commit()
            return jsonify({"message": "New admin user created"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Failed to create user: {str(e)}"}), 500

# Class-based view to handle admin listing
class AdminsResource(MethodView):
    def get(self):
        current_user = get_current_user()
        if not current_user or not is_superuser(current_user):
            abort(403, description="Access denied. Superuser only.")
        
        # Fetch all admin users and serialize them
        admin_users = User.query.filter_by(role='admin').all()
        admin_users_data = [{"id": user.id, "name": user.name, "username": user.username, "email": user.email} for user in admin_users]
        return jsonify(admin_users_data)

# Register the admin listing route with the Flask app
app.add_url_rule('/admins', view_func=AdminsResource.as_view('admins'))

# Register AdminHandler for creating admin users
AdminHandler()

# Class-based view to handle clerk listing
class ClerkListView(MethodView):
    @jwt_required()  # Requires JWT authentication
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if current_user.role != 'admin':
            return jsonify({'message': 'Unauthorized'}), 401

        # Fetch all clerk users and serialize them
        clerk_users = User.query.filter_by(role='clerk').all()
        serialized_clerk_users = [user.serialize() for user in clerk_users]

        return jsonify(serialized_clerk_users), 200

# Register the clerk listing route with the Flask app
app.add_url_rule('/clerks', view_func=ClerkListView.as_view('clerk_list'))


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
