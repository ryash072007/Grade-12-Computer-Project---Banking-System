"""
The main file for 12th Grade Computer Project 2024 for:
1. Yash
2. Atharv

Project Idea: Banking System

Features:
1. User Authentication -> Username and Password
2. Multiple Account Types and Account Creation
    i. Savings Account -> Simple Interest Calculation
    ii. Checkings Account -> Basic deposition and withdrawal functions without interest
3. Simple Interest Calculation:
    i. View interest gathered over time
    ii. Simple one for Savings account and can only take out certain amount of times a month
4. Basic Fund Transfer:
    i. Allow transfer within the same user -> list self option
    ii. Allow transfer between different users
5. Loan Management:
    i. Loan Applications -> Make your own loan with different conditions for different interest rates
    ii Loan Repayment -> Users can make manual repayments and the system keeps track of it
6. Account Statement:
    i. User can view all the transations that have been processed

"""

import mysql.connector
from mysql.connector import Error
import datetime


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="banking_system",
            user="root",
            password="mysql",
            port=3307,
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None


def register_user(connection, username, password):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        connection.commit()
        print("User registered successfully!")
    except Error as e:
        print(f"Error: '{e}'")


def login_user(connection, username, password):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM Users WHERE username=%s AND password=%s", (username, password)
    )
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return user
    else:
        print("Login failed!")
        return None


def create_account(connection, user_id, account_type):
    cursor = connection.cursor()
    interest_rate = 3.5 if account_type == "savings" else 0.0
    cursor.execute(
        "INSERT INTO Accounts (user_id, account_type, interest_rate, last_interest_date) VALUES (%s, %s, %s, CURDATE())",
        (user_id, account_type, interest_rate),
    )
    connection.commit()
    print(f"{account_type.capitalize()} account created successfully!")


def deposit(connection, user_id, account_id, amount):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Accounts SET balance = balance + %s WHERE id = %s", (amount, account_id)
    )
    cursor.execute(
        "INSERT INTO Transactions (user_id, account_id, transaction_type, amount) VALUES (%s, %s, 'deposit', %s)",
        (user_id, account_id, amount),
    )
    connection.commit()
    print("Deposit successful!")


def withdraw(connection, user_id, account_id, amount):
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM Accounts WHERE id = %s AND user_id = %s", (account_id, user_id))
    balance = cursor.fetchone()
    if balance:
        balance = balance[0]
    else:
        print("Unauthorised user for account")
        return
    if balance >= amount:
        cursor.execute(
            "UPDATE Accounts SET balance = balance - %s WHERE id = %s",
            (amount, account_id),
        )
        cursor.execute(
            "INSERT INTO Transactions (user_id, account_id, transaction_type, amount) VALUES (%s, %s, 'withdrawal', %s)",
            (user_id, account_id, amount),
        )
        connection.commit()
        print("Withdrawal successful!")
        return True
    else:
        print("Insufficient balance!")
        return False


def calculate_interest(connection, account_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT balance, interest_rate, last_interest_date, account_type FROM Accounts WHERE id = %s",
        (account_id,),
    )
    balance, interest_rate, last_interest_date, account_type = cursor.fetchone()
    if account_type != "savings":
        print("Account is not a savings account")
        return
    today = datetime.date.today()
    days_diff = (today - last_interest_date).days
    if days_diff > 0:
        interest = (balance * interest_rate * days_diff) / (365 * 100)
        cursor.execute(
            "UPDATE Accounts SET balance = balance + %s, last_interest_date = %s WHERE id = %s",
            (interest, today, account_id),
        )
        connection.commit()
        print(f"Interest calculated: {interest:.2f}")
    else:
        print("Last interest was already added today")


def transfer_funds(connection, user_id, from_account_id, to_account_id, amount):
    if withdraw(connection, user_id, from_account_id, amount):
        deposit(connection, user_id, to_account_id, amount)
    print("Funds transferred successfully!")


def apply_for_loan(connection, user_id, loan_amount, interest_rate, loan_period):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Loans (user_id, loan_amount, interest_rate, loan_period) VALUES (%s, %s, %s, %s)",
        (user_id, loan_amount, interest_rate, loan_period),
    )
    connection.commit()
    print("Loan application successful!")


def repay_loan(connection, loan_id, account_id, amount, user_id):
    cursor = connection.cursor()
    query = """
    SELECT loan_amount FROM Loans WHERE id = %s
    """
    cursor.execute(query, (loan_id, ))
    loan_amount = cursor.fetchone()[0]
    is_active = "True"
    if amount - float(loan_amount) >= 0:
        is_active = "False"

    if withdraw(connection, user_id, account_id, amount):
        cursor.execute(
            "UPDATE Loans SET loan_amount = loan_amount - %s , active = %s WHERE id = %s",
            (amount, is_active, loan_id),
        )
        connection.commit()
        print("Loan repayment successful!")
    else:
        print("Repayment Failed")


def view_statement(connection, account_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Transactions WHERE account_id = %s", (account_id,))
    transactions = cursor.fetchall()
    for transaction in transactions:
        print(transaction)


def get_all_active_loans(connection, user_id):
    cursor = connection.cursor()
    query = """
    SELECT * FROM Loans 
    WHERE user_id = %s AND active = "True"
    """
    cursor.execute(query, (user_id, ))
    active_loans = cursor.fetchall()

    if active_loans:
            print("\nYour Loans:")
            for loan in active_loans:
                loan_id, _, loan_amount, interest_rate, loan_period, _ = (
                    loan
                )
                print(f"Loan ID: {loan_id}")
                print(f"Loan Amount: ${loan_amount:.2f}")
                print(f"Interest Rate: {interest_rate}% per annum")
                print(f"loan_period: {loan_period}")
                print("-" * 30)
    else:
        print("No Loans found.")

    return active_loans

def get_all_accounts(connection, user_id):
    cursor = connection.cursor()
    query = """
    SELECT id, account_type, balance, interest_rate, last_interest_date 
    FROM Accounts 
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    accounts = cursor.fetchall()

    if accounts:
        print("\nYour Accounts:")
        for account in accounts:
            account_id, account_type, balance, interest_rate, last_interest_date = (
                account
            )
            print(f"Account ID: {account_id}")
            print(f"Account Type: {account_type.capitalize()}")
            print(f"Balance: ${balance:.2f}")
            print(f"Interest Rate: {interest_rate}% per annum")
            print(f"Last Interest Date: {last_interest_date}")
            print("-" * 30)
    else:
        print("No accounts found.")

    return accounts


def main():
    connection = create_connection()
    if not connection:
        return

    while True:
        print("\nWelcome to the Banking System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(connection, username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = login_user(connection, username, password)
            if user:
                user_menu(connection, user)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()


def user_menu(connection, user):
    while True:
        print("\nUser Menu")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer Funds")
        print("5. Apply for Loan")
        print("6. Repay Loan")
        print("7. View Account Statement")
        print("8. View All Accounts")
        print("9. View All Loans")
        print("10. Calculate Interest")
        print("11. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            account_type = input("Enter account type (savings/checkings): ")
            create_account(connection, user[0], account_type)
        elif choice == "2":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to deposit: "))
            deposit(connection, user[0], account_id, amount)
        elif choice == "3":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to withdraw: "))
            withdraw(connection, user[0], account_id, amount)
        elif choice == "4":
            from_account_id = int(input("Enter your account ID: "))
            to_account_id = int(input("Enter recipient account ID: "))
            amount = float(input("Enter amount to transfer: "))
            transfer_funds(connection, user[0], from_account_id, to_account_id, amount)
        elif choice == "5":
            loan_amount = float(input("Enter loan amount: "))
            interest_rate = float(input("Enter interest rate: "))
            loan_period = int(input("Enter loan period (in months): "))
            apply_for_loan(connection, user[0], loan_amount, interest_rate, loan_period)
        elif choice == "6":
            loan_id = int(input("Enter loan ID: "))
            repay_from_account_id = int(input("Enter account to repay from: "))
            amount = float(input("Enter amount to repay: "))
            repay_loan(connection, loan_id, repay_from_account_id, amount, user[0])
        elif choice == "7":
            account_id = int(input("Enter account ID: "))
            view_statement(connection, account_id)
        elif choice == "8":
            get_all_accounts(connection, user[0])
        elif choice == "9":
            get_all_active_loans(connection, user[0])
        elif choice == "10":
            account_id = int(input("Enter account ID: "))
            calculate_interest(connection, account_id)
        elif choice == "11":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
