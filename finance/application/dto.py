from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional, Protocol, Self


@dataclass
class InteractorResultDto:
    success: bool
    operation: str
    data: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class BudgetItemDto:
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
class TransactionDto:
    reference: str
    day: str
    source: str
    amount: str
    notes: str
    category: str
    month: str
    tag: str
    comments: str
    ignore: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        return cls(
            reference=data['reference'],
            day=data['day'].isoformat() if isinstance(data['day'], date) else data['day'],
            source=data['source'],
            amount=str(data['amount']),
            notes=data['notes'],
            category=data['category'],
            month=str(data['month']),
            tag=data['tag'],
            comments=data['comments'],
            ignore=str(data['ignore']),
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
            'tag': self.tag,
            'comments': self.comments,
            'ignore': self.ignore,
        }


class CellDto(Protocol):

    @property
    def value(self) -> str:
        ...


@dataclass
class StrCellDto(CellDto):
    data: str

    @property
    def value(self) -> str:
        return self.data


@dataclass
class MoneyCellDto(CellDto):
    amount: float
    formatting: str = '{:,.2f}'

    @property
    def value(self) -> str:
        return self.formatting.format(self.amount)



@dataclass
class PercentageCellDto(CellDto):
    amount: float
    formatting: str = '{:.2%}'

    @property
    def value(self) -> str:
        return self.formatting.format(self.amount)


@dataclass
class TableDto:
    fields: List[str]
    rows: List[List[str]] = field(default_factory=list)
    
    def add_row(self, data: List[CellDto]) -> None:
        self.rows.append([cell.value for cell in data])

    def to_dict(self) -> Dict[str, List[str] | List[List[str]]]:
        return {
            'fields': self.fields,
            'rows': self.rows
        }
