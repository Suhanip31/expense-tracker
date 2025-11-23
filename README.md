# Expense Tracker (CLI)

## About

I built this CLI-based Expense Tracker to easily keep track of my personal expenses. It helps me log daily spending, view summaries by category or month, search expenses, and visualize trends with charts. This project is perfect for learning Python, pandas, and matplotlib while building a practical tool.

## Features

* Add expenses with date, category, amount, and description
* View all expenses (latest first)
* Delete expenses by date
* Summarize expenses by category or month
* Search expenses by date, category, or keywords
* Export expenses to CSV
* Visualize spending with bar, pie, and monthly trend charts

## Installation

1. Clone or download this repository
2. Make sure you have Python installed (tested with Python 3.10+)
3. Install required packages:

   ```bash
   pip install pandas matplotlib
   

## Usage

1. Open terminal or PowerShell in the project folder
2. Run the program:

   ```bash
   python expense_tracker_pandas.py
   ```
3. Follow the menu to add expenses, view summaries, or generate charts.

### Example

```
===== EXPENSE TRACKER (PANDAS) =====
1. Add Expense
2. View All Expenses
...
Enter your choice: 1
Enter date (YYYY-MM-DD) [default today]: 2025-03-12
Enter category: food
Enter amount: 550
Enter description: dinner
Expense added successfully!
```

## Folder Structure

```
expense-tracker/
├── expense_tracker_pandas.py   # Main Python script
├── expenses_pandas.csv         # CSV file storing expenses
├── charts/                     # Folder for saved charts
└── README.md
```

## License

This project is open source and free to use.
