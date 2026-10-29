# NovaStore - Simple E-commerce Store Web Application

A full-featured, responsive, and modern E-commerce Store web application built with **Python Flask**, **SQLite / MySQL**, **HTML5**, **CSS3**, and **Bootstrap 5**.

Developed as a college mini-project with an emphasis on clean architecture, responsive design, data validation, and intuitive administration.

---

## 🌟 Key Features

### 👤 Customer Features
1. **User Registration & Security**:
   - Register with Name, Email, Password, Phone Number, and Default Delivery Address.
   - Client-side & Server-side validation with duplicate email prevention.
   - Secure password hashing using PBKDF2 with SHA-256 (`werkzeug.security`).
2. **Authentication & Session**:
   - Secure login and logout with session state persistence.
   - 1-Click demo login buttons for rapid testing/evaluation.
3. **Product Catalog & Discovery**:
   - Dynamic product listing with responsive cards, badges, and pricing.
   - Category filtering (Electronics, Fashion, Home & Living, Accessories, etc.).
   - Keyword search across product titles and descriptions.
   - Sorting by Price (Low to High, High to Low), Newest, and Alphabetical.
4. **Product Details Page**:
   - Full product description, category tag, high-res image preview.
   - Real-time stock status indicator (*In Stock*, *Low Stock*, *Out of Stock*).
   - Quantity selector with maximum stock constraints.
   - Similar / Related products recommendations.
5. **Shopping Cart Management**:
   - Add items directly from catalog or detail page.
   - Real-time cart badge counter in the navigation bar.
   - Inline quantity increase/decrease buttons with instant subtotal calculation.
   - Remove individual items or clear entire cart.
   - Automated shipping cost calculation (Free shipping over ₹499).
6. **Checkout & Order Processing**:
   - Pre-filled customer shipping details (editable at checkout).
   - Choice of payment methods: Cash on Delivery (COD), Credit/Debit Card (simulated), UPI/Digital Wallet.
   - Stock verification prior to final order confirmation.
7. **Order Confirmation & Invoicing**:
   - Printable invoice receipt with Order ID, itemized totals, and tracking status.
8. **Order History**:
   - Collapsible historical orders with dates, delivery destinations, and color-coded status badges (*Pending*, *Shipped*, *Delivered*, *Cancelled*).
9. **User Profile**:
   - Update personal contact information, default delivery address, or change password.

### 🛠️ Admin Management Portal
1. **Admin Authentication**:
   - Role-based access control (`@admin_required` decorator).
2. **Executive Dashboard**:
   - High-level KPIs: Total Revenue, Total Orders, Active Products, Low Stock Alerts, Registered Customers.
   - Recent customer orders table with inline status update dropdown.
3. **Product & Inventory Management**:
   - View all products with stock indicators and thumbnail previews.
   - Add new products with file upload or default vector illustrations.
   - Edit product name, category, price, stock quantity, and description.
   - Delete products with confirmation alert.
4. **Order Management**:
   - Filter customer orders by status (*All*, *Pending*, *Shipped*, *Delivered*, *Cancelled*).
   - Update order fulfillment status inline with database synchronization.
   - View customer contact and delivery address for shipping.
5. **Customer Directory**:
   - List registered customers with lifetime order counts, total spent, and join date.

---

## 📁 Project Folder Structure

```
e commerce store/
├── app.py                      # Main Flask application and route handlers
├── config.py                   # Configuration settings (Secret key, DB path, uploads)
├── db.py                       # Database connection, initialization, and seeding
├── schema.sql                  # SQLite DDL creation script
├── schema_mysql.sql            # MySQL DDL creation script (for phpMyAdmin / CLI)
├── generate_assets.py          # Vector SVG product illustration generator
├── test_workflow.py            # Automated end-to-end integration test suite
├── requirements.txt            # Python dependencies
├── README.md                   # Installation & execution manual
├── PROJECT_DOCUMENTATION.md    # College mini-project technical report (ER, Use Case, Schema)
├── static/
│   ├── css/
│   │   └── style.css           # Custom modern styles, animations & design system
│   ├── js/
│   │   └── main.js             # Form validation, autofill helpers, toasts
│   └── uploads/                # Product image repository (includes 13 sample SVGs)
└── templates/
    ├── base.html               # Shared layout (Navbar, Footer, Cart Counter, Flashes)
    ├── index.html              # Home page with hero, categories & featured items
    ├── products.html           # Catalog page with search, filters & sort
    ├── product_detail.html     # Single product preview with quantity selector
    ├── cart.html               # Shopping cart table & summary
    ├── checkout.html           # Shipping address & order confirmation
    ├── order_success.html      # Order receipt / printable invoice
    ├── orders.html             # Customer past order history
    ├── login.html              # Login page with 1-click test credentials
    ├── register.html           # Registration form
    ├── profile.html            # Profile & password management
    └── admin/
        ├── layout.html         # Admin sidebar & portal layout
        ├── dashboard.html      # Metrics overview & recent orders
        ├── products.html       # Inventory management table
        ├── product_form.html   # Add / Edit product form
        ├── orders.html         # Customer order management & status updater
        └── customers.html      # Registered customer directory
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Step 1: Open Terminal in Project Directory
```bash
cd "c:\Users\user\Desktop\e commerce store"
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

*Note: On first launch, `ecommerce.db` is automatically created and populated with sample users, products, and initial demo orders. No manual database setup is required!*

### Step 4: Open in Your Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Default Login Credentials

For demonstration and testing purposes, pre-configured accounts are provided:

| Role | Email | Password | Access |
|---|---|---|---|
| **Store Administrator** | `admin@ecommerce.com` | `admin123` | Full access to Admin Portal (`/admin`) and Store |
| **Demo Customer** | `john@example.com` | `password123` | Shopping cart, checkout, order history |

> **Pro-Tip**: On the **Sign In** page, click the **Admin** or **Customer** 1-click buttons to instantly autofill the credentials!

---

## 🗄️ Database Setup Options

### Option A: SQLite (Default - Recommended for instant running)
- Zero configuration required. The file `ecommerce.db` is managed locally in the project root.
- Schema is defined in `schema.sql`.

### Option B: MySQL (For College Evaluation)
If your college evaluator specifically requests a MySQL database:
1. Open **phpMyAdmin** or MySQL CLI.
2. Run the `schema_mysql.sql` script to create the `ecommerce_db` database and tables:
   ```bash
   mysql -u root -p < schema_mysql.sql
   ```
3. All table schemas and foreign key constraints are identical between SQLite and MySQL.

---

## 🧪 Running Automated Tests

An automated test suite is included in `test_workflow.py` verifying all 12 core user and admin flows:
```bash
python test_workflow.py
```
Expected output:
```
=== Running Complete End-to-End Test Suite ===
[PASS] 1. Customer login successful
[PASS] 2. Add to cart successful (Product #2, Qty 2)
[PASS] 3. Cart page displays product and calculates subtotal
[PASS] 4. Checkout successfully confirmed and placed order
[PASS] 5. Customer order history verified
[PASS] 6. Customer logged out
[PASS] 7. Admin login successful
[PASS] 8. Admin dashboard metrics loaded
[PASS] 9. Admin added new product successfully
[PASS] 10. Admin customer list verified
[PASS] 11. Admin product view and catalog verification verified
[PASS] 12. Admin order status successfully updated to Shipped
=== ALL 12 TESTS PASSED CLEANLY! ===
```

---

## 📄 License & Attribution
Designed and built for educational mini-project submission. Free to use, adapt, and expand.
