import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

date_format = "%d-%m-%Y"

class CSV:
    CSV_FILE = "finance_data.csv"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        df = pd.DataFrame([new_entry])
        df.to_csv(cls.CSV_FILE, mode='a', header=False, index=False)

    @classmethod
    def get_transactions(cls, startDate, endDate):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = df["Date"].map(lambda x: datetime.strptime(x, date_format))
        startDate = datetime.strptime(startDate, date_format)
        endDate = datetime.strptime(endDate, date_format)

        mask = (df["Date"] >= startDate) & (df["Date"] <= endDate)
        filtered_data = df.loc[mask]
        if filtered_data.empty:
            print("No Transactions")
        else:
            print(f"Transactions from {startDate.strftime(date_format)} to {endDate.strftime(date_format)}")
            print(filtered_data.to_string(index=False, formatters={"Date": lambda x: x.strftime(date_format)}))
            
            total_income = filtered_data[filtered_data["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_data[filtered_data["Category"] == "Expense"]["Amount"].sum()
            
            print("\nSummary:")
            print(f"Total Income: ₹{total_income:.2f}")
            print(f"Total Expense: ₹{total_expense:.2f}")
            print(f"Net Savings: ₹{(total_income-total_expense):.2f}")
            
            return filtered_data 

def add():
    CSV.initialize_csv()
    date = get_date("Enter the Date of the transaction (dd-mm-yyyy). Press enter for using today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plotTransactions(dataframe):
    dataframe.set_index('Date', inplace=True)

    income = dataframe[dataframe["Category"]=="Income"].resample('D').sum().reindex(dataframe.index, fill_value=0)
    expense = dataframe[dataframe["Category"]=="Expense"].resample('D').sum().reindex(dataframe.index, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income.index, income["Amount"], label="Income", color="g")
    plt.plot(expense.index, expense["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over time-range")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            startDate = get_date("Enter start date (dd-mm-yyyy): ")
            endDate = get_date("Enter end date (dd-mm-yyyy): ")
            filteredData = CSV.get_transactions(startDate, endDate)

            if input("Do you want to see a plot of the data? (y/n): ").lower() == 'y':
                plotTransactions(filteredData)
        elif choice == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()
