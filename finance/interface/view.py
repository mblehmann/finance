from dataclasses import dataclass
from typing import Any, Dict, List, Protocol, Self, Tuple


@dataclass
class TableViewModel:
    fields: List[str]
    rows: List[List[str]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        return cls(
            fields=data['fields'],
            rows=data['rows']
        )


@dataclass
class BudgetItemViewModel:
    identifier: str
    name: str
    amount: str
    category: str
    note: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        return cls(
            identifier=str(data['identifier']),
            name=data['name'],
            amount=str(data['amount']),
            category=data['category'],
            note=data['note']
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            'identifier': self.identifier,
            'name': self.name,
            'amount': self.amount,
            'category': self.category,
            'note': self.note
        }


@dataclass
class BudgetErrorViewModel:
    command: str
    message: str
    

class BudgetViewInterface(Protocol):
    
    def show_item(self, command: str, item: BudgetItemViewModel) -> None:
        ...
    
    def show_list(self, command: str, items: List[BudgetItemViewModel]) -> None:
        ...
    
    def show_table(self, command: str, data: TableViewModel) -> None:
        ...
    
    def show_failure(self, error: BudgetErrorViewModel) -> None:
        ...


@dataclass
class TransactionViewModel:
    reference: str
    day: str
    source: str
    amount: str
    notes: str
    category: str
    month: str
    comments: str
    exclude: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any], notes_length: int = 0) -> Self:
        return cls(
            reference=data['reference'],
            day=data['day'],
            source=data['source'],
            amount=str(data['amount']),
            notes=data['notes'][:notes_length] if notes_length else data['notes'],
            category=data['category'],
            month=data['month'],
            comments=data['comments'],
            exclude=data['exclude'],
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            'reference': self.reference,
            'day': self.day,
            'source': self.source,
            'amount': self.amount,
            'notes': self.notes,
            'category': self.category,
            'month': self.month,
            'comments': self.comments,
            'exclude': self.exclude,
        }
    

@dataclass
class HistoryErrorViewModel:
    command: str
    message: str
    

class HistoryViewInterface(Protocol):
    
    def show_item(self, command: str, item: TransactionViewModel) -> None:
        ...
    
    def show_list(self, command: str, items: List[TransactionViewModel]) -> None:
        ...

    def show_message(self, message: str) -> None:
        ...
    
    def show_failure(self, error: HistoryErrorViewModel) -> None:
        ...


@dataclass
class MonthResultViewModel:
    month: str
    incomes: str
    expenses: str
    result: str
    income_details: Dict[str, str]
    expense_details: Dict[str, str]
    category_details: Dict[str, str]


@dataclass
class CategoryReportViewModel:
    category: str
    budget: Tuple[str, str]
    used: Tuple[str, str]
    leftover: Tuple[str, str]
    monthly_details: Dict[str, Tuple[str, str]]


class ReportViewInterface(Protocol):

    def show_month_result(self, header: str, result: MonthResultViewModel) -> None:
        ...

    def show_category_report(self, header: str, report: CategoryReportViewModel) -> None:
        ...
