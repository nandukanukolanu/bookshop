import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich.text import Text
from datetime import datetime
from decimal import Decimal

console = Console()

class Book:
    def __init__(self, book_id, title, author, price, stock):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = Decimal(str(price))
        self.stock = stock

    def to_dict(self):
        return {
            'id': self.book_id,
            'title': self.title,
            'author': self.author,
            'price': float(self.price),
            'stock': self.stock
        }


class BookStore:
    def __init__(self):
        self.books = [
            Book(1, "The Great Gatsby", "F. Scott Fitzgerald", 12.99, 15),
            Book(2, "To Kill a Mockingbird", "Harper Lee", 14.99, 12),
            Book(3, "1984", "George Orwell", 13.99, 20),
            Book(4, "Pride and Prejudice", "Jane Austen", 11.99, 18),
            Book(5, "The Catcher in the Rye", "J.D. Salinger", 10.99, 10),
            Book(6, "Brave New World", "Aldous Huxley", 13.99, 14),
            Book(7, "The Hobbit", "J.R.R. Tolkien", 15.99, 8),
            Book(8, "Dune", "Frank Herbert", 16.99, 11),
            Book(9, "Foundation", "Isaac Asimov", 14.99, 9),
            Book(10, "Neuromancer", "William Gibson", 12.99, 12),
        ]
        self.cart = {}
        self.order_history = []

    def display_welcome(self):
        console.clear()
        welcome_text = """
        ╔═══════════════════════════════════════╗
        ║       📚 ELEGANT BOOK STORE 📚        ║
        ║    Your Gateway to Literary Worlds    ║
        ╚═══════════════════════════════════════╝
        """
        console.print(Text(welcome_text, style="bold cyan"))

    def display_books(self):
        console.clear()
        console.print(Panel.fit("📚 Available Books", style="bold magenta"))
        
        table = Table(title="", style="cyan")
        table.add_column("ID", style="bold yellow", width=5)
        table.add_column("Title", style="bold white", width=30)
        table.add_column("Author", style="cyan", width=25)
        table.add_column("Price", style="bold green", width=10)
        table.add_column("Stock", style="bold blue", width=8)

        for book in self.books:
            table.add_row(
                str(book.book_id),
                book.title,
                book.author,
                f"${book.price:.2f}",
                str(book.stock)
            )

        console.print(table)

    def add_to_cart(self):
        self.display_books()
        console.print()
        
        try:
            book_id = int(Prompt.ask("[bold cyan]Enter Book ID to add to cart[/bold cyan]", default="0"))
            
            if book_id == 0:
                return
            
            book = next((b for b in self.books if b.book_id == book_id), None)
            
            if not book:
                console.print("[bold red]❌ No books found![/bold red]")
                return
            
            if book.stock == 0:
                console.print("[bold red]❌ Out of stock![/bold red]")
                return
            
            max_quantity = min(book.stock, 5)
            quantity = int(Prompt.ask(
                f"[bold cyan]Enter quantity (max {max_quantity})[/bold cyan]",
                default="1"
            ))
            
            if quantity <= 0 or quantity > max_quantity:
                console.print("[bold red]❌ Invalid quantity![/bold red]")
                return
            
            if book_id in self.cart:
                self.cart[book_id]['quantity'] += quantity
            else:
                self.cart[book_id] = {'book': book, 'quantity': quantity}
            
            console.print(f"[bold green]✅ Added {quantity} copy/copies of '{book.title}' to cart![/bold green]")
        
        except ValueError:
            console.print("[bold red]❌ Invalid input![/bold red]")
        
        input("\nPress Enter to continue...")

    def view_cart(self):
        console.clear()
        
        if not self.cart:
            console.print(Panel("[yellow]Your cart is empty![/yellow]", style="bold red"))
            input("Press Enter to continue...")
            return

        console.print(Panel.fit("🛒 Shopping Cart", style="bold magenta"))
        
        table = Table(style="cyan")
        table.add_column("Title", style="bold white", width=30)
        table.add_column("Author", style="cyan", width=20)
        table.add_column("Price", style="bold green", width=10)
        table.add_column("Qty", style="bold yellow", width=5)
        table.add_column("Subtotal", style="bold green", width=12)

        total = Decimal('0')
        
        for book_id, item in self.cart.items():
            book = item['book']
            qty = item['quantity']
            subtotal = book.price * qty
            total += subtotal
            
            table.add_row(
                book.title,
                book.author,
                f"${book.price:.2f}",
                str(qty),
                f"${subtotal:.2f}"
            )

        console.print(table)
        console.print()
        
        discount_text = Text(f"{'─' * 50}\n", style="dim cyan")
        console.print(discount_text, end='')
        
        console.print(f"[bold yellow]Subtotal:[/bold yellow] ${total:.2f}")
        console.print(f"[bold yellow]Tax (10%):[/bold yellow] ${total * Decimal('0.1'):.2f}")
        console.print(f"[bold green]Total:[/bold green] [bold green]${total * Decimal('1.1'):.2f}[/bold green]")

        choice = Prompt.ask("\n[bold cyan]Options: (c)heckout, (r)emove item, (b)ack[/bold cyan]", choices=['c', 'r', 'b'])
        
        if choice == 'c':
            self.checkout()
        elif choice == 'r':
            self.remove_from_cart()

    def remove_from_cart(self):
        console.clear()
        console.print(Panel.fit("🗑️  Remove Item", style="bold red"))
        
        try:
            book_id = int(Prompt.ask("[bold cyan]Enter Book ID to remove[/bold cyan]"))
            
            if book_id in self.cart:
                book_title = self.cart[book_id]['book'].title
                del self.cart[book_id]
                console.print(f"[bold green]✅ '{book_title}' removed from cart![/bold green]")
            else:
                console.print("[bold red]❌ Item not in cart![/bold red]")
        
        except ValueError:
            console.print("[bold red]❌ Invalid input![/bold red]")
        
        input("\nPress Enter to continue...")

    def checkout(self):
        console.clear()
        
        if not self.cart:
            console.print(Panel("[yellow]Cart is empty![/yellow]", style="bold red"))
            input("Press Enter to continue...")
            return

        console.print(Panel.fit("💳 Checkout", style="bold magenta"))
        
        name = Prompt.ask("[bold cyan]Enter full name[/bold cyan]")
        email = Prompt.ask("[bold cyan]Enter email[/bold cyan]")
        address = Prompt.ask("[bold cyan]Enter address[/bold cyan]")
        
        total = Decimal('0')
        for item in self.cart.values():
            total += item['book'].price * item['quantity']
        
        final_total = total * Decimal('1.1')
        
        console.print(f"\n[bold yellow]Order Total: ${final_total:.2f}[/bold yellow]")
        
        if Confirm.ask("[bold cyan]Confirm purchase?[/bold cyan]"):
            order = {
                'order_id': len(self.order_history) + 1,
                'customer': name,
                'email': email,
                'address': address,
                'items': dict(self.cart),
                'total': float(final_total),
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.order_history.append(order)
            
            for book_id, item in self.cart.items():
                book = next(b for b in self.books if b.book_id == book_id)
                book.stock -= item['quantity']
            
            self.cart = {}
            
            order_confirmation = f"""
            ╔════════════════════════════════════╗
            ║      ✅ ORDER CONFIRMED! ✅      ║
            ╚════════════════════════════════════╝
            
            Order ID: #{order['order_id']}
            Customer: {name}
            Email: {email}
            Total: ${order['total']:.2f}
            
            Thank you for your purchase!
            """
            
            console.print(Text(order_confirmation, style="bold green"))
        else:
            console.print("[bold yellow]Checkout cancelled.[/bold yellow]")
        
        input("\nPress Enter to continue...")

    def view_order_history(self):
        console.clear()
        
        if not self.order_history:
            console.print(Panel("[yellow]No orders yet![/yellow]", style="bold blue"))
            input("Press Enter to continue...")
            return

        console.print(Panel.fit("📋 Order History", style="bold magenta"))
        
        for order in self.order_history:
            order_text = f"""
            Order ID: #{order['order_id']} | Date: {order['date']}
            Customer: {order['customer']} | Email: {order['email']}
            """
            console.print(Panel(order_text.strip(), style="dim cyan"))
            
            table = Table(style="cyan", show_header=True)
            table.add_column("Title", style="bold white", width=30)
            table.add_column("Quantity", style="bold yellow", width=8)
            table.add_column("Price", style="bold green", width=10)
            
            for book_id, item in order['items'].items():
                table.add_row(
                    item['book'].title,
                    str(item['quantity']),
                    f"${item['book'].price:.2f}"
                )
            
            console.print(table)
            console.print(f"[bold green]Total: ${order['total']:.2f}[/bold green]\n")
        
        input("Press Enter to continue...")

    def display_menu(self):
        console.clear()
        console.print(Panel.fit("Main Menu", style="bold magenta"))
        
        menu_options = """
        [bold cyan]1.[/bold cyan] [bold white]Browse Books[/bold white]
        [bold cyan]2.[/bold cyan] [bold white]Add to Cart[/bold white]
        [bold cyan]3.[/bold cyan] [bold white]View Cart[/bold white]
        [bold cyan]4.[/bold cyan] [bold white]Order History[/bold white]
        [bold cyan]5.[/bold cyan] [bold white]Exit[/bold white]
        """
        
        console.print(menu_options)
        choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]", choices=['1', '2', '3', '4', '5'])
        
        return choice

    def run(self):
        self.display_welcome()
        input("Press Enter to start shopping...")
        
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.display_books()
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.add_to_cart()
            elif choice == '3':
                self.view_cart()
            elif choice == '4':
                self.view_order_history()
            elif choice == '5':
                console.print(Panel("[bold green]Thank you for shopping! Goodbye![/bold green]", style="bold cyan"))
                break


if __name__ == "__main__":
    store = BookStore()
    store.run()
