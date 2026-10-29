import os

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

# SVG templates for Indian Market Products with rich modern gradients & icons
products_svg = {
    "boat_earbuds.svg": {
        "title": "boAt Airdopes 141",
        "category": "Electronics",
        "grad1": "#000000",
        "grad2": "#e50914",
        "accent": "#ff4b2b",
        "icon": """
            <rect x="130" y="150" width="140" height="90" rx="35" fill="#1e1e1e" stroke="#ff4b2b" stroke-width="4"/>
            <line x1="130" y1="190" x2="270" y2="190" stroke="#ff4b2b" stroke-width="2"/>
            <circle cx="200" cy="190" r="10" fill="#00ff87"/>
            <rect x="155" y="110" width="18" height="42" rx="9" fill="#ffffff"/>
            <rect x="225" y="110" width="18" height="42" rx="9" fill="#ffffff"/>
        """
    },
    "oneplus_phone.svg": {
        "title": "OnePlus Nord CE4 5G",
        "category": "Electronics",
        "grad1": "#0d1b2a",
        "grad2": "#1b263b",
        "accent": "#00f2fe",
        "icon": """
            <rect x="135" y="100" width="130" height="200" rx="18" fill="#1b2838" stroke="#00f2fe" stroke-width="4"/>
            <rect x="145" y="115" width="110" height="170" rx="10" fill="#0b132b"/>
            <circle cx="200" cy="125" r="4" fill="#00f2fe"/>
            <circle cx="165" cy="140" r="12" fill="#203a43" stroke="#00f2fe" stroke-width="2"/>
            <circle cx="165" cy="170" r="12" fill="#203a43" stroke="#00f2fe" stroke-width="2"/>
        """
    },
    "hp_laptop.svg": {
        "title": "HP 15s Core i5",
        "category": "Electronics",
        "grad1": "#141e30",
        "grad2": "#243b55",
        "accent": "#4facfe",
        "icon": """
            <rect x="100" y="130" width="200" height="120" rx="10" fill="#1e293b" stroke="#4facfe" stroke-width="4"/>
            <rect x="115" y="145" width="170" height="90" rx="5" fill="#0f172a"/>
            <circle cx="200" cy="190" r="14" fill="#4facfe" opacity="0.8"/>
            <path d="M70 250 L330 250 L310 265 L90 265 Z" fill="#94a3b8"/>
        """
    },
    "smart_watch.svg": {
        "title": "Noise ColorFit Pulse",
        "category": "Electronics",
        "grad1": "#1f1c2c",
        "grad2": "#928dab",
        "accent": "#a8ff78",
        "icon": """
            <rect x="175" y="90" width="50" height="220" rx="12" fill="#374151"/>
            <rect x="150" y="150" width="100" height="100" rx="20" fill="#111827" stroke="#a8ff78" stroke-width="4"/>
            <text x="200" y="195" font-family="Arial" font-size="20" fill="#a8ff78" text-anchor="middle" font-weight="bold">10:08</text>
            <text x="200" y="220" font-family="Arial" font-size="11" fill="#ffffff" text-anchor="middle">7,420 STEPS</text>
        """
    },
    "gaming_keyboard.svg": {
        "title": "Zebronics RGB Keyboard",
        "category": "Electronics",
        "grad1": "#0f2027",
        "grad2": "#203a43",
        "accent": "#00f2fe",
        "icon": """
            <rect x="90" y="165" width="220" height="95" rx="12" fill="#1b2838" stroke="#00f2fe" stroke-width="4"/>
            <rect x="110" y="180" width="22" height="18" rx="3" fill="#ff007f"/>
            <rect x="140" y="180" width="22" height="18" rx="3" fill="#00f2fe"/>
            <rect x="170" y="180" width="22" height="18" rx="3" fill="#4facfe"/>
            <rect x="200" y="180" width="22" height="18" rx="3" fill="#f093fb"/>
            <rect x="230" y="180" width="22" height="18" rx="3" fill="#00ff87"/>
            <rect x="260" y="180" width="26" height="18" rx="3" fill="#ffaa00"/>
            <rect x="130" y="215" width="130" height="18" rx="4" fill="#00f2fe" opacity="0.8"/>
        """
    },
    "typec_charger.svg": {
        "title": "Portronics 20W Fast Charger",
        "category": "Electronics",
        "grad1": "#373b44",
        "grad2": "#4286f4",
        "accent": "#f27121",
        "icon": """
            <rect x="150" y="160" width="100" height="85" rx="16" fill="#ffffff" stroke="#4286f4" stroke-width="4"/>
            <rect x="175" y="125" width="14" height="35" rx="4" fill="#94a3b8"/>
            <rect x="211" y="125" width="14" height="35" rx="4" fill="#94a3b8"/>
            <rect x="180" y="215" width="40" height="12" rx="4" fill="#4286f4"/>
            <polygon points="198,175 190,195 200,195 195,210 210,190 200,190" fill="#f27121"/>
        """
    },
    "mens_shirt.svg": {
        "title": "Men's Cotton Casual Shirt",
        "category": "Fashion",
        "grad1": "#1e3c72",
        "grad2": "#2a5298",
        "accent": "#6dd5ed",
        "icon": """
            <path d="M140 135 L170 150 L200 135 L230 150 L260 135 L285 185 L250 195 L245 270 L155 270 L150 195 L115 185 Z" fill="#ffffff" stroke="#2a5298" stroke-width="4"/>
            <line x1="200" y1="135" x2="200" y2="270" stroke="#2a5298" stroke-width="3"/>
            <circle cx="200" cy="180" r="4" fill="#2a5298"/>
            <circle cx="200" cy="210" r="4" fill="#2a5298"/>
            <circle cx="200" cy="240" r="4" fill="#2a5298"/>
        """
    },
    "anarkali_kurti.svg": {
        "title": "Floral Anarkali Kurti",
        "category": "Fashion",
        "grad1": "#d31027",
        "grad2": "#ea384d",
        "accent": "#ffd200",
        "icon": """
            <path d="M160 120 L185 145 L200 135 L215 145 L240 120 L255 160 L235 170 L280 270 L120 270 L165 170 L145 160 Z" fill="#ffd200" stroke="#ffffff" stroke-width="4"/>
            <circle cx="200" cy="170" r="10" fill="#d31027"/>
            <circle cx="200" cy="205" r="10" fill="#d31027"/>
            <circle cx="200" cy="240" r="10" fill="#d31027"/>
        """
    },
    "running_shoes.svg": {
        "title": "Sparx Mesh Running Shoes",
        "category": "Fashion",
        "grad1": "#ff416c",
        "grad2": "#ff4b2b",
        "accent": "#ffe600",
        "icon": """
            <path d="M100 230 Q120 175 170 175 L230 185 Q280 175 300 215 Q310 235 280 250 L120 250 Q100 250 100 230 Z" fill="#ffffff" stroke="#ff416c" stroke-width="4"/>
            <path d="M140 250 L270 250 Q290 250 280 235 L130 235 Z" fill="#ffe600"/>
            <circle cx="260" cy="242" r="8" fill="#ff416c"/>
            <path d="M160 205 Q200 180 240 215" fill="none" stroke="#ff416c" stroke-width="6" stroke-linecap="round"/>
        """
    },
    "denim_jeans.svg": {
        "title": "Roadster Stretch Jeans",
        "category": "Fashion",
        "grad1": "#2c3e50",
        "grad2": "#3498db",
        "accent": "#ecf0f1",
        "icon": """
            <rect x="150" y="115" width="100" height="25" rx="5" fill="#8d6e63"/>
            <path d="M150 140 L195 140 L190 270 L155 270 Z" fill="#2980b9" stroke="#ffffff" stroke-width="3"/>
            <path d="M205 140 L250 140 L245 270 L210 270 Z" fill="#2980b9" stroke="#ffffff" stroke-width="3"/>
            <line x1="170" y1="160" x2="185" y2="160" stroke="#ecf0f1" stroke-width="3"/>
            <line x1="215" y1="160" x2="230" y2="160" stroke="#ecf0f1" stroke-width="3"/>
        """
    },
    "mixer_grinder.svg": {
        "title": "Prestige Iris 750W Mixer",
        "category": "Home & Living",
        "grad1": "#11998e",
        "grad2": "#38ef7d",
        "accent": "#ffffff",
        "icon": """
            <rect x="150" y="195" width="100" height="75" rx="16" fill="#ffffff" stroke="#11998e" stroke-width="4"/>
            <circle cx="200" cy="235" r="14" fill="#e74c3c"/>
            <path d="M160 195 L170 120 L230 120 L240 195 Z" fill="#b0bec5" stroke="#37474f" stroke-width="4"/>
            <path d="M235 140 Q260 160 238 180" fill="none" stroke="#37474f" stroke-width="6" stroke-linecap="round"/>
            <rect x="180" y="108" width="40" height="12" rx="4" fill="#37474f"/>
        """
    },
    "milton_bottle.svg": {
        "title": "Milton Thermosteel 1L",
        "category": "Home & Living",
        "grad1": "#00b4db",
        "grad2": "#0083b0",
        "accent": "#bbf2f6",
        "icon": """
            <rect x="175" y="115" width="50" height="25" rx="6" fill="#37474f"/>
            <rect x="185" y="105" width="30" height="12" rx="3" fill="#78909c"/>
            <path d="M170 145 Q200 140 230 145 L230 265 Q230 275 200 275 Q170 275 170 265 Z" fill="#ffffff" stroke="#0083b0" stroke-width="4"/>
            <rect x="180" y="170" width="40" height="70" rx="4" fill="#0083b0" opacity="0.3"/>
            <circle cx="200" cy="205" r="10" fill="#00b4db"/>
        """
    },
    "electric_kettle.svg": {
        "title": "Pigeon 1.5L Electric Kettle",
        "category": "Home & Living",
        "grad1": "#4b134f",
        "grad2": "#c94b4b",
        "accent": "#fbc2eb",
        "icon": """
            <path d="M160 140 L240 140 L230 240 L165 240 Z" fill="#f5f5f5" stroke="#c94b4b" stroke-width="4"/>
            <rect x="155" y="240" width="90" height="14" rx="4" fill="#37474f"/>
            <path d="M235 155 Q265 190 230 225" fill="none" stroke="#37474f" stroke-width="7" stroke-linecap="round"/>
            <polygon points="150,150 162,145 162,170" fill="#c94b4b"/>
            <circle cx="200" cy="190" r="10" fill="#e74c3c"/>
        """
    },
    "orthopedic_pillow.svg": {
        "title": "Wakefit Orthopedic Pillow",
        "category": "Home & Living",
        "grad1": "#3a1c71",
        "grad2": "#d76d77",
        "accent": "#ffaf7b",
        "icon": """
            <rect x="110" y="150" width="180" height="100" rx="30" fill="#ffffff" stroke="#ffaf7b" stroke-width="5"/>
            <path d="M130 190 Q200 160 270 190 Q200 220 130 190 Z" fill="#ffaf7b" opacity="0.3"/>
            <circle cx="200" cy="190" r="8" fill="#d76d77"/>
        """
    },
    "atomic_habits.svg": {
        "title": "Atomic Habits Book",
        "category": "Books",
        "grad1": "#f12711",
        "grad2": "#f5af19",
        "accent": "#ffffff",
        "icon": """
            <rect x="140" y="110" width="125" height="180" rx="8" fill="#ffffff" stroke="#d35400" stroke-width="4"/>
            <rect x="140" y="110" width="18" height="180" rx="4" fill="#e67e22"/>
            <circle cx="205" cy="170" r="28" fill="#f5af19" opacity="0.4"/>
            <circle cx="205" cy="170" r="18" fill="#f12711"/>
            <text x="205" y="235" font-family="Arial" font-size="12" fill="#2c3e50" text-anchor="middle" font-weight="bold">ATOMIC</text>
            <text x="205" y="250" font-family="Arial" font-size="10" fill="#e74c3c" text-anchor="middle">HABITS</text>
        """
    },
    "parker_pen.svg": {
        "title": "Parker Vector Rollerball Pen",
        "category": "Accessories",
        "grad1": "#232526",
        "grad2": "#414345",
        "accent": "#f1c40f",
        "icon": """
            <polygon points="195,95 205,95 210,250 190,250" fill="#2c3e50" stroke="#f1c40f" stroke-width="2"/>
            <polygon points="190,250 210,250 200,285" fill="#f1c40f"/>
            <rect x="193" y="120" width="14" height="40" rx="3" fill="#f1c40f"/>
            <circle cx="200" cy="285" r="3" fill="#000000"/>
        """
    },
    "default_product.svg": {
        "title": "Store Product",
        "category": "General",
        "grad1": "#434343",
        "grad2": "#000000",
        "accent": "#00c6ff",
        "icon": """
            <rect x="140" y="150" width="120" height="110" rx="10" fill="#ffffff" opacity="0.15" stroke="#00c6ff" stroke-width="4"/>
            <polygon points="200,165 240,235 160,235" fill="none" stroke="#ffffff" stroke-width="4"/>
            <circle cx="200" cy="205" r="10" fill="#00c6ff"/>
        """
    }
}

for filename, item in products_svg.items():
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad_{filename.split('.')[0]}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{item['grad1']}" />
      <stop offset="100%" stop-color="{item['grad2']}" />
    </linearGradient>
    <linearGradient id="cardGrad_{filename.split('.')[0]}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.04" />
    </linearGradient>
    <filter id="glow_{filename.split('.')[0]}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="15" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="400" height="400" fill="url(#bgGrad_{filename.split('.')[0]})" />

  <!-- Ambient Glow -->
  <circle cx="90" cy="90" r="110" fill="{item['accent']}" opacity="0.22" filter="url(#glow_{filename.split('.')[0]})" />
  <circle cx="320" cy="310" r="130" fill="#ffffff" opacity="0.1" filter="url(#glow_{filename.split('.')[0]})" />

  <!-- Central Card Backdrop -->
  <rect x="40" y="40" width="320" height="320" rx="28" fill="url(#cardGrad_{filename.split('.')[0]})" stroke="#ffffff" stroke-width="1.5" stroke-opacity="0.25" />

  <!-- Category Tag -->
  <rect x="65" y="65" width="115" height="26" rx="13" fill="#ffffff" opacity="0.18" />
  <text x="122" y="82" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle" letter-spacing="1">{item['category'].upper()}</text>

  <!-- Product Icon Graphic -->
  <g>
    {item['icon']}
  </g>

  <!-- Product Title Bar -->
  <text x="200" y="325" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="600" fill="#ffffff" text-anchor="middle" letter-spacing="0.5">{item['title']}</text>
</svg>"""
    filepath = os.path.join(UPLOADS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)

print(f"Generated {len(products_svg)} SVG product images in {UPLOADS_DIR}")
