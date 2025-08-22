import tkinter as tk
from tkinter import ttk
import datetime
from manager import ExpenseManager
from charts import show_charts
import requests

manager = ExpenseManager()

def toggle_date():
    if use_today_var.get():
        today = datetime.date.today().strftime("%Y-%m-%d")
        date_entry.delete(0, tk.END)
        date_entry.insert(0, today)
        date_entry.config(state="disabled")
    else:
        date_entry.config(state="normal")
        date_entry.delete(0, tk.END)

def add_expense():
    date = date_entry.get()
    category = category_var.get()
    amount = expense_entry.get()

    if date and category and amount:
        manager.add(date, category, amount)
        tree.insert("", "end", values=(date, category, amount))
        date_entry.config(state="normal")
        date_entry.delete(0, tk.END)
        expense_entry.delete(0, tk.END)
        category_dropdown.current(0)
        if use_today_var.get():
            use_today_var.set(False)
            toggle_date()
    
    if date and category and amount:        
        try:
            response = requests.post("http://127.0.0.1:5000/expenses", json={
                "date": date,
                "category": category,
                "amount": amount
            })
            print("API response:", response.json())
        except Exception as e:
            print("Error sending to API:", e)

def delete_expense():
    selected = tree.selection()
    for item_id in selected:
        index = tree.index(item_id)
        manager.delete_by_index(index)
        tree.delete(item_id)
        
        try:
            response = requests.delete(f"http://127.0.0.1:5000/expenses/{item_id}")
            print("Deleted from API:", response.json())
        except Exception as e:
            print("Error deleting from API:", e)

def show_expense_charts():
    show_charts(manager.expenses)

# ----------------- Main Window -----------------
root = tk.Tk()
root.title("Smart Expense Tracker")
root.geometry("700x500")
root.configure(bg="#f0f2f5")  # light background

# ----------------- Title Section -----------------
tk.Label(root, text="💰 Smart Expense Tracker", font=("Arial", 16, "bold"), bg="#f0f2f5", fg="#333").pack(pady=10)
tk.Label(root, text="Enter your expense details below", font=("Arial", 11), bg="#f0f2f5", fg="#555").pack(pady=5)

# ----------------- Input Form -----------------
form_frame = tk.Frame(root, bg="#f0f2f5")
form_frame.pack(pady=10)

# Row 0: Date
tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#f0f2f5", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
date_entry = tk.Entry(form_frame, font=("Arial", 10))
date_entry.grid(row=0, column=1, padx=10)

use_today_var = tk.BooleanVar()
today_checkbox = tk.Checkbutton(form_frame, text="Use current date", variable=use_today_var,
                                command=toggle_date, bg="#f0f2f5", font=("Arial", 9))
today_checkbox.grid(row=0, column=2, padx=10)

# Row 1: Category
tk.Label(form_frame, text="Category:", bg="#f0f2f5", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
categories = ["Food", "Transport", "Shopping", "Health", "Electricity Bill", "Gas Bill", "Other"]
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(form_frame, textvariable=category_var, values=categories, state="readonly", width=20)
category_dropdown.grid(row=1, column=1, padx=10)
category_dropdown.current(0)

# Row 2: Expense
tk.Label(form_frame, text="Amount:", bg="#f0f2f5", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
expense_entry = tk.Entry(form_frame, font=("Arial", 10))
expense_entry.grid(row=2, column=1, padx=10)

# ----------------- Buttons Section -----------------
button_frame = tk.Frame(root, bg="#f0f2f5")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Expense", command=add_expense,
          bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, relief="raised").grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="Delete Expense", command=delete_expense,
          bg="#dc3545", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, relief="raised").grid(row=0, column=1, padx=10)

tk.Button(button_frame, text="Show Expense Chart", command=show_expense_charts,
          bg="#007bff", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, relief="raised").grid(row=0, column=2, padx=10)

# ----------------- Table Section -----------------
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("Date", "Category", "Expense")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

tree.pack(fill="both", expand=True)

# Load previous expenses and insert into table
manager.load()
for row in manager.expenses:
    tree.insert("", "end", values=row)

# ----------------- Start the App -----------------
root.mainloop()
