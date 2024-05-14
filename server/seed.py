from flask_bcrypt import Bcrypt
from app import app, db
from models import User, Store, Product, Payment, PaymentStatus, Request
from datetime import datetime, date 


bcrypt = Bcrypt(app)

def main():
    with app.app_context():
        User.query.delete()
        # Seeding users
        users = [

            User(username="Teddy",name = "Teddy Maina" ,email="mainateddy9@gmail.com", password=bcrypt.generate_password_hash("Clerk1@pass").decode('utf-8'), role='clerk', image="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"),
            User(username="Brian", name = "Brian Murigi" ,email="brianmurigi19@gmail.com", password=bcrypt.generate_password_hash("Clerk1@pass").decode('utf-8'), role='clerk', image="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"), 
            User(username="vLeyian", name = "Victor Leyian" ,email="leyianv360@gmail.com", password=bcrypt.generate_password_hash("Clerk1@pass").decode('utf-8'), role='clerk', image="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"),
            User(username="Ronnie", name = "Ronnie Langat" ,email="ronnielangat2020@gmail.com", password=bcrypt.generate_password_hash("Admin1@pass").decode('utf-8'), role='admin', image="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"),
            User(username="Dave Roy ", name = "Dave Roy Mutisya" ,email="daveroymutisya2@gmail.com", password=bcrypt.generate_password_hash("Merchant1@pass").decode('utf-8'), role='merchant', image="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")


        ]
        db.session.add_all(users)
        db.session.commit()

        Store.query.delete()    
        # Seeding stores
        stores = [
  
            Store(name="Quickmart", location="Kilimani", user_id=2),
            Store(name="Naivas", location="Thome", user_id=3),
            Store(name="Carefour", location="Karen", user_id=3)

        ]
        db.session.add_all(stores)
        db.session.commit() 

        Product.query.delete()
        # Seeding products
        products = [
            Product(name="Milk", price=70, stock_quantity=50, buying_price=600, selling_price=670, store_id=1, image="https://i0.wp.com/www.neokingshop.online/wp-content/uploads/2020/07/KCC-gold-crown-log-life-milk-carton.jpeg?fit=302%2C302&ssl=1"),
            Product(name="Salt", price=90, stock_quantity=20, buying_price=90, selling_price=180, store_id=2, image="https://greenspoon.co.ke/wp-content/uploads/2023/10/Greenspoon-Kensalt-2Kg-1.jpg"),
            Product(name="Bread", price=20, stock_quantity=70, buying_price=90, selling_price=120, store_id=3, image="https://www.beeqasi.co.ke/wp-content/uploads/2020/08/SUPERLOAF.jpeg")
        ]
        db.session.add_all(products)
        db.session.commit()  

        Payment.query.delete()
        # Seeding payments
        payments = [
            Payment(store_id=1, status=PaymentStatus.PAID, amount=1000, method="Cash", due_date=datetime.strptime("2024-06-01", "%Y-%m-%d").date()),
            Payment(store_id=2, status=PaymentStatus.NOT_PAID, amount=1500, method="Card", due_date=datetime.strptime("2024-06-05", "%Y-%m-%d").date()),
            Payment(store_id=3, status=PaymentStatus.NOT_PAID, amount=2000, method="Cash", due_date=datetime.strptime("2024-06-07", "%Y-%m-%d").date())
        ]
        db.session.add_all(payments)
        db.session.commit() 

        Request.query.delete()
        # Seeding requests
        requests = [
            Request(store_id=1, product_id=1, quantity=10, requester_name="Victor Leyian", requester_contact="1234567890", status="Pending"),
            Request(store_id=2, product_id=2, quantity=15, requester_name="Teddy Maina", requester_contact="0987654321", status="Approved"),
            Request(store_id=3, product_id=3, quantity=20, requester_name="Brian Murigi", requester_contact="9876543210", status="Pending")
        ]
        db.session.add_all(requests)
        db.session.commit()    

        print("Done seeding!")

if __name__ == "__main__":
    main()
