import tkinter as tk
from tkinter import ttk, messagebox
import math
import mysql.connector
from PIL import Image, ImageTk

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="loan"
)

cursor = db.cursor()

# Create the 'loans' table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        loan_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(255),
        loan_amount DECIMAL(10, 2),
        interest_rate DECIMAL(5, 2),
        loan_term INT,
        total_repayment DECIMAL(10, 2),
        monthly_payment DECIMAL(10, 2),
        aadhar_card VARCHAR(12)
    )
""")
db.commit()

# List to store loan data
loans = []

# Function to calculate total repayment
def calculate_total_repayment(loan_amount, interest_rate):
    return loan_amount + (loan_amount * interest_rate / 100)

# Function to calculate monthly payment
def calculate_monthly_payment(loan_amount, interest_rate, loan_term):
    monthly_interest_rate = interest_rate / 12 / 100
    num_payments = loan_term
    return (loan_amount * monthly_interest_rate) / (1 - math.pow(1 + monthly_interest_rate, -num_payments))

# Applying for a loan
def apply_loan():
    # Get loan details from the GUI
    loan_id = loan_id_entry.get()
    customer_name = customer_name_entry.get()
    loan_amount = float(loan_amount_entry.get())
    interest_rate = float(interest_rate_entry.get())
    loan_term = int(loan_term_entry.get())
    aadhar_card = aadhar_card_entry.get()

    # Calculate total repayment amount
    total_repayment = calculate_total_repayment(loan_amount, interest_rate)

    # Calculate monthly payment
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)

    # Insert loan details into the database
    sql = "INSERT INTO loans (loan_id, customer_name, loan_amount, interest_rate, loan_term, total_repayment, monthly_payment, aadhar_card) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (loan_id, customer_name, loan_amount, interest_rate, loan_term, total_repayment, monthly_payment, aadhar_card)
    cursor.execute(sql, values)
    db.commit()

    # Delete entry
    clear_loan_fields()

    # Show a confirmation message
    messagebox.showinfo("Loan Application", f"Loan ID: {loan_id}\nLoan application for {customer_name} submitted.\nTotal Repayment: Rs {total_repayment:.2f}")

# Clear loan entry fields
def clear_loan_fields():
    loan_id_entry.delete(0, tk.END)
    customer_name_entry.delete(0, tk.END)
    loan_amount_entry.delete(0, tk.END)
    interest_rate_entry.delete(0, tk.END)
    loan_term_entry.delete(0, tk.END)
    aadhar_card_entry.delete(0, tk.END)

# Display existing loans
def display_loans():
    loan_listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM loans")
    existing_loans = cursor.fetchall()
    for loan in existing_loans:
        loan_id, customer_name, loan_amount, interest_rate, loan_term, total_repayment, monthly_payment, aadhar_card = loan
        loan_listbox.insert(tk.END, f"Loan ID: {loan_id}, Customer: {customer_name}, Loan Amount: Rs {loan_amount:.2f}, Interest Rate: {interest_rate}%, Loan Term: {loan_term} months, Total Repayment: Rs {total_repayment:.2f}, Monthly Payment: Rs {monthly_payment:.2f}, Aadhar Card: {aadhar_card}")

# Update loan details
def update_loan():
    loan_id = update_loan_id_entry.get()
    new_interest_rate = float(update_interest_rate_entry.get())

    # Update loan details in the database
    sql = "UPDATE loans SET interest_rate = %s WHERE loan_id = %s"
    values = (new_interest_rate, loan_id)
    cursor.execute(sql, values)
    db.commit()

    if cursor.rowcount > 0:
        # Calculate total repayment and monthly payment with the new interest rate
        cursor.execute("SELECT loan_amount, loan_term FROM loans WHERE loan_id = %s", (loan_id,))
        result = cursor.fetchone()
        if result:
            loan_amount, loan_term = result
            total_repayment = calculate_total_repayment(loan_amount, new_interest_rate)
            monthly_payment = calculate_monthly_payment(loan_amount, new_interest_rate, loan_term)

            # Update the total_repayment and monthly_payment fields in the database
            update_sql = "UPDATE loans SET total_repayment = %s, monthly_payment = %s WHERE loan_id = %s"
            update_values = (total_repayment, monthly_payment, loan_id)
            cursor.execute(update_sql, update_values)
            db.commit()

            messagebox.showinfo("Loan Update", f"Loan ID: {loan_id} updated.\nUpdated Interest Rate: {new_interest_rate}%")
        else:
            messagebox.showerror("Loan Update", f"Loan ID: {loan_id} not found.")
    else:
        messagebox.showerror("Loan Update", f"Loan ID: {loan_id} not found.")

    # Clear the entry fields
    update_loan_id_entry.delete(0, tk.END)
    update_interest_rate_entry.delete(0, tk.END)

# Delete loan
def delete_loan():
    loan_id = delete_loan_id_entry.get()

    # Delete loan from the database
    sql = "DELETE FROM loans WHERE loan_id = %s"
    values = (loan_id,)
    cursor.execute(sql, values)
    db.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Loan Delete", f"Loan ID: {loan_id} deleted.")
    else:
        messagebox.showerror("Loan Delete", f"Loan ID: {loan_id} not found.")

    # Clear the entry field
    delete_loan_id_entry.delete(0, tk.END)

# Search for a loan
def search_loan():
    loan_id = search_loan_id_entry.get()

    # Retrieve loan from the database
    sql = "SELECT * FROM loans WHERE loan_id = %s"
    values = (loan_id,)
    cursor.execute(sql, values)
    loan = cursor.fetchone()

    if loan:
        loan_id, customer_name, loan_amount, interest_rate, loan_term, total_repayment, monthly_payment, aadhar_card = loan
        messagebox.showinfo("Loan Search", f"Loan ID: {loan_id}\nCustomer: {customer_name}\nLoan Amount: Rs {loan_amount:.2f}\nInterest Rate: {interest_rate}%\nLoan Term: {loan_term} months\nTotal Repayment: Rs {total_repayment:.2f}\nMonthly Payment: Rs {monthly_payment:.2f}\nAadhar Card: {aadhar_card}")
    else:
        messagebox.showerror("Loan Search", f"Loan ID: {loan_id} not found.")

# Main application
app = tk.Tk()
app.title("Loan Management System")

# Set the window size
app.geometry("800x600")

# Load a background image
background_image = Image.open(r"C:\Users\Hasan\OneDrive\Pictures\cyber security\1680349809923.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Create a label for the background image
background_label = tk.Label(app, image=background_photo)
background_label.place(x=0, y=0, width=800, height=600)

# Create styles for widgets
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

# Loan Application
frame_loan_application = ttk.LabelFrame(app, text="Loan Application")
frame_loan_application.place(x=20, y=20, width=400, height=400)

label_loan_id = ttk.Label(frame_loan_application, text="Loan ID:")
label_customer_name = ttk.Label(frame_loan_application, text="Customer Name:")
label_loan_amount = ttk.Label(frame_loan_application, text="Loan Amount (Rs):")
label_interest_rate = ttk.Label(frame_loan_application, text="Interest Rate (%):")
label_loan_term = ttk.Label(frame_loan_application, text="Loan Term (months):")
label_aadhar_card = ttk.Label(frame_loan_application, text="Aadhar Card Number:")

loan_id_entry = ttk.Entry(frame_loan_application)
customer_name_entry = ttk.Entry(frame_loan_application)
loan_amount_entry = ttk.Entry(frame_loan_application)
interest_rate_entry = ttk.Entry(frame_loan_application)
loan_term_entry = ttk.Entry(frame_loan_application)
aadhar_card_entry = ttk.Entry(frame_loan_application)

apply_button = ttk.Button(frame_loan_application, text="Apply for Loan", command=apply_loan)
display_button = ttk.Button(frame_loan_application, text="Display Loans", command=display_loans)

label_loan_id.grid(row=0, column=0, padx=10, pady=5, sticky="e")
loan_id_entry.grid(row=0, column=1, padx=10, pady=5)
label_customer_name.grid(row=1, column=0, padx=10, pady=5, sticky="e")
customer_name_entry.grid(row=1, column=1, padx=10, pady=5)
label_loan_amount.grid(row=2, column=0, padx=10, pady=5, sticky="e")
loan_amount_entry.grid(row=2, column=1, padx=10, pady=5)
label_interest_rate.grid(row=3, column=0, padx=10, pady=5, sticky="e")
interest_rate_entry.grid(row=3, column=1, padx=10, pady=5)
label_loan_term.grid(row=4, column=0, padx=10, pady=5, sticky="e")
loan_term_entry.grid(row=4, column=1, padx=10, pady=5)
label_aadhar_card.grid(row=5, column=0, padx=10, pady=5, sticky="e")
aadhar_card_entry.grid(row=5, column=1, padx=10, pady=5)

apply_button.grid(row=6, column=0, columnspan=1, pady=10)
display_button.grid(row=6, column=1, columnspan=2, pady=10)

# Loan Update
frame_loan_update = ttk.LabelFrame(app, text="Loan Update")
frame_loan_update.place(x=450, y=20, width=300, height=150)

label_update_loan_id = ttk.Label(frame_loan_update, text="Loan ID to Update:")
label_update_interest_rate = ttk.Label(frame_loan_update, text="New Interest Rate (%):")

update_loan_id_entry = ttk.Entry(frame_loan_update)
update_interest_rate_entry = ttk.Entry(frame_loan_update)

update_button = ttk.Button(frame_loan_update, text="Update Loan", command=update_loan)

label_update_loan_id.grid(row=0, column=0, padx=10, pady=5, sticky="e")
update_loan_id_entry.grid(row=0, column=1, padx=10, pady=5)
label_update_interest_rate.grid(row=1, column=0, padx=10, pady=5, sticky="e")
update_interest_rate_entry.grid(row=1, column=1, padx=10, pady=5)
update_button.grid(row=2, column=0, columnspan=2, pady=10)

# Loan Delete
frame_loan_delete = ttk.LabelFrame(app, text="Loan Delete")
frame_loan_delete.place(x=450, y=200, width=300, height=100)

label_delete_loan_id = ttk.Label(frame_loan_delete, text="Loan ID to Delete:")
delete_loan_id_entry = ttk.Entry(frame_loan_delete)
delete_button = ttk.Button(frame_loan_delete, text="Delete Loan", command=delete_loan)

label_delete_loan_id.grid(row=0, column=0, padx=10, pady=5, sticky="e")
delete_loan_id_entry.grid(row=0, column=1, padx=10, pady=5)
delete_button.grid(row=1, column=0, columnspan=2, pady=10)

# Loan Search
frame_loan_search = ttk.LabelFrame(app, text="Loan Search")
frame_loan_search.place(x=450, y=330, width=300, height=100)

label_search_loan_id = ttk.Label(frame_loan_search, text="Loan ID to Search:")
search_loan_id_entry = ttk.Entry(frame_loan_search)
search_button = ttk.Button(frame_loan_search, text="Search Loan", command=search_loan)

label_search_loan_id.grid(row=0, column=0, padx=10, pady=5, sticky="e")
search_loan_id_entry.grid(row=0, column=1, padx=10, pady=5)
search_button.grid(row=1, column=0, columnspan=2, pady=10)

# Display Loans listbox
frame_loan_list = ttk.LabelFrame(app, text="Loan List")
frame_loan_list.place(x=20, y=450, width=730, height=120)

loan_listbox = tk.Listbox(frame_loan_list, width=80, height=6)
loan_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Main loop
app.mainloop()
