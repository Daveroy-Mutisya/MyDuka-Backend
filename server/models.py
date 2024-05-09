from flask_sqlalchemy import SQLAlchemy

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

    
    # Adds expired, broken and damaged if the store is food, furniture and book respectively
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.set_condition() #this automatically sets the condition of the good when creating a new store instance

    def set_condition(self):
        if 'food'in self.name.lower():
            self.condition = 'expired'

        elif 'furniture' in self.name.lower():
            self.condition = 'broken'

        elif 'books' in self.name.lower():
            self.condition = 'damaged'

        else:
            self.condition = 'unknown'
