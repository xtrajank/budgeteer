# Budgeteer
A Python-based tool for personal finance analysis using Pandas.
Budgeteer imports bank transaction CSVs, categorizes expenses using keyword rules, summarizes spending trends, and compares actual expenses against your budget goals — all without needing Excel formulas or manual tracking.

Features:
- Load bank data from CSV
- Categorize transactions using keyword-based rules
- Summarize total spending by category
- Analyze spending trends over custom periods (weekly, biweekly, monthly, etc.)
- Set budget goals and compare against real spending
- Generate a baseline budget from your actual habits
- Detect duplicate transactions
- Export cleaned and categorized data back to CSV
- Full unit-tested code using pytest

Requirements:
- Python 3.8+
- pandas
- pytest (for testing)

How it Works:
1. Load Data
    Your Transaction CSV should have at least these columns:
        Date, Description, Deposits, Withdrawls

    The program cleans up the data, removes commas, and parses data

2. Apply Categorization rules
    Assign keywords to categorize your data: (category, description keyword)
        tracker.apply_rule('Food', 'starbucks')
        tracker.apply_rule('Housing', 'cheque')
        tracker.categorize()

3. View and Analyze Spending
- Summarize all time spending
    tracker.summarize_total_spend_by_category()
- Summarize per period
    tracker.calc_spending_totals_for_period(freq='M', period_index=1)
- Summarize average per period
    tracker.calc_spending_averages(freq='2W')

4. Budget Planning
- Generate a baseline budget
    tracker.generate_baseline_budget(freq='2W')
- Set and compare goals
    tracker.add_budget_goal('food', 300.0)
    tracker.compare_to_goals(freq='2W', period_index=1)

5. Export Data
- Cleaned and categorized data can be exported back to CSV:
    tracker.export_csv('output.csv')

Coming Soon:
- Plot spending vs. budget
- Web UI