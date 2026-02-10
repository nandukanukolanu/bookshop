# 📚 Elegant Online Bookstore

A beautiful, text-based online bookstore application built with Python and the `rich` library for an elegant terminal UI.

## Features

✨ **Rich & Elegant UI**
- Beautiful colored tables and panels
- Interactive menu system
- Smooth user experience

📖 **Bookstore Features**
- Browse a curated collection of books
- Add books to shopping cart
- View and manage shopping cart
- Checkout with customer details
- Order confirmation
- View order history
- Real-time inventory management

💳 **Shopping Experience**
- Add multiple copies of books
- Remove items from cart
- Automatic tax calculation
- Order history tracking

## Installation

1. Ensure you have Python 3.6+ installed

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Execute the bookstore:
```bash
python bookstore.py
```

## How to Use

1. **Browse Books** - View all available books with details
2. **Add to Cart** - Select a book ID and enter quantity
3. **View Cart** - See items in your cart with prices and subtotal
4. **Checkout** - Enter your details and confirm purchase
5. **Order History** - View all your previous orders

## Sample Book Catalog

The store includes 10 classic and popular books:
- The Great Gatsby
- To Kill a Mockingbird
- 1984
- Pride and Prejudice
- The Catcher in the Rye
- Brave New World
- The Hobbit
- Dune
- Foundation
- Neuromancer

## Technologies Used

- **Python 3.x** - Core language
- **Rich Library** - Terminal UI with colors, tables, and panels
- **Decimal** - Accurate price calculations

## Customization

You can easily customize:
- Book catalog in the `__init__` method of `BookStore` class
- Colors and styling in the `rich` library calls
- Tax percentage (currently 10%)
- Maximum quantity per order (currently 5)

Enjoy your elegant shopping experience! 🛍️