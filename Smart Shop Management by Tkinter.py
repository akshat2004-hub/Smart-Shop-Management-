import tkinter as tk
from tkinter import simpledialog, messagebox

# Class for a Product
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} - Rs.{self.price} (Quantity: {self.quantity})"

# Class for a Shop
class Shop:
    def __init__(self):
        self.inventory = {}
        self.customers = {}
        self.sales = []

    def add_product(self, product):
        if product.name in self.inventory:
            self.inventory[product.name].quantity += product.quantity
        else:
            self.inventory[product.name] = product

    def update_price(self, product_name, new_price):
        if product_name in self.inventory:
            self.inventory[product_name].price = new_price

    def remove_product(self, product_name):
        if product_name in self.inventory:
            del self.inventory[product_name]

    def add_customer(self, username, password, wallet):
        if username in self.customers:
            return False
        self.customers[username] = {'password': password, 'wallet': wallet, 'history': []}
        return True

    def check_customer(self, username, password):
        return username in self.customers and self.customers[username]['password'] == password

    def check_admin(self, username, password):
        return username == "admin" and password == "admin123"

    def get_product_list(self):
        return [f"{p.name} - Rs.{p.price} (Qty: {p.quantity})" for p in self.inventory.values()]

    def get_customer_details(self):
        return [f"{user}: Wallet - Rs.{self.customers[user]['wallet']}" for user in self.customers]

    def get_sales_history(self):
        return "\n".join(self.sales) if self.sales else "No sales recorded yet."

    def sell_product(self, product_name, quantity, customer):
        if product_name in self.inventory:
            product = self.inventory[product_name]
            if product.quantity >= quantity:
                total_cost = quantity * product.price
                if self.customers[customer]['wallet'] >= total_cost:
                    self.customers[customer]['wallet'] -= total_cost
                    product.quantity -= quantity
                    self.customers[customer]['history'].append(f"Bought {quantity} {product_name}(s) for Rs.{total_cost}")
                    self.sales.append(f"{customer} bought {quantity} {product_name}(s) for Rs.{total_cost}")
                    if product.quantity == 0:
                        del self.inventory[product_name]
                    return True, f"{customer} bought {quantity} {product_name}(s) for Rs.{total_cost}."
                return False, "Not enough money."
            return False, f"Not enough {product_name} in stock."
        return False, f"{product_name} is not available."

# Login Page
class LoginPage:
    def __init__(self, root, shop):
        self.root = root
        self.shop = shop
        root.title("Login")
        root.geometry("300x250")
        root.configure(bg='#f0f0f0')

        tk.Label(root, text="Username:", bg= '#f0f0f0').pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:", bg= '#f0f0f0').pack(pady=5)
        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Register New Customer", command=self.register_customer, bg= '#4CAF50').pack(pady=10)

        tk.Button(root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.shop.check_admin(username, password):
            messagebox.showinfo("Welcome", f"Welcome, Admin!")
            self.root.destroy()
            root = tk.Tk()
            AdminApp(root, self.shop)
            root.mainloop()
        elif self.shop.check_customer(username, password):
            messagebox.showinfo("Welcome", f"Welcome, {username}!")
            self.root.destroy()
            root = tk.Tk()
            CustomerApp(root, self.shop, username)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    def register_customer(self):
        username = simpledialog.askstring("Register", "Enter new username:")
        password = simpledialog.askstring("Register", "Enter new password:", show='*')
        wallet = simpledialog.askinteger("Register", "Enter initial wallet balance:")
        if username and password and wallet is not None:
            if self.shop.add_customer(username, password, wallet):
                messagebox.showinfo("Success", "Customer registered successfully!")
            else:
                messagebox.showerror("Error", "Username already exists!")

# Admin Panel
class AdminApp:
    def __init__(self, root, shop):
        self.shop = shop
        self.root = root
        root.title("Admin Panel")
        root.geometry("400x400")

        tk.Label(root, text="Admin Dashboard", font=("Arial", 14)).pack(pady=5)
        tk.Button(root, text="View Products", command=self.view_products).pack(pady=5)
        tk.Button(root, text="View Sales", command=self.view_sales).pack(pady=5)
        tk.Button(root, text="View Customers", command=self.view_customers).pack(pady=5)
        tk.Button(root, text="Add Product", command=self.add_product).pack(pady=5)
        tk.Button(root, text="Update Product Price", command=self.update_price).pack(pady=5)
        tk.Button(root, text="Logout", command=self.logout).pack(pady=5)

    def view_products(self):
        products = "\n".join(self.shop.get_product_list())
        messagebox.showinfo("Available Products", products)

    def view_sales(self):
        sales = self.shop.get_sales_history()
        messagebox.showinfo("Sales History", sales)

    def view_customers(self):
        customers = "\n".join(self.shop.get_customer_details())
        messagebox.showinfo("Customer Details", customers)

    def add_product(self):
        name = simpledialog.askstring("Add Product", "Enter product name:")
        price = simpledialog.askfloat("Add Product", "Enter product price:")
        quantity = simpledialog.askinteger("Add Product", "Enter product quantity:")
        if name and price and quantity:
            self.shop.add_product(Product(name, price, quantity))
            messagebox.showinfo("Success", "Product added successfully!")

    def update_price(self):
        name = simpledialog.askstring("Update Price", "Enter product name:")
        new_price = simpledialog.askfloat("Update Price", "Enter new price:")
        if name in self.shop.inventory:
            self.shop.update_price(name, new_price)
            messagebox.showinfo("Success", "Price updated successfully!")
        else:
            messagebox.showerror("Error", "Product not found!")

    def logout(self):
        messagebox.showinfo("Goodbye", "Thank you for visiting!")
        self.root.destroy()
        root = tk.Tk()
        LoginPage(root, self.shop)
        root.mainloop()
       

# Customer Panel
class CustomerApp:
    def __init__(self, root, shop, username):
        self.shop = shop
        self.username = username
        self.root = root
        root.title("Customer Panel")
        root.geometry("400x400")
        
        tk.Label(root, text=f"Welcome, {username}!", font=("Arial", 14)).pack(pady=5)
        tk.Button(root, text="View Products", command=self.view_products).pack(pady=5)
        tk.Button(root, text="Buy Product", command=self.buy_product).pack(pady=5)
        tk.Button(root, text="View Wallet Balance", command=self.view_wallet).pack(pady=5)
        tk.Button(root, text="View Purchase History", command=self.view_history).pack(pady=5)
        tk.Button(root, text="Add Money to Wallet", command=self.add_money).pack(pady=5)
        tk.Button(root, text="Request Refund", command=self.request_refund).pack(pady=5)
        tk.Button(root, text="Logout", command=self.logout).pack(pady=5)

    def view_products(self):
        products = "\n".join(self.shop.get_product_list())
        messagebox.showinfo("Available Products", products)

    def buy_product(self):
        product_name = simpledialog.askstring("Buy Product", "Enter product name:")
        quantity = simpledialog.askinteger("Buy Product", "Enter quantity:")
        if product_name and quantity:
            success, message = self.shop.sell_product(product_name, quantity, self.username)
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

    def view_wallet(self):
        wallet_balance = self.shop.customers[self.username]['wallet']
        messagebox.showinfo("Wallet Balance", f"Your wallet balance is Rs.{wallet_balance}")

    def view_history(self):
        history = "\n".join(self.shop.customers[self.username]['history'])
        messagebox.showinfo("Purchase History", history if history else "No purchases yet.")

    def add_money(self):
        amount = simpledialog.askinteger("Add Money", "Enter amount to add:")
        if amount and amount > 0:
            self.shop.customers[self.username]['wallet'] += amount
            messagebox.showinfo("Success", f"Rs.{amount} added to your wallet.")
        else:
            messagebox.showerror("Error", "Invalid amount.")

    def request_refund(self):
        messagebox.showinfo("Request Refund", "Contact admin for refund requests.")

    def logout(self):
        messagebox.showinfo("Goodbye", "Thank you for visiting!")
        self.root.destroy()
        root = tk.Tk()
        LoginPage(root, self.shop)
        root.mainloop() 
       
    
if __name__ == "__main__":
    shop = Shop()
    shop.add_product(Product("Apple", 10, 100))
    shop.add_product(Product("Banana", 5, 200))
    shop.add_product(Product("Orange", 8, 150))
    shop.add_customer("testuser", "password", 1000)
    root = tk.Tk()
    LoginPage(root, shop)
    root.mainloop()
