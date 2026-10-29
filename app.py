import os
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, g, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from db import get_db, close_db, init_db

app = Flask(__name__)
app.config.from_object(Config)

# Register teardown
app.teardown_appcontext(close_db)

# ---------------------------------------------------------
# Helper Functions & Decorators
# ---------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Admin login required.', 'warning')
            return redirect(url_for('login', next=request.url))
        if session.get('role') != 'admin':
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Context Processor for dynamic cart badge count and categories
@app.context_processor
def inject_global_data():
    cart_count = 0
    if 'user_id' in session:
        db = get_db()
        cur = db.execute("SELECT SUM(quantity) as total_qty FROM cart WHERE user_id = ?", (session['user_id'],))
        row = cur.fetchone()
        if row and row['total_qty']:
            cart_count = row['total_qty']

    # Get unique categories
    db = get_db()
    categories_rows = db.execute("SELECT DISTINCT category FROM products ORDER BY category ASC").fetchall()
    categories = [row['category'] for row in categories_rows]

    return {
        'cart_count': cart_count,
        'global_categories': categories,
        'current_user': {
            'id': session.get('user_id'),
            'name': session.get('user_name'),
            'email': session.get('user_email'),
            'role': session.get('role')
        } if 'user_id' in session else None
    }

# ---------------------------------------------------------
# Customer & Public Routes
# ---------------------------------------------------------

@app.route('/')
def index():
    """Home page with hero banner, featured categories, and top products."""
    db = get_db()
    featured_products = db.execute(
        "SELECT * FROM products ORDER BY product_id ASC LIMIT 8"
    ).fetchall()
    
    categories = db.execute(
        "SELECT category, COUNT(*) as count FROM products GROUP BY category"
    ).fetchall()
    
    return render_template('index.html', products=featured_products, categories=categories)

@app.route('/products')
def products():
    """Product catalog with search, category filtering, and sorting."""
    db = get_db()
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    sort = request.args.get('sort', 'newest')

    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    if query:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])

    if category:
        sql += " AND category = ?"
        params.append(category)

    if sort == 'price-low':
        sql += " ORDER BY price ASC"
    elif sort == 'price-high':
        sql += " ORDER BY price DESC"
    elif sort == 'name-asc':
        sql += " ORDER BY name ASC"
    else:  # newest / default
        sql += " ORDER BY product_id DESC"

    products_list = db.execute(sql, params).fetchall()

    return render_template(
        'products.html',
        products=products_list,
        current_query=query,
        current_category=category,
        current_sort=sort
    )

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product details page."""
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
    
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('products'))

    # Fetch related products from the same category
    related_products = db.execute(
        "SELECT * FROM products WHERE category = ? AND product_id != ? LIMIT 4",
        (product['category'], product_id)
    ).fetchall()

    return render_template('product_detail.html', product=product, related_products=related_products)

# ---------------------------------------------------------
# Authentication Routes
# ---------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Customer registration route."""
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        # Validation
        if not name or not email or not password:
            flash("Name, Email, and Password are required.", "danger")
            return render_template('register.html', name=name, email=email, phone=phone, address=address)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('register.html', name=name, email=email, phone=phone, address=address)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('register.html', name=name, email=email, phone=phone, address=address)

        db = get_db()
        existing_user = db.execute("SELECT user_id FROM users WHERE email = ?", (email,)).fetchone()
        if existing_user:
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for('login'))

        hashed_pw = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (name, email, password, phone, address, role) VALUES (?, ?, ?, ?, ?, 'customer')",
            (name, email, hashed_pw, phone, address)
        )
        db.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User and Admin login route."""
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        next_url = request.form.get('next') or request.args.get('next')

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template('login.html', email=email)

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['role'] = user['role']

            flash(f"Welcome back, {user['name']}!", "success")

            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))

            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password. Please try again.", "danger")
            return render_template('login.html', email=email)

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout current user."""
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page to view and update details."""
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE user_id = ?", (session['user_id'],)).fetchone()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')

        if not name:
            flash("Name cannot be empty.", "danger")
            return render_template('profile.html', user=user)

        if new_password:
            if not current_password or not check_password_hash(user['password'], current_password):
                flash("Current password is required and must be correct to change password.", "danger")
                return render_template('profile.html', user=user)
            if len(new_password) < 6:
                flash("New password must be at least 6 characters.", "danger")
                return render_template('profile.html', user=user)
            hashed_pw = generate_password_hash(new_password)
            db.execute(
                "UPDATE users SET name = ?, phone = ?, address = ?, password = ? WHERE user_id = ?",
                (name, phone, address, hashed_pw, session['user_id'])
            )
        else:
            db.execute(
                "UPDATE users SET name = ?, phone = ?, address = ? WHERE user_id = ?",
                (name, phone, address, session['user_id'])
            )

        db.commit()
        session['user_name'] = name
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

# ---------------------------------------------------------
# Shopping Cart Routes
# ---------------------------------------------------------

@app.route('/cart')
@login_required
def cart():
    """View shopping cart."""
    db = get_db()
    cart_items = db.execute("""
        SELECT c.cart_id, c.quantity, p.product_id, p.name, p.price, p.image, p.stock, p.category,
               (c.quantity * p.price) as subtotal
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = ?
        ORDER BY c.cart_id DESC
    """, (session['user_id'],)).fetchall()

    subtotal = sum(item['subtotal'] for item in cart_items)
    shipping = 0.0 if (subtotal >= 499 or subtotal == 0) else 49.0
    grand_total = subtotal + shipping

    return render_template(
        'cart.html',
        cart_items=cart_items,
        subtotal=subtotal,
        shipping=shipping,
        grand_total=grand_total
    )

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add item to shopping cart."""
    if 'user_id' not in session:
        flash("Please log in to add items to your shopping cart.", "warning")
        return redirect(url_for('login', next=request.referrer or url_for('products')))

    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    db = get_db()
    product = db.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('products'))

    if product['stock'] <= 0:
        flash(f"Sorry, '{product['name']}' is out of stock.", "danger")
        return redirect(request.referrer or url_for('products'))

    # Check existing item in user's cart
    existing_item = db.execute(
        "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
        (session['user_id'], product_id)
    ).fetchone()

    if existing_item:
        new_quantity = existing_item['quantity'] + quantity
        if new_quantity > product['stock']:
            flash(f"Only {product['stock']} units available in stock. Cart updated to maximum available.", "warning")
            new_quantity = product['stock']
        else:
            flash(f"Updated quantity for '{product['name']}' in cart.", "success")
        db.execute("UPDATE cart SET quantity = ? WHERE cart_id = ?", (new_quantity, existing_item['cart_id']))
    else:
        if quantity > product['stock']:
            quantity = product['stock']
            flash(f"Only {product['stock']} units available. Added maximum stock to cart.", "warning")
        else:
            flash(f"Added '{product['name']}' to your cart!", "success")
        db.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (session['user_id'], product_id, quantity)
        )

    db.commit()
    return redirect(request.referrer or url_for('cart'))

@app.route('/cart/update/<int:cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    """Update item quantity in cart."""
    action = request.form.get('action')  # 'increase', 'decrease', or 'set'
    db = get_db()

    cart_item = db.execute("""
        SELECT c.*, p.stock, p.name FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.cart_id = ? AND c.user_id = ?
    """, (cart_id, session['user_id'])).fetchone()

    if not cart_item:
        flash("Cart item not found.", "danger")
        return redirect(url_for('cart'))

    if action == 'increase':
        new_qty = cart_item['quantity'] + 1
    elif action == 'decrease':
        new_qty = cart_item['quantity'] - 1
    elif action == 'set':
        try:
            new_qty = int(request.form.get('quantity', 1))
        except ValueError:
            new_qty = 1
    else:
        new_qty = cart_item['quantity']

    if new_qty <= 0:
        db.execute("DELETE FROM cart WHERE cart_id = ?", (cart_id,))
        flash(f"Removed '{cart_item['name']}' from cart.", "info")
    elif new_qty > cart_item['stock']:
        flash(f"Cannot exceed available stock ({cart_item['stock']} items).", "warning")
        db.execute("UPDATE cart SET quantity = ? WHERE cart_id = ?", (cart_item['stock'], cart_id))
    else:
        db.execute("UPDATE cart SET quantity = ? WHERE cart_id = ?", (new_qty, cart_id))

    db.commit()
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:cart_id>', methods=['POST', 'GET'])
@login_required
def remove_from_cart(cart_id):
    """Remove item from cart."""
    db = get_db()
    db.execute("DELETE FROM cart WHERE cart_id = ? AND user_id = ?", (cart_id, session['user_id']))
    db.commit()
    flash("Item removed from your cart.", "info")
    return redirect(url_for('cart'))

@app.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    """Clear all items from cart."""
    db = get_db()
    db.execute("DELETE FROM cart WHERE user_id = ?", (session['user_id'],))
    db.commit()
    flash("Your shopping cart has been cleared.", "info")
    return redirect(url_for('cart'))

# ---------------------------------------------------------
# Checkout & Orders Routes
# ---------------------------------------------------------

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page to enter shipping details and confirm order."""
    db = get_db()
    cart_items = db.execute("""
        SELECT c.cart_id, c.quantity, p.product_id, p.name, p.price, p.stock, p.image,
               (c.quantity * p.price) as subtotal
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = ?
    """, (session['user_id'],)).fetchall()

    if not cart_items:
        flash("Your cart is empty. Please add items before checking out.", "warning")
        return redirect(url_for('products'))

    user = db.execute("SELECT * FROM users WHERE user_id = ?", (session['user_id'],)).fetchone()
    subtotal = sum(item['subtotal'] for item in cart_items)
    shipping = 0.0 if subtotal >= 499 else 49.0
    grand_total = subtotal + shipping

    if request.method == 'POST':
        shipping_name = request.form.get('shipping_name', '').strip()
        shipping_phone = request.form.get('shipping_phone', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', 'Credit Card')

        if not shipping_name or not shipping_address or not shipping_phone:
            flash("Please complete all shipping address fields.", "danger")
            return render_template(
                'checkout.html',
                cart_items=cart_items,
                subtotal=subtotal,
                shipping=shipping,
                grand_total=grand_total,
                user=user
            )

        # Validate stock availability for each item
        for item in cart_items:
            if item['quantity'] > item['stock']:
                flash(f"Insufficient stock for '{item['name']}'. Only {item['stock']} available.", "danger")
                return redirect(url_for('cart'))

        full_shipping_info = f"{shipping_name} | Phone: {shipping_phone} | Address: {shipping_address} (Paid via {payment_method})"

        # 1. Create order
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, shipping_address, status)
            VALUES (?, ?, ?, 'Pending')
        """, (session['user_id'], grand_total, full_shipping_info))
        order_id = cursor.lastrowid

        # 2. Transfer cart items to order_items & decrement stock
        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (order_id, item['product_id'], item['quantity'], item['price']))

            cursor.execute("""
                UPDATE products SET stock = stock - ? WHERE product_id = ?
            """, (item['quantity'], item['product_id']))

        # 3. Clear user's cart
        cursor.execute("DELETE FROM cart WHERE user_id = ?", (session['user_id'],))
        db.commit()

        flash(f"Order #{order_id} placed successfully! Thank you for your purchase.", "success")
        return redirect(url_for('order_success', order_id=order_id))

    return render_template(
        'checkout.html',
        cart_items=cart_items,
        subtotal=subtotal,
        shipping=shipping,
        grand_total=grand_total,
        user=user
    )

@app.route('/order-success/<int:order_id>')
@login_required
def order_success(order_id):
    """Order confirmation & receipt summary page."""
    db = get_db()
    order = db.execute(
        "SELECT * FROM orders WHERE order_id = ? AND user_id = ?",
        (order_id, session['user_id'])
    ).fetchone()

    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('orders'))

    items = db.execute("""
        SELECT oi.*, p.name, p.image, p.category, (oi.quantity * oi.price) as item_subtotal
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    """, (order_id,)).fetchall()

    return render_template('order_success.html', order=order, items=items)

@app.route('/orders')
@login_required
def orders():
    """Customer's order history page."""
    db = get_db()
    user_orders = db.execute("""
        SELECT o.*, COUNT(oi.order_item_id) as item_count
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.user_id = ?
        GROUP BY o.order_id
        ORDER BY o.order_date DESC
    """, (session['user_id'],)).fetchall()

    # Fetch order items mapped by order_id for detail expansion
    orders_with_items = []
    for ord_row in user_orders:
        items = db.execute("""
            SELECT oi.*, p.name, p.image, p.category, (oi.quantity * oi.price) as item_total
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = ?
        """, (ord_row['order_id'],)).fetchall()
        orders_with_items.append({
            'order': ord_row,
            'order_items': items
        })

    return render_template('orders.html', orders_with_items=orders_with_items)

# ---------------------------------------------------------
# Admin Portal Routes
# ---------------------------------------------------------

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with high-level statistics and recent orders."""
    db = get_db()

    # Metrics
    total_revenue_row = db.execute(
        "SELECT SUM(total_amount) as total FROM orders WHERE status != 'Cancelled'"
    ).fetchone()
    total_revenue = total_revenue_row['total'] or 0.0

    total_orders = db.execute("SELECT COUNT(*) as count FROM orders").fetchone()['count']
    total_products = db.execute("SELECT COUNT(*) as count FROM products").fetchone()['count']
    total_customers = db.execute("SELECT COUNT(*) as count FROM users WHERE role = 'customer'").fetchone()['count']
    low_stock_count = db.execute("SELECT COUNT(*) as count FROM products WHERE stock < 10").fetchone()['count']

    # Recent orders
    recent_orders = db.execute("""
        SELECT o.*, u.name as customer_name, u.email as customer_email
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_date DESC
        LIMIT 6
    """).fetchall()

    return render_template(
        'admin/dashboard.html',
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_products=total_products,
        total_customers=total_customers,
        low_stock_count=low_stock_count,
        recent_orders=recent_orders
    )

@app.route('/admin/products')
@admin_required
def admin_products():
    """Admin products catalog management table."""
    db = get_db()
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    sql = "SELECT * FROM products WHERE 1=1"
    params = []
    if query:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    if category:
        sql += " AND category = ?"
        params.append(category)

    sql += " ORDER BY product_id DESC"
    products_list = db.execute(sql, params).fetchall()

    return render_template(
        'admin/products.html',
        products=products_list,
        current_query=query,
        current_category=category
    )

@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add a new product."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', 0)
        stock = request.form.get('stock', 0)
        description = request.form.get('description', '').strip()

        if not name or not category or not price:
            flash("Product name, category, and price are required.", "danger")
            return render_template('admin/product_form.html', action="Add", product=None)

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            flash("Invalid price or stock value.", "danger")
            return render_template('admin/product_form.html', action="Add", product=None)

        image_filename = 'default_product.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                image_filename = filename

        db = get_db()
        db.execute("""
            INSERT INTO products (name, description, price, category, image, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, price, category, image_filename, stock))
        db.commit()

        flash(f"Product '{name}' added successfully!", "success")
        return redirect(url_for('admin_products'))

    return render_template('admin/product_form.html', action="Add", product=None)

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit an existing product."""
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('admin_products'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', 0)
        stock = request.form.get('stock', 0)
        description = request.form.get('description', '').strip()

        if not name or not category or not price:
            flash("Name, category, and price are required.", "danger")
            return render_template('admin/product_form.html', action="Edit", product=product)

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            flash("Invalid price or stock value.", "danger")
            return render_template('admin/product_form.html', action="Edit", product=product)

        image_filename = product['image']
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                image_filename = filename

        db.execute("""
            UPDATE products
            SET name = ?, description = ?, price = ?, category = ?, image = ?, stock = ?
            WHERE product_id = ?
        """, (name, description, price, category, image_filename, stock, product_id))
        db.commit()

        flash(f"Product '{name}' updated successfully!", "success")
        return redirect(url_for('admin_products'))

    return render_template('admin/product_form.html', action="Edit", product=product)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Delete a product."""
    db = get_db()
    db.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    db.commit()
    flash("Product deleted successfully.", "info")
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """View and filter all customer orders."""
    db = get_db()
    status_filter = request.args.get('status', 'all')

    sql = """
        SELECT o.*, u.name as customer_name, u.email as customer_email,
               COUNT(oi.order_item_id) as item_count
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
    """
    params = []
    if status_filter != 'all':
        sql += " WHERE o.status = ?"
        params.append(status_filter)

    sql += " GROUP BY o.order_id ORDER BY o.order_date DESC"
    orders_list = db.execute(sql, params).fetchall()

    # Preload details for quick expand
    detailed_orders = []
    for ord_row in orders_list:
        items = db.execute("""
            SELECT oi.*, p.name, p.image, (oi.quantity * oi.price) as item_total
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = ?
        """, (ord_row['order_id'],)).fetchall()
        detailed_orders.append({
            'order': ord_row,
            'order_items': items
        })

    return render_template(
        'admin/orders.html',
        detailed_orders=detailed_orders,
        current_status=status_filter
    )

@app.route('/admin/orders/update-status/<int:order_id>', methods=['POST'])
@admin_required
def admin_update_order_status(order_id):
    """Update order status: Pending, Shipped, Delivered, Cancelled."""
    new_status = request.form.get('status')
    valid_statuses = {'Pending', 'Shipped', 'Delivered', 'Cancelled'}

    if new_status in valid_statuses:
        db = get_db()
        db.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))
        db.commit()
        flash(f"Order #{order_id} status updated to {new_status}.", "success")
    else:
        flash("Invalid status specified.", "danger")

    return redirect(request.referrer or url_for('admin_orders'))

@app.route('/admin/customers')
@admin_required
def admin_customers():
    """View registered customer list."""
    db = get_db()
    customers = db.execute("""
        SELECT u.user_id, u.name, u.email, u.phone, u.address, u.created_at,
               COUNT(o.order_id) as total_orders,
               COALESCE(SUM(o.total_amount), 0) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.user_id = o.user_id AND o.status != 'Cancelled'
        WHERE u.role = 'customer'
        GROUP BY u.user_id
        ORDER BY u.created_at DESC
    """).fetchall()

    return render_template('admin/customers.html', customers=customers)

# ---------------------------------------------------------
# Application Initialization
# ---------------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        init_db()
    print("=" * 60)
    print("Simple E-commerce Store running on http://127.0.0.1:5000")
    print("Admin credentials: admin@ecommerce.com / admin123")
    print("Customer credentials: john@example.com / password123")
    print("=" * 60)
    app.run(debug=True, port=5000)
