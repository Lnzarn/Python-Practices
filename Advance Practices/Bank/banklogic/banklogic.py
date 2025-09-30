import sqlite3


def get_connection(dbname):
    try:
        return sqlite3.connect(dbname)
    except Exception as e:
        print(f"Error: {e}")
        raise


def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE,
        password TEXT,
        balance INTEGER
    )
    """
    try:
        with connection:
            connection.execute(query)
        print("Table created successfully!")
    except Exception as e:
        print("Error:", e)


def insert_user(connection, name: str, age: int, email: str, password: str):
    query = """
    INSERT INTO users (name, age, email, password, balance) VALUES (?, ?, ?, ?, ?)
    """
    try:
        with connection:
            connection.execute(query, (name, age, email, password, 0))
        print(f"{name} has been added successfully!")
    except Exception as e:
        print("Error:", e)


def search_users(connection) -> list[tuple]:
    query = "SELECT * FROM users"
    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
    except Exception as e:
        print(e)


def delete_user(connection, user_id: int):
    query = "DELETE FROM users WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (user_id,))
        print("Successfully deleted!")
    except Exception as e:
        print("Error:", e)


def update_email(connection, email: str, user_id: int):
    query = "UPDATE users SET email = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (email, user_id))
        print(f"Email has been changed into {email}")
    except Exception as e:
        print("Error:", e)


def update_money(connection, amount: int, user_id: int):
    query = "UPDATE users SET balance = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (amount, user_id))
    except Exception as e:
        print("Error:", e)


def update_password(connection, password: str, user_id: int):
    query = "UPDATE users SET password = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (password, user_id))
        print("Password has been successfully changed")
    except Exception as e:
        print("Error:", e)


def verify_user(connection, username, password):
    query = "SELECT password FROM users WHERE name = ?"
    try:
        with connection:
            result = connection.execute(query, (username,)).fetchone()

        if result is None:
            print("Doesn't exists")
            return False

        true_pass = result[0]

        if password == true_pass:
            print("You have logged in")
            return True
        else:
            print("login failed")
            return False
    except Exception as e:
        print("Error:", e)
        return False


def admin_panel(connection):
    again = 'y'
    while again != 'n':
        print("\n___Admin Panel___")
        admin_choice = input("Enter (add, search, delete, update): ").lower()

        if admin_choice == 'add':
            name = input("\nEnter name: ")
            password = input("Enter password: ")
            age = int(input("Enter age: "))
            email = input("Enter email: ")
            insert_user(connection, name, age, email, password)

        elif admin_choice == 'search':
            print("\nAll users:")
            for user in search_users(connection):
                print(user)

        elif admin_choice == 'delete':
            user_id = int(input("\nEnter ID: "))
            delete_user(connection, user_id)

        elif admin_choice == 'update':
            user_id = int(input("\nEnter ID: "))
            email = input("Enter new email: ")
            update_email(connection, email, user_id)

        again = input("Try again?(y/n): ").lower()

    return


def check_details(connection, user_id):
    query = "SELECT name, age, email FROM users WHERE id = ?"
    try:
        with connection:
            result = connection.execute(query, (user_id,)).fetchone()
        balance = float(result[0])
        name = result[0]
        age = result[1]
        email = result[2]

        print("\n___Bank___")
        print(f"Your Name: {name}")
        print(f"Your Age: {age}")
        print(f"Your Email: {email}")
    except Exception as e:
        print("Error:", e)


def check_balance(connection, user_id):
    query = "SELECT balance FROM users WHERE id = ?"
    try:
        with connection:
            result = connection.execute(query, (user_id,)).fetchone()
        return float(result[0])

    except Exception as e:
        print("Error:", e)


def deposit_money(connection, user_id, amount_to_deposit):
    query = "SELECT balance FROM users WHERE id = ?"
    try:
        with connection:
            result = connection.execute(query, (user_id,)).fetchone()
        current_amount = result[0]
        if amount_to_deposit < 0:
            print("Error: Transaction failed.")
            return False

        if current_amount is None:
            print("Error: No balance available")
            return False
        else:
            new_amount = current_amount + amount_to_deposit
            update_money(connection, new_amount, user_id)
            return True

    except ValueError:
        print("Error: Invalid input (must be a number).")
    except Exception as e:
        print("Error:", e)


def withdraw_money(connection, user_id):
    query = "SELECT balance FROM users WHERE id = ?"
    try:
        with connection:
            result = connection.execute(query, (user_id,)).fetchone()
        if result is None:
            print("Error: User not found.")
            return

        current_amount = result[0]
        print("\n___Bank___")
        amount_to_withdraw = int(input("Enter amount to withdraw: "))
        if amount_to_withdraw < 0:
            print("Error: Transaction failed.")
            return

        if current_amount >= amount_to_withdraw:
            new_amount = current_amount - amount_to_withdraw
            update_money(connection, new_amount, user_id)
        else:
            print("Transaction failed. Not enough balance to proceed.")
    except ValueError:
        print("Error: Invalid input (must be a number).")
    except Exception as e:
        print("Error:", e)


def transfer_money(connection, user_id, transfer_uid):
    query = "SELECT balance FROM users WHERE id = ?"
    try:
        with connection:
            result_from = connection.execute(query, (user_id,)).fetchone()
            result_to = connection.execute(query, (transfer_uid,)).fetchone()
        if result_to is None:
            print("Error: This user doesn't exist")
            return

        sender_balance = result_from[0]
        receiver_balance = result_to[0]
        print("___Bank___")
        amount_to_transfer = int(input("Enter amount to transfer: "))

        if sender_balance >= amount_to_transfer:
            sender_balance -= amount_to_transfer
            receiver_balance += amount_to_transfer
            update_money(connection, sender_balance, user_id)
            update_money(connection, receiver_balance, transfer_uid)
        else:
            print("Transaction failed. Not enough balance to proceed.")
    except ValueError:
        print("Error: Invalid input (must be a number).")
    except Exception as e:
        print("Error:", e)


def print_menu(connection, user_id):
    again = 'y'
    while again != 'n':
        print("___Menu___")
        print(f"\nHELLO! Please choose an appropriate action.")
        print("1. Check Details")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Transfer")
        print("5. Exit")
        choice = int(input("> "))

        if choice == 1:
            check_details(connection, user_id)
        elif choice == 2:
            withdraw_money(connection, user_id)
        elif choice == 3:
            deposit_money(connection, user_id)
        elif choice == 4:
            tranfer_uid = int(input("Enter the User ID to tranfer money to: "))
            transfer_money(connection, user_id, tranfer_uid)
        elif choice == 5:
            break
        else:
            print("Error: Please enter an appropriate number")
        again = input("Try again?(y/n): ").lower()


def get_userid(connection, username):
    query = "SELECT id FROM users WHERE name = ?"
    try:
        with connection:
            result = connection.execute(query, (username,)).fetchone()
        id = result[0]
        return id
    except Exception as e:
        print("Error:", e)


# def main():
#     connection = get_connection("./bankdb.db")

#     try:
#         create_table(connection)

#         while True:

#             username = "Lanz"
#             password = "test"

#             if username == 'admin' and password == 'admin':
#                 admin_panel(connection)
#                 login_status = False
#             else:
#                 login_status = verify_user(connection, username, password)

#             if login_status:
#                 user_id = get_userid(connection, username)
#                 break

#         print_menu(connection, user_id)
#     finally:
#         connection.close()


# if __name__ == "__main__":
#     main()
