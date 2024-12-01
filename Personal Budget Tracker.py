import json
from datetime import datetime
import os

class BudgetTracker:
    def __init__(self, filename = 'budget_data.json'):
        """

        Initialize the budget tracker with a JSON file for persistent storage

        Args:
             filename (str): Name of the file to store budget data. Defaults to 'budget_data.json'.
        """

        self.filename = filename
        self.budget_data = self.load_data()

    def load_data(self):
        """
        Load existing budget data from the JSON file.
        If the file doesn't exist, return an initial data structure.

        Returns:
             dict: Budget data with income, expenses, and categories
        """
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'income' : [],
                'expenses' : [],
                'categories' : {
                    'income' : ['Salary', 'Freelance', 'Investments'],
                    'expenses' : ['Rent', 'Food', 'Transportation', 'Utilities', 'Entertainment']
                }
            }
    def save_data(self):
        """

        Save the current budget data to the JSON file
        """
        with open(self.filename, 'w') as file:
            json.dump(self.budget_data, file, indent = 4)

    def add_income(self, amount, category, date = None):
        """
        Add a new income entry

        Args:
            amount (float): Amount of income
            category (str): Category of income
            date (str, optional): Date of income. Defaults to current date.
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        #Validate inputs
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Invalid amount.PLease enter a positive number.")
            return

        if category not in self.budget_data['categories']['income']:
            print(f"Category '{category}' not found. Would you like to add it ?")
            add_new = input("Enter 'y' to add the new category : ").lower()
            if add_new == 'y':
                self.budget_data['categories']['income'].append(category)
            else:
                return

        income_entry = {
            'amount' : amount,
            'category' : category,
            'date' : date
        }

        self.budget_data['income'].append(income_entry)
        self.save_data()
        print(f"Income of rupees {amount} from {category} added successfully!")

    def add_expense(self, amount, category, date = None):
        """
        Add a new expense entry.

        Args:
            amount(float) : Amount of expense
            category (str) : Category of expense
            date (str, optional) : Date of Expense. Defaults to current date.
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

            # Validate inputs
            if not isinstance(amount, (int, float)) or amount <= 0:
                print("Invalid amount. Please enter a positive number.")
                return

            if category not in self.budget_data['categories']['expenses']:
                print(f"Category '{category}' not found. Would you ike to dd it?")
                add_new = input("Enter 'y' to add the new category :").lower()
                if add_new == 'y':
                    self.budget_data['categories']['expenses'].append(category)
                else:
                    return

            expense_entry = {
                'amount' : amount,
                'category' : category,
                'date' : date
            }

            self.budget_data['expenses'].append(expense_entry)
            self.save_data()
            print(f"Expense of rupees {amount} for {category} added successfully!")

    def get_total_income(self, start_date = None, end_data = None):
        """

        Calculate total income within an optional date range


        Args:
            start_date (str, optional) : Start date for calculation
            end_data (str, optional) : End date for calculation

        Returns:
              float : Total income
        """

        return self._calculate_total(self.budget_data['income'], start_date, end_data)

    def get_total_expenses(self, start_date = None, end_date = None):
        """

        Calculate total expenses within an optional date range


        Args:
             start_date (str, optional) : Start date for calculation
             end_date (str, optional) : End date for calculation

        Returns:
            float : Total expenses
        """
        return self._calculate_total(self.budget_data['expenses'], start_date, end_date)

    def _calculate_total(self, transactions, start_date = None, end_date = None):
        """

        Helper method to calculate total of transactions within a date range

        Args:
            transactions (list) : List of income or expense transactions
            start_date (str, optional) : Start date for calculation
            end_date (str, optional) : End date for calculation

        Returns:
            float : Total of transactions
        """
        if start_date is None and end_date is None:
            return sum(transactions['amount'] for transaction in transactions)

        # Convert dates if provided

        start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.min
        end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.max

        return sum(
            transaction['amount']
            for transaction in transactions
            if start <= datetime.strptime(transaction['date'], "%Y-%m-%d") <= end
        )

    def get_category_breakdown(self, transaction_type):
        """

        Get a breakdown of transactions by category.

        Args:
            transaction_type (str) : 'income' or 'expenses'

        Returns:
            dict : Breakdown of transactions by category
        """
        if transaction_type not in ['income', 'expenses']:
            print("Invalid transaction type. Use 'income' or 'expenses'. ")
            return {}

        breakdown = {}
        for transaction in self.budget_data[transaction_type]:
            category = transaction['category']
            amount = transaction['amount']
            breakdown[category] = breakdown.get(category, 0) + amount

        return breakdown

    def monthly_summary(self):
        """

        Generate a monthly summary of income and expenses.

        Returns:
             dict : Summary of monthly financial information
        """

        current_month = datetime.now().strftime("%Y-%m")
        monthly_income = sum(
            transaction['amount']
            for transaction in self.budget_data['income']
            if transaction['date'].startswith(current_month)
        )
        monthly_expenses = sum(
            transaction['amount']
            for transaction in self.budget_data['expenses']
            if transaction['date'].stsrtswith(current_month)
        )

        return {
            'total income' : monthly_income,
            'total expenses' : monthly_expenses,
            'net savings' : monthly_income - monthly_expenses
        }

def main():
    """
    Main function to provide an interactive budget tracking interface

    """

    tracker = BudgetTracker()

    while True:
        print("\n--- Personal Budget Tracker ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Total Income")
        print("4. Category Breakdown")
        print("5. Category Breakdown")
        print("6. Monthly Summary")
        print("7. Exit")

        choices = input("Enter your choice (1 - 7) : ")

        try:
            # Add income
            if choices == '1':
                amount = float(input("Enter income amount : "))
                category = input("Enter income category : ")
                tracker.add_income(amount, category)

            # add expense
            elif choices == '2':
                amount = float("Enter expense amount : ")
                category = input("Enter expense category : ")
                tracker.add_expense(amount, category)

            # View Total Income
            elif choices == '3':
                start_date = input("Enter start date (YYYY-MM-DD, or press Enter to skip) : ") or None
                end_date = input("Enter end date (YYYY-MM-DD, or press Enter to skip) : ") or None
                total_income = tracker.get_total_income(start_date, end_date)
                print(f"Total Income : rupees {total_income:.2f}")

            # View Total Expenses
            elif choices == '4':
                start_date = input("Enter start date (YYYY-MM-DD or press Enter to skip) : ") or None
                end_date = input("Enter end date (YYYY-MM-DD or press Enter to skip) : ") or None
                total_expenses = tracker.get_total_expenses(start_date, end_date)
                print(f"Total Expenses : rupees {total_expenses:.2f}")

            # Category Breakdown
            elif choices == '5':
                trans_type = input("Enter transaction type (income/expenses) : ").lower()
                breakdown = tracker.get_category_breakdown(trans_type)
                print("\nCategory Breakdown : ")
                for category, amount in breakdown.items():
                    print(f" {category} : rupees{amount:.2f}")

            # Monthly Summary
            elif choices == '6':
                summary = tracker.monthly_summary()
                print("\nMonthly Summary : ")
                print(f"Total Income : rupees {summary['total income']:.2f}")
                print(f"Total Expenses : rupees {summary['total expenses']:.2f}")
                print(f"Net Savings : rupees {summary['net savings']:.2f}")

            elif choices == '7':
                print("Thank you for using Personal Budget Tracker!")
                break

            else:
                print("Invalid choice. Please try again")

        except ValueError:
            print("Invalid input. Please enter the valid number.")
        except Exception as e:
            print(f"An error occurred : {e}")


if __name__ == "__main__":
    main()






















