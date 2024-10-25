import csv
from typing import List

from finance.application.dto import BudgetItemDto, TransactionDto
from finance.application.interface import BudgetRepositoryInterface, HistoryRepositoryInterface


class CsvBudgetRepository(BudgetRepositoryInterface):

    def save_budget(self, filename: str, budget: List[BudgetItemDto]) -> None:
        with open(filename, 'w', newline='') as csv_file:
            csv_write = csv.writer(csv_file)
            for item in budget:
                csv_write.writerow(list(item.to_dict().values()))

    def load_budget(self, filename: str) -> List[BudgetItemDto]:
        budget = []
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                item = BudgetItemDto(*row)
                budget.append(item)
        return budget


class CsvHistoryRepository(HistoryRepositoryInterface):

    def save_history(self, filename: str, history: List[TransactionDto]) -> None:
        with open(filename, 'w', newline='') as csv_file:
            csv_write = csv.writer(csv_file)
            for item in history:
                csv_write.writerow(item.to_dict().values())

    def load_history(self, filename: str) -> List[TransactionDto]:
        history = []
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                item = TransactionDto(*row)
                history.append(item)
        return history
