import calendar
import csv
from collections import defaultdict
from datetime import datetime
from expence import Expense

class ExpenseManager:
    def __init__(self):
        # Default categories
        default_categories = ["Food", "Transportation", "Utilities", "Entertainment","Healthcare", "Groceries", "Education"]

        # Initialize expenses dictionary with default categories
        self.expenses = defaultdict(list)
        for category in default_categories:
            self.expenses[category]  # This ensures each default category has an empty list
        
        self.expense_file = "week2 /docs/expenses.csv"
        self.load_expenses()

    def add_expense(self):
            # showing the existing categories
            existing_categories = list(self.expenses.keys())
            if existing_categories:
                print("\n\n============================================ ADDING AN EXPENSE ================================")
                print("\nExisting Categories:")
                for i, category in enumerate(existing_categories, start=1):
                    print(f"{i}. {category}")
                print(f"{len(existing_categories) + 1}. Add a new category")
                print(f"{len(existing_categories) + 2}. Delete an existing category")
            else:
                print("No categories found. You'll need to add a new category.")

            # Get the user's choice for the category
            choice = input("Choose a category by number, or enter 'new' to add a new category, 'delete' to delete a category: ").strip()

            # Determine category based on choice
            if choice.lower() == 'new' or (existing_categories and choice == str(len(existing_categories) + 1)):
                category = input("Enter the new category name: ").strip()
                if category in self.expenses:
                    print(f"Category '{category}' already exists. Selecting existing category.")
                else:
                    print(f"Creating new category '{category}'...")
                    self.expenses[category] = []  # Initialize the new category with an empty list
            elif choice.lower() == 'delete' or (existing_categories and choice == str(len(existing_categories) + 2)):
                delete_choice = input("Enter the number of the category to delete: ").strip()
                if delete_choice.isdigit() and 1 <= int(delete_choice) <= len(existing_categories):
                    category_to_delete = existing_categories[int(delete_choice) - 1]
                    confirm_delete = input(f"Are you sure you want to delete the category '{category_to_delete}'? (yes/no): ").strip().lower()
                    if confirm_delete == 'yes':
                        del self.expenses[category_to_delete]
                        print(f"Category '{category_to_delete}' deleted successfully.")
                        self.save_expenses()  # Save the changes
                        return  # Exit after deletion
                    else:
                        print("Category deletion canceled.")
                        return
                else:
                    print("Invalid choice. Please try again.")
                    return
            elif choice.isdigit() and 1 <= int(choice) <= len(existing_categories):
                category = existing_categories[int(choice) - 1]
                print(f"Selected category '{category}'.")
            else:
                print("Invalid choice. Please try again.")
                return  # Exit if invalid choice

            # Get amount and date for the expense
            try:
                amount = float(input("Enter the expense amount: "))
                # Choose today’s date or enter a custom date
                date_choice = input("Enter 'today' for today's date, or 'custom' to enter a specific date: ").strip().lower()
                if date_choice == 'today':
                    date = datetime.today()
                elif date_choice == 'custom':
                    date_str = input("Enter the date of the expense (YYYY-MM-DD): ")
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                else:
                    print("Invalid choice for date. Please try again.")
                    return
                expense = Expense(category, amount, date)
                self.expenses[category].append(expense)
                print("Expense added successfully.")
            except ValueError as e:
                print(f"Error: {e}. Please ensure amount is a number and date is in YYYY-MM-DD format.")

            # Save to file after adding the expense
            self.save_expenses()
    def calculate_total(self, category=None, month=None):
        total = 0.0

        # Calculate total by category (case-insensitive)
        if category:
            category_lower = category.lower()  # Convert user input to lowercase
            for cat, expenses in self.expenses.items():
                if cat.lower() == category_lower:  # Compare in lowercase
                    total = sum(expense.amount for expense in expenses)

                    break

        # Calculate total by month
        elif month:
            try:
                year, month_num = map(int, month.split("-"))
                total = sum(
                    expense.amount for expenses in self.expenses.values()
                    for expense in expenses if expense.date.year == year and expense.date.month == month_num
                )

            except ValueError:
                print("Invalid month format. Please enter month in 'YYYY-MM' format.")
        return total

    def save_expenses(self):
        with open(self.expense_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Amount", "Date"])
            for expenses in self.expenses.values():
                for expense in expenses:
                    writer.writerow([expense.category, expense.amount, expense.date.strftime("%Y-%m-%d")])
    def view_expenses(self, category=None, month=None):
        found_expenses = []

        # Check for expenses by category (case-insensitive)
        if category:
            category_lower = category.lower()  # Converting user input to lowercase
            for cat, expenses in self.expenses.items():
                if cat.lower() == category_lower:  # Comparing in lowercase
                    found_expenses = expenses
                    break
            if not found_expenses:
                print(f"No expenses found for category: {category}")
                return  # Exit if no expenses for the given category

        # Check for expenses by month
        elif month:
            try:
                year, month_num = map(int, month.split("-"))
                for expenses in self.expenses.values():
                    for expense in expenses:
                        # Compare year and month directly with expense's date attributes
                        if expense.date.year == year and expense.date.month == month_num:
                            found_expenses.append(expense)
            except ValueError:
                print("Invalid month format. Please enter month in 'YYYY-MM' format.")
                return

        # Display the found expenses
        if found_expenses:
            print("\nExpenses:")
            for expense in found_expenses:
                print(f"Category: {expense.category}, Amount: {expense.amount} XAF, Date: {expense.date}")
        else:
            print("No expenses found for the specified filters.")

    def load_expenses(self):
        try:
            with open(self.expense_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = row["Category"]
                    amount = float(row["Amount"])
                    date = datetime.strptime(row["Date"], "%Y-%m-%d")
                    self.expenses[category].append(Expense(category, amount, date))
                print(self.expenses)
        except FileNotFoundError:
            print("No existing expense file found. Starting with a blank record.")
