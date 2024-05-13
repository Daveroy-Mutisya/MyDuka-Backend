# from datetime import datetime
# from enum import Enum
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.orm import validates
# import re

# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     image = db.Column(db.String(100), nullable=True)
#     role = db.Column(db.String(20), nullable=False)
    
#     # Provide a default value for the entries column
#     entries = db.Column(db.Integer, default=0, nullable=False)


#     @validates('email')
#     def validate_email(self, key, email):
#         assert '@' in email
#         assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Invalid email format"
#         return email
    
#     @validates('password')
#     def validate_password(self, key, password):
#         assert len(password) > 8
#         assert re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter"
#         assert re.search(r"[a-z]", password), "Password should contain at least one lowercase letter"
#         assert re.search(r"[0-9]", password), "Password should contain at least one digit"
#         assert re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password should contain at least one special character"
#         return password

#     def __repr__(self):
#         return f"<User {self.id}, {self.name},{self.role}, {self.email}, {self.password}>"
   


# # Define Product Model
# class Product(db.Model, SerializerMixin):
#     __tablename__ = 'products'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     image = db.Column(db.String, nullable=True)
#     price = db.Column(db.Integer, nullable=False)
#     condition = db.Column(db.String(100), nullable=True)
#     stock_quantity = db.Column(db.Integer, nullable=False, default=0)
#     spoil_quantity = db.Column(db.Integer, nullable=False, default=0)
#     buying_price = db.Column(db.Integer, nullable=False)
#     selling_price = db.Column(db.Integer, nullable=False)

#     # Define the store_id foreign key without backref
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

#     # Define the relationship with backref
#     store = db.relationship('Store', back_populates='products')  # Adding back reference

#     def __repr__(self):
#         return f"Product(name='{self.name}', store_id='{self.store_id}')"




# class Store(db.Model):
#     __tablename__ = 'stores'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     location = db.Column(db.String(100), nullable=False)
    
#     # Define user_id as a foreign key
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
#     # Define the relationship with the User model
#     user = db.relationship('User', backref=db.backref('stores', lazy=True))

#     def __repr__(self):
#         return f"Store(name='{self.name}')"

# # Define PaymentStatus Enum
# class PaymentStatus(Enum):
#     NOT_PAID = 'Not Paid'
#     PAID = 'Paid'


# # Define Payment Model
# class Payment(db.Model, SerializerMixin):
#     __tablename__ = 'payments'
#     id = db.Column(db.Integer, primary_key=True)
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
#     store = db.relationship('Store', backref='payments')
#     status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.NOT_PAID, nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     amount = db.Column(db.Integer)
#     method = db.Column(db.String)
#     due_date = db.Column(db.Date, nullable=False)


# # Define Request Model
# class Request(db.Model, SerializerMixin): 
#     __tablename__ = 'requests'
#     id = db.Column(db.Integer, primary_key=True)
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
#     store = db.relationship('Store', backref='requests')
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     product = db.relationship('Product', backref='requests')
#     quantity = db.Column(db.Integer, nullable=False)
#     requester_name = db.Column(db.String(100), nullable=False)
#     requester_contact = db.Column(db.String(100), nullable=False)
#     status = db.Column(db.String(50), nullable=False, default='Pending')

#     @validates('quantity')
#     def validate_quantity(self, key, quantity):
#         assert quantity > 0, "Quantity must be a positive integer"
#         return quantity

from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), nullable=False)
    
    # Provide a default value for the entries column
    entries = db.Column(db.Integer, default=0, nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Invalid email format"
        return email
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 8
        assert re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter"
        assert re.search(r"[a-z]", password), "Password should contain at least one lowercase letter"
        assert re.search(r"[0-9]", password), "Password should contain at least one digit"
        assert re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password should contain at least one special character"
        return password

    def __repr__(self):
        return f"<User {self.id}, {self.username}, {self.role}, {self.email}, {self.password}>"

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(100), nullable=True)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    spoil_quantity = db.Column(db.Integer, nullable=False, default=0)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship('Store', backref='products')  # Ensure correct back reference

    def __repr__(self):
        return f"Product(name='{self.name}', store_id='{self.store_id}')"

class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('stores', lazy=True))
    
    def __repr__(self):
        return f"Store(name='{self.name}')"

class PaymentStatus(Enum):
    NOT_PAID = 'Not Paid'
    PAID = 'Paid'

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

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        assert quantity > 0, "Quantity must be a positive integer"
        return quantity
