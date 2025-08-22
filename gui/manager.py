import csv
import os

class ExpenseManager:
    def __init__(self, filename="data/expenses.csv"):
        self.filename = filename
        self.expenses = []
        self.load()

    def load(self):
        try:
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                next(reader, None) 
                self.expenses = [row for row in reader]
                return self.expenses
        except FileNotFoundError:
            self.expenses = []

    def save(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount"])
            writer.writerows(self.expenses)

    def add(self, date, category, amount):
        self.expenses.append([date, category, amount])
        self.save()

    def delete_by_index(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self.save()
