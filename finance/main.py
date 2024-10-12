import sys
sys.path.append('/Users/matheus/projects/finance')

from finance.domain.finance import Finance
from finance.domain.transaction import History
from finance.domain.budget import Budget
from finance.infrastructure.factory import CmdComponentFactory
from finance.infrastructure.ui import FinanceCmd
from finance.infrastructure.repository import CsvBudgetRepository, CsvHistoryRepository


if __name__ == '__main__':
    finance = Finance(Budget(), History())
    budget_repository = CsvBudgetRepository()
    history_repository = CsvHistoryRepository()
    factory = CmdComponentFactory()
    budget_controller = factory.get_budget_controller(finance.budget, budget_repository)
    history_controller = factory.get_history_controller(finance.history, history_repository)
    report_controller = factory.get_report_controller(finance.history, finance.budget)

    # Create and run the CLI
    cli = FinanceCmd(budget_controller, history_controller, report_controller)
    cli.cmdloop()
