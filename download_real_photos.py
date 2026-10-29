import os
import urllib.request

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

# High-resolution real product photography from Unsplash
IMAGE_URLS = {
    "boat_earbuds.jpg": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80",
    "oneplus_phone.jpg": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=600&auto=format&fit=crop&q=80",
    "hp_laptop.jpg": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80",
    "smart_watch.jpg": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop&q=80",
    "gaming_keyboard.jpg": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80",
    "typec_charger.jpg": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop&q=80",
    "mens_shirt.jpg": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&auto=format&fit=crop&q=80",
    "anarkali_kurti.jpg": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&auto=format&fit=crop&q=80",
    "running_shoes.jpg": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80",
    "denim_jeans.jpg": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600&auto=format&fit=crop&q=80",
    "mixer_grinder.jpg": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=600&auto=format&fit=crop&q=80",
    "milton_bottle.jpg": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80",
    "electric_kettle.jpg": "https://images.unsplash.com/photo-1594213114663-d94db9b17125?w=600&auto=format&fit=crop&q=80",
    "orthopedic_pillow.jpg": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&auto=format&fit=crop&q=80",
    "atomic_habits.jpg": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80",
    "parker_pen.jpg": "https://images.unsplash.com/photo-1585336261026-4186644199b8?w=600&auto=format&fit=crop&q=80",
    "default_product.jpg": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop&q=80"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for filename, url in IMAGE_URLS.items():
    filepath = os.path.join(UPLOADS_DIR, filename)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(filepath, 'wb') as f:
                    f.write(data)
                print(f"[SUCCESS] Downloaded real photo: {filename} ({len(data)} bytes)")
            else:
                print(f"[SKIP] Small response for {filename}")
    except Exception as e:
        print(f"[ERROR] Failed downloading {filename}: {e}")

print("Real product photo download process completed!")
