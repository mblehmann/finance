from typing import Dict, List

from finance.application.dto import InteractorResultDto
from finance.application.interface import ReportPresenterInterface
from finance.domain.budget import Budget, BudgetCategory
from finance.domain.report import CategoryReport, MonthResult
from finance.domain.transaction import History, Transaction


class CategoryReportUseCase:

    def __init__(self, budget: Budget, history: History, presenter: ReportPresenterInterface) -> None:
        self.budget = budget
        self.history = history
        self.presenter = presenter

    def execute(self, category: str, months: int) -> None:
        budget = self.budget.get_budget_item_by_name(category)
        transactions = self.history.get_transactions_by_category(category)
        report = CategoryReport(category, months, budget.amount, transactions)
        result = InteractorResultDto(success=True, operation='Category Report', data=report)
        self.presenter.present_category_report(result)


class AllCategoryReportUseCase:

    def __init__(self, budget: Budget, category_report_use_case: CategoryReportUseCase) -> None:
        self.budget = budget
        self.category_report_use_case = category_report_use_case

    def execute(self, months: int) -> None:
        items = self.budget.list_budget_items()
        for item in items:
            self.category_report_use_case.execute(item.name, months)


class MonthResultUseCase:

    def __init__(self, budget: Budget, history: History, presenter: ReportPresenterInterface) -> None:
        self.budget = budget
        self.history = history
        self.presenter = presenter

    def execute(self, month: int) -> None:
        transactions = self.history.get_transactions_by_month(month)
        items = {category: [item.name for item in self.budget.get_budget_item_by_category(category)] for category in BudgetCategory}
        report = MonthResult(month, transactions, items)
        result = InteractorResultDto(success=True, operation='Month Result', data=report)
        self.presenter.present_month_result(result)
