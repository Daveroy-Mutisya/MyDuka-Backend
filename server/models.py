from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# Define User Model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Superuser, Admin, Clerk, Merchant
    # Add more fields as needed (e.g., contact_info, permissions)


# Define Product Model
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(100), nullable=True)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    spoil_quantity = db.Column(db.Integer, nullable=False, default=0)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship('Store', backref='products')
    # Add more fields as needed


# Define Store Model
class Store(db.Model, SerializerMixin):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='stores')
    # Add more fields as needed

    products = db.relationship('Product', backref='store', lazy=True)

    def __repr__(self):
        return f"Store(name='{self.name}', location='{self.location}')"


# Define PaymentStatus Enum
class PaymentStatus(Enum):
    NOT_PAID = 'Not Paid'
    
    PAID = 'Paid'


# Define Payment Model
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship('Store', backref='payments')
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.NOT_PAID, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    method = db.Column(db.String)
    due_date = db.Column(db.Date, nullable=False)
    # Add more fields as needed


# Define Request Model
class Request(db.Model, SerializerMixin): 
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship('Store', backref='requests')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='requests')
    quantity = db.Column(db.Integer, nullable=False)
    requester_name = db.Column(db.String(100), nullable=False)
    requester_contact = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    # Add more fields as needed

    
