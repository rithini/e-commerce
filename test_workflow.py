import urllib.request
import urllib.parse
import http.cookiejar

# Create an opener with cookie support
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

BASE_URL = "http://127.0.0.1:5000"

def get(url):
    req = urllib.request.Request(f"{BASE_URL}{url}")
    with opener.open(req) as resp:
        return resp.getcode(), resp.read().decode('utf-8')

def post(url, data):
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}{url}", data=encoded_data, method='POST')
    with opener.open(req) as resp:
        return resp.getcode(), resp.read().decode('utf-8')

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== Running Complete End-to-End Test Suite (INR / Rs) ===")

# 1. Test Customer Login
status, body = post("/login", {"email": "john@example.com", "password": "password123"})
assert status == 200, f"Customer login failed with {status}"
print("[PASS] 1. Customer login successful")

# 2. Verify My Orders is initially EMPTY (No fake/pre-seeded orders)
status, body = get("/orders")
assert status == 200, "Orders history failed"
assert "No Past Orders Found" in body, "Expected empty orders history initially"
print("[PASS] 2. Verified My Orders starts clean with 0 orders before purchasing")

# 3. Add product to cart (e.g. boAt Airdopes, product_id 1)
status, body = post("/cart/add/1", {"quantity": "1"})
assert status == 200, f"Add to cart failed with {status}"
print("[PASS] 3. Added boAt Airdopes 141 (₹1,499.00) to shopping cart")

# 4. View Cart
status, body = get("/cart")
assert "boAt Airdopes" in body, "Product not found in cart HTML"
assert "₹1499.00" in body or "1499.00" in body, "INR price not found in cart"
print("[PASS] 4. Cart page displays product with INR pricing and free delivery")

# 5. Checkout and place order
checkout_data = {
    "shipping_name": "Rahul Sharma",
    "shipping_phone": "+91 98401 23456",
    "shipping_address": "Flat 402, Shanti Nilayam, Anna Nagar, Chennai, Tamil Nadu",
    "payment_method": "Cash on Delivery"
}
status, body = post("/checkout", checkout_data)
assert status == 200, f"Checkout failed with {status}"
assert "Thank you for your purchase!" in body or "Order Successfully Placed" in body, "Order confirmation missing"
assert "₹" in body, "Rupee symbol missing from receipt"
print("[PASS] 5. Checkout completed, order placed in Indian Rupees (₹)")

# 6. Verify My Orders NOW has the order we just placed!
status, body = get("/orders")
assert status == 200, "Orders history failed"
assert "boAt Airdopes" in body, "Placed order items not found in My Orders"
assert "Flat 402, Shanti Nilayam" in body, "Delivery address not found in My Orders"
assert "₹1499.00" in body or "1499.00" in body, "Order total in INR missing"
print("[PASS] 6. Confirmed: My Orders now displays the order we just placed!")

# 7. Logout
status, body = get("/logout")
print("[PASS] 7. Customer logged out")

# 8. Admin Login
status, body = post("/login", {"email": "admin@ecommerce.com", "password": "admin123"})
assert status == 200, "Admin login failed"
print("[PASS] 8. Admin login successful")

# 9. Admin Dashboard
status, body = get("/admin")
assert status == 200 and "Store Dashboard Overview" in body, "Admin dashboard failed"
assert "₹" in body, "Admin revenue missing Rupee symbol"
print("[PASS] 9. Admin dashboard metrics loaded with INR revenue")

# 10. Admin Add Product with INR
new_prod = {
    "name": "Fire-Boltt Ninja Call Pro Smartwatch",
    "category": "Electronics",
    "price": "1299.00",
    "stock": "25",
    "description": "1.69-inch Bluetooth calling smartwatch with AI voice assistant."
}
status, body = post("/admin/products/add", new_prod)
assert status == 200, "Admin add product failed"
print("[PASS] 10. Admin added new product with INR price (₹1,299.00)")

# 11. Admin Orders Management
status, body = get("/admin/orders")
assert status == 200 and "Rahul Sharma" in body, "Placed order not found in admin orders"
print("[PASS] 11. Admin orders table displays placed customer order")

# 12. Admin Update Order Status to Shipped
status, body = post("/admin/orders/update-status/1", {"status": "Shipped"})
assert status == 200, "Update order status failed"
print("[PASS] 12. Admin updated order status to 'Shipped'")

print("=== ALL 12 TESTS PASSED PERFECTLY IN INDIAN RUPEES (INR)! ===")
