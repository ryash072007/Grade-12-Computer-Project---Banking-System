import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import datetime
from main import *

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="test_banking",
            user="root",
            password="mysql",
            # port=3307
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

# User registration
def register_user(connection, username, password):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        connection.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except Error as e:
        messagebox.showerror("Error", f"Error: '{e}'")

# User login
def login_user(connection, username, password):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM Users WHERE username=%s AND password=%s", (username, password)
    )
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("Success", "Login successful!")
        return user
    else:
        messagebox.showerror("Error", "Login failed!")
        return None

# Tkinter GUI Setup
class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.connection = create_connection()

        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.login_screen()

    # Login screen
    def login_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Banking System Login", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.main_frame, text="Register", command=self.register_screen).pack()

    # Registration screen
    def register_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Banking System Registration", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Login", command=self.login_screen).pack()

    # Login function
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = login_user(self.connection, username, password)
        if user:
            self.user = user
            self.user_menu()

    # Register function
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        register_user(self.connection, username, password)
        self.login_screen()

    # User menu after login
    def user_menu(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Banking System Dashboard", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.main_frame, text="Create Account", command=self.create_account_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Deposit", command=self.deposit_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Withdraw", command=self.withdraw_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Transfer Funds", command=self.transfer_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Apply for Loan", command=self.loan_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.login_screen).pack(pady=10)

    # Create account screen
    def create_account_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Create Account", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Account Type (savings/checkings)").pack(pady=5)
        self.account_type_entry = tk.Entry(self.main_frame)
        self.account_type_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Create", command=self.create_account).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.user_menu).pack()

    def create_account(self):
        account_type = self.account_type_entry.get()
        create_account(self.connection, self.user[0], account_type)
        messagebox.showinfo("Success", f"{account_type.capitalize()} account created successfully!")
        self.user_menu()

    # Deposit screen
    def deposit_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Deposit", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Account ID").pack(pady=5)
        self.account_id_entry = tk.Entry(self.main_frame)
        self.account_id_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Amount").pack(pady=5)
        self.amount_entry = tk.Entry(self.main_frame)
        self.amount_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Deposit", command=self.deposit).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.user_menu).pack()

    def deposit(self):
        account_id = int(self.account_id_entry.get())
        amount = float(self.amount_entry.get())
        deposit(self.connection, self.user[0], account_id, amount)
        messagebox.showinfo("Success", "Deposit successful!")
        self.user_menu()

    # Withdraw screen
    def withdraw_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Withdraw", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Account ID").pack(pady=5)
        self.account_id_entry = tk.Entry(self.main_frame)
        self.account_id_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Amount").pack(pady=5)
        self.amount_entry = tk.Entry(self.main_frame)
        self.amount_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Withdraw", command=self.withdraw).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.user_menu).pack()

    def withdraw(self):
        account_id = int(self.account_id_entry.get())
        amount = float(self.amount_entry.get())
        withdraw(self.connection, self.user[0], account_id, amount)
        messagebox.showinfo("Success", "Withdrawal successful!")
        self.user_menu()

    # Fund transfer screen
    def transfer_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Transfer Funds", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="From Account ID").pack(pady=5)
        self.from_account_entry = tk.Entry(self.main_frame)
        self.from_account_entry.pack(pady=5)

        tk.Label(self.main_frame, text="To Account ID").pack(pady=5)
        self.to_account_entry = tk.Entry(self.main_frame)
        self.to_account_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Amount").pack(pady=5)
        self.amount_entry = tk.Entry(self.main_frame)
        self.amount_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Transfer", command=self.transfer_funds).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.user_menu).pack()

    def transfer_funds(self):
        from_account_id = int(self.from_account_entry.get())
        to_account_id = int(self.to_account_entry.get())
        amount = float(self.amount_entry.get())
        transfer_funds(self.connection, self.user[0], from_account_id, to_account_id, amount)
        messagebox.showinfo("Success", "Transfer successful!")
        self.user_menu()

    # Loan application screen
    def loan_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Apply for Loan", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Loan Amount").pack(pady=5)
        self.loan_amount_entry = tk.Entry(self.main_frame)
        self.loan_amount_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Interest Rate").pack(pady=5)
        self.interest_rate_entry = tk.Entry(self.main_frame)
        self.interest_rate_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Loan Period (in months)").pack(pady=5)
        self.loan_period_entry = tk.Entry(self.main_frame)
        self.loan_period_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Apply", command=self.apply_loan).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.user_menu).pack()

    def apply_loan(self):
        loan_amount = float(self.loan_amount_entry.get())
        interest_rate = float(self.interest_rate_entry.get())
        loan_period = int(self.loan_period_entry.get())
        apply_for_loan(self.connection, self.user[0], loan_amount, interest_rate, loan_period)
        messagebox.showinfo("Success", "Loan application successful!")
        self.user_menu()

    # Helper function to clear the frame
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
