from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Self

from domain.exception import TransactionExistsException, TransactionNotFoundException, TransactionUpdateException


@dataclass
class Transaction:
    reference: str
    day: date
    source: str
    amount: float
    notes: str
    category: str = field(compare=False)
    month: int = field(compare=False)
    comments: str = field(compare=False)
    exclude: bool = field(compare=False)

    # @property
    # def month(self) -> int:
    #     return self.day.month

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> Self:
        return cls(
            reference=data['reference'],
            day=date.fromisoformat(data['day']),
            source=data['source'],
            amount=float(data['amount']),
            notes=data['notes'],
            category=data['category'],
            month=int(data['month']),
            comments=data['comments'],
            exclude=True if data['exclude'] == 'True' else False,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'reference': self.reference,
            'day': self.day.isoformat(),
            'source': self.source,
            'amount': self.amount,
            'notes': self.notes,
            'category': self.category,
            'month': self.month,
            'comments': self.comments,
            'exclude': self.exclude,
        }

    def get_different_fields(self, other: Self) -> List[str]:
        fields = ['reference', 'day', 'source', 'amount', 'notes']
        difference = [field for field in fields if self.__getattribute__(field) != other.__getattribute__(field)]
        return difference


class History:

    def __init__(self) -> None:
        self.items: Dict[str, Transaction] = {}
		
    def has_transaction(self, reference: str) -> bool:
        return reference in self.items

    def add_transaction(self, transaction: Transaction) -> Transaction:
        if self.has_transaction(transaction.reference):
            raise TransactionExistsException(f'Failed to add transaction. Transaction with reference "{transaction.reference}" already exists')
        
        self.items[transaction.reference] = transaction
        return self.items[transaction.reference]
    
    def update_transaction(self, transaction: Transaction) -> Transaction:
        if not self.has_transaction(transaction.reference):
            raise TransactionNotFoundException(f'Failed to update transaction. Transaction with reference "{transaction.reference}" does not exist')

        current_transaction = self.get_transaction(transaction.reference)
        if transaction != current_transaction:
            fields = transaction.get_different_fields(current_transaction)
            raise TransactionUpdateException(f'Failed to update transaction. The following immutable fields were going to be changed: {' '.join(fields)}')
        
        self.items[transaction.reference] = transaction
        return self.items[transaction.reference]
    
    def delete_transaction(self, reference: str) -> Transaction:
        if not self.has_transaction(reference):
            raise TransactionNotFoundException(f'Failed to update transaction. Transaction with reference "{reference}" does not exist')

        transaction = self.items.pop(reference)
        return transaction
    
    def get_transaction(self, reference: str) -> Transaction:
        if not self.has_transaction(reference):
            raise TransactionNotFoundException(f'Failed to update transaction. Transaction with reference "{reference}" does not exist')

        transaction = self.items[reference]
        return transaction
    
    def get_unreviewed_transactions(self) -> List[Transaction]:
        return list(filter(lambda item: not item.category, self.items.values()))
        # return [item for item in self.items.values() if not item.category]

    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        return list(filter(lambda item: item.category == category, self.items.values()))
        # return [item for item in self.items.values() if item.category == category]

    def get_transactions_by_month(self, month: int) -> List[Transaction]:
        return list(filter(lambda item: item.month == month, self.items.values()))
        # return [item for item in self.items.values() if item.month == month]

    def list_transactions(self) -> List[Transaction]:
        return list(self.items.values())
