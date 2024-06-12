from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Constants
EXCEL_FILE = "inventory.xlsx"

# Define the discount coupons data structure
discount_coupons = {
    'DISCOUNT10': {'discount_percentage': 0.1, 'max_discount': 150},
    'DISCOUNT20': {'discount_percentage': 0.2, 'max_discount': 200},
    # Add more discount coupons as needed
}

def ApplyDiscountCoupon(cartValue, discountId):
    # Check if the provided discount ID exists in the discount_coupons dictionary
    if discountId in discount_coupons:
        discount_info = discount_coupons[discountId]
        discount_percentage = discount_info['discount_percentage']
        max_discount = discount_info['max_discount']
        
        # Calculate the discount amount
        discount_amount = min(cartValue * discount_percentage, max_discount)
        
        # Calculate the discounted price
        discounted_price = max(cartValue - discount_amount, 0)
        
        return discounted_price
    else:
        # If the discount ID is not found in the discount_coupons dictionary, return the original cart value
        return cartValue

class Product:
    def __init__(self, product_id, brand, model, price):
        self.product_id = product_id
        self.brand = brand
        self.model = model
        self.price = price
        self.quantity = 0

class Inventory:
    def __init__(self):
        self.load_inventory()

    def load_inventory(self):
        try:
            self.df = pd.read_excel(EXCEL_FILE)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=["Product ID", "Brand", "Model", "Price", "Quantity"])

    def save_inventory(self):
        self.df.to_excel(EXCEL_FILE, index=False)

    def add_product(self, product):
        new_row = {
            "Product ID": product.product_id,
            "Brand": product.brand,
            "Model": product.model,
            "Price": product.price,
            "Quantity": product.quantity
        }
        new_df = pd.DataFrame([new_row])
        self.df = pd.concat([self.df, new_df], ignore_index=True)
        self.save_inventory()

    def update_quantity(self, product_id, quantity):
        if product_id in self.df["Product ID"].values:
            self.df.loc[self.df["Product ID"] == product_id, "Quantity"] += quantity
            self.save_inventory()

    def remove_item(self, product_id):
        if product_id in self.df["Product ID"].values:
            self.df = self.df[self.df["Product ID"] != product_id]
            self.save_inventory()
            return True, f"Removed product {product_id} from inventory."
        else:
            return False, f"Product {product_id} not found in inventory."

    def get_inventory(self):
        return self.df

inventory = Inventory()

def init_db():
    conn = sqlite3.connect('cart.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_to_cart(product_id, quantity):
    conn = sqlite3.connect('cart.db')
    cursor = conn.cursor()
    cursor.execute('SELECT quantity FROM cart WHERE product_id = ?', (product_id,))
    result = cursor.fetchone()
    
    if result:
        new_quantity = result[0] + quantity
        cursor.execute('UPDATE cart SET quantity = ? WHERE product_id = ?', (new_quantity, product_id))
    else:
        cursor.execute('INSERT INTO cart (product_id, quantity) VALUES (?, ?)', (product_id, quantity))
    
    conn.commit()
    conn.close()

def get_cart_contents():
    conn = sqlite3.connect('cart.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart')
    cart_items = cursor.fetchall()
    conn.close()
    return cart_items

def get_cart_total(inventory_df):
    cart_items = get_cart_contents()
    total_price = 0
    if not inventory_df.empty:
        for item in cart_items:
            product_id, quantity = item[1], item[2]
            product_price = inventory_df.loc[inventory_df["Product ID"] == product_id, "Price"].values
            if len(product_price) > 0:
                total_price += product_price[0] * quantity
    return total_price

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'add_product' in request.form:
            brand = request.form['brand']
            model = request.form['model']
            price = float(request.form['price'])
            product_id = f"{brand}_{model}"
            product = Product(product_id, brand, model, price)
            inventory.add_product(product)
            flash(f"Product {model} added to inventory.")
        elif 'update_quantity' in request.form:
            product_id = request.form['product_id']
            quantity = int(request.form['quantity'])
            inventory.update_quantity(product_id, quantity)
            flash(f"Inventory updated for Product ID {product_id}.")
        elif 'remove_item' in request.form:
            product_id = request.form['product_id']
            success, message = inventory.remove_item(product_id)
            if success:
                flash(message)
            else:
                flash(message, 'error')

    inventory_data = inventory.get_inventory()
    brands = sorted(["HP", "Lenovo", "Acer", "Asus", "Microsoft", "Samsung"])
    return render_template('admin.html', inventory_data=inventory_data, brands=brands)

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        add_to_cart(product_id, quantity)
        flash(f"Added {quantity} units of {product_id} to cart.")

    inventory_data = inventory.get_inventory()
    cart_items = get_cart_contents()
    total_price = get_cart_total(inventory.get_inventory())
    brands = ["All"] + inventory.get_inventory()["Brand"].unique().tolist()
    models = ["All"] + inventory.get_inventory()["Model"].unique().tolist()
    min_price, max_price = inventory.get_inventory()["Price"].min(), inventory.get_inventory()["Price"].max()

    return render_template('customer.html', inventory_data=inventory_data, cart_items=cart_items, total_price=total_price, brands=brands, models=models, min_price=min_price, max_price=max_price)

@app.route('/apply_discount', methods=['POST'])
def apply_discount():
    data = request.json
    cart_value = data.get('cart_value')
    discount_id = data.get('discount_id')

    if cart_value is None or discount_id is None:
        return jsonify({'error': 'Invalid request'}), 400

    # Check if the provided discount ID exists in the discount_coupons dictionary
    if discount_id in discount_coupons:
        discount_info = discount_coupons[discount_id]
        discount_percentage = discount_info['discount_percentage']
        max_discount = discount_info['max_discount']
        
        # Calculate the discount amount
        discount_amount = min(cart_value * discount_percentage, max_discount)
        
        # Calculate the discounted price
        discounted_price = max(cart_value - discount_amount, 0)
        
        return jsonify({'discounted_price': discounted_price}), 200
    else:
        return jsonify({'error': 'Invalid discount ID'}), 400

if __name__ == '__main__':
    app.run(debug=True)
