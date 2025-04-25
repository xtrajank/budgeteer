import pandas as pd

class BudgetTracker:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.clean_data()
        self.rules_dict = {}
        self.budget_goals = {}

    def clean_data(self):
        # standardize columns, convert date, drop rows with missing important data
        self.data.columns = [col.strip().lower() for col in self.data.columns]
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data.dropna(subset=['date'], inplace=True)

        for col in ['deposits', 'withdrawls', 'balance']:
            self.data[col] = (self.data[col].astype(str).str.replace(',', '', regex=False).astype(float))

    def apply_rule(self, category: str, keyword: str) -> dict:
        # add a rule to rule dictionary
        # if the category is already set
        if category.lower() in self.rules_dict:
            self.rules_dict[category.lower()].append(keyword.lower())
        else:
            self.rules_dict[category.lower()] = [keyword.lower()]
        return self.rules_dict
    
    def categorize(self):
        # apply category rules for a keyword lookup
        self.data['category'] = self.data['description'].apply(lambda desc: self.match_category(desc))

    def match_category(self, desc):
        # matches the category to be used in categorize
        for category, keywords in self.rules_dict.items():
            if desc.lower() in keywords:
                return category
        return 'miscellaneous'
    
    def summarize_total_spend_by_category(self):
        return self.data.groupby('category')['withdrawls'].sum().sort_values()
    
    def summarize_spend_by_category_period(self, freq='2W'):
        '''
        Calculates the total spent per category for a certain period length (default: biweekly)
        Frequency options (Pandas-style): 'W' (weekly), '2W' (biweekly), 'M' (monthly), 
        'D' (daily), 'Q' (quarterly), 'Y' (yearly) etc.
        '''
        if 'date' not in self.data.columns or 'category' not in self.data.columns:
            raise ValueError('Data must include \'date\' and \'category\' columns.')

        # set date as index
        data = self.data.copy()
        data.set_index('date', inplace=True)

        # resample by period and group by category for whole table
        period_summary = data.groupby([pd.Grouper(freq=freq), 'category'])['withdrawls'].sum()

        # pivot table: rows = periods, columns = categories
        period_data = period_summary.unstack(fill_value=0)

        return period_data
    
    def calc_spending_totals_for_period(self, freq='2W', period_index=1):
        '''
        Calculates the total spent per category for a certain period length (default: biweekly) and period (most recent is the default at 1).
        Frequency options (Pandas-style): 'W' (weekly), '2W' (biweekly), 'M' (monthly), 
        'D' (daily), 'Q' (quarterly), 'Y' (yearly) etc.
        Period_index=1 is the most recent period
        '''
        period_data = self.summarize_spend_by_category_period(freq)

        # check that the period index in range
        if period_index > len(period_data):
            raise ValueError(f'Requested period_index={period_index} is out of range. Only {len(period_data)} available.')

        # use negative index to get the n-th most recent period 
        return period_data.iloc[-period_index]

    def calc_spending_averages(self, freq='2W'):
        '''
        Calculate average spending per pay period (default: biweekly).
        Frequency options (Pandas-style): 'W' (weekly), '2W' (biweekly), 'M' (monthly), 
        'D' (daily), 'Q' (quarterly), 'Y' (yearly) etc.
        '''
        period_data = self.summarize_spend_by_category_period(freq)

        # return average per category across periods
        return period_data.mean().sort_values()

    def generate_baseline_budget(self, freq='2W'):
        '''
        Calculate average amount spent per category.
        Output a baseline budget that reflects spending habits
        '''
        period_data = self.summarize_spend_by_category_period(freq)

        # get average spend per category across periods
        avg_per_category = period_data.mean().sort_values()
        avg_per_category = avg_per_category.abs()

        # store as baseline
        self.baseline_budget = avg_per_category.to_dict()

        return self.baseline_budget
    
    def add_budget_goal(self, category: str, goal: float):
        '''
        Set a goal in the budget dictionary.
        '''
        self.budget_goals[category.lower()] = goal

    def compare_to_goals(self, freq='2W', period_index=1):
        '''
        Compare the goals set to your average spend for that period (default: biweekly).
        Frequency options (Pandas-style): 'W' (weekly), '2W' (biweekly), 'M' (monthly), 
        'D' (daily), 'Q' (quarterly), 'Y' (yearly) etc.
        '''
        category_spend = self.calc_spending_totals_for_period(freq, period_index)

        for category, spend in category_spend.items():
            if category.lower() in self.budget_goals:
                difference = spend - self.budget_goals[category]
                message = f'{category.title()} | Actual: ${spend:.2f} Goal: ${self.budget_goals[category]:.2f} | Difference: ${abs(difference):.2f}'
                if difference > 0:
                    message += ' over budget'
                elif difference < 0:
                    message += ' under budget'
                print(message)
            else:
                print(f'No goal set for {category}')

    def detect_duplicates(self):
        return self.data[self.data.duplicated(subset=['date', 'deposits', 'withdrawls', 'description'], keep=False)]
    
    def export_csv(self, out_path):
        self.data.to_csv(out_path, index=False)