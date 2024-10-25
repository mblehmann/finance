from dataclasses import dataclass
from typing import Dict, List, Tuple

from finance.domain.budget import BudgetCategory
from finance.domain.transaction import Transaction


@dataclass
class MonthResult:
    month: int
    transactions: List[Transaction]
    categories: Dict[BudgetCategory, List[str]]

    @property
    def income_categories(self) -> List[str]:
        return self.categories[BudgetCategory.Income]

    @property
    def income_transactions(self) -> List[Transaction]:
        return [transaction for transaction in self.transactions if transaction.category in self.income_categories]

    @property
    def income_details(self) -> Dict[str, float]:
        return {name: sum([transaction.amount for transaction in self.get_transactions_by_name(name)]) for name in self.income_categories}

    @property
    def incomes(self) -> float:
        return sum([transaction.amount for transaction in self.income_transactions])
    
    @property
    def expense_categories(self) -> List[str]:
        return self.categories[BudgetCategory.Needs] + self.categories[BudgetCategory.Wants] + self.categories[BudgetCategory.Savings]
    
    @property
    def expense_transactions(self) -> List[Transaction]:
        return [transaction for transaction in self.transactions if transaction.category in self.expense_categories]

    @property
    def expense_details(self) -> Dict[str, float]:
        return {name: sum([transaction.amount for transaction in self.get_transactions_by_name(name)]) for name in self.expense_categories}
    
    @property
    def expenses(self) -> float:
        return sum([transaction.amount for transaction in self.expense_transactions])
    
    @property
    def result(self) -> float:
        return self.incomes + self.expenses
    
    @property
    def category_details(self) -> Dict[BudgetCategory, float]:
        return {category: sum([transaction.amount for transaction in self.get_transactions_by_category(category)]) for category in BudgetCategory if category != BudgetCategory.Empty}

    def get_transactions_by_name(self, name: str) -> List[Transaction]:
        return [transaction for transaction in self.transactions if transaction.category == name]

    def get_transactions_by_category(self, category: BudgetCategory):
        return [transaction for transaction in self.transactions if transaction.category in self.categories[category]]


@dataclass
class CategoryReport:
    category: str
    months: int
    budget: float
    transactions: List[Transaction]

    @property
    def budget_per_month(self) -> float:
        return self.budget / 12.0
    
    @property
    def used(self) -> float:
        return sum([transaction.amount for transaction in self.transactions])
    
    @property
    def used_average(self) -> float:
        return self.used / self.months
    
    @property
    def leftover(self) -> float:
        return self.budget + self.used if self.used <= 0 else self.budget - self.used
    
    @property
    def leftover_average(self) -> float:
        return self.leftover / (12 - self.months) if self.months < 12 else 0
    
    @property
    def monthly_distribution(self) -> Dict[int, Tuple[float, float]]:
        return {month: (self.get_used_per_month(month), self.get_result_per_month(month)) for month in range(1, self.months+1)}

    def get_used_per_month(self, month: int) -> float:
        return sum([transaction.amount for transaction in self.transactions if transaction.month == month])

    def get_result_per_month(self, month: int) -> float:
        used_per_month = self.get_used_per_month(month)
        return self.budget_per_month + used_per_month if used_per_month <= 0 else used_per_month - self.budget_per_month