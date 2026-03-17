import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

FILE_NAME = "expenses.csv"

# -------------------------------
# Initialize CSV file
# -------------------------------
def initialize_file():
    try:
        with open(FILE_NAME, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    except FileExistsError:
        pass

# -------------------------------
# Add Expense Function
# -------------------------------
def add_expense():
    date = date_entry.get()
    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")

    category = category_entry.get()
    amount = amount_entry.get()
    description = desc_entry.get()

    if category == "" or amount == "":
        messagebox.showerror("Error", "Category and Amount are required")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    messagebox.showinfo("Success", "Expense Added Successfully!")

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

# -------------------------------
# View Expenses
# -------------------------------
def view_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)

            expenses = ""
            for row in reader:
                expenses += f"{row[0]} | {row[1]} | ₹{row[2]} | {row[3]}\n"

        if expenses == "":
            expenses = "No expenses found."

        messagebox.showinfo("All Expenses", expenses)

    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found")

# -------------------------------
# GUI Window
# -------------------------------
initialize_file()

root = tk.Tk()
root.title("Smart Expense Tracker")
root.geometry("400x350")

tk.Label(root, text="Smart Expense Tracker", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="View Expenses", command=view_expenses).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white").pack(pady=10)

root.mainloop()
