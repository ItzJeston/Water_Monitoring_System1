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
# Add Expense
# -------------------------------
def add_expense():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")

    category = input("Enter category (Food/Travel/Shopping/Bills/Others): ")
    
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("❌ Amount must be positive.")
            return
    except ValueError:
        print("❌ Invalid amount.")
        return

    description = input("Enter description: ")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    print("✅ Expense added successfully!")


# -------------------------------
# View All Expenses
# -------------------------------
def view_expenses():
    total = 0
    print("\n--- All Expenses ---")
    
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            print(f"Date: {row[0]}, Category: {row[1]}, Amount: ₹{row[2]}, Note: {row[3]}")
            total += float(row[2])

    print(f"\n💰 Total Spending: ₹{total}")


# -------------------------------
# Monthly Report
# -------------------------------
def monthly_report():
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    total = 0
    print(f"\n--- Report for {month}/{year} ---")

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            expense_date = datetime.strptime(row[0], "%Y-%m-%d")
            if expense_date.month == int(month) and expense_date.year == int(year):
                print(f"{row[0]} | {row[1]} | ₹{row[2]} | {row[3]}")
                total += float(row[2])

    print(f"\n📊 Monthly Total: ₹{total}")


# -------------------------------
# Category-wise Analysis
# -------------------------------
def category_analysis():
    category_total = {}

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            category = row[1]
            amount = float(row[2])
            category_total[category] = category_total.get(category, 0) + amount

    print("\n--- Category-wise Spending ---")
    for category, amount in category_total.items():
        print(f"{category}: ₹{amount}")


# -------------------------------
# Budget Check
# -------------------------------
def budget_check():
    try:
        budget = float(input("Enter your monthly budget: "))
    except ValueError:
        print("❌ Invalid budget.")
        return

    total = 0
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            total += float(row[2])

    if total > budget:
        print(f"⚠ ALERT! Budget exceeded by ₹{total - budget}")
    else:
        print(f"✅ You are within budget. Remaining: ₹{budget - total}")


# -------------------------------
# Main Menu
# -------------------------------
def main():
    initialize_file()

    while True:
        print("\n====== SMART EXPENSE TRACKER ======")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Monthly Report")
        print("4. Category-wise Analysis")
        print("5. Budget Check")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_report()
        elif choice == "4":
            category_analysis()
        elif choice == "5":
            budget_check()
        elif choice == "6":
            print("👋 Thank you for using Expense Tracker!")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
