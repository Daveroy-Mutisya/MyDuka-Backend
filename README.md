# MyDuka-Backend
## Project Description: 

"MyDuka" is an inventory management application designed to streamline record-keeping and stock-taking processes for businesses. The application offers a comprehensive solution for generating and visualizing weekly, monthly, and annual reports, empowering business owners to make more informed decisions.

The application features a secure authentication system that allows only the superuser, typically the merchant, to initiate the registration process. The superuser can invite admins by sending tokenized links to their email, enabling them to register within a specified timeframe.

Once registered, admins are tasked with adding data entry clerks who will manage inventory details on the application's dashboard. Clerks can record various details such as the number of items received, payment status (paid or unpaid), current stock quantity, quantity of spoiled items, and buying and selling prices. Additionally, clerks can request additional product supply directly from the dashboard, with these requests routed to the store admin for approval.

Store admins have access to detailed reports on individual entries, allowing them to monitor performance and manage supply requests from clerks. They can also view a comprehensive breakdown of paid and unpaid products, facilitating efficient management of supplier payments. Store admins have the authority to change payment statuses, inactivate or delete clerk accounts, and add new clerks as needed.

Furthermore, the application prioritizes data visualization, presenting reports in easy-to-understand graphical representations such as linear graphs and bar charts. This visual approach enhances decision-making by providing clear insights into store performance and product status.

For merchants, the application offers additional functionalities, including the ability to add, deactivate, or delete admin accounts. Merchants can access store-by-store reports with visually appealing graphs, allowing them to analyze individual store performance and product statuses efficiently.

"MyDuka" aims to revolutionize inventory management for businesses by providing a user-friendly platform for record-keeping, report generation, and data visualization, ultimately empowering business owners to optimize their operations and drive growth.

## Installation Guide
### Prerequisites

- Python (>=3.8)
- pipenv 

### Installation RoadMap
Sure, here's the installation steps formatted for a README:

---

### Installation Steps

1. **Clone the repository:**

    ```
    git clone git@github.com:dmbeastz/MyDuka-Backend.git
    ```

2. **Create a virtual environment and install the project dependencies:**

    ```
    pipenv install
    ```

3. **Activate the virtual environment:**

    *Skip this step if you didn't create a virtual environment.*

    ```
    pipenv shell
    ```

4. **Navigate to the project directory:**

    ```
    cd MyDuka-Backend
    ```

--- 

These steps will guide you through the process of setting up the backend for MyDuka application.

### Diagram

![MyDuka Backend Rep](https://github.com/dmbeastz/MyDuka-Backend/assets/145768413/2426c2b3-2d2b-409e-bdec-d5e38f23caa4)


### Backend Endpoints
#### Authentication:
- POST /register-admin: Initialize the registration process for an admin (superuser only).
- POST /register-clerk: Register a new clerk (admin only).
- POST /signin: Sign in with email and password. Returns access and refresh tokens.

#### Employees:
- GET /admins: Retrieve all admin users (superuser only).
- POST /admins: Create a new admin user (superuser only).
- GET /clerks: Retrieve all clerk users (admin only).
- POST /clerks: Create a new clerk user (admin only).
- GET /user/{id}: Retrieve a user by ID (admin or self only).
- PATCH /user/{id}: Update a user by ID (admin or self only).
- DELETE /user/{id}: Delete a user by ID (admin only).

#### Dashboard (Clerk):
- GET /dashboard: Retrieve dashboard details (clerk only).
- POST /requests: Make a product supply request (clerk only).

#### Store Admin:
- GET /dashboard: Retrieve dashboard details (store admin only).
- GET /reports: Retrieve detailed reports on individual entries (store admin only).
- PATCH /requests/{request_id}: Approve or decline supply requests from clerks (store admin only).
- PATCH /payments/{payment_id}: Change payment status to paid for unpaid products (store admin only).
- PATCH /clerks/{clerk_id}: Deactivate or delete a clerk's account and add new clerks (store admin only).

#### Merchant:
- GET /admins: Retrieve all admin users (merchant only).
- POST /admins: Create a new admin user (merchant only).
- GET /store-reports: Retrieve store-by-store reports in well-visualized graphs (merchant only).
- GET /store/{store_id}/performance: Retrieve individual store performance, including individual product performance (merchant only).
- GET /store/{store_id}/payments: Retrieve paid and unpaid products for each store (merchant only).



