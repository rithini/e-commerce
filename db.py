import sqlite3
import os
from werkzeug.security import generate_password_hash
from flask import g
from config import Config

def get_db():
    """Connect to SQLite database and return connection with row factory."""
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE)
        g.db.row_factory = sqlite3.Row
        # Enable foreign key support in SQLite
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    """Close the database connection if open."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(force_reseed=False):
    """Initialize the database tables and seed sample data if empty or forced."""
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    
    if user_count == 0 or force_reseed:
        seed_data(conn)
        
    conn.commit()
    conn.close()

def seed_data(conn):
    """Seed initial demo users and Indian market products. NO fake orders are seeded."""
    cursor = conn.cursor()
    
    # Clean tables and reset sequence if reseeding
    cursor.execute("DELETE FROM cart")
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM users")
    try:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('products', 'users', 'cart', 'orders', 'order_items')")
    except sqlite3.OperationalError:
        pass
    
    # 1. Admin User
    admin_pw = generate_password_hash("admin123")
    cursor.execute("""
        INSERT INTO users (name, email, password, phone, address, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Store Administrator", "admin@ecommerce.com", admin_pw, "+91 98765 43210", "100 MG Road, Bengaluru, Karnataka, India", "admin"))
    
    # 2. Demo Customer User (Starts with NO orders - orders will only be saved when customer orders)
    customer_pw = generate_password_hash("password123")
    cursor.execute("""
        INSERT INTO users (name, email, password, phone, address, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Rahul Sharma", "john@example.com", customer_pw, "+91 98401 23456", "Flat 402, Shanti Nilayam, Anna Nagar, Chennai, Tamil Nadu", "customer"))

    # 3. Diverse Products in Indian Rupees (INR / ₹)
    sample_products = [
        (
            "boAt Airdopes 141 ANC Wireless Earbuds",
            "Active Noise Cancellation (up to 32dB), 42 hours total playtime, ENx quad mics for clear calling, and Beast mode for gaming. IPX5 sweat and water resistance.",
            1499.00,
            "Electronics",
            "boat_earbuds.jpg",
            45
        ),
        (
            "OnePlus Nord CE4 5G (8GB RAM, 128GB)",
            "Qualcomm Snapdragon 7 Gen 3 processor, 100W SUPERVOOC ultra-fast charging, 5500 mAh battery, and 120Hz AMOLED display with Sony LYT-600 OIS camera.",
            24999.00,
            "Electronics",
            "oneplus_phone.jpg",
            18
        ),
        (
            "HP 15s Intel Core i5 12th Gen Laptop",
            "12th Gen Intel Core i5-1235U, 16GB DDR4 RAM, 512GB NVMe SSD, 15.6-inch FHD micro-edge anti-glare display, Intel Iris Xe graphics, and Windows 11 with MS Office.",
            52990.00,
            "Electronics",
            "hp_laptop.jpg",
            10
        ),
        (
            "Noise ColorFit Pulse 3 Bluetooth Smart Watch",
            "1.96-inch TFT color display, Bluetooth calling with dial pad, 100+ sports modes, 24/7 heart rate and SpO2 tracking, and 7-day battery endurance.",
            1799.00,
            "Electronics",
            "smart_watch.jpg",
            60
        ),
        (
            "Zebronics Transformer RGB Gaming Keyboard",
            "Braided cable with gold-plated USB, multi-color dynamic LED breathing modes, integrated smartphone holder, and laser keycaps for ultra-durable tactile typing.",
            1199.00,
            "Electronics",
            "gaming_keyboard.jpg",
            35
        ),
        (
            "Portronics 20W Fast Type-C Wall Charger",
            "Power Delivery (PD 3.0) 20W ultra-compact adapter for iPhones, iPads, and Android devices with intelligent multi-layer surge protection.",
            499.00,
            "Electronics",
            "typec_charger.jpg",
            75
        ),
        (
            "Men's Slim Fit 100% Cotton Casual Shirt",
            "Premium breathable cotton fabric with spread collar, curved hemline, buttoned cuffs, and modern checks pattern ideal for both office and casual weekends.",
            899.00,
            "Fashion",
            "mens_shirt.jpg",
            40
        ),
        (
            "Women's Pure Cotton Floral Anarkali Kurti",
            "Elegant calf-length flared Anarkali kurti with intricate ethnic floral motifs, round neck with lace borders, and three-quarter sleeves crafted from pure soft cotton.",
            1249.00,
            "Fashion",
            "anarkali_kurti.jpg",
            32
        ),
        (
            "Sparx Ultra-Light Mesh Running Shoes",
            "Engineered breathable mesh upper, cushioned memory foam insole, anti-skid shock absorbing EVA sole for running, workouts, and daily fitness walk.",
            1199.00,
            "Fashion",
            "running_shoes.jpg",
            50
        ),
        (
            "Roadster Regular Fit Stretchable Denim Jeans",
            "Classic 5-pocket styling in mid-wash indigo denim, elastane blend for flexible all-day comfort, and reinforced double stitching with heavy-duty metal rivets.",
            1399.00,
            "Fashion",
            "denim_jeans.jpg",
            28
        ),
        (
            "Prestige Iris 750W Mixer Grinder (3 Jars)",
            "Heavy-duty 750-watt copper winding motor, 3 stainless steel multi-utility grinding jars with transparent dome lids, overload protector, and 3-speed control.",
            2999.00,
            "Home & Living",
            "mixer_grinder.jpg",
            22
        ),
        (
            "Milton Thermosteel Flip Lid Flask Bottle (1000ml)",
            "Vacuum insulated 304 food-grade stainless steel bottle. Keeps water, tea, or beverages piping hot for 24 hours or chilled cold for 24 hours. 100% leak-proof.",
            849.00,
            "Home & Living",
            "milton_bottle.jpg",
            55
        ),
        (
            "Pigeon 1.5L Stainless Steel Electric Kettle",
            "1500W rapid boil heating base, 360-degree cordless swivel base, automatic shut-off with boil-dry protection, and ergonomic cool-touch handle.",
            699.00,
            "Home & Living",
            "electric_kettle.jpg",
            65
        ),
        (
            "Wakefit Orthopedic Memory Foam Pillow",
            "High-density responsive memory foam engineered to align cervical spine and relieve neck strain. Includes breathable, washable hypoallergenic outer cover.",
            999.00,
            "Home & Living",
            "orthopedic_pillow.jpg",
            30
        ),
        (
            "Atomic Habits by James Clear (Paperback)",
            "The globally acclaimed #1 New York Times bestseller on proven frameworks for building good habits, breaking bad ones, and mastering tiny behaviors that lead to remarkable results.",
            449.00,
            "Books",
            "atomic_habits.jpg",
            80
        ),
        (
            "Parker Vector Matte Black Rollerball Pen",
            "Iconic arrow clip, stainless steel body with fine matte black finish, smooth free-flowing Navigator rollerball ink refill for effortless executive handwriting.",
            349.00,
            "Accessories",
            "parker_pen.jpg",
            90
        )
    ]
    
    cursor.executemany("""
        INSERT INTO products (name, description, price, category, image, stock)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_products)

    # NOTE: NO pre-seeded orders! Customers start with an empty order history,
    # and only orders placed by the user will be saved in the database.
    
    conn.commit()
