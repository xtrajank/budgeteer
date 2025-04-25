from budgeteer import BudgetTracker

def test_budget_tracker(csv_path):
    print("\n Starting BudgetTracker Test...\n")
    
    # 1. Initialize Tracker
    tracker = BudgetTracker(csv_path)
    print("Loaded data successfully.\n")
    
    # 2. Apply categorization rules
    tracker.apply_rule('Housing', 'cheque')
    tracker.apply_rule('Tax', 'tax')
    tracker.apply_rule('Interest', 'interest')
    tracker.categorize()
    print("Applied categorization rules.\n")
    
    # 3. View categorized data (first 5 rows)
    print("Categorized Data Sample:")
    print(tracker.data[['date', 'description', 'withdrawls', 'category']].head(), "\n")
    
    # 4. Summarize total spending
    print("Total Spending by Category:")
    print(tracker.summarize_total_spend_by_category(), "\n")
    
    # 5. Spending averages over biweekly periods
    print("Average Spending per Biweekly Period:")
    print(tracker.calc_spending_averages(freq='2W'), "\n")
    
    # 6. Generate a baseline budget
    print("Generated Baseline Budget:")
    baseline = tracker.generate_baseline_budget(freq='2W')
    print(baseline, "\n")
    
    # 7. Set budget goals manually
    tracker.add_budget_goal('housing', 500000.0)
    tracker.add_budget_goal('tax', 200000.0)
    tracker.add_budget_goal('interest', 250000.0)
    print("Budget goals set.\n")
    
    # 8. Compare actual spending to budget goals
    print("Comparison to Budget Goals (Most Recent Biweekly Period):")
    tracker.compare_to_goals(freq='2W', period_index=1)
    print()
    
    # 9. Detect duplicates
    duplicates = tracker.detect_duplicates()
    print(f"Found {len(duplicates)} duplicate transactions.\n")
    
    # 10. Export cleaned, categorized data
    tracker.export_csv('output_cleaned_transactions.csv')
    print("Exported cleaned data to 'output_cleaned_transactions.csv'\n")

    print("Test Completed.\n")

def main():
    test_budget_tracker('test/50000_BT_Records.csv')

if __name__ == '__main__':
    main()
