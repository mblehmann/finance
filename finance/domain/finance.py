from dataclasses import dataclass

from finance.domain.budget import Budget
from finance.domain.transaction import History


@dataclass
class Finance:
    budget: Budget
    history: History
