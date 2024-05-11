from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from flask_marshmallow import Marshmallow
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask import Blueprint, jsonify
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myduka.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing Flask-Migrate and other extensions
migrate = Migrate(app, db)
ma = Marshmallow
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
jwt = JWTManager()


# Initialize SQLAlchemy
db.init_app(app)
jwt.init_app(app)






















if __name__ == '__main__':
    app.run(debug=True)