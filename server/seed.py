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
            User(username="Victor Leyian", email="leyianv360@gmail.com", password=bcrypt.generate_password_hash("Clerk1@pass").decode('utf-8'), role='clerk'),
            User(username="Teddy Maina", email="clerk1@example.com", password=bcrypt.generate_password_hash("Clerk1@pass").decode('utf-8'), role='clerk'),
            User(username="Ronnie Langat", email="admin1@example.com", password=bcrypt.generate_password_hash("Admin1@pass").decode('utf-8'), role='admin'),
            User(username="Dave Roy", email="daveroymutisya2@gmail.com", password=bcrypt.generate_password_hash("Merchant1@pass").decode('utf-8'), role='merchant')
        ]
        db.session.add_all(users)
        db.session.commit()     

        # Seeding stores
        stores = [
            Store(name="Naivas", location="Thika", user_id=2),
            Store(name="Carrefour", location="Karen", user_id=3),
            Store(name="Tuskeys", location="Thome", user_id=3)
        ]
        db.session.add_all(stores)
        db.session.commit()    

        # Seeding products
        products = [
            Product(name="Milk", profit=70, stock_quantity=50, buying_price=600, selling_price=670, store_id=1, image="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxITEhUTEhMVFhUXEhUVFxUYFRYXFhUYFRUXFhUVFRcYHSkgGRomGxUYITEhJSorLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGysjHyUrLS01NTc3LS8tLS0tLS8tLS0tKy0tNTAtLS0tLS0tLS0tLS0tLy0uLS0tLS0tLS0tLf/AABEIAOEA4QMBIgACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAABAUCAwYBB//EAD0QAAEDAgMECAIIBgIDAAAAAAEAAhEDIQQSMQVBUXEGIjJhgZGhscHRBxNCUmJygvAUIzOSouFDslNz4v/EABkBAQADAQEAAAAAAAAAAAAAAAACAwQBBf/EACsRAAICAQQBAwIGAwAAAAAAAAABAhEDEiExQQQTUZEi8DJhccHR4UJSof/aAAwDAQACEQMRAD8A+4IiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAItNXFU29p7RzcAolbblBv255NJ+Ci5RXLOqLZYosKVUOAc0yCJBG9ZqRwIiIAiIgCIiAIiIAiIgCIiAIiIAi8c4DUwo9TaFIavb4GfZcbS5OpNklFWVNt0xoHHkI91GqbeP2WDxPyUHlguySxyfReIubqbXqnQgch85UWpiqjtXu8zHoq35Eeiaws6t9Vo1IHMgKNU2pRH2weUn2XLwmVQfkvpElhXbL6pt6mOy1x8gFFq7ff9ljRzJPyVUQmVVvNN9k1iibsVt2qNXEflaoNXG1XiYebxDnEeN7f780eak2aB3k/JDRqHV4HIeRVTnJ9l8ccEuvv9DSW1D90L1jg2zngme4crLcMIIgkm83Ph5J/Cs+6PG/uo0zrceCbsvaTqJjVhN28O9veuso1WuAc0yDoVxOVS9nY91I2u09pvxHetOLNp2fBlyY73R1yLXQrNe0OaZBWxbTMEREAREQBERAFqr4hjO04CdJ3xw81tXOdJn/zaQ7nesCPMBQyS0xslBW6LOptikNCTyHzhRqm3h9lh8THsqaEDVkeebNCxRLB+2ap0yjw+ajvx1U6vd4W9lohewoPJJ9klCK6MTJ1M+qQsoXsKBIwhIWcJCAxhIWUIEBjCQsoSEBhCQj6jRqQOZAWLa7e88gT66KSxylwiLnFcsyXiya7uPjAXsruhrljXfBqe8DUrUa7Vrr4N5uKkD8o91DqU2AHM/OQ2Yy23xJ3XC14sfjvZ6m/+fyYcmXyr+mKSLClXY6QDp+/gshOoHqFXYUPc2GNawXzG4Jkx1ZBuIvbfxBCsMPRLRBM/Abhe6ryxhDirNGL1JR+t/BL2fjX0nTbL9pt/O+hXU4eu17Q5pke3ce9ceWqRgMW6k6RcHUcf996hjztOnwSlivdcnWotWGxDXtzNNvUdxW1bE7M4REXQEREAXNdNgQ2jUH2ahaf1Cfdi6VVXSjD58NUG9oDx+ghx9AVDIri0Sg6aKJrpAI3iVkoeyqoNMd1vJSqtVrRL3Bo4kgD1XnGwzheqsO3qMkMz1CBoxtv7nQPVeM2jXdZmHy/+2q1l7bmB53ny8VNYptWkQeSKdNlrCBQM1Y/bYBGjabnEH87nAH+1KeCfq6rVdzeGAchRa33UvRl3sc9WPW5YEb93FRzi6emYE8G9Y+TZXjMI0fPU+LnSTrxW0Uhw+Kaca5l8f2c1ZHwvk1/xIOjXHwA9HEFRqm0gOA5mSOYHzU75bgoTsXTjMWEyJEhsuAIabk2IJAIMRN1bjcP8YX+v8bFWWOVraSRo/jS42cT4QPYrLWS9wDRYy86xN7xxWyg6pUBgBjYscsE7tJkWMjgRBkXd5g9lNA/mCbkZYGUgGzgBpYSBNpIECw0yzpLek17ff7meHiSbuUmzPCup5nBrQNIMROsyItcGx13KbCyZTAEAAaad1gvcqwZZ63tdG+EFFGBC8hbISFUTK6pswF2pykkkXkyCIzT2ZMwZggRC24fBsp9kR3/vTkOA4KZCjVwGnMYiLzFvxCfVWSyzapsRhGw1zR2eJ7Im51NlrqYlo1tzIHdoJPotVamB2nuPV3AiQD1u0Ym2nCbL2nSaCIYS0gmSSYsBcHjv5KptmhY4JWH4vcLngBfcZkxNjOhXtMkmHNcO/NY8IiP3Cxa1+mZo07A8dBf1QYOTJzE8SYGs21I0XNyTUETsDjHUnfuHD5rqcLiW1G5m+I3g8CuP+pMRMeZPOSfgpeFxLqZzNPMbj3FaMWVw2fBjy41LdcnVotGDxTajZb4jeCt63Jp7oxtUERF0BY1aYcC06EEHkRCyRAfLaJqMc5jC1rpLS5wLgC0xOUEXXjMEw9avUNRxvcABv5QNPElTukmGy4isOPWH6gHH1lKD6TQGtYHPImDJ1sCbaTqRMTzivDUE2o277I+RHLNpRlSPKdS38vK1otJEDwJgLbQqBh6zvrKhaCACAIOhBNu/9wcq2DqVMuYgCQcoEFsgTvIkESDeZgyCVMFBtJktbpym5k33C5MDyTL5KaVvf8roYfCqVvd/fRhgHuLesDMyDBAcDoQCSRy+ClwobsU8jqsBkAizjfNlcDpELF7azgb5L8WwBYRYTNzv3DivPnNSd0erHC0qbROjetbqzRMkWvxgWvbmFFxDWOy5niQACGy6esIjhOnitNI0Gnq5id1y37PG25sEfhULJxwprv4JlXGNaGuvDhIMbrTr3GeQK00qpMvZSAJdlJ3zG+BpIglS8KWOYMotoBuEcJ91tLgNT6qSv3INxW2nc04V7iDmblM8pEA6T3x4LfC1srtdo4G02O6SJ8wVCO2mSIa4yOEXuMsHfIIjiNy6R0uT2RYrwkKsrV6zw/IIiMsGQ4FoMtMDiYvqBPBeNwdctguAMtdmaYjTM2ABIt6xuXRofDdE6riGgxv3DSbSIlY/Wk9mNPWAY8itI2ZJBc64cXAgAGT3mbQSI7+4KaxkW/fouJnJpLh2aaT3HUWPhALQY85C1nCXnNxBgdoaNkngFLKFdshRFpYbLYF0cLW7tFn9Q3hPO/utx4+qiV9pUWa1G+Bn2XKJamSAEhUuI6TUx2Gl3ebBVeK6Q1naENHcPiV2jlnWFQMVtKkztOk/daJPouPq4l7+25x5klaQ4B0DXVNJyzvei21TWxIYxha0Nc5xJ1AsLDvIXbrh/o1w39ar3tYP+zvdq7hbcCqBmyO5BERXFYREQHJdMKH86k/7zSw+B/8AtVOw4HjE+VvIj1XTdMaM0A4ase13gbe5C5XBHLUIG+Y88zPYLPl2TLYcov1kEbcT3SsoWSjRZBaKzmuB6ptlOmh0teLa/iUarRBnPVA6sQCXGJPEyTdpniFMrYTM+Z6sQWm4Ougi27esW7OZaZNhPAw0tnyMKLRqjkiu/hGmg2kSGgOdZ1zMQ49Yce0066HetBxZa8NbSA1BNyQQ4gyeZmeDlaNwzAZDROsxJniJ5LaQiRCWVP3KumK7nODiQwgw4EAt0giOZ14LyrsovILnRYC2YmNTBcbTLu6DG6Vawsajw0S4gDiSB7rpWsrXBDobMY3e483EbmiOrFuqFIZh2AkhoBNyYEnmdSotbbeHbrUB/KC72sq6v0spjsMc7mQ0fFdoi5t8s6BIXIVuldU9lrB4E+squrbYrv1qO5Ax7QmkjZ3deuxgl7mt5kBVmI6RUG6Fzj+EW8yuLLibyvF3SLOmr9Kj9imObjPoFArdIq7t4HIAeuqpalSNxJOgH70UavWLQMzgCTAaPO7nfIKccbZFyos62Ke7tOceZJWmVAbXaIl2Z0nzAkxu8UbjiSA0C51PC0wOXuOKl6bOa0S3VTMN3anQDn39yjOrkkjPDQYcQAJPATPnu9siwukNnKZl1t5k5OJ7zYeC0NwzMzQXNBiAwHTQgAb4uSTqb7grIxiuSEmzfUxDWzG4Trckza/5TJWeEBy5ndpxk/AdwhV7q9IVCxrXVH2GsgZbxJ0A38ryrhjC4gDUwAO8qOSOlcckoOz6p0Hw2TB0+Ly55/Uer/iGq+WrCUBTYxg0axrRyaAPgtq1RVJIobthERdOBERARdqUPrKNRnFhjnqPVfPnOOUO0LY82/6hfS1wPSHDfV1Xt+y8EcswsfX0VeRbE4clhgqsjuiRyO7vhSQFyLOkJw7Q0sLjFhMAX4+KjVumFd3ZYxnm4/JYdJos7gLCtWawS9waPxED3XzrEbZxD+1VdyByjyaoRJJkmV3SLO+xHSTDt0cXn8I+JgKrxPS8/wDHTA73GfQLkauIa2xN9YFzHEjcO82VdiNuNGkf9j6EN8nFWwwSnwiEskY8nV4nb+If/wAhA4N6vsq6pUc4ySSe8yuWq7aedJ84/wCoB9Vp/j6h3jxc7d+Zy0LwZdsqfkLo62V6Fy9OvVyh3E2HXaSAJLpDha481YYHaJmCZAcGuvMZjAc1wAkSQCCJvqoz8VxVp2djmTe5cheogWUuPF6UK042sWU3OGoaSJ0ndK6lboN0rMKrpuLmIGU6T3j4qJiaIacznNaSN8eAA3ga95jhCrcLtSq6qzM62YAgAAXt8Vr2vWzVncB1R4a+srdDx5xlpvozSyxcbJ9XFUmNBgvzSBu7JuL3ideMlasVtItDcjWiWZrjMRJNvj4qBizDaY4Mn+5xPyW3Etms1m4fVt8g0H4q2OGNpvfkreR9fkdQww0F25oJPIXXG08QWuLx2jmvwzakd9yul2hjmfV1GteCchsDMT1dRbUhUuCwGelUcAS4EZRyu4RvsQoeKlCMpTXNInnuTSiWfR2i36vMLuJIPdGg9j4rreiWF+sxdIbg7Of0DN7gLkdgYaqzNmbDSBqbyO7l7L6V9G2FmrVqfdYGjm8z7M9VnzK83NlsHWPg+gIiK8qCIiAIiIAuc6Z4PNTzjUW+I+PmujUfH0M9Nzd5FuYuPVcatUdTo+NbWHZPNQArbatOxH3Xen7IVUQZWLjY0chzgBJsALngq3E41xsy1ibnKSAJJJ1aI3C9xMSpO0tG8M4mdNCWz3Zsq52hjHAOBzEkEDrREmXHSZJWnDCOnUyjLk0ujOvh3usSCIa6BIAz6S0iS7zKwbhOrmBzAGCGi4Noud19e4rx+JeYvEZYgaZezc6xJ8ytTw4zJ1WpZ0trMjnEm1hTDcoc03JEkz1j1T1dYAFvxLFuJaDZhjqyPs9qXAEiYMN1B3qB9WR/pTMNg6rjAHmL+Q08YC5KTauLQ1Sf4UevxLiIgRBG8ky7PJ0vKsdi4E9p2kiebTIb53PCAOMScFsgCC8+X7t4eatQ0AQAABw0CySzuqTNGLDK9UxK9AUNlYPqOaW9jQ/6VhSpOccrQSTuCplBxpPk0xknuYFQNtOii/8ASPNwXW4bBMowXdeodGjdy+aqOkuzQ9nVIaXEEjUC89WPBWwxuLUn7kZTtNI4NrSAHj7xHi3KfivatOGtJ1dmPhMD1BXRUdjsyBjiXQ4u4aiI5WUkU6TYs0ZW2mJAHO61T82Ke25THxpMoquCe6o0BpIAptmLQGibnxUl+xHve5znAAuJtcwTZWZxoNmg5pAAILdQTNxpAK1fxryOq0TAO86vLbRutMrM/Ml1saV4d8jDbIpMEXdNjmOsGdBy9FOp02tENAA4AQotGm8vBf8AZNSNJvAbYdwPmpj3gakDmqZZJT5dk3CMOD0BfSvo/wANlwub/wAlRzvBvUHq0+a+asdIkL7JsfC/VUKVP7tNoPOL+sqeFfUVZXsTERFqKAiIgCIiAIiID5n0pwRp4moIs+XN7wRMeBkeC5ioLL6Z07w00mVI7LwCeAcCB/lA/Uvm1YQSO8rJmVSL8b2IxbIg6cFXVdjUzoSO7UfP1VivQoKbXB2UIy5RUjYg+96f7WbNit3u8hHuSrJ7gASdBdaquLY2JMSJAgye6OKmnOXCK3ixLlGFHZ1Nu6eZ+AgI7GMbIaCcuoaLN56BYVMb/UHYIaC2dTInTjuUYMzlj8heHshwBjrNtfuV8MTe+Tj7ZCU0toE+rjQGtMXdoDaLSS47go1eq91MOJaLmW36/wB0Rrfgt1HZwyZXiesXRJhs7gdYUylSa0Q0AfPio68cPwq3ZLTOfOyoi0KL87XkATTyuE6XkQuq2JXZlLQA2pxP2uR+Co16CqvVeq6LFjVUXeOxLactHWeRc/A8B3clTVHl0kla3vAuT4laTiJHVBPoPMpOUpnYpRNwVdSwBIOYxIIMGZJMybAKX1zGg9TKtMF0ZxVa4pVCLXd1G8+tE+qr0WWLK4rYpqlJg7fWJM31JiNAsxVP2Wx3mw8tV3WB+j55j62q1o+6wFx8zAHkVf4HoZhKerDUPF5n/EQ30VkcL9iuWW+z5ZhsPUq9VuZx4UwSeVpKv8B0KxLzJptZ+Kob+Ql3mAvqNDDsYMrGtaODQAPILYrVi92VvIcfs/oIxpBq1S4gg5WgNaYMwZkkeS7BEVkYqPBBtvkIiKRwIiIAiIgCIiA0Y3DCpTcx2jmkfI+a+O7ToltVzSLg+osfZfaV80+kDA5MQHgWqNnxGvz8VTmW1lmN7nEY3EOY5oDR1jGYmwPeAsTXqMe1r8pDjAIBBB75UjHYfO0t37jwI0WNDDGQ55zOAgWgN4wOPeoxlDRuvf8AoSU9WxXDGvzBwdmGaC2BJG9waBIHMqRRwT7A2yVCWuN5ablWLWAaAXXj6zRqQFJ5+oKjiw/7OzCtRnrBrS8aF27xWWDoZGBszG/iSZKCvOjSe+IHqlOnVeYGv3WguP78FTctOlltK7NrlrdXbuv3C/tzVzgOhmKq3NMgEa1XZR/br6LpcB9HrR/Vq/pptA/yd8gurG2cc0fP/rXnRsfmN/IKZhdnVqrv5bHv7mtJHif9r6rgei+Epdmi1x4v65/ysPBW7WgCAIHBWLCReQ+Y7O6A4h3ayUx+I53eQkeoXR4LoHh2/wBR76h4dhvkL+q6xFNY4kNbIeC2VQpf06TG94Azf3G6mIimlREIiLoCIiAIiIAiIgCIiAIiIAiIgC5vp7gs+GzgXpuDv0mzvcHwXSLXiKIexzHaOaWnkRBXJK1R1OmfDapiYEngtXX3lrfMn1hfScF9H9IGa1V7zwaAxvjqfULocDsPDUv6dFgI+0Rmd/c6Ss8cUi15EfJsD0fxFaMlOq8Heeq3zMCF0Wz/AKPapvUfTp9zQXu5HQDzK+kIrFiXZDW+jmsD0IwjO0HVD+N1v7WwPOVfYXB06YimxrBwa0D2W9FNRS4ItthERSOBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREB//2Q=="),
            Product(name="Sugar", profit=200, stock_quantity=100, buying_price=120, selling_price=180, store_id=2, image=""),
            Product(name="Bread", profit=150, stock_quantity=80, buying_price=90, selling_price=120, store_id=3, image=""),
            Product(name="Cooking Oil", profit=150, stock_quantity=80, buying_price=90, selling_price=120, store_id=3, image=""),
            Product(name="Jik", profit=200, stock_quantity=100, buying_price=120, selling_price=180, store_id=2, image=""),
            Product(name="Tomato Sauce", profit=150, stock_quantity=80, buying_price=90, selling_price=120, store_id=3, image=""),
            Product(name="Yoghurt", profit=200, stock_quantity=100, buying_price=120, selling_price=180, store_id=2, image=""),
            Product(name="Downy", profit=150, stock_quantity=80, buying_price=90, selling_price=120, store_id=3, image=""),
            Product(name="Rice", profit=200, stock_quantity=100, buying_price=120, selling_price=180, store_id=2, image=""),
            Product(name="Eggs", profit=150, stock_quantity=80, buying_price=90, selling_price=120, store_id=3, image=""),
            Product(name="Omo", profit=200, stock_quantity=100, buying_price=120, selling_price=180, store_id=2, image=""),
        ]
        db.session.add_all(products)
        db.session.commit()    

        # Seeding payments
        payments = [
            Payment(store_id=1, status=PaymentStatus.PAID, amount=1000, method="Cash", due_date=datetime.strptime("2024-06-01", "%Y-%m-%d").date()),
            Payment(store_id=2, status=PaymentStatus.NOT_PAID, amount=1500, method="Card", due_date=datetime.strptime("2024-06-05", "%Y-%m-%d").date()),
            Payment(store_id=3, status=PaymentStatus.NOT_PAID, amount=2000, method="Cash", due_date=datetime.strptime("2024-06-07", "%Y-%m-%d").date())
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
