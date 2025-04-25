import pytest
import pandas as pd
from src.budgeteer import BudgetTracker

@pytest.fixture
def tracker(tmp_path):
    csv_data = """Date,Description,Deposits,Withdrawls,Balance
20-Aug-2020,Cheque,"582,827.75",0.00,"609,730.09"
20-Aug-2020,Interest,0.00,"76,216.26","533,513.83"
20-Aug-2020,Cheque,0.00,"177,837.94","355,675.89"
20-Aug-2020,Tax,0.00,"50,810.84","304,865.05"
"""

    # Save sample CSV to a temp file
    csv_path = tmp_path / "test_data.csv"
    with open(csv_path, "w") as f:
        f.write(csv_data)

    tracker = BudgetTracker(str(csv_path))

    tracker.apply_rule('Housing', 'cheque')
    tracker.apply_rule('Tax', 'tax')
    tracker.apply_rule('Interest', 'interest')
    tracker.categorize()

    return tracker

# tests
def test_clean_data(tracker):
    assert 'date' in tracker.data.columns
    assert pd.api.types.is_datetime64_any_dtype(tracker.data['date'])
    assert tracker.data.isnull().sum().sum() == 0 # no missing values

def test_categorization(tracker):
    categories = tracker.data['category'].unique()
    assert 'housing' in categories
    assert 'tax' in categories
    assert 'interest' in categories

def test_summarize_total_spend(tracker):
    total_spend = tracker.summarize_total_spend_by_category()
    assert isinstance(total_spend, pd.Series)
    assert not total_spend.empty

def test_spending_averages(tracker):
    averages = tracker.calc_spending_averages()
    assert isinstance(averages, pd.Series)
    assert all(averages >= 0)

def test_baseline_budget(tracker):
    budget = tracker.generate_baseline_budget()
    assert isinstance(budget, dict)
    assert 'housing' in budget
    assert all(value >= 0 for value in budget.values())

def test_budget_goals(tracker):
    tracker.add_budget_goal('housing', 1000.0)
    tracker.add_budget_goal('tax', 500.0)
    assert tracker.budget_goals['housing'] == 1000.0
    assert tracker.budget_goals['tax'] == 500.0

def test_compare_to_goals(tracker, capsys):
    tracker.add_budget_goal('housing', 1000000.0)
    tracker.add_budget_goal('tax', 100000.0)
    tracker.compare_to_goals(freq='2W', period_index=1)

    captured = capsys.readouterr()
    assert "Actual:" in captured.out
    assert "Goal:" in captured.out

def test_detect_duplicates(tracker):
    duplicates = tracker.detect_duplicates()
    assert isinstance(duplicates, pd.DataFrame)
    assert duplicates.empty

def test_export_csv(tmp_path, tracker):
    output_path = tmp_path / "output.csv"
    tracker.export_csv(str(output_path))
    assert output_path.exists()