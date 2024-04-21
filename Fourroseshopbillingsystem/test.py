import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from datetime import datetime, timedelta

class TailoringShopBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tailoring Shop Billing System")
        self.root.geometry("1000x800")

        # Set background color
        self.root.configure(bg='#E6E6FA')  # Lavender color

        # Create labels with color
        label_bg_color = '#ADD8E6'  # Light Blue color

        self.bill_no_label = tk.Label(root, text="Bill No:", bg=label_bg_color, font=('Helvetica', 12))
        self.bill_no_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.bill_no_entry = tk.Entry(root, font=('Helvetica', 12))
        self.bill_no_entry.grid(row=0, column=1, padx=10, pady=10)

        self.bill_amount_given_label = tk.Label(root, text="Bill Amount Given:", bg=label_bg_color, font=('Helvetica', 12))
        self.bill_amount_given_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.bill_amount_given_entry = tk.Entry(root, font=('Helvetica', 12))
        self.bill_amount_given_entry.grid(row=1, column=1, padx=10, pady=10)

        self.bill_amount_pending_label = tk.Label(root, text="Bill Amount Pending:", bg=label_bg_color, font=('Helvetica', 12))
        self.bill_amount_pending_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.bill_amount_pending_entry = tk.Entry(root, font=('Helvetica', 12))
        self.bill_amount_pending_entry.grid(row=2, column=1, padx=10, pady=10)

        self.total_bill_amount_label = tk.Label(root, text="Total Bill Amount:", bg=label_bg_color, font=('Helvetica', 12))
        self.total_bill_amount_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.total_bill_amount_entry = tk.Entry(root, font=('Helvetica', 12))
        self.total_bill_amount_entry.grid(row=3, column=1, padx=10, pady=10)

        # Create button with color
        button_bg_color = '#90EE90'  # Light Green color
        self.collect_button = tk.Button(root, text="Total", command=self.collect_payment, bg=button_bg_color, font=('Helvetica', 12))
        self.collect_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Search button
        self.search_button = tk.Button(root, text="Search Bill", command=self.search_bill, bg=button_bg_color, font=('Helvetica', 12))
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        # Show All Bills button
        self.show_all_bills_button = tk.Button(root, text="Show All Bills", command=self.show_all_bills, bg=button_bg_color, font=('Helvetica', 12))
        self.show_all_bills_button.grid(row=4, column=2, pady=10)

        # Update button
        self.update_button = tk.Button(root, text="Update", command=self.update_bill, bg=button_bg_color, font=('Helvetica', 12))
        self.update_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Total Profit of All Bills button
        self.total_profit_all_button = tk.Button(root, text="Total Profit of All Bills", command=self.calculate_total_profit_all, bg=button_bg_color, font=('Helvetica', 12))
        self.total_profit_all_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Total Profit of One Month button
        self.total_profit_one_month_button = tk.Button(root, text="Total Profit of One Month", command=self.calculate_total_profit_one_month, bg=button_bg_color, font=('Helvetica', 12))
        self.total_profit_one_month_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Total daily amounts with color
        self.total_daily_label = tk.Label(root, text="Total Daily Amounts", bg=label_bg_color, font=('Helvetica', 12))
        self.total_daily_label.grid(row=8, column=0, columnspan=3, pady=10)

        self.total_collected_label = tk.Label(root, text="Total Collected:", bg=label_bg_color, font=('Helvetica', 12))
        self.total_collected_label.grid(row=9, column=0, padx=10, pady=10, sticky='e')
        self.total_collected_value = tk.Label(root, text="0", bg=label_bg_color, font=('Helvetica', 12))
        self.total_collected_value.grid(row=9, column=1, padx=10, pady=10, sticky='w')

        self.total_bill_amount_given_label = tk.Label(root, text="Total Bill Amount Given:", bg=label_bg_color, font=('Helvetica', 12))
        self.total_bill_amount_given_label.grid(row=10, column=0, padx=10, pady=10, sticky='e')
        self.total_bill_amount_given_value = tk.Label(root, text="0", bg=label_bg_color, font=('Helvetica', 12))
        self.total_bill_amount_given_value.grid(row=10, column=1, padx=10, pady=10, sticky='w')

        self.total_bill_amount_pending_label = tk.Label(root, text="Total Bill Amount Pending:", bg=label_bg_color, font=('Helvetica', 12))
        self.total_bill_amount_pending_label.grid(row=11, column=0, padx=10, pady=10, sticky='e')
        self.total_bill_amount_pending_value = tk.Label(root, text="0", bg=label_bg_color, font=('Helvetica', 12))
        self.total_bill_amount_pending_value.grid(row=11, column=1, padx=10, pady=10, sticky='w')

        self.total_profit_label = tk.Label(root, text="Total Profit:", bg=label_bg_color, font=('Helvetica', 12))
        self.total_profit_label.grid(row=12, column=0, padx=10, pady=10, sticky='e')
        self.total_profit_value = tk.Label(root, text="0", bg=label_bg_color, font=('Helvetica', 12))
        self.total_profit_value.grid(row=12, column=1, padx=10, pady=10, sticky='w')

        # Create a label to display the total daily bill amount
        self.total_daily_bill_amount_label = tk.Label(root, text="Total Daily Bill Amount:", bg=label_bg_color, font=('Helvetica', 12))
        self.total_daily_bill_amount_label.grid(row=13, column=0, padx=10, pady=10, sticky='e')
        self.total_daily_bill_amount_value = tk.Label(root, text="0", bg=label_bg_color, font=('Helvetica', 12))
        self.total_daily_bill_amount_value.grid(row=13, column=1, padx=10, pady=10, sticky='w')

        # Create a text widget to display collected data
        self.collected_data_text = tk.Text(root, height=10, width=40, wrap=tk.WORD, font=('Helvetica', 12))
        self.collected_data_text.grid(row=9, column=2, rowspan=5, padx=10, pady=10)

        # Database connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fourrose"
        )

        # Create a database cursor
        self.cursor = self.db_connection.cursor()

        # Add the missing column to the database table
        self.check_and_add_created_at_column()

        # Initialize variables for total amounts
        self.total_collected = 0
        self.total_bill_amount_given = 0
        self.total_bill_amount_pending = 0
        self.total_profit = 0
        self.total_daily_bill_amount = 0

        # List to store collected data
        self.collected_data = []

    def check_and_add_created_at_column(self):
        try:
            # Check if the 'created_at' column exists
            self.cursor.execute("DESCRIBE billing_data")
            columns = [column[0] for column in self.cursor.fetchall()]

            if 'created_at' not in columns:
                # Add the 'created_at' column if it doesn't exist
                self.cursor.execute("ALTER TABLE billing_data ADD COLUMN created_at DATETIME")
                self.db_connection.commit()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def collect_payment(self):
        try:
            bill_no = self.bill_no_entry.get()

            # Check if the bill number already exists
            existing_data = self.fetch_from_database(bill_no)

            if existing_data:
                messagebox.showerror("Error", f"Bill No {bill_no} already exists. Please use a different Bill No.")
                return

            bill_amount_given = float(self.bill_amount_given_entry.get())
            bill_amount_pending = float(self.bill_amount_pending_entry.get())
            total_bill_amount = float(self.total_bill_amount_entry.get())

            # Update total collected, total bill amount given, and total bill amount pending
            self.total_collected += bill_amount_given
            self.total_bill_amount_given += bill_amount_given
            self.total_bill_amount_pending += (total_bill_amount - bill_amount_given)
            self.total_profit += bill_amount_given - total_bill_amount  # Update total profit

            # Add data to the collected_data list
            self.collected_data.append({"Bill No": bill_no, "Amount Given": bill_amount_given, "Amount Pending": bill_amount_pending})

            # Update labels
            self.total_collected_value.config(text=str(self.total_collected))
            self.total_bill_amount_given_value.config(text=str(self.total_bill_amount_given))
            self.total_bill_amount_pending_value.config(text=str(self.total_bill_amount_pending))
            self.total_profit_value.config(text=str(self.total_profit))

            # Save data to the database
            self.save_to_database(bill_no, bill_amount_given, bill_amount_pending, total_bill_amount)

            # Display collected data in the text widget
            self.display_collected_data()

            # Update total daily bill amount
            self.total_daily_bill_amount += total_bill_amount
            self.total_daily_bill_amount_value.config(text=str(self.total_daily_bill_amount))

            # Reset input fields
            self.bill_no_entry.delete(0, tk.END)
            self.bill_amount_given_entry.delete(0, tk.END)
            self.bill_amount_pending_entry.delete(0, tk.END)
            self.total_bill_amount_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for amount fields.")

    def save_to_database(self, bill_no, amount_given, amount_pending, total_bill_amount):
        try:
            now = datetime.now()
            created_at = now.strftime("%Y-%m-%d %H:%M:%S")
            query = "INSERT INTO billing_data (bill_no, amount_given, amount_pending, total_bill_amount, created_at) VALUES (%s, %s, %s, %s, %s)"
            values = (bill_no, amount_given, amount_pending, total_bill_amount, created_at)
            self.cursor.execute(query, values)
            self.db_connection.commit()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fetch_from_database(self, bill_no):
        try:
            query = "SELECT * FROM billing_data WHERE bill_no = %s"
            values = (bill_no,)
            self.cursor.execute(query, values)
            return self.cursor.fetchone()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def display_collected_data(self):
        # Clear the text widget
        self.collected_data_text.delete(1.0, tk.END)

        # Display the updated collected data
        for data in self.collected_data:
            bill_no = data["Bill No"]
            amount_given = data["Amount Given"]
            amount_pending = data["Amount Pending"]

            self.collected_data_text.insert(tk.END, f"Bill No: {bill_no}\n")
            self.collected_data_text.insert(tk.END, f"Amount Given: {amount_given}\n")
            self.collected_data_text.insert(tk.END, f"Amount Pending: {amount_pending}\n")
            self.collected_data_text.insert(tk.END, "-" * 30 + "\n")

    def show_all_bills(self):
        try:
            # Fetch all data from the database
            query = "SELECT * FROM billing_data"
            self.cursor.execute(query)
            all_data = self.cursor.fetchall()

            # Display all data in a new window
            all_bills_window = tk.Toplevel(self.root)
            all_bills_window.title("All Bills")

            # Create a text widget to display all data
            all_bills_text = tk.Text(all_bills_window, height=20, width=60, wrap=tk.WORD, font=('Helvetica', 12))
            all_bills_text.pack(padx=10, pady=10)

            # Display the data in the text widget
            for data in all_data:
                bill_no = data[0]
                amount_given = data[1]
                amount_pending = data[2]
                total_bill_amount = data[3]
                created_at = data[4]

                all_bills_text.insert(tk.END, f"Bill No: {bill_no}\n")
                all_bills_text.insert(tk.END, f"Amount Given: {amount_given}\n")
                all_bills_text.insert(tk.END, f"Amount Pending: {amount_pending}\n")
                all_bills_text.insert(tk.END, f"Total Bill Amount: {total_bill_amount}\n")
                all_bills_text.insert(tk.END, f"Created At: {created_at}\n")
                all_bills_text.insert(tk.END, "-" * 50 + "\n")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def search_bill(self):
        try:
            # Prompt user for the bill number
            bill_no = simpledialog.askstring("Search Bill", "Enter Bill No:")

            if bill_no:
                # Fetch data from the database based on the bill number
                query = "SELECT * FROM billing_data WHERE bill_no = %s"
                values = (bill_no,)
                self.cursor.execute(query, values)
                data = self.cursor.fetchone()

                if data:
                    # Display the data in a new window
                    search_result_window = tk.Toplevel(self.root)
                    search_result_window.title(f"Search Result - Bill No: {bill_no}")

                    # Create a text widget to display the search result
                    search_result_text = tk.Text(search_result_window, height=10, width=40, wrap=tk.WORD, font=('Helvetica', 12))
                    search_result_text.pack(padx=10, pady=10)

                    # Display the data in the text widget
                    amount_given = data[1]
                    amount_pending = data[2]
                    total_bill_amount = data[3]
                    created_at = data[4]

                    search_result_text.insert(tk.END, f"Bill No: {bill_no}\n")
                    search_result_text.insert(tk.END, f"Amount Given: {amount_given}\n")
                    search_result_text.insert(tk.END, f"Amount Pending: {amount_pending}\n")
                    search_result_text.insert(tk.END, f"Total Bill Amount: {total_bill_amount}\n")
                    search_result_text.insert(tk.END, f"Created At: {created_at}\n")

                else:
                    messagebox.showinfo("Search Result", f"No data found for Bill No {bill_no}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def update_bill(self):
        try:
            # Prompt user for the bill number
            bill_no = simpledialog.askstring("Update Bill", "Enter Bill No:")

            if bill_no:
                # Fetch data from the database based on the bill number
                query = "SELECT * FROM billing_data WHERE bill_no = %s"
                values = (bill_no,)
                self.cursor.execute(query, values)
                data = self.cursor.fetchone()

                if data:
                    # Prompt user for the updated values
                    updated_amount_given = simpledialog.askfloat("Update Bill", "Enter Updated Amount Given:", minvalue=0)
                    updated_amount_pending = simpledialog.askfloat("Update Bill", "Enter Updated Amount Pending:", minvalue=0)
                    updated_total_bill_amount = simpledialog.askfloat("Update Bill", "Enter Updated Total Bill Amount:", minvalue=0)

                    # Update the values in the database
                    update_query = "UPDATE billing_data SET amount_given = %s, amount_pending = %s, total_bill_amount = %s WHERE bill_no = %s"
                    update_values = (updated_amount_given, updated_amount_pending, updated_total_bill_amount, bill_no)
                    self.cursor.execute(update_query, update_values)
                    self.db_connection.commit()

                    messagebox.showinfo("Update Successful", f"Bill No {bill_no} updated successfully.")

                else:
                    messagebox.showinfo("Update Bill", f"No data found for Bill No {bill_no}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def calculate_total_profit_all(self):
        try:
            # Fetch all data from the database
            query = "SELECT * FROM billing_data"
            self.cursor.execute(query)
            all_data = self.cursor.fetchall()

            # Calculate total profit from all bills
            total_profit_all = sum(data[1] for data in all_data)

            messagebox.showinfo("Total Profit of All Bills", f"The total profit from all bills is: {total_profit_all}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def calculate_total_profit_one_month(self):
        try:
            # Prompt user for the month and year
            month = simpledialog.askinteger("Total Profit for One Month", "Enter Month (1-12):", minvalue=1, maxvalue=12)
            year = simpledialog.askinteger("Total Profit for One Month", "Enter Year:", minvalue=1900, maxvalue=datetime.now().year)

            if month and year:
                # Fetch data from the database for the specified month and year
                query = "SELECT * FROM billing_data WHERE MONTH(created_at) = %s AND YEAR(created_at) = %s"
                values = (month, year)
                self.cursor.execute(query, values)
                monthly_data = self.cursor.fetchall()

                # Calculate total profit for the specified month
                total_profit_month = sum(data[1] for data in monthly_data)

                messagebox.showinfo("Total Profit for One Month", f"The total profit for {month}/{year} is: {total_profit_month}")

            else:
                messagebox.showwarning("Input Error", "Please enter valid values for Month and Year.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


# Create the main Tkinter window
root = tk.Tk()

# Create an instance of the TailoringShopBillingApp class
app = TailoringShopBillingApp(root)

# Run the Tkinter event loop
root.mainloop()
