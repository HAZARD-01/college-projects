import tkinter as tk
from tkinter import messagebox

class RestaurantOrderingApp:
    def _init_(self, master):
        self.master = master
        self.master.title("Restaurant Ordering Chatbot")

        self.items = {
            "Burger": 5.99,
            "Pizza": 8.99,
            "Salad": 6.49,
            "Fries": 2.99
        }

        self.selected_items = {}
        self.total = tk.DoubleVar()
        self.total.set(0.0)

        self.create_widgets()

    def create_widgets(self):
        self.item_label = tk.Label(self.master, text="Select Item:")
        self.item_label.grid(row=0, column=0)

        self.item_var = tk.StringVar()
        self.item_dropdown = tk.OptionMenu(self.master, self.item_var, *self.items.keys())
        self.item_dropdown.grid(row=0, column=1)

        self.price_label = tk.Label(self.master, text="Price:")
        self.price_label.grid(row=0, column=2)

        self.price_var = tk.DoubleVar()
        self.price_label_display = tk.Label(self.master, textvariable=self.price_var)
        self.price_label_display.grid(row=0, column=3)

        self.item_var.trace("w", self.update_price)

        self.add_button = tk.Button(self.master, text="Add to Order", command=self.add_to_order)
        self.add_button.grid(row=0, column=4)

        self.order_label = tk.Label(self.master, text="Your Order:")
        self.order_label.grid(row=1, column=0, columnspan=2)

        self.order_text = tk.Text(self.master, height=10, width=30)
        self.order_text.grid(row=2, column=0, columnspan=5)

        self.address_label = tk.Label(self.master, text="Address:")
        self.address_label.grid(row=3, column=0)

        self.address_entry = tk.Entry(self.master)
        self.address_entry.grid(row=3, column=1)

        self.phone_label = tk.Label(self.master, text="Phone Number:")
        self.phone_label.grid(row=3, column=2)

        self.phone_entry = tk.Entry(self.master)
        self.phone_entry.grid(row=3, column=3)

        self.total_label = tk.Label(self.master, text="Total Payable Amount:")
        self.total_label.grid(row=4, column=0)

        self.total_amount_label = tk.Label(self.master, textvariable=self.total)
        self.total_amount_label.grid(row=4, column=1)

        self.confirm_button = tk.Button(self.master, text="Confirm Order", command=self.confirm_order)
        self.confirm_button.grid(row=5, column=0, columnspan=5)

    def update_price(self, *args):
        item = self.item_var.get()
        price = self.items[item]
        self.price_var.set(price)

    def add_to_order(self):
        item = self.item_var.get()
        price = self.items[item]
        self.selected_items[item] = price
        self.total.set(self.total.get() + price)
        self.order_text.insert(tk.END, f"{item}: ${price}\n")

    def confirm_order(self):
        address = self.address_entry.get()
        phone_number = self.phone_entry.get()

        if not address or not phone_number:
            messagebox.showerror("Error", "Please provide both address and phone number.")
        else:
            messagebox.showinfo("Order Confirmation", f"Your order has been confirmed! We will deliver it to:\nAddress: {address}\nPhone Number: {phone_number}\nTotal Payable Amount: ${self.total.get()}\n\nThank you!")

            self.master.destroy()

def main():
    root = tk.Tk()
    app = RestaurantOrderingApp(root)
    root.mainloop()

if _name_ == "_main_":
    main()