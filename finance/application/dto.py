from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, Optional, Self


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
    comments: str
    exclude: str

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
            comments=data['comments'],
            exclude=str(data['exclude']),
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
    