import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime
import mysql.connector
from decimal import Decimal

total_expense = 0.0
expenses = []

def connect_to_database():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="expense tracker"
        )
        return db_connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to the database: {err}")
        return None

def create_expenses_table_if_not_exists():
    db_connection = connect_to_database()
    if db_connection:
        cursor = db_connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS Expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                description VARCHAR(255) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                payee VARCHAR(255) NOT NULL,
                payment_method VARCHAR(255) NOT NULL,
                date DATETIME NOT NULL
            )
        """
        cursor.execute(create_table_query)
        db_connection.commit()
        cursor.close()
        db_connection.close()

def fetch_expenses_from_db():
    global total_expense
    create_expenses_table_if_not_exists()
    db_connection = connect_to_database()
    if db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM Expenses")
        fetched_expenses = cursor.fetchall()
        cursor.close()
        db_connection.close()

        for expense in fetched_expenses:
            expenses.append({
                "Description": expense[1],
                "Amount": expense[2],
                "Payee": expense[3],
                "Payment Method": expense[4],
                "Date": expense[5]
            })
            total_expense += float(expense[2])

def calculate_total_expense_of_month():
    global total_expense
    db_connection = connect_to_database()
    if db_connection:
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        cursor = db_connection.cursor()
        cursor.execute("SELECT SUM(amount) FROM Expenses WHERE date >= %s", (start_of_month,))
        total_expense = cursor.fetchone()[0] or 0
        cursor.close()
        db_connection.close()
    update_total_label()

def add_expense():
    global total_expense
    description = description_entry.get()
    amount_str = amount_entry.get()  # Get the amount as a string
    payee = payee_entry.get()
    payment_method = payment_method_var.get()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if description and amount_str and payee:
        try:
            amount = Decimal(amount_str)  # Convert the amount to Decimal

            if (total_expense + amount) < 0:
                messagebox.showwarning("Negative Expense", "Expense amount cannot be negative.")
                return

            total_expense += amount

            db_connection = connect_to_database()
            if db_connection:
                cursor = db_connection.cursor()
                insert_query = "INSERT INTO Expenses (description, amount, payee, payment_method, date) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (description, amount, payee, payment_method, date))
                db_connection.commit()
                cursor.close()
                db_connection.close()

                expense = {
                    "Description": description,
                    "Amount": amount,
                    "Payee": payee,
                    "Payment Method": payment_method,
                    "Date": date
                }

                expenses.append(expense)
                update_expense_listbox()
                description_entry.delete(0, tk.END)
                amount_entry.delete(0, tk.END)
                payee_entry.delete(0, tk.END)
                update_total_label()
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
    else:
        messagebox.showerror("Error", "Please enter description, amount, and payee.")

def update_total_label():
    global total_expense
    total_label.config(text=f"Total Expense: {total_expense:.2f}")

def update_expense_listbox():
    expense_listbox.delete(0, tk.END)
    for i, expense in enumerate(expenses, start=1):
        entry = f"{i}. Date: {expense['Date']} - Description: {expense['Description']}, Payee: {expense['Payee']}, Amount: {expense['Amount']:.2f}, Payment Method: {expense['Payment Method']}"
        expense_listbox.insert(tk.END, entry)

def delete_expense():
    global total_expense
    selected_index = expense_listbox.curselection()
    if selected_index:
        index = int(selected_index[0])
        expense = expenses[index]
        confirmation = messagebox.askyesno("Delete Expense", f"Are you sure you want to delete this expense?\n{expense['Description']} ({expense['Payee']}): {expense['Amount']:.2f}")
        if confirmation:
            expenses.pop(index)
            update_expense_listbox()
            total_expense -= expense["Amount"]
            update_total_label()

            db_connection = connect_to_database()
            if db_connection:
                cursor = db_connection.cursor()
                delete_query = "DELETE FROM Expenses WHERE date = %s"
                cursor.execute(delete_query, (expense['Date'],))
                db_connection.commit()
                cursor.close()
                db_connection.close()
    else:
        messagebox.showerror("Error", "Please select an expense to delete.")

def update_expense():
    global total_expense
    selected_index = expense_listbox.curselection()
    if selected_index:
        index = int(selected_index[0])
        selected_expense = expenses[index]
        new_description = simpledialog.askstring("Update Description", "New Description:", initialvalue=selected_expense["Description"])
        new_amount_str = simpledialog.askstring("Update Amount", "New Amount:", initialvalue=selected_expense["Amount"])
        new_payee = simpledialog.askstring("Update Payee", "New Payee:", initialvalue=selected_expense["Payee"])
        new_payment_method = simpledialog.askstring("Update Payment Method", "New Payment Method:", initialvalue=selected_expense["Payment Method"])

        if new_description and new_amount_str and new_payee and new_payment_method:
            try:
                new_amount = Decimal(new_amount_str)  # Convert the amount to Decimal

                if (total_expense - selected_expense["Amount"] + new_amount) < 0:
                    messagebox.showwarning("Negative Expense", "Expense amount cannot be negative.")
                    return

                total_expense = total_expense - selected_expense["Amount"] + new_amount

                db_connection = connect_to_database()
                if db_connection:
                    cursor = db_connection.cursor()
                    update_query = "UPDATE Expenses SET description = %s, amount = %s, payee = %s, payment_method = %s WHERE date = %s"
                    cursor.execute(update_query, (new_description, new_amount, new_payee, new_payment_method, selected_expense["Date"]))
                    db_connection.commit()
                    cursor.close()
                    db_connection.close()

                    expenses[index] = {
                        "Description": new_description,
                        "Amount": new_amount,
                        "Payee": new_payee,
                        "Payment Method": new_payment_method,
                        "Date": selected_expense["Date"]
                    }

                    update_expense_listbox()
                    update_total_label()
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
        else:
            messagebox.showerror("Error", "Please enter all fields.")
    else:
        messagebox.showerror("Error", "Please select an expense to update.")

def calculate_and_display_total_of_custom_month():
    try:
        # Prompt user for the month and year
        month = simpledialog.askinteger("Total Expense for Custom Month", "Enter Month (1-12):", minvalue=1, maxvalue=12)
        year = simpledialog.askinteger("Total Expense for Custom Month", "Enter Year:", minvalue=1900, maxvalue=datetime.now().year)

        if month and year:
            # Fetch data from the database for the specified month and year
            start_of_custom_month = datetime(year, month, 1, 0, 0, 0)
            end_of_custom_month = start_of_custom_month.replace(month=month % 12 + 1) if month < 12 else start_of_custom_month.replace(year=year + 1, month=1)

            db_connection = connect_to_database()
            if db_connection:
                cursor = db_connection.cursor()
                cursor.execute("SELECT SUM(amount) FROM Expenses WHERE date >= %s AND date < %s", (start_of_custom_month, end_of_custom_month))
                total_expense_custom_month = cursor.fetchone()[0] or 0
                cursor.close()
                db_connection.close()

                messagebox.showinfo("Total Expense for Custom Month", f"The total expense for {month}/{year} is: {total_expense_custom_month:.2f}")

        else:
            messagebox.showwarning("Input Error", "Please enter valid values for Month and Year.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

root = tk.Tk()
root.title("Expense Tracker")

font = ('Arial', 16)

frame = tk.Frame(root, bg="lightgray")
frame.pack(padx=20, pady=20)

description_label = tk.Label(frame, text="Description:", bg="lightgray", font=font)
description_entry = tk.Entry(frame, width=40, font=font)
amount_label = tk.Label(frame, text="Amount:", bg="lightgray", font=font)
amount_entry = tk.Entry(frame, width=20, font=font)
payee_label = tk.Label(frame, text="Payee:", bg="lightgray", font=font)
payee_entry = tk.Entry(frame, width=20, font=font)
payment_method_label = tk.Label(frame, text="Payment Method:", bg="lightgray", font=font)
payment_method_var = tk.StringVar()
payment_method_var.set("Cash")
payment_method_optionmenu = tk.OptionMenu(frame, payment_method_var, "Cash", "Card", "Online")
payment_method_optionmenu.config(font=font)
add_button = tk.Button(frame, text="Add Expense", command=add_expense, bg="black", fg="white", font=font)
delete_button = tk.Button(frame, text="Delete Expense", command=delete_expense, bg="black", fg="white", font=font)
update_button = tk.Button(frame, text="Update Expense", command=update_expense, bg="black", fg="white", font=font)
view_button = tk.Button(frame, text="View Expenses", command=update_expense_listbox, bg="black", fg="white", font=font)
calculate_month_button = tk.Button(frame, text="Exp in Month", command=calculate_and_display_total_of_custom_month, bg="black", fg="white", font=font)
expense_listbox = tk.Listbox(frame, width=60, height=10, bg="lightyellow", font=font)
total_label = tk.Label(frame, text="Total Expense: 0.00", bg="lightgray", font=font)

description_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
description_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3)
amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
amount_entry.grid(row=1, column=1, padx=5, pady=5)
payee_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
payee_entry.grid(row=1, column=3, padx=5, pady=5)
payment_method_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
payment_method_optionmenu.grid(row=2, column=1, padx=5, pady=5, columnspan=3)
add_button.grid(row=3, column=0, padx=5, pady=5, columnspan=4)
delete_button.grid(row=4, column=0, padx=5, pady=5, columnspan=4)
update_button.grid(row=5, column=0, padx=5, pady=5, columnspan=4)
view_button.grid(row=6, column=0, padx=5, pady=5, columnspan=4)
calculate_month_button.grid(row=7, column=0, padx=5, pady=5, columnspan=4)
expense_listbox.grid(row=8, column=0, columnspan=4, padx=5, pady=5)
total_label.grid(row=9, column=0, columnspan=4, padx=5, pady=5)

fetch_expenses_from_db()
calculate_total_expense_of_month()

root.mainloop()
