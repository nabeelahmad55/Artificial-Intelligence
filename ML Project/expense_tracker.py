import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"


def load_expenses():
    """Load expenses from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_expenses(expenses):
    """Save expenses to JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense():
    """Add a new expense entry."""
    description = input("Enter description: ")
    amount = float(input("Enter amount (PKR): "))
    category = input("Enter category (food, travel, etc.): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    expenses = load_expenses()
    expenses.append({
        "description": description,
        "amount": amount,
        "category": category,
        "date": date
    })
    save_expenses(expenses)
    print("\n✅ Expense added successfully!\n")


def view_expenses():
    """View all expenses."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    print("\n------ Expense List ------")
    total = 0
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. {exp['description']} - PKR {exp['amount']} ({exp['category']}) on {exp['date']}")
        total += exp["amount"]
    print(f"\n💰 Total Spent: PKR {total}\n")


def delete_expense():
    """Delete an expense by its number."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses to delete.\n")
        return

    view_expenses()
    try:
        num = int(input("Enter the number of the expense to delete: "))
        if 1 <= num <= len(expenses):
            removed = expenses.pop(num - 1)
            save_expenses(expenses)
            print(f"\n🗑️ Deleted: {removed['description']} (PKR {removed['amount']})\n")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def main():
    """Main menu loop."""
    while True:
        print("========== Expense Tracker ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Exit")
        choice = input("Select an option (1-4): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            print("\nGoodbye! 👋")
            break
        else:
            print("\nInvalid option, please try again.\n")


if __name__ == "__main__":
    main()
