from typing import Protocol
from uuid import UUID


class FinanceControllerInterface(Protocol):

    def save(self, name: str) -> None:
        ...

    def load(self, name: str) -> None:
        ...


class BudgetControllerInterface(Protocol):

    def add_budget_item(self, name: str, amount: float, category: str, note: str) -> None:
        ...
        
    def update_budget_item(self, identifier: UUID, **kwargs) -> None:
        ...

    def delete_budget_item(self, identifier: UUID) -> None:
        ...
        
    def get_budget_items(self, category: str) -> None:
        ...

    def list_budget_items(self) -> None:
        ...
    
    def show_summary(self) -> None:
        ...
        
    def save_budget(self, project_name: str) -> None:
        ...
        
    def load_budget(self, project_name: str) -> None:
        ...


class HistoryControllerInterface(Protocol):

    def import_transactions(self, filename: str) -> None:
        ...

    def review_transactions(self) -> None:
        ...

    def update_transaction(self, reference: str, category: str, comments: str) -> None:
        ...

    def delete_transaction(self, reference: str) -> None:
        ...
        
    def save_budget(self, project_name: str) -> None:
        ...
        
    def load_budget(self, project_name: str) -> None:
        ...


class ReportControllerInterface(Protocol):

    def get_report_by_category(self, category: str) -> None:
        ...

    def get_report_by_month(self, month: int) -> None:
        ...
