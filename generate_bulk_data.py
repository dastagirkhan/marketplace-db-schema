import os
import random
import string
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv
from faker import Faker

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'marketplace_db')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Initialize Faker
fake = Faker()

def generate_users(num_users=50):
    """Generate sample users"""
    users = []
    for _ in range(num_users):
        user = (
            fake.user_name(),
            fake.email(),
            fake.password(),
            fake.first_name(),
            fake.last_name()
        )
        users.append(user)
    return users

def generate_categories():
    """Generate sample categories"""
    main_categories = [
        ('Electronics', 'Electronic devices and accessories', None),
        ('Fashion', 'Clothing, shoes, and accessories', None),
        ('Home & Garden', 'Home improvement and garden supplies', None),
        ('Books', 'Books and publications', None),
        ('Sports', 'Sports equipment and accessories', None)
    ]
    
    sub_categories = [
        ('Smartphones', 'Mobile phones and accessories', 1),
        ('Laptops', 'Portable computers', 1),
        ('Men\'s Clothing', 'Clothing for men', 2),
        ('Women\'s Clothing', 'Clothing for women', 2),
        ('Kitchen', 'Kitchen appliances and accessories', 3),
        ('Garden Tools', 'Tools for gardening', 3),
        ('Fiction', 'Fiction books', 4),
        ('Non-Fiction', 'Non-fiction books', 4),
        ('Fitness', 'Fitness equipment', 5),
        ('Outdoor Sports', 'Outdoor sports equipment', 5)
    ]
    
    return main_categories + sub_categories

def generate_products(num_products=100):
    """Generate sample products"""
    products = []
    for _ in range(num_products):
        product = (
            random.randint(1, 50),  # seller_id
            random.randint(1, 15),  # category_id
            fake.product_name(),
            fake.text(),
            round(random.uniform(10, 1000), 2),  # price
            random.randint(0, 100)  # stock_quantity
        )
        products.append(product)
    return products

def generate_orders(num_orders=200):
    """Generate sample orders"""
    status_options = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    orders = []
    for _ in range(num_orders):
        order = (
            random.randint(1, 50),  # user_id
            random.choice(status_options),
            round(random.uniform(20, 2000), 2)  # total_amount
        )
        orders.append(order)
    return orders

def generate_order_items(num_items=500):
    """Generate sample order items"""
    order_items = []
    for _ in range(num_items):
        item = (
            random.randint(1, 200),  # order_id
            random.randint(1, 100),  # product_id
            random.randint(1, 5),    # quantity
            round(random.uniform(10, 500), 2)  # unit_price
        )
        order_items.append(item)
    return order_items

def generate_payments(num_payments=200):
    """Generate sample payments"""
    payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer']
    status_options = ['pending', 'completed', 'failed', 'refunded']
    
    payments = []
    for order_id in range(1, num_payments + 1):
        payment = (
            order_id,
            round(random.uniform(20, 2000), 2),  # amount
            random.choice(payment_methods),
            random.choice(status_options),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))  # transaction_id
        )
        payments.append(payment)
    return payments

def generate_reviews(num_reviews=300):
    """Generate sample reviews"""
    reviews = []
    for _ in range(num_reviews):
        review = (
            random.randint(1, 100),  # product_id
            random.randint(1, 50),   # user_id
            random.randint(1, 5),    # rating
            fake.text()              # comment
        )
        reviews.append(review)
    return reviews

def generate_shipping_info(num_shipping=200):
    """Generate sample shipping information"""
    shipping_methods = ['standard', 'express', 'overnight', 'international']
    
    shipping_info = []
    for order_id in range(1, num_shipping + 1):
        info = (
            order_id,
            fake.street_address(),
            fake.secondary_address() if random.random() > 0.5 else None,
            fake.city(),
            fake.state(),
            fake.postcode(),
            fake.country(),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=12)),  # tracking_number
            random.choice(shipping_methods)
        )
        shipping_info.append(info)
    return shipping_info

def generate_discounts(num_discounts=20):
    """Generate sample discounts"""
    discount_types = ['percentage', 'fixed_amount']
    
    discounts = []
    for _ in range(num_discounts):
        start_date = datetime.now() + timedelta(days=random.randint(-30, 30))
        end_date = start_date + timedelta(days=random.randint(1, 90))
        
        discount = (
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),  # code
            fake.text(),  # description
            random.choice(discount_types),
            round(random.uniform(5, 50), 2),  # discount_value
            start_date,
            end_date,
            round(random.uniform(50, 200), 2),  # minimum_purchase
            random.randint(50, 1000)  # usage_limit
        )
        discounts.append(discount)
    return discounts

def insert_sample_data():
    """Insert all sample data into the database"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cur = conn.cursor()
        
        # Insert users
        users_data = generate_users()
        cur.executemany(
            "INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
            users_data
        )
        
        # Insert categories
        categories_data = generate_categories()
        cur.executemany(
            "INSERT INTO categories (name, description, parent_category_id) VALUES (%s, %s, %s)",
            categories_data
        )
        
        # Insert products
        products_data = generate_products()
        cur.executemany(
            "INSERT INTO products (seller_id, category_id, name, description, price, stock_quantity) VALUES (%s, %s, %s, %s, %s, %s)",
            products_data
        )
        
        # Insert orders
        orders_data = generate_orders()
        cur.executemany(
            "INSERT INTO orders (user_id, status, total_amount) VALUES (%s, %s, %s)",
            orders_data
        )
        
        # Insert order items
        order_items_data = generate_order_items()
        cur.executemany(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
            order_items_data
        )
        
        # Insert payments
        payments_data = generate_payments()
        cur.executemany(
            "INSERT INTO payments (order_id, amount, payment_method, status, transaction_id) VALUES (%s, %s, %s, %s, %s)",
            payments_data
        )
        
        # Insert reviews
        reviews_data = generate_reviews()
        cur.executemany(
            "INSERT INTO reviews (product_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)",
            reviews_data
        )
        
        # Insert shipping information
        shipping_data = generate_shipping_info()
        cur.executemany(
            "INSERT INTO shipping_info (order_id, address_line1, address_line2, city, state, postal_code, country, tracking_number, shipping_method) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            shipping_data
        )
        
        # Insert discounts
        discounts_data = generate_discounts()
        cur.executemany(
            "INSERT INTO discounts (code, description, discount_type, discount_value, start_date, end_date, minimum_purchase, usage_limit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            discounts_data
        )
        
        conn.commit()
        print("Sample data inserted successfully")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error inserting sample data: {e}")
        raise

def main():
    """Main function to generate and insert sample data"""
    try:
        insert_sample_data()
        print("Data generation completed successfully")
    except Exception as e:
        print(f"Data generation failed: {e}")

if __name__ == '__main__':
    main()
