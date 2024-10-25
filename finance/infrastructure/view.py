from prettytable import PrettyTable
from typing import Dict, List

from finance.interface.view import BudgetErrorViewModel, BudgetItemViewModel, BudgetViewInterface, CategoryReportViewModel, HistoryErrorViewModel, HistoryViewInterface, MonthResultViewModel, ReportViewInterface, TableViewModel, TransactionViewModel


class CmdBudgetView(BudgetViewInterface):

    def show_item(self, command: str, item: BudgetItemViewModel) -> None:
        print(f'{command}')
        for key, value in item.to_dict().items():
            print(f'\t{key}: {value}')
        print()

    def show_list(self, command: str, items: List[BudgetItemViewModel]) -> None:
        print(f'{command}')
        budget = PrettyTable()
        budget.field_names = list(items[0].to_dict().keys())
        for item in items:
            budget.add_row(list(item.to_dict().values()))
        print(budget)
        print()

    def show_table(self, command: str, data: TableViewModel) -> None:
        print(f'{command}')
        table = PrettyTable()
        table.field_names = data.fields
        for row in data.rows:
            table.add_row(row)
        print(table)
        print()

    def show_failure(self, error: BudgetErrorViewModel) -> None:
        print(f'{error.command}')
        print(f'\t{error.message}')
        print()


class CmdHistoryView(HistoryViewInterface):
    
    def show_item(self, command: str, item: TransactionViewModel) -> None:
        print(f'{command}')
        for key, value in item.to_dict().items():
            print(f'\t{key}: {value}')
        print()
    
    def show_list(self, command: str, items: List[TransactionViewModel]) -> None:
        print(f'{command}')
        history = PrettyTable(max_table_width=300)
        history.field_names = list(items[0].to_dict().keys())
        for item in items:
            history.add_row(list(item.to_dict().values()))
        print(history)
        print()

    def show_message(self, message: str) -> None:
        print(f'{message}')
        print()
    
    def show_failure(self, error: HistoryErrorViewModel) -> None:
        print(f'{error.command}')
        print(f'\t{error.message}')
        print()


class CmdReportView(ReportViewInterface):

    def show_month_result(self, header: str, result: MonthResultViewModel) -> None:
        print(f'{header}')
        self.print_section('Overview')
        print(f'\tIncomes: {result.incomes}')
        print(f'\tExpenses: {result.expenses}')
        print(f'\tResult: {result.result}')
        self.print_section('Income Details')
        income_table = PrettyTable(['Category', 'Amount'])
        for category, amount in result.income_details.items():
            income_table.add_row([category, amount])
        print(income_table)
        self.print_section('Expense Details')
        expense_table = PrettyTable(['Category', 'Amount'])
        for category, amount in result.expense_details.items():
            expense_table.add_row([category, amount])
        print(expense_table)
        self.print_section('Category Details')
        category_table = PrettyTable(['Category', 'Amount'])
        for category, amount in result.category_details.items():
            category_table.add_row([category, amount])
        print(category_table)
        print()


    def print_section(self, section: str) -> None:
        print('\n-----------------------------------------')
        print(section)

    def show_category_report(self, header: str, report: CategoryReportViewModel) -> None:
        print(f'{header}')
        self.print_section('Overview')
        print(f'\tBudget: {' / '.join(report.budget)}')
        print(f'\tUsed: {' / '.join(report.used)}')
        print(f'\tLeftover: {' / '.join(report.leftover)}')
        self.print_section('Monthly Details')
        month_table = PrettyTable(['Month', 'Amount', 'Result'])
        for month, (amount, result) in report.monthly_details.items():
            month_table.add_row([month, amount, result])
        print(month_table)
        print()
