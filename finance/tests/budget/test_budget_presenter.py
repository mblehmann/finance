import unittest
from unittest.mock import Mock
from uuid import uuid4

from finance.application.dto import InteractorResultDto
from finance.infrastructure.presenter import CmdBudgetPresenter
from finance.interface.view import BudgetErrorViewModel, BudgetItemViewModel, BudgetViewInterface, TableViewModel


class TestCmdBudgetPresenter(unittest.TestCase):

    def setUp(self):
        self.mock_view = Mock(spec=BudgetViewInterface)
        self.presenter = CmdBudgetPresenter(self.mock_view)

    def test_present_budget_item_success(self):
        data = {
            'identifier': uuid4(),
            'name': 'name',
            'amount': 1.61,
            'category': 'category',
            'note': 'note',
        }
        result = InteractorResultDto(True, 'budget item', data, 28)
        item = BudgetItemViewModel.from_dict(data)

        self.presenter.present_budget_item(result)

        self.mock_view.show_item.assert_called_once_with('budget item succeeded', item)

    def test_present_budget_item_failure(self):
        data = {
            'identifier': uuid4(),
            'name': 'name',
            'amount': 1.61,
            'category': 'category',
            'note': 'note',
        }
        result = InteractorResultDto(False, 'budget item', data, 28)
        error = BudgetErrorViewModel('budget item failed', 28)

        self.presenter.present_budget_item(result)

        self.mock_view.show_failure.assert_called_once_with(error)

    def test_present_budget_list_success(self):
        data = {
            'identifier': uuid4(),
            'name': 'name',
            'amount': 1.61,
            'category': 'category',
            'note': 'note',
        }
        result = InteractorResultDto(True, 'budget list', [data], 28)
        items = [BudgetItemViewModel.from_dict(data)]

        self.presenter.present_budget_list(result)

        self.mock_view.show_list.assert_called_once_with('budget list succeeded', items)

    def test_present_budget_list_empty(self):
        result = InteractorResultDto(True, 'budget list', [], 28)
        error = BudgetErrorViewModel('budget list failed', 'The budget has no items')

        self.presenter.present_budget_list(result)

        self.mock_view.show_failure.assert_called_once_with(error)

    def test_present_budget_list_failure(self):
        data = {
            'identifier': uuid4(),
            'name': 'name',
            'amount': 1.61,
            'category': 'category',
            'note': 'note',
        }
        result = InteractorResultDto(False, 'budget list', [data], 28)
        error = BudgetErrorViewModel('budget list failed', 28)

        self.presenter.present_budget_list(result)

        self.mock_view.show_failure.assert_called_once_with(error)

    def test_present_budget_table_success(self):
        data = {
            'fields':['a'],
            'rows': [['b']],
        }
        result = InteractorResultDto(True, 'budget table', data, 28)
        table = TableViewModel.from_dict(data)

        self.presenter.present_budget_table(result)

        self.mock_view.show_table.assert_called_once_with('budget table succeeded', table)

    def test_present_budget_table_failure(self):
        data = {
            'fields':['a'],
            'rows': [['b']],
        }
        result = InteractorResultDto(False, 'budget table', data, 28)
        error = BudgetErrorViewModel('budget table failed', 28)

        self.presenter.present_budget_table(result)

        self.mock_view.show_failure.assert_called_once_with(error)
        
    def test_present_success(self):
        result = InteractorResultDto(True, 'success', 14, 28)
        error = BudgetErrorViewModel('success succeeded', 14)

        self.presenter.present_success(result)

        self.mock_view.show_failure.assert_called_once_with(error)

    def test_present_failure(self):
        result = InteractorResultDto(False, 'failure', 14, 28)
        error = BudgetErrorViewModel('failure failed', 28)

        self.presenter.present_failure(result)

        self.mock_view.show_failure.assert_called_once_with(error)


if __name__ == '__main__':
    unittest.main()
    