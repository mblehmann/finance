from domain.report import CategoryReport, MonthResult
from finance.application.dto import InteractorResultDto
from finance.application.interface import BudgetPresenterInterface, HistoryPresenterInterface, ReportPresenterInterface
from finance.interface.view import BudgetViewInterface, BudgetItemViewModel, BudgetErrorViewModel, CategoryReportViewModel, HistoryErrorViewModel, HistoryViewInterface, MonthResultViewModel, ReportViewInterface, TransactionViewModel


class CmdBudgetPresenter(BudgetPresenterInterface):

    def __init__(self, view: BudgetViewInterface) -> None:
        self.view = view

    def present_budget_item(self, result: InteractorResultDto) -> None:
        if not result.success:
            self.present_failure(result)
            return
        
        item = BudgetItemViewModel.from_dict(result.data)
        self.view.show_item(f'{result.operation} succeeded', item)

    def present_budget_list(self, result: InteractorResultDto) -> None:
        if not result.success:
            self.present_failure(result)
            return
        
        if not result.data:
            result.error = 'The budget has no items'
            self.present_failure(result)
            return

        items = [BudgetItemViewModel.from_dict(item) for item in result.data]
        self.view.show_list(f'{result.operation} succeeded', items)

    def present_success(self, result: InteractorResultDto) -> None:
        message = BudgetErrorViewModel(f'{result.operation} succeeded', result.data)
        self.view.show_failure(message)

    def present_failure(self, result: InteractorResultDto) -> None:
        error = BudgetErrorViewModel(f'{result.operation} failed', result.error)
        self.view.show_failure(error)


class CmdHistoryPresenter(HistoryPresenterInterface):

    def __init__(self, view: HistoryViewInterface) -> None:
        self.view = view

    def present_import_transactions(self, result: InteractorResultDto) -> None:
        if not result.success:
            self.present_failure(result)
            return
        
        imported = [TransactionViewModel.from_dict(item, 45) for item in result.data['imported']]
        if imported:
            self.view.show_list(f'{result.operation} succeeded: {len(imported)} transactions imported', imported)
        else:
            result.error = 'No transactions were imported'
            self.present_failure(result)

        duplicated = result.data['duplicated']
        if duplicated:
            error = HistoryErrorViewModel(f'{result.operation} warning: {len(duplicated)} transactions duplicated', '\n\t'.join(duplicated))
            self.view.show_failure(error)

    def present_review_transactions(self, result: InteractorResultDto) -> None:
        ...

    def present_transaction(self, result: InteractorResultDto) -> None:
        if not result.success:
            self.present_failure(result)
            return
        
        item = TransactionViewModel.from_dict(result.data)
        self.view.show_item(f'{result.operation} succeeded', item)

    def present_history(self, result: InteractorResultDto) -> None:
        ...

    def present_success(self, result: InteractorResultDto) -> None:
        message = HistoryErrorViewModel(f'{result.operation} succeeded', result.data)
        self.view.show_failure(message)

    def present_failure(self, result: InteractorResultDto) -> None:
        error = HistoryErrorViewModel(f'{result.operation} failed', result.error)
        self.view.show_failure(error)


class CmdReportPresenter(ReportPresenterInterface):

    def __init__(self, view: ReportViewInterface) -> None:
        self.view = view

    def present_month_result(self, result: InteractorResultDto) -> None:
        report: MonthResult = result.data
        income_details = {name: self.currency_format(amount) for name, amount in sorted(report.income_details.items(), key=lambda item: item[1], reverse=True)}
        expense_details = {name: self.currency_format(amount) for name, amount in sorted(report.expense_details.items(), key=lambda item: item[1])}
        category_details = {name: self.currency_format(amount) for name, amount in report.category_details.items()}
        data = MonthResultViewModel(str(report.month),
                                    self.currency_format(report.incomes),
                                    self.currency_format(report.expenses),
                                    self.currency_format(report.result),
                                    income_details,
                                    expense_details,
                                    category_details)
        self.view.show_month_result(f'{result.operation}: {report.month}', data)

    def present_category_report(self, result: InteractorResultDto) -> None:
        report: CategoryReport = result.data
        monthly_details = {str(month): (self.currency_format(amount), self.currency_format(result)) for month, (amount, result) in sorted(report.monthly_distribution.items())}
        data = CategoryReportViewModel(report.category,
                                       (self.currency_format(report.budget), self.currency_format(report.budget_per_month)),
                                       (self.currency_format(report.used), self.currency_format(report.used_average)),
                                       (self.currency_format(report.leftover), self.currency_format(report.leftover_average)),
                                       monthly_details)
        self.view.show_category_report(f'{result.operation}: {report.category}', data)

    def currency_format(self, value: float) -> str:
        return f'{value:,.2f}'
