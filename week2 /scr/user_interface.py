from expense_manager import ExpenseManager
def main():
    manager = ExpenseManager()
    
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add a new expense")
        print("2. View expenses")
        print("3. Calculate total expenses by category or month")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            manager.add_expense()
        
        elif choice == "2":
            manager.view_expenses()

            filter_type = input("\n\nHow do you want to view your Expences: \n1. Category\n2. Month\n:")

            if filter_type.lower() == "category":
                category = input("Enter category: ")
                manager.view_expenses(category=category.lower())
            elif filter_type.lower() == "month":
                month = input("Enter month (YYYY-MM): ")
                manager.view_expenses(month=month)
        
        elif choice == "3":
            filter_type = input("Calculate total by (category/month): ")
            if filter_type == "category":
                category = input("Enter category: ")
                total = manager.calculate_total(category=category)
                print(f"Total expenses for {category}: {total:.2f}XAF")
            elif filter_type == "month":
                month = input("Enter month (YYYY-MM): ")
                total = manager.calculate_total(month=month)
                print(f"Total expenses for {month}: {total:.2f}XAF")
        
        elif choice == "4":
            manager.save_expenses()
            print("Expenses saved. Exiting the program.")
            break
        
        else:
            print("Invalid option. Please try again.")

