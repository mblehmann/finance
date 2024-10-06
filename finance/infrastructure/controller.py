from uuid import UUID
from application.dto import InteractorResultDto
from application.interface import HistoryPresenterInterface, InputReaderInterface
from finance.interface.controller import BudgetControllerInterface, HistoryControllerInterface, ReportControllerInterface
from finance.interface.facade import BudgetUseCaseFacade, HistoryUseCaseFacade, ReportUseCaseFacade


class CmdBudgetController(BudgetControllerInterface):
    
    def __init__(self, budget_use_case_facade: BudgetUseCaseFacade):
        self.budget_use_cases = budget_use_case_facade

    def add_budget_item(self, name: str, amount: float, category: str, note: str) -> None:
        self.budget_use_cases.add_use_case.execute(name, amount, category, note)
        
    def update_budget_item(self, identifier: UUID, **kwargs) -> None:
        self.budget_use_cases.update_use_case.execute(identifier, **kwargs)

    def delete_budget_item(self, identifier: UUID) -> None:
        self.budget_use_cases.delete_use_case.execute(identifier)
        
    def get_budget_items(self, category: str) -> None:
        self.budget_use_cases.get_by_category_use_case.execute(category)
        
    def list_budget_items(self) -> None:
        self.budget_use_cases.list_use_case.execute()

    def show_summary(self) -> None:
        self.budget_use_cases.summary_use_case.execute()
        
    def save_budget(self, project_name: str) -> None:
        self.budget_use_cases.save_use_case.execute(project_name)
        
    def load_budget(self, project_name: str) -> None:
        self.budget_use_cases.load_use_case.execute(project_name)


class CmdHistoryController(HistoryControllerInterface):
    
    def __init__(self, history_use_case_facade: HistoryUseCaseFacade, reader: InputReaderInterface, presenter: HistoryPresenterInterface):
        self.history_use_cases = history_use_case_facade
        self.reader = reader
        self.presenter = presenter

    def import_transactions(self, filename: str) -> None:
        self.history_use_cases.import_use_case.execute(filename)

    def update_transaction(self, reference: str, category: str, comments: str) -> None:
        self.history_use_cases.update_use_case.execute(reference, category, comments)

    def delete_transaction(self, reference: str) -> None:
        self.history_use_cases.delete_use_case.execute(reference)

    def review_transactions(self) -> None:
        transactions = self.history_use_cases.review_use_case.execute()
        total = len(transactions)

        for index, transaction in enumerate(transactions):
            operation = f'Review Transaction {index+1}/{total}'
            review = InteractorResultDto(success=True, operation=operation, data=transaction.to_dict())
            self.presenter.present_transaction(review)
            user_input = self.reader.get_input('Delete or categorize: ').split()
            category = user_input[0]
            comments = ' '.join(user_input[1:])
            if category == 'delete':
                self.delete_transaction(transaction.reference)
            else:
                self.update_transaction(transaction.reference, category, comments)

        self.history_use_cases.review_use_case.execute()
        
    def save_budget(self, project_name: str) -> None:
        self.history_use_cases.save_use_case.execute(project_name)
        
    def load_budget(self, project_name: str) -> None:
        self.history_use_cases.load_use_case.execute(project_name)


class CmdReportController(ReportControllerInterface):

    def __init__(self, report_use_case_facade: ReportUseCaseFacade):
        self.report_use_case_facade = report_use_case_facade

    def get_report_by_category(self, category: str, months: int) -> None:
        if category == 'all':
            self.report_use_case_facade.all_category_report.execute(months)
        else:
            self.report_use_case_facade.category_report.execute(category, months)

    def get_report_by_month(self, month: int) -> None:
        self.report_use_case_facade.month_report.execute(month)
