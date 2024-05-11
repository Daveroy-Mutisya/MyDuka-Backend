from flask_bcrypt import Bcrypt
from app import app, db
from models import User, Store, Product, Payment, PaymentStatus, Request

bcrypt = Bcrypt(app)

def main():
    with app.app_context():
        # Seeding users
        users = [
            User(username="clerk1", email="clerk1@example.com", password=bcrypt.generate_password_hash("Clerk1pass").decode('utf-8'), role='clerk'),
            User(username="admin1", email="admin1@example.com", password=bcrypt.generate_password_hash("Admin1pass").decode('utf-8'), role='admin'),
            User(username="merchant1", email="merchant1@example.com", password=bcrypt.generate_password_hash("Merchant1pass").decode('utf-8'), role='merchant')
        ]
        db.session.add_all(users)
        db.session.commit()    

        # Seeding stores
        stores = [
            Store(name="Store A", location="Location A", user_id=2),
            Store(name="Store B", location="Location B", user_id=3),
            Store(name="Store C", location="Location C", user_id=3)
        ]
        db.session.add_all(stores)
        db.session.commit()    

        # Seeding products
        products = [
            Product(name="Product 1", price=100, stock_quantity=50, buying_price=50, selling_price=80, store_id=1),
            Product(name="Product 2", price=200, stock_quantity=100, buying_price=120, selling_price=180, store_id=2),
            Product(name="Product 3", price=150, stock_quantity=80, buying_price=90, selling_price=120, store_id=3)
        ]
        db.session.add_all(products)
        db.session.commit()    

        # Seeding payments
        payments = [
            Payment(store_id=1, status=PaymentStatus.PAID, amount=1000, method="Cash", due_date="2024-06-01"),
            Payment(store_id=2, status=PaymentStatus.NOT_PAID, amount=1500, method="Card", due_date="2024-06-05"),
            Payment(store_id=3, status=PaymentStatus.NOT_PAID, amount=2000, method="Cash", due_date="2024-06-07")
        ]
        db.session.add_all(payments)
        db.session.commit()    

        # Seeding requests
        requests = [
            Request(store_id=1, product_id=1, quantity=10, requester_name="John Doe", requester_contact="1234567890", status="Pending"),
            Request(store_id=2, product_id=2, quantity=15, requester_name="Jane Doe", requester_contact="0987654321", status="Approved"),
            Request(store_id=3, product_id=3, quantity=20, requester_name="Alice Smith", requester_contact="9876543210", status="Pending")
        ]
        db.session.add_all(requests)
        db.session.commit()    

        print("Done seeding!")

if __name__ == "__main__":
    main()
