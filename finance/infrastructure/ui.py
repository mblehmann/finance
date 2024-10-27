import os
from uuid import UUID
import cmd

from finance.interface.controller import BudgetControllerInterface, HistoryControllerInterface, ReportControllerInterface


class BudgetCmd(cmd.Cmd):
    prompt = 'budget> '

    def __init__(self, budget_controller: BudgetControllerInterface):
        super().__init__()
        self.budget_controller = budget_controller

    def do_add(self, args: str) -> None:
        """add <name> <amount> <category> <note>: Adds a new budget item with name, amount, category, and note"""
        parameters = args.split()
        if len(parameters) < 4:
            self.do_help('add')
            return
        
        name, amount, category = parameters[:3]
        note = ' '.join(parameters[3:])
        try:
            amount = float(amount)
        except ValueError as e:
            print(f'The amount should be a number. {str(e)}')
            return
        
        self.budget_controller.add_budget_item(name, amount, category, note)

    def do_update(self, args: str) -> None:
        """update <identifier> <name> <amount> <category> <note>: Updates the budget item (name, amount, category, and note) with given identifier"""
        parameters = args.split()
        if len(parameters) < 5:
            self.do_help('update')
            return
        
        identifier, name, amount, category = parameters[:4]
        note = ' '.join(parameters[4:])
        try:
            identifier = UUID(identifier)
        except ValueError as e:
            print(f'The identifier should be a valid UUID. {str(e)}: "{identifier}"')
            return
        try:
            amount = float(amount)
        except ValueError as e:
            print(f'The amount should be a number. {str(e)}')
            return
        
        fields = {'name': name, 'amount': amount, 'category': category, 'note': note}
        self.budget_controller.update_budget_item(identifier, **fields)

    def do_update_name(self, args: str) -> None:
        """update_name <identifier> <name>: Updates the budget item name with given identifier"""
        parameters = args.split()
        if len(parameters) < 2:
            self.do_help('update_name')
            return
        
        identifier, name = parameters[:2]
        try:
            identifier = UUID(identifier)
        except ValueError as e:
            print(f'The identifier should be a valid UUID. {str(e)}: "{identifier}"')
            return
        
        fields = {'name': name}
        self.budget_controller.update_budget_item(identifier, **fields)

    def do_update_amount(self, args: str) -> None:
        """update_amount <identifier> <amount>: Updates the budget item amount with given identifier"""
        parameters = args.split()
        if len(parameters) < 2:
            self.do_help('update_amount')
            return
        
        identifier, amount = parameters[:2]
        try:
            identifier = UUID(identifier)
        except ValueError as e:
            print(f'The identifier should be a valid UUID. {str(e)}: "{identifier}"')
            return
        try:
            amount = float(amount)
        except ValueError as e:
            print(f'The amount should be a number. {str(e)}')
            return
        
        fields = {'amount': amount}
        self.budget_controller.update_budget_item(identifier, **fields)

    def do_update_category(self, args: str) -> None:
        """update_category <identifier> <category>: Updates the budget item category with given identifier"""
        parameters = args.split()
        if len(parameters) < 2:
            self.do_help('update_category')
            return
        
        identifier, category = parameters[:2]
        try:
            identifier = UUID(identifier)
        except ValueError as e:
            print(f'The identifier should be a valid UUID. {str(e)}: "{identifier}"')
            return
        
        fields = {'category': category}
        self.budget_controller.update_budget_item(identifier, **fields)

    def do_update_note(self, args: str) -> None:
        """update_note <identifier> <note>: Updates the budget item note with given identifier"""
        parameters = args.split()
        if len(parameters) < 2:
            self.do_help('update_note')
            return
        
        identifier = parameters[0]
        note = ' '.join(parameters[1:])
        try:
            identifier = UUID(identifier)
        except ValueError as e:
            print(f'The identifier should be a valid UUID. {str(e)}: "{identifier}"')
            return
        
        fields = {'note': note}
        self.budget_controller.update_budget_item(identifier, **fields)

    def do_get(self, args: str) -> None:
        """get <category>: Gets the budget items with given category"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('get')
            return
        
        category = parameters[0]
        self.budget_controller.get_budget_items(category)

    def do_delete(self, args: str) -> None:
        """delete <identifier>: Deletes the budget item with given identifier"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('delete')
            return
        
        identifier = parameters[0]
        try:
            identifier = UUID(identifier)
        except ValueError as e:
            print(f'The identifier should be a valid UUID. {str(e)}: "{identifier}"')
            return
        
        self.budget_controller.delete_budget_item(identifier)

    def do_list(self, _: str) -> None:
        """list: Lists all the budget items"""
        self.budget_controller.list_budget_items()

    def do_show_overview(self, _: str) -> None:
        """show_overview: Gets the budget overview"""
        self.budget_controller.show_budget_overview()

    def do_show_distribution(self, _: str) -> None:
        """show_distribution: Gets the budget distribution by category"""
        self.budget_controller.show_budget_distribution()

    def do_save(self, args: str) -> None:
        """save <name>: Saves the budget with the given project name"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('save')
            return

        project_name = parameters[0]
        os.makedirs(project_name, exist_ok=True)
        self.budget_controller.save_budget(project_name)

    def do_load(self, args: str) -> None:
        """load <name>: Loads the budget with the given project name"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('load')
            return

        project_name = parameters[0]
        self.budget_controller.load_budget(project_name)
    
    def do_quit(self, _: str) -> bool:
        """quit: Quits the program"""
        return True


class HistoryCmd(cmd.Cmd):
    prompt = 'history> '

    def __init__(self, history_controller: HistoryControllerInterface):
        super().__init__()
        self.history_controller = history_controller

    def do_import(self, args: str) -> None:
        """import <filename>: Imports the transactions in the file"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('import')
            return
        
        filename = parameters[0]
        self.history_controller.import_transactions(filename)

    def do_update(self, args: str) -> None:
        """update <reference> <category> <month> <tag> <comments>: Updates the transaction (category, month, tag, comments) with given reference"""
        parameters = args.split()
        if len(parameters) < 5:
            self.do_help('update')
            return
        
        reference, category, month, tag = parameters[:4]
        comments = ' '.join(parameters[4:])
        try:
            month = int(month)
        except ValueError as e:
            print(f'The month should be a number. {str(e)}')
            return

        self.history_controller.update_transaction(reference, category, month, tag, comments)

    def do_delete(self, args: str) -> None:
        """delete <reference>: Deletes the transaction with given reference"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('delete')
            return
        
        reference = parameters[0]
        self.history_controller.delete_transaction(reference)

    def do_review(self, _: str) -> None:
        """review: Reviews the uncategorized transactions"""
        self.history_controller.review_transactions()

    def do_save(self, args: str) -> None:
        """save <name>: Saves the history with the given project name"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('save')
            return

        project_name = parameters[0]
        os.makedirs(project_name, exist_ok=True)
        self.history_controller.save_budget(project_name)

    def do_load(self, args: str) -> None:
        """load <name>: Loads the history with the given project name"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('load')
            return

        project_name = parameters[0]
        self.history_controller.load_budget(project_name)
    
    def do_quit(self, _: str) -> bool:
        """quit: Quits the program"""
        return True


class ReportCmd(cmd.Cmd):
    prompt = 'report> '

    def __init__(self, report_controller: ReportControllerInterface):
        super().__init__()
        self.report_controller = report_controller

    def do_report_category(self, args: str) -> None:
        """report_category <category> <months>: Reports the category for the number of months"""
        parameters = args.split()
        if len(parameters) < 2:
            self.do_help('report_category')
            return
        
        category = parameters[0]
        months = int(parameters[1])
        self.report_controller.get_report_by_category(category, months)

    def do_report_month(self, args: str) -> None:
        """report_month <month>: Reports the month"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('report_month')
            return
        
        try:
            month = int(parameters[0])
        except ValueError as e:
            self.do_help('report_month')
            return
        
        self.report_controller.get_report_by_month(month)
        

class FinanceCmd(cmd.Cmd):
    prompt = 'finance> '

    def __init__(self, budget_controller: BudgetControllerInterface, history_controller: HistoryControllerInterface, report_controller: ReportControllerInterface):
        super().__init__()
        self.budget_cmd = BudgetCmd(budget_controller)
        self.history_cmd = HistoryCmd(history_controller)
        self.report_cmd = ReportCmd(report_controller)

    def do_budget(self, _) -> None:
        """enter budget prompt"""
        self.budget_cmd.cmdloop()
        
    def do_history(self, _) -> None:
        """enter history prompt"""
        
    def do_report(self, _) -> None:
        """enter report prompt"""

    def do_import_transactions(self, args: str) -> None:
        """import_transactions <filename>: Imports the transactions in the file"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('import_transactions')
            return
        
        filename = parameters[0]
        self.history_controller.import_transactions(filename)

    def do_update_transaction(self, args: str) -> None:
        """update_transaction <reference> <category> <comments>: Updates the transaction (category, comments) with given reference"""
        parameters = args.split()
        if len(parameters) < 3:
            self.do_help('update_transaction')
            return
        
        reference, category = parameters[:2]
        comments = ' '.join(parameters[2:])
        self.history_controller.update_transaction(reference, category, comments)

    def do_delete_transaction(self, args: str) -> None:
        """delete_transaction <reference>: Deletes the transaction with given reference"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('delete_transaction')
            return
        
        reference = parameters[0]
        self.history_controller.delete_transaction(reference)

    def do_review_transactions(self, _: str) -> None:
        """review_transactions: Reviews the uncategorized transactions"""
        self.history_controller.review_transactions()

    def do_report_category(self, args: str) -> None:
        """report_category <category> <months>: Reports the category for the number of months"""
        parameters = args.split()
        if len(parameters) < 2:
            self.do_help('report_category')
            return
        
        category = parameters[0]
        months = int(parameters[1])
        self.report_controller.get_report_by_category(category, months)

    def do_report_month(self, args: str) -> None:
        """report_month <month>: Reports the month"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('report_month')
            return
        
        try:
            month = int(parameters[0])
        except ValueError as e:
            self.do_help('report_month')
            return
        
        self.report_controller.get_report_by_month(month)

    def do_save(self, args: str) -> None:
        """save <name>: Saves the finance with the given project name"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('save')
            return

        project_name = parameters[0]
        os.makedirs(project_name, exist_ok=True)
        self.budget_cmd.do_save(project_name)
        self.history_cmd.do_save(project_name)

    def do_load(self, args: str) -> None:
        """load <name>: Loads the finance with the given project name"""
        parameters = args.split()
        if len(parameters) < 1:
            self.do_help('load')
            return

        project_name = parameters[0]
        self.budget_cmd.do_load(project_name)
        self.history_cmd.do_load(project_name)

    def do_quit(self, _: str) -> bool:
        """quit: Quits the program"""
        return True
