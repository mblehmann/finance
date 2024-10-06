from dataclasses import dataclass
from domain.budget import Budget
from domain.transaction import History


@dataclass
class Finance:
    budget: Budget
    history: History
