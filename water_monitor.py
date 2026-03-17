import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import date
import hashlib
import re

# ---------------- FILE PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USAGE_FILE = os.path.join(BASE_DIR, "usage_data.csv")
USERS_FILE = os.path.join(BASE_DIR, "users.txt")

# ---------------- CONSTANTS ----------------
WATER_RATE = 0.02
ELECTRICITY_RATE = 6
WATER_LIMIT = 300
ELECTRICITY_LIMIT = 7

current_user_email = None

# ---------------- SECURITY ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ---------------- FILE CREATION ----------------
def create_files():
    if not os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Email", "Date", "Water", "Electricity",
                "WaterAlert", "ElectricityAlert",
                "WaterBill", "ElectricityBill", "TotalBill"
            ])

    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

# ---------------- PASSWORD TOGGLE ----------------
def toggle_password():
    if show_pass_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# ---------------- USER FUNCTIONS ----------------
def register():
    name = name_entry.get().strip()
    email = email_entry.get().strip().lower()
    password = password_entry.get().strip()

    if not name or not email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return

    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3 and parts[1] == email:
                messagebox.showerror("Error", "Email already registered")
                return

    with open(USERS_FILE, "a") as f:
        f.write(f"{name},{email},{hash_password(password)}\n")

    messagebox.showinfo("Success", "Registration successful")
    clear_login_fields()

def login():
    global current_user_email
    email = email_entry.get().strip().lower()
    password = password_entry.get().strip()
    hashed = hash_password(password)

    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue
            _, saved_email, saved_pwd = parts
            if saved_email == email and saved_pwd == hashed:
                current_user_email = email
                open_dashboard()
                return

    messagebox.showerror("Error", "Invalid email or password\nPlease register if you don't have an account")

def logout():
    global current_user_email
    current_user_email = None
    dashboard_frame.pack_forget()
    login_frame.pack()

# ---------------- DASHBOARD FUNCTIONS ----------------
def add_usage():
    try:
        water = float(water_entry.get())
        electricity = float(electricity_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid numbers")
        return

    today = date.today().isoformat()

    water_alert = "Yes" if water > WATER_LIMIT else "No"
    electricity_alert = "Yes" if electricity > ELECTRICITY_LIMIT else "No"

    water_bill = water * WATER_RATE
    electricity_bill = electricity * ELECTRICITY_RATE
    total_bill = water_bill + electricity_bill

    with open(USAGE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            current_user_email, today, water, electricity,
            water_alert, electricity_alert,
            water_bill, electricity_bill, total_bill
        ])

    alert_msg = "Usage saved successfully!\n"
    if water_alert == "Yes":
        alert_msg += "⚠ High Water Usage\n"
    if electricity_alert == "Yes":
        alert_msg += "⚠ High Electricity Usage"

    messagebox.showinfo("Status", alert_msg)
    water_entry.delete(0, tk.END)
    electricity_entry.delete(0, tk.END)

def view_report():
    total_water = total_elec = total_bill = 0

    with open(USAGE_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Email"] == current_user_email:
                total_water += float(row["Water"])
                total_elec += float(row["Electricity"])
                total_bill += float(row["TotalBill"])

    messagebox.showinfo(
        "Usage Report",
        f"Total Water Used: {total_water:.2f} L\n"
        f"Total Electricity Used: {total_elec:.2f} Units\n\n"
        f"Total Bill: ₹{total_bill:.2f}"
    )

def open_dashboard():
    login_frame.pack_forget()
    dashboard_frame.pack()

def clear_login_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Water & Electricity Monitoring System")
root.geometry("480x560")
root.configure(bg="#f4f6f8")

create_files()

# ---------------- LOGIN FRAME ----------------
login_frame = tk.Frame(root, bg="#f4f6f8")
login_frame.pack(pady=30)

tk.Label(login_frame, text="User Login / Register",
         font=("Helvetica", 18, "bold"), bg="#f4f6f8").pack(pady=15)

tk.Label(login_frame, text="Name", bg="#f4f6f8").pack(anchor="w")
name_entry = tk.Entry(login_frame, width=30)
name_entry.pack(pady=5)

tk.Label(login_frame, text="Email (Unique ID)", bg="#f4f6f8").pack(anchor="w")
email_entry = tk.Entry(login_frame, width=30)
email_entry.pack(pady=5)

tk.Label(login_frame, text="Password", bg="#f4f6f8").pack(anchor="w")
password_entry = tk.Entry(login_frame, width=30, show="*")
password_entry.pack(pady=5)

show_pass_var = tk.BooleanVar()
tk.Checkbutton(login_frame, text="Show Password",
               variable=show_pass_var,
               command=toggle_password,
               bg="#f4f6f8").pack()

tk.Button(login_frame, text="Login", width=25,
          bg="#4CAF50", fg="white", command=login).pack(pady=5)

tk.Button(login_frame, text="Register", width=25,
          bg="#2196F3", fg="white", command=register).pack()

# ---------------- DASHBOARD FRAME ----------------
dashboard_frame = tk.Frame(root, bg="#f4f6f8")

tk.Label(dashboard_frame, text="Dashboard",
         font=("Helvetica", 18, "bold"), bg="#f4f6f8").pack(pady=15)

tk.Label(dashboard_frame, text="Water Usage (Liters)", bg="#f4f6f8").pack()
water_entry = tk.Entry(dashboard_frame, width=25)
water_entry.pack(pady=5)

tk.Label(dashboard_frame, text="Electricity Usage (Units)", bg="#f4f6f8").pack()
electricity_entry = tk.Entry(dashboard_frame, width=25)
electricity_entry.pack(pady=5)

tk.Button(dashboard_frame, text="Add Usage", width=30,
          bg="#FF9800", fg="white", command=add_usage).pack(pady=8)

tk.Button(dashboard_frame, text="View Report", width=30,
          bg="#9C27B0", fg="white", command=view_report).pack(pady=5)

tk.Button(dashboard_frame, text="Logout", width=30,
          bg="#f44336", fg="white", command=logout).pack(pady=10)

root.mainloop()