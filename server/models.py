from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy import Numeric
import datetime

db = SQLAlchemy()

# Define User Model
class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Superuser, Admin, Clerk, Merchant
    # Add other relevant fields

# Define Product Model
class Product(db.Model):
    _tablename_ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('Store', backref='products')
    # Add other relevant fields

# Define Store Model
class Store(db.Model):
    _tablename_ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(100), nullable=True)
    payment_status = db.Column(db.String(20), default="Not Paid", nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_amount = db.Column(Numeric(10,2), nullable=True)
    payment_method = db.Column(Enum('N/A', 'Bank transfer', 'Mpesa', 'Credit'), nullable=False , default = 'N/A')
    payment_due_date = db.Column(db.Date, nullable=False)


    def __init__(self, name, location, payment_status = "Not Paid", payment_method=None, payment_date=None, payment_due_date=None):
        self.name = name
        self.location = location
        self.set_condition() #this automatically sets the condition of the good when creating a new store instance
        self.payment_status = payment_status # adds whether the item has been paid for or not
        if payment_method is not None:
            self.payment_method = payment_method # adds how the item was paid for
        self.set_payment_dates(payment_date, payment_due_date)  # Set payment dates

    
    # Adds expired, broken and damaged if the store is food, furniture and book respectively
    def set_condition(self):
        if 'food'in self.name.lower():
            self.condition = 'expired'

        elif 'furniture' in self.name.lower():
            self.condition = 'broken'

        elif 'books' in self.name.lower():
            self.condition = 'damaged'

        else:
            self.condition = 'unknown'


    def set_payment_dates(self, payment_date=None, payment_due_date=None):
        # Set default payment date to current date if not provided
        if self.payment_status != "Not Paid" and payment_date is None:
            self.payment_date = datetime.datetime.now().date()
        else:
            self.payment_date = payment_date

        # Set default payment due date to 30 days from the current date if not provided
        if payment_due_date is None:
            self.payment_due_date = datetime.datetime.now().date() + datetime.timedelta(days=30)
        else:
            self.payment_due_date = payment_due_date


    



    
    
    
