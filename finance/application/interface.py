from typing import List, Protocol

from finance.application.dto import BudgetItemDto, InteractorResultDto, TransactionDto


class BudgetRepositoryInterface(Protocol):

    def save_budget(self, filename: str, budget: List[BudgetItemDto]) -> None:
        ...

    def load_budget(self, filename: str) -> List[BudgetItemDto]:
        ...


class HistoryRepositoryInterface(Protocol):

    def save_history(self, filename: str, history: List[TransactionDto]) -> None:
        ...

    def load_history(self, filename: str) -> List[TransactionDto]:
        ...


class BudgetPresenterInterface(Protocol):

    def present_budget_item(self, result: InteractorResultDto) -> None:
        ...

    def present_budget_list(self, result: InteractorResultDto) -> None:
        ...

    def present_success(self, result: InteractorResultDto) -> None:
        ...

    def present_failure(self, result: InteractorResultDto) -> None:
        ...


class HistoryPresenterInterface(Protocol):

    def present_import_transactions(self, result: InteractorResultDto) -> None:
        ...

    def present_review_transactions(self, result: InteractorResultDto) -> None:
        ...

    def present_transaction(self, result: InteractorResultDto) -> None:
        ...

    def present_history(self, result: InteractorResultDto) -> None:
        ...

    def present_success(self, result: InteractorResultDto) -> None:
        ...

    def present_failure(self, result: InteractorResultDto) -> None:
        ...


class ReportPresenterInterface(Protocol):

    def present_month_result(self, result: InteractorResultDto) -> None:
        ...
        
    def present_category_report(self, result: InteractorResultDto) -> None:
        ...


class InputReaderInterface(Protocol):

    def get_input(self, prompt: str) -> str:
        ...


class TransactionImporterInterface(Protocol):

    def import_transactions(self, filename: str) -> List[TransactionDto]:
        ...
