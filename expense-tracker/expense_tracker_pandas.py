

import os
import pandas as pd
from datetime import datetime

# Force charts folder creation with absolute path
charts_folder = r"C:\Users\kisha\OneDrive\Desktop\resume project\charts"
if not os.path.exists(charts_folder):
    os.makedirs(charts_folder)
    print(f"'charts' folder created at: {charts_folder}")
else:
    print(f"'charts' folder already exists at: {charts_folder}")


DATA_FILE = "expenses_pandas.csv"
CSV_COLUMNS = ["date", "category", "amount", "description"]

def ensure_datafile():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=CSV_COLUMNS)
        df.to_csv(DATA_FILE, index=False)

def load_df():
    ensure_datafile()
    df = pd.read_csv(DATA_FILE)
    # ensure correct dtypes
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    return df

def save_df(df):
    df.to_csv(DATA_FILE, index=False)

def add_expense():
    date = input("Enter date (YYYY-MM-DD) [default today]: ").strip() or datetime.today().strftime("%Y-%m-%d")
    category = input("Enter category (food, travel, shopping, etc): ").strip()
    amount = input("Enter amount: ").strip()
    description = input("Enter description: ").strip()

    # validate
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        amount = float(amount)
    except:
        print("Amount must be a number.")
        return

    df = load_df()
    new_row = {"date": date, "category": category, "amount": amount, "description": description}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_df(df)
    print("Expense added successfully!\n")

def view_expenses(limit=None):
    df = load_df()
    if df.empty:
        print("\n--- No expenses found ---\n")
        return
    # show newest first
    df_sorted = df.sort_values(by="date", ascending=False)
    if limit:
        df_sorted = df_sorted.head(limit)
    print("\n--- All Expenses ---")
    for _, row in df_sorted.iterrows():
        print(f"Date: {row['date']}, Category: {row['category']}, Amount: {row['amount']}, Description: {row['description']}")
    print()

def delete_by_date():
    df = load_df()
    if df.empty:
        print("No expenses to delete.")
        return
    print("\n--- All Expenses ---")
    view_expenses()
    target = input("Enter the date (YYYY-MM-DD) of expense to delete (this will delete ALL rows with this date): ").strip()
    try:
        datetime.strptime(target, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return
    before_count = len(df)
    df = df[df["date"] != target]
    after_count = len(df)
    if after_count < before_count:
        save_df(df)
        print(f"Deleted {before_count - after_count} record(s) with date {target}.\n")
    else:
        print("No records found with that date.\n")

def search_expenses():
    df = load_df()
    if df.empty:
        print("No expenses found.")
        return
    print("\nSearch by:")
    print("1. Date (YYYY-MM-DD)")
    print("2. Category")
    print("3. Keyword in description")
    choice = input("Enter choice: ").strip()
    if choice == "1":
        date = input("Enter date (YYYY-MM-DD): ").strip()
        res = df[df["date"] == date]
    elif choice == "2":
        cat = input("Enter category (case insensitive): ").strip().lower()
        res = df[df["category"].str.lower() == cat]
    elif choice == "3":
        kw = input("Enter keyword: ").strip().lower()
        res = df[df["description"].str.lower().str.contains(kw, na=False)]
    else:
        print("Invalid choice.")
        return

    if res.empty:
        print("No results found.")
    else:
        res = res.sort_values(by="date", ascending=False)
        print("\n--- Search Results ---")
        for _, row in res.iterrows():
            print(f"Date: {row['date']}, Category: {row['category']}, Amount: {row['amount']}, Description: {row['description']}")
    print()

import matplotlib.pyplot as plt

def show_category_graph(df):
    if df.empty:
        print("No expenses to show graph.")
        return

    category_sum = df.groupby("category")["amount"].sum()

    # Bar Chart
    bar_path = os.path.join(charts_folder, "category_bar_chart.png")
    ax = category_sum.plot(kind='bar')
    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(bar_path)   # Save bar chart
    plt.show()
    plt.close()
    print(f"Bar chart saved to: {bar_path}")

    # Pie Chart
    pie_path = os.path.join(charts_folder, "category_pie_chart.png")
    ax = category_sum.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Category-wise Expense Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(pie_path)   # Save pie chart
    plt.show()
    plt.close()
    print(f"Pie chart saved to: {pie_path}")

def show_monthly_trend(df):
    if df.empty:
        print("No expenses to show monthly trend.")
        return

    # Ensure month column exists
    df["month"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m")
    monthly_sum = df.groupby("month")["amount"].sum().sort_index()

    # Line chart
    trend_path = os.path.join(charts_folder, "monthly_trend.png")
    ax = monthly_sum.plot(kind='line', marker='o')
    plt.title("Monthly Expense Trend")
    plt.xlabel("Month (YYYY-MM)")
    plt.ylabel("Total Amount")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(trend_path)  # Save line chart
    plt.show()
    plt.close()
    print(f"Monthly trend chart saved to: {trend_path}")


def summary_by_category():
    df = load_df()
    if df.empty:
        print("No data for summary.")
        return
    s = df.groupby("category", as_index=False)["amount"].sum().sort_values(by="amount", ascending=False)
    print("\n--- Summary by Category ---")
    for _, row in s.iterrows():
        print(f"{row['category']}: ₹{row['amount']:.2f}")
    print()

def summary_by_month():
    df = load_df()
    if df.empty:
        print("No data for monthly summary.")
        return
    # create month column YYYY-MM
    df["month"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m")
    s = df.groupby("month", as_index=False)["amount"].sum().sort_values(by="month")
    print("\n--- Summary by Month (YYYY-MM) ---")
    for _, row in s.iterrows():
        print(f"{row['month']}: ₹{row['amount']:.2f}")
    print()

def export_clean_csv():
    df = load_df()
    if df.empty:
        print("No data to export.")
        return
    out_path = input("Enter export filename (default export_expenses.csv): ").strip() or "export_expenses.csv"
    df.to_csv(out_path, index=False)
    print(f"Exported to {out_path}\n")

def menu():
    print("===== EXPENSE TRACKER (PANDAS) =====")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Delete Expense by Date")
    print("4. Summary by Category")
    print("5. Summary by Month")
    print("6. Search Expenses")
    print("7. Export CSV")
    print("8. Show Category Graph") 
    print("9. Show Monthly Trend Graph")
    print("10.Exit")

def main():
    ensure_datafile()
    while True:
        menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_by_date()
        elif choice == "4":
            summary_by_category()
        elif choice == "5":
            summary_by_month()
        elif choice == "6":
            search_expenses()
        elif choice == "7":
            export_clean_csv()
        elif choice == "8":
            df = load_df()
            show_category_graph(df)
        elif choice == "9":
            df = load_df()
            show_monthly_trend(df)
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.\n")

if __name__ == "__main__":
    main()
