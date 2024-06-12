# Laptop-Inventory-serviceSure, here's a `README.md` file for your project:

```markdown
# Ecommerce Inventory Management System

This project is a simple Ecommerce Inventory Management System built using Flask, SQLite, and Pandas. It features an Admin interface for managing inventory and a Customer interface for browsing and purchasing products. Additionally, it supports discount coupons and cart functionality.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Routes](#routes)
- [Admin View](#admin-view)
- [Customer View](#customer-view)
- [Backend Logic](#backend-logic)
- [Discount Coupons](#discount-coupons)
- [Contributing](#contributing)
- [License](#license)

## Overview

The project consists of a Flask web application that provides two main interfaces:
1. **Admin Interface**: For managing the product inventory.
2. **Customer Interface**: For browsing products, adding items to the cart, and applying discount coupons.

## Project Structure

```
.
├── static
│   └── style.css
├── templates
│   ├── index.html
│   ├── admin.html
│   └── customer.html
├── inventory.xlsx
├── cart.db
└── app.py
```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/ecommerce-inventory-system.git
   ```
2. Navigate to the project directory:
   ```sh
   cd ecommerce-inventory-system
   ```
3. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have the `inventory.xlsx` file in the project directory.
2. Run the Flask application:
   ```sh
   python app.py
   ```
3. Open a web browser and navigate to `http://127.0.0.1:5000`.

## Routes

- **`/`**: Home page with links to Admin and Customer views.
- **`/admin`**: Admin view for managing inventory.
- **`/customer`**: Customer view for browsing and purchasing products.
- **`/apply_discount`**: Endpoint to apply discount coupons.

## Admin View

The Admin interface allows managing the product inventory. It supports adding new products, updating quantities, and removing items.

### Adding a Product

To add a product, fill out the brand, model, and price fields in the form and submit. The product will be added to the inventory.

### Updating Quantity

To update the quantity of a product, provide the Product ID and the quantity to be added/subtracted.

### Removing a Product

To remove a product, provide the Product ID and submit. The product will be removed from the inventory.

## Customer View

The Customer interface allows browsing products, adding items to the cart, applying discount coupons, and viewing the cart.

### Browsing Products

The inventory is displayed in a table format. Each product has an "Add to Cart" button to add the product to the cart.

### Adding to Cart

When clicking "Add to Cart", a popup asks for the quantity. The item is then added to the cart with the specified quantity.

### Viewing Cart

The cart is displayed in a sidebar, showing the added items and the total price. The total price can be recalculated after applying discount coupons.

### Applying Discount Coupons

Enter a discount code in the provided field and click "Apply Coupon". The total price will be updated with the discount applied if the coupon is valid.

## Backend Logic

The backend logic includes the following main functionalities:

### Inventory Management

- **`Inventory`** class handles loading, saving, and managing the product inventory using Pandas.
- **`add_product`** method adds a new product to the inventory.
- **`update_quantity`** method updates the quantity of an existing product.
- **`remove_item`** method removes a product from the inventory.
- **`get_inventory`** method retrieves the current inventory data.

### Cart Management

- **`init_db`** initializes the SQLite database for the cart.
- **`add_to_cart`** adds a product to the cart.
- **`get_cart_contents`** retrieves the contents of the cart.
- **`get_cart_total`** calculates the total price of the items in the cart.

## Discount Coupons

Discount coupons are defined in the `discount_coupons` dictionary in `app.py`. Each coupon has a discount percentage and a maximum discount value.

```python
discount_coupons = {
    'DISCOUNT10': {'discount_percentage': 0.1, 'max_discount': 150},
    'DISCOUNT20': {'discount_percentage': 0.2, 'max_discount': 200},
    # Add more discount coupons as needed
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
```

Save the above content to a file named `README.md` in your project directory. This file provides an overview of the project, installation instructions, usage details, and information on how to contribute.
