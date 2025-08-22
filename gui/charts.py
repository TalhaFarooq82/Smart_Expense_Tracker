import matplotlib
import matplotlib.pyplot as plt

def show_charts(expenses):
    if not expenses:
        return

    # Create dictionaries to hold totals
    category_totals = {}
    date_totals = {}

    # Loop through each expense
    for item in expenses:
        date = item[0]
        category = item[1]
        amount = float(item[2])

        # Add to category totals
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

        # Add to date totals
        if date in date_totals:
            date_totals[date] += amount
        else:
            date_totals[date] = amount

    # Create a pie chart for category totals
    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    plt.pie(
        list(category_totals.values()),
        labels=list(category_totals.keys()),
        autopct='%1.1f%%'
    )
    plt.title("Pie: Expenses by Category")

    # Create a bar chart for category totals
    plt.subplot(1, 3, 2)
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    plt.bar(categories, amounts, color='skyblue')
    plt.title("Bar: Category Expenses")
    plt.xticks(rotation=45)

    # Create a line chart for date totals
    plt.subplot(1, 3, 3)
    sorted_dates = sorted(date_totals.items())  # list of (date, total)
    x_dates = []
    y_amounts = []
    for pair in sorted_dates:
        x_dates.append(pair[0])
        y_amounts.append(pair[1])

    plt.plot(x_dates, y_amounts, marker='o')
    plt.title("Line: Expenses Over Time")
    plt.xticks(rotation=45)

    # Show all charts
    plt.tight_layout()
    plt.show()
