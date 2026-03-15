from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "souqfresh_dxb_2024"

PRODUCTS = [
    # ── FRUITS (10) ──
    {"id": 1,  "name": "Mango Alphonso 1kg",       "origin": "India",              "price": 22.00, "cat": "Fruits",     "img": "https://rawabihypermarket.com/uploads/product_images/featured_image/Mango_Alphonsa_India_1Kg535610.JPG"},
    {"id": 2,  "name": "Strawberries 500g",         "origin": "Egypt",              "price": 11.00, "cat": "Fruits",     "img": "https://barnhillboxes.com/wp-content/uploads/2020/10/PHOTO-2020-10-22-10-11-32.jpg"},
    {"id": 3,  "name": "Watermelon Seedless 3kg",   "origin": "UAE Farm",           "price": 14.00, "cat": "Fruits",     "img": "https://images.pexels.com/photos/1313267/pexels-photo-1313267.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 4,  "name": "Banana Cavendish 1kg",      "origin": "Philippines",        "price": 5.50,  "cat": "Fruits",     "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTZvDXhBdGYRA6vxPmQn6lYQXZBqbiBSifNQ&s"},
    {"id": 5,  "name": "Red Grapes 500g",           "origin": "South Africa",       "price": 13.50, "cat": "Fruits",     "img": "https://images.pexels.com/photos/708777/pexels-photo-708777.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 6,  "name": "Pomegranate 2pc",           "origin": "Iran",               "price": 8.50,  "cat": "Fruits",     "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZo1RRztZVHCa0v9OLgjcQYYsnuoTKLpWRGw&s"},
    {"id": 7,  "name": "Kiwi Green 6pc",            "origin": "New Zealand",        "price": 12.00, "cat": "Fruits",     "img": "https://images.pexels.com/photos/51312/kiwi-fruit-vitamins-healthy-eating-51312.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 8,  "name": "Papaya Fresh 1pc",          "origin": "UAE Farm",           "price": 9.00,  "cat": "Fruits",     "img": "https://talabat.dhmedia.io/image/darkstores/groceries-catalog/products-uae/UAE_2509043540002.jpg?size=520"},
    {"id": 9,  "name": "Blueberries 125g",          "origin": "Spain",              "price": 16.00, "cat": "Fruits",     "img": "https://images.unsplash.com/photo-1594002348772-bc0cb57ade8b?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": 10, "name": "Pineapple Fresh 1pc",       "origin": "Costa Rica",         "price": 10.00, "cat": "Fruits",     "img": "https://images.pexels.com/photos/947879/pexels-photo-947879.jpeg?auto=compress&cs=tinysrgb&w=400"},

    # ── VEGETABLES (10) ──
    {"id": 11, "name": "Tomatoes 1kg",              "origin": "UAE Local",          "price": 4.50,  "cat": "Vegetables", "img": "https://images.pexels.com/photos/533280/pexels-photo-533280.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 12, "name": "Baby Spinach 200g",         "origin": "UAE Hydroponic",     "price": 6.75,  "cat": "Vegetables", "img": "https://images.pexels.com/photos/2325843/pexels-photo-2325843.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 13, "name": "Broccoli Fresh",            "origin": "Kenya",              "price": 7.00,  "cat": "Vegetables", "img": "https://images.unsplash.com/photo-1614336215203-05a588f74627?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": 14, "name": "Carrots 500g",              "origin": "UAE Farm",           "price": 3.25,  "cat": "Vegetables", "img": "https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 15, "name": "Bell Peppers Mix 3pc",      "origin": "Netherlands",        "price": 9.00,  "cat": "Vegetables", "img": "https://images.pexels.com/photos/594137/pexels-photo-594137.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 16, "name": "Cucumber 3pc",              "origin": "UAE Local",          "price": 3.50,  "cat": "Vegetables", "img": "https://images.pexels.com/photos/2329440/pexels-photo-2329440.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 17, "name": "Sweet Corn 3pc",            "origin": "UAE Farm",           "price": 5.00,  "cat": "Vegetables", "img": "https://images.pexels.com/photos/547263/pexels-photo-547263.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 18, "name": "Eggplant 2pc",              "origin": "UAE Local",          "price": 4.00,  "cat": "Vegetables", "img": "https://images.pexels.com/photos/321551/pexels-photo-321551.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 19, "name": "Garlic White 250g",         "origin": "China",              "price": 5.50,  "cat": "Vegetables", "img": "https://images.unsplash.com/photo-1587049693270-c7560da11218?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fEdhcmxpYyUyMFdoaXRlfGVufDB8fDB8fHww"},
    {"id": 20, "name": "Zucchini 3pc",              "origin": "UAE Farm",           "price": 6.00,  "cat": "Vegetables", "img": "https://images.unsplash.com/photo-1692956475726-d4a90d0dfbdf?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},

    # ── DAIRY (10) ──
    {"id": 21, "name": "Camel Milk Fresh 1L",       "origin": "UAE Local Farm",     "price": 18.00, "cat": "Dairy",      "img": "https://prod-spinneys-cdn-new.azureedge.net/media/images/products/2024/07/6291115000014.jpg"},
    {"id": 22, "name": "Labneh Organic 400g",       "origin": "Lulu Farms UAE",     "price": 9.50,  "cat": "Dairy",      "img": "https://prod-waitrose.azureedge.net/media/cache/7c/2b/7c2b34e807766a0fe957640830a20781.jpg"},
    {"id": 23, "name": "Halloumi Cheese 250g",      "origin": "Cyprus",             "price": 14.75, "cat": "Dairy",      "img": "https://images.pexels.com/photos/773253/pexels-photo-773253.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 24, "name": "Greek Yoghurt 500g",        "origin": "Al Marai UAE",       "price": 8.25,  "cat": "Dairy",      "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgklSME7mrq2PptgSZw5wMEdfUMfoCfvmSYg&s"},
    {"id": 25, "name": "Full Cream Milk 2L",        "origin": "Al Ain Farms",       "price": 7.50,  "cat": "Dairy",      "img": "https://f.nooncdn.com/p/pzsku/Z042321EE606919E530E9Z/45/1766744143/3329b943-d2b1-439a-b6bd-c3d141b14192.jpg?width=800"},
    {"id": 26, "name": "Butter Unsalted 200g",      "origin": "President, France",  "price": 11.00, "cat": "Dairy",      "img": "https://f.nooncdn.com/p/pzsku/ZEA5ECD5D53D458701D9FZ/45/1746690767/630e7fb6-9676-42b2-b1a3-d2bc1695c297.jpg?width=800"},
    {"id": 27, "name": "Cheddar Cheese 200g",       "origin": "Anchor, NZ",         "price": 13.50, "cat": "Dairy",      "img": "https://f.nooncdn.com/p/pzsku/ZE352AC023D72730A4E89Z/45/1745576706/2ca9a1f8-3db4-4b64-a2bb-ce36689ac0d3.jpg?width=800"},
    {"id": 28, "name": "Cream Cheese 200g",         "origin": "Philadelphia, USA",  "price": 12.00, "cat": "Dairy",      "img": "https://f.nooncdn.com/p/pzsku/ZC0C7EF745E6D23FA79B6Z/45/1746424142/bdcf70e8-6834-468a-9b27-305d69c9c1cf.jpg?width=800"},
    {"id": 29, "name": "Mozzarella 125g",           "origin": "Italy",              "price": 15.00, "cat": "Dairy",      "img": "https://f.nooncdn.com/p/pzsku/Z4DBDCD676F05B3923D79Z/45/1750848656/e7296195-f1ec-42ba-ad8f-85a27356391a.jpg?width=800"},
    {"id": 30, "name": "Sour Cream 200ml",          "origin": "Al Marai UAE",       "price": 7.00,  "cat": "Dairy",      "img": "https://f.nooncdn.com/p/pzsku/Z0C768DC874198934DD77Z/45/1746423929/f093cfc6-8800-4b79-ac6f-bcf0de495a01.jpg?width=800"},

    # ── MEAT (10) ──
    {"id": 31, "name": "Chicken Breast 1kg",        "origin": "UAE Halal",          "price": 28.00, "cat": "Meat",       "img": "https://f.nooncdn.com/p/pzsku/Z29E19981C1AE9014A270Z/45/1746424021/ac7cd4ec-6723-4aef-898d-19abf0499ae9.jpg?width=800"},
    {"id": 32, "name": "Lamb Chops 500g",           "origin": "Australia Halal",    "price": 45.00, "cat": "Meat",       "img": "https://images.pexels.com/photos/65175/pexels-photo-65175.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 33, "name": "Beef Mince 500g",           "origin": "Brazil Halal",       "price": 32.00, "cat": "Meat",       "img": "https://m.media-amazon.com/images/I/71RsLVQSuZL._AC_SY300_SX300_QL70_ML2_.jpg"},
    {"id": 34, "name": "Whole Chicken 1.5kg",       "origin": "UAE Halal",          "price": 22.50, "cat": "Meat",       "img": "https://bf1af2.akinoncloudcdn.com/products/2024/09/11/82370/34477c7c-e4c8-49b7-8a32-45f610197607_size1920_cropCenter.jpg"},
    {"id": 35, "name": "Salmon Fillet 400g",        "origin": "Norway",             "price": 52.00, "cat": "Meat",       "img": "https://bf1af2.akinoncloudcdn.com/products/2025/05/17/147589/87047240-f652-41ea-9c0e-396c703bca6d_size1920_cropCenter.jpg"},
    {"id": 36, "name": "Shrimps Large 500g",        "origin": "UAE Seas",           "price": 38.00, "cat": "Meat",       "img": "https://bf1af2.akinoncloudcdn.com/products/2025/09/22/615796/0deda218-5166-40aa-8b23-3f7bd7cf01d6_size1920_cropCenter.jpg"},
    {"id": 37, "name": "Beef Steak 300g",           "origin": "Australia Halal",    "price": 58.00, "cat": "Meat",       "img": "https://bf1af2.akinoncloudcdn.com/products/2024/10/01/147531/9fd0384d-ed7e-4f4c-a0af-8766678c5576_size1920_cropCenter.jpg"},
    {"id": 38, "name": "Turkey Mince 500g",         "origin": "UAE Halal",          "price": 26.00, "cat": "Meat",       "img": "https://prod-spinneys-cdn-new.azureedge.net/media/cache/97/25/972524062140746db33b013d0e5b0e62.jpg"},
    {"id": 39, "name": "Tuna Steaks 2pc",           "origin": "Maldives",           "price": 44.00, "cat": "Meat",       "img": "https://bf1af2.akinoncloudcdn.com/products/2025/11/29/617079/10bbd9c1-49e4-4af0-8c83-6941f5fa4f36_size1920_cropCenter.jpg"},
    {"id": 40, "name": "Lamb Mince 500g",           "origin": "New Zealand Halal",  "price": 36.00, "cat": "Meat",       "img": "https://prod-spinneys-cdn-new.azureedge.net/media/cache/c2/28/c22827f33af7d2f5f66ae294aaea25e2.jpg"},

    # ── BAKERY (10) ──
    {"id": 41, "name": "Pita Bread Fresh 6pk",      "origin": "Arabic Bakery DXB",  "price": 4.50,  "cat": "Bakery",     "img": "https://images-na.ssl-images-amazon.com/images/I/71jAlgIekOL._UL1200_.jpg"},
    {"id": 42, "name": "Sourdough Loaf",            "origin": "Baker & Spice DXB",  "price": 18.00, "cat": "Bakery",     "img": "https://images.pexels.com/photos/1387070/pexels-photo-1387070.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 43, "name": "Croissants 4pc",            "origin": "French Bakery DXB",  "price": 14.50, "cat": "Bakery",     "img": "https://mcgrocer.com/cdn/shop/files/1280x1280_38a170b0-bf0a-484a-8d32-ad801ec59ced.jpg?v=1769995198&width=800"},
    {"id": 44, "name": "Kunafa Pastry 500g",        "origin": "UAE Sweets",         "price": 19.00, "cat": "Bakery",     "img": "https://prod-spinneys-cdn-new.azureedge.net/media/cache/72/10/7210e7972be9688f54243ea1443b7ff4.jpg"},
    {"id": 45, "name": "Dates Walnut Cake",         "origin": "Local Bakery DXB",   "price": 24.00, "cat": "Bakery",     "img": "https://addictedtodates.com/wp-content/uploads/2023/11/date-and-walnut-cake.jpg"},
    {"id": 46, "name": "Manakish Zaatar",           "origin": "Syrian Bakery DXB",  "price": 7.00,  "cat": "Bakery",     "img": "https://f.nooncdn.com/p/pzsku/Z402BE8B6E08E188E0E1FZ/45/1752848195/15964e1d-7a33-4329-beeb-6e64684cde27.jpg?width=800"},
    {"id": 47, "name": "Bagel Sesame 4pc",          "origin": "The Cheesecake DXB", "price": 16.00, "cat": "Bakery",     "img": "https://f.nooncdn.com/p/pzsku/ZF8043005E51A28272B02Z/45/1753785287/64c37e32-0d18-484c-9d79-95272cc33632.jpg?width=800"},
    {"id": 48, "name": "Cinnamon Roll 4pc",         "origin": "Illy Bakery DXB",    "price": 20.00, "cat": "Bakery",     "img": "https://prod-spinneys-cdn-new.azureedge.net/media/cache/08/99/089966f975ded98bb6c747cfd4f17cde.jpg"},
    {"id": 49, "name": "Whole Wheat Bread",         "origin": "Spinneys Bakery",    "price": 8.50,  "cat": "Bakery",     "img": "https://images.pexels.com/photos/1775043/pexels-photo-1775043.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 50, "name": "Baklava Box",               "origin": "Turkish Sweets DXB", "price": 35.00, "cat": "Bakery",     "img": "https://thebaklavabox.com/cdn/shop/files/assorted-baklava-box-750gm-818929.jpg?v=1745430672"},

    # ── DRINKS (10) ──
    {"id": 51, "name": "Fresh Orange Juice 1L",     "origin": "Squeezed Daily DXB", "price": 13.00, "cat": "Drinks",     "img": "https://bf1af2.akinoncloudcdn.com/products/2024/09/12/84188/ea2b2ed6-0b50-4470-8057-2ab6e428e4a8_size1080_cropCenter.jpg"},
    {"id": 52, "name": "Laban Ayran 1L",            "origin": "Al Marai UAE",       "price": 6.25,  "cat": "Drinks",     "img": "https://prod-spinneys-cdn-new.azureedge.net/media/cache/9c/df/9cdf9ab921fa26f97b1328b276a66f73.jpg"},
    {"id": 53, "name": "Coconut Water 330ml",       "origin": "Thailand",           "price": 8.50,  "cat": "Drinks",     "img": "https://f.nooncdn.com/p/pzsku/Z0B4C391832234BDB9CE5Z/45/_/1662368124/8f2ce256-c76e-4790-b683-d0f396218f0e.jpg?width=800"},
    {"id": 54, "name": "Sparkling Water 6pk",       "origin": "San Pellegrino",     "price": 19.00, "cat": "Drinks",     "img": "https://f.nooncdn.com/p/pnsku/N29007294A/45/_/1764173542/cb36aca3-650a-4aae-96e6-407f5782a247.jpg?width=800"},
    {"id": 55, "name": "Mango Lassi 500ml",         "origin": "Local Kitchen DXB",  "price": 11.00, "cat": "Drinks",     "img": "https://cdn.mafrservices.com/sys-master-root/h9a/hac/48391260700702/1917445_main.jpg?im=Resize=376"},
    {"id": 56, "name": "Arabic Coffee Blend",       "origin": "Yemen Reserve",      "price": 34.00, "cat": "Drinks",     "img": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTOJ1AZv8SToYhh8TIt7Qitpcd3tcrfI8uw37RlM2fZEDkcAU2S53XaQCjjQMrZNKZ7V9aTUY4uB_LWwmxO-UfRXOIefKlalgCecXwmXnsc6AluMnhdxCPR6lU2L3tkKlyr6pSyK_4Eidg&usqp=CAc"},
    {"id": 57, "name": "Cold Brew Coffee 225ml",    "origin": "Nightjar DXB",       "price": 18.00, "cat": "Drinks",     "img": "https://m.media-amazon.com/images/I/717i9XbUq-L._AC_SX300_SY300_QL70_ML2_.jpg"},
    {"id": 58, "name": "Green Tea 100 bags",        "origin": "Japan Sencha",       "price": 14.00, "cat": "Drinks",     "img": "https://m.media-amazon.com/images/I/81F2KE+S59L._AC_SY445_.jpg"},
    {"id": 59, "name": "Pomegranate Juice 1L",      "origin": "Iran Premium",       "price": 22.00, "cat": "Drinks",     "img": "https://bf1af2.akinoncloudcdn.com/products/2024/09/10/63300/3714d7be-6b41-4fa4-93fc-03fe2cd856bf_size1080_cropCenter.jpg"},
    {"id": 60, "name": "Rose Milk 500ml",           "origin": "Saffron Rose DXB",   "price": 12.00, "cat": "Drinks",     "img": "https://cdn.mafrservices.com/sys-master-root/heb/h53/62150874103838/1928517_main.jpg?im=Resize=376"},

    # ── SNACKS (10) ──
    {"id": 61, "name": "Medjool Dates 500g",        "origin": "Madinah, KSA",       "price": 32.00, "cat": "Snacks",     "img": "https://m.media-amazon.com/images/I/61UHAtBJDhL._AC_SX679_.jpg"},
    {"id": 62, "name": "Mixed Nuts 500g",           "origin": "Turkey & Iran",      "price": 28.50, "cat": "Snacks",     "img": "https://m.media-amazon.com/images/I/61yBN47QsPL._AC_SY300_SX300_QL70_ML2_.jpg"},
    {"id": 63, "name": "Hummus Classic 400g",       "origin": "Lebanon",            "price": 10.50, "cat": "Snacks",     "img": "https://minbaladeh.world/storage/16196864210.jpg"},
    {"id": 64, "name": "Dark Chocolate 100g",       "origin": "Belgium",            "price": 15.00, "cat": "Snacks",     "img": "https://bf1af2.akinoncloudcdn.com/products/2024/09/11/97512/d161c8d5-58c5-4d06-8f4d-e07d3f647998_size1080_cropCenter.jpg"},
    {"id": 65, "name": "Pistachios Roasted 250g",   "origin": "Iran Premium",       "price": 22.00, "cat": "Snacks",     "img": "https://c8n.tradeling.com/img/plain/pim/rs:auto:200::0/f:webp/q:90/up/670d080a1ba2d14673487d2d/18e9e475867026263c9442ab70f8c5b1.jpg"},
    {"id": 66, "name": "Peanut Butter 340g",        "origin": "Skippy, USA",        "price": 16.00, "cat": "Snacks",     "img": "https://f.nooncdn.com/p/pzsku/ZB66DA04CD9EABFFE4825Z/45/1763224549/de49c3b5-2619-4abe-bb0e-dac2b8b7219c.jpg?width=800"},
    {"id": 67, "name": "Pringles Original 165g",    "origin": "USA",                "price": 11.00, "cat": "Snacks",     "img": "https://f.nooncdn.com/p/pzsku/ZFE7B10F1E0BE810DD90EZ/45/1750500224/45d607b9-2bd9-404a-99c1-b6020b6e877a.jpg?width=800"},
    {"id": 68, "name": "Cashews Salted 300g",       "origin": "Vietnam",            "price": 19.00, "cat": "Snacks",     "img": "https://m.media-amazon.com/images/I/81bde6QmJwS._AC_SY445_.jpg"},
    {"id": 69, "name": "Protein Bar 60g",           "origin": "Quest, USA",         "price": 13.00, "cat": "Snacks",     "img": "https://bf1af2.akinoncloudcdn.com/products/2024/09/11/88101/b13fcae6-9550-4874-8f7b-9a83205cfd83_size1080_cropCenter.jpg"},
    {"id": 70, "name": "Ajwa Dates Gift Box 150gm",  "origin": "Al-Madinah KSA",     "price": 48.00, "cat": "Snacks",     "img": "https://m.media-amazon.com/images/I/51axEFttRlL._AC_.jpg"},

    # ── ORGANIC (10) ──
    {"id": 71, "name": "Organic Avocado 2pc",       "origin": "Kenya Certified",    "price": 16.00, "cat": "Organic",    "img": "https://images.pexels.com/photos/557659/pexels-photo-557659.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 72, "name": "Sidr Honey 500g",           "origin": "Yemen Organic",      "price": 65.00, "cat": "Organic",    "img": "https://qaenat.com/cdn/shop/files/HP_SIDR_76fdf587-41ea-4751-8f3c-0b7cb5110744.jpg?v=1772278903&width=800"},
    {"id": 73, "name": "Organic Eggs 12pc",         "origin": "UAE Free Range",     "price": 19.50, "cat": "Organic",    "img": "https://images.pexels.com/photos/162712/egg-white-food-protein-162712.jpeg?auto=compress&cs=tinysrgb&w=400"},
    {"id": 74, "name": "Organic Quinoa 500g",       "origin": "Peru Certified",     "price": 24.00, "cat": "Organic",    "img": "https://f.nooncdn.com/p/pzsku/Z0E6E2585649C863B2815Z/45/1746423759/c9e01ea2-95b1-4547-9486-d6fe45c53290.jpg?width=800"},
    {"id": 75, "name": "Organic Olive Oil 500ml",   "origin": "Palestine",          "price": 48.00, "cat": "Organic",    "img": "https://prod-spinneys-cdn-new.azureedge.net/media/cache/d1/89/d189153fdc6680a1d656e21082b18c9a.jpg"},
    {"id": 76, "name": "Organic Chia Seeds 250g",   "origin": "Bolivia",            "price": 18.00, "cat": "Organic",    "img": "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/elz/elz08496/g/2.jpg"},
    {"id": 77, "name": "Organic Almond Milk 1L",    "origin": "Alpro, Belgium",     "price": 21.00, "cat": "Organic",    "img": "https://f.nooncdn.com/p/pzsku/Z35AF1F7D275C2B22CD58Z/45/1765139749/7a9a0c47-d608-4189-a5fd-02377bfc8a42.jpg?width=800"},
    {"id": 78, "name": "Organic Brown Rice 1kg",    "origin": "Thailand",           "price": 14.50, "cat": "Organic",    "img": "https://m.media-amazon.com/images/I/81v6QHxEohL._AC_SY300_SX300_QL70_ML2_.jpg"},
    {"id": 79, "name": "Organic Turmeric 200g",     "origin": "India Certified",    "price": 12.00, "cat": "Organic",    "img": "https://bf1af2.akinoncloudcdn.com/products/2025/02/06/335601/40d27a28-ef08-4f4d-9be5-7fe9a4e65beb_size1080_cropCenter.jpg"},
    {"id": 80, "name": "Organic Medjool Dates 1kg", "origin": "Jordan Valley",      "price": 72.00, "cat": "Organic",    "img": "https://www.letsorganic.com/cdn/shop/files/Organic_Dates_Medjool_1KG_360x.webp?v=1749896847"},
]

CATEGORIES = ["All", "Fruits", "Vegetables", "Dairy", "Meat", "Bakery", "Drinks", "Snacks", "Organic"]
DELIVERY_FEE = 10.00

@app.route("/")
def index():
    session["cart"] = {}
    return render_template("index.html", categories=CATEGORIES)

@app.route("/api/products")
def api_products():
    cat = request.args.get("cat", "All")
    q = request.args.get("q", "").lower()
    cart = session.get("cart", {})
    items = PRODUCTS
    if cat != "All":
        items = [p for p in items if p["cat"] == cat]
    if q:
        items = [p for p in items if q in p["name"].lower() or q in p["origin"].lower() or q in p["cat"].lower()]
    result = []
    for p in items:
        item = dict(p)
        item["in_cart"] = str(p["id"]) in cart
        item["qty"] = cart.get(str(p["id"]), {}).get("qty", 0)
        result.append(item)
    return jsonify(result)

@app.route("/api/cart/add", methods=["POST"])
def cart_add():
    data = request.get_json()
    pid = str(data.get("id"))
    cart = session.get("cart", {})
    product = next((p for p in PRODUCTS if str(p["id"]) == pid), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    if pid not in cart:
        cart[pid] = {"qty": 0, "price": product["price"], "name": product["name"],
                     "origin": product["origin"], "img": product["img"]}
    cart[pid]["qty"] += 1
    session["cart"] = cart
    return jsonify({"cart_count": sum(v["qty"] for v in cart.values()), "message": f"{product['name']} added!"})

@app.route("/api/cart/update", methods=["POST"])
def cart_update():
    data = request.get_json()
    pid = str(data.get("id"))
    delta = int(data.get("delta", 0))
    cart = session.get("cart", {})
    if pid in cart:
        cart[pid]["qty"] = max(0, cart[pid]["qty"] + delta)
        if cart[pid]["qty"] == 0:
            del cart[pid]
    session["cart"] = cart
    return jsonify({"cart_count": sum(v["qty"] for v in cart.values())})

@app.route("/api/cart", methods=["GET"])
def cart_get():
    cart = session.get("cart", {})
    items = [{"id": k, **v} for k, v in cart.items()]
    subtotal = sum(v["price"] * v["qty"] for v in cart.values())
    total = subtotal + (DELIVERY_FEE if items else 0)
    return jsonify({
        "items": items,
        "subtotal": round(subtotal, 2),
        "delivery": DELIVERY_FEE if items else 0,
        "total": round(total, 2),
        "cart_count": sum(v["qty"] for v in cart.values())
    })

@app.route("/api/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", {})
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400
    subtotal = sum(v["price"] * v["qty"] for v in cart.values())
    total = subtotal + DELIVERY_FEE
    session["last_order"] = {"items": dict(cart), "total": round(total, 2)}
    session["cart"] = {}
    return jsonify({"success": True, "total": round(total, 2),
                    "subtotal": round(subtotal, 2),
                    "items_count": f"{sum(v['qty'] for v in cart.values())} items",
                    "message": f"Order placed! AED {total:.2f} — delivering in 30 min!"})

if __name__ == "__main__":
    app.run(debug=True)