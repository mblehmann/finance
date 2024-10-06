from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Self
from uuid import UUID

from finance.domain.exception import BudgetItemExistsException, BudgetItemNotFoundException


class BudgetCategory(Enum):
    Empty = 0,
    Income = 1,
    Needs = 2,
    Wants = 3,
    Savings = 4,


@dataclass
class BudgetItem:
    identifier: UUID
    name: str = field(compare=False)
    amount: float = field(compare=False)
    category: BudgetCategory = field(compare=False)
    note: str = field(compare=False)

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> Self:
        return cls(
            identifier=UUID(data['identifier']),
            name=data['name'],
            amount=float(data['amount']),
            category=BudgetCategory[data['category']],
            note=data['note']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'identifier': self.identifier,
            'name': self.name,
            'amount': self.amount,
            'category': self.category.name,
            'note': self.note
        }


class Budget:
    
    def __init__(self) -> None:
        self.items: Dict[UUID, BudgetItem] = {}

    def add_budget_item(self, budget_item: BudgetItem) -> BudgetItem:
        if budget_item.identifier in self.items:
            raise BudgetItemExistsException(f'Failed to add a budget item. Item with identifier "{budget_item.identifier}" already exists')

        self.items[budget_item.identifier] = budget_item
        return self.items[budget_item.identifier]

    def update_budget_item(self, budget_item: BudgetItem) -> BudgetItem:
        if budget_item.identifier not in self.items:
            raise BudgetItemNotFoundException(f'Failed to update a budget item. Item with identifier "{budget_item.identifier}" does not exist')

        self.items[budget_item.identifier] = budget_item
        return self.items[budget_item.identifier]

    def delete_budget_item(self, budget_identifier: UUID) -> BudgetItem:
        if budget_identifier not in self.items:
            raise BudgetItemNotFoundException(f'Failed to delete a budget item. Item with identifier "{budget_identifier}" does not exist')

        item = self.items.pop(budget_identifier)
        return item

    def get_budget_item(self, budget_identifier: UUID) -> BudgetItem:
        if budget_identifier not in self.items:
            raise BudgetItemNotFoundException(f'Failed to get a budget item. Item with identifier "{budget_identifier}" does not exist')

        item = self.items[budget_identifier]
        return item

    def get_budget_item_by_name(self, budget_name: str) -> BudgetItem:
        for item in self.items.values():
            if item.name == budget_name:
                return item
        raise BudgetItemNotFoundException(f'Failed to get a budget item. Item with name "{budget_name}" does not exist')

    def get_budget_item_by_category(self, budget_category: BudgetCategory) -> List[BudgetItem]:
        return [item for item in self.items.values() if item.category.name == budget_category.name]

    def list_budget_items(self) -> List[BudgetItem]:
        return list(self.items.values())
