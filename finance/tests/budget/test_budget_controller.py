import unittest
from unittest.mock import Mock
from uuid import uuid4

from application.budget_interactor import AddBudgetItemUseCase, DeleteBudgetItemUseCase, GetBudgetItemByCategoryUseCase, ListBudgetItemsUseCase, LoadBudgetUseCase, SaveBudgetUseCase, ShowBudgetDistributionUseCase, ShowBudgetOverviewUseCase, UpdateBudgetItemUseCase
from finance.infrastructure.controller import CmdBudgetController
from finance.interface.facade import BudgetUseCaseFacade


class TestCmdBudgetController(unittest.TestCase):

    def setUp(self):
        self.mock_facade = Mock(spec=BudgetUseCaseFacade)
        self.mock_facade.add_use_case = Mock(spec=AddBudgetItemUseCase)
        self.mock_facade.update_use_case = Mock(spec=UpdateBudgetItemUseCase)
        self.mock_facade.delete_use_case = Mock(spec=DeleteBudgetItemUseCase)
        self.mock_facade.get_by_category_use_case = Mock(spec=GetBudgetItemByCategoryUseCase)
        self.mock_facade.list_use_case = Mock(spec=ListBudgetItemsUseCase)
        self.mock_facade.overview_use_case = Mock(spec=ShowBudgetOverviewUseCase)
        self.mock_facade.distribution_use_case = Mock(spec=ShowBudgetDistributionUseCase)
        self.mock_facade.save_use_case = Mock(spec=SaveBudgetUseCase)
        self.mock_facade.load_use_case = Mock(spec=LoadBudgetUseCase)
        self.controller = CmdBudgetController(self.mock_facade)

    def test_add_budget_item(self):
        name = 'name'
        amount = 3.14
        category = 'category'
        note = 'note'
        
        self.controller.add_budget_item(name, amount, category, note)

        self.mock_facade.add_use_case.execute.assert_called_once_with(name, amount, category, note)

    def test_update_budget_item(self):
        identifier = uuid4()
        data = {
            'name': 'name',
            'amount': 3.14,
            'category': 'category',
            'note': 'note'
        }
        
        self.controller.update_budget_item(identifier, **data)

        self.mock_facade.update_use_case.execute.assert_called_once_with(identifier, **data)

    def test_delete_budget_item(self):
        identifier = uuid4()
        
        self.controller.delete_budget_item(identifier)

        self.mock_facade.delete_use_case.execute.assert_called_once_with(identifier)

    def test_get_budget_items(self):
        category = 'category'

        self.controller.get_budget_items(category)

        self.mock_facade.get_by_category_use_case.execute.assert_called_once_with(category)

    def test_list_budget_items(self):
        self.controller.list_budget_items()

        self.mock_facade.list_use_case.execute.assert_called_once_with()

    def test_show_budget_overview(self):
        self.controller.show_budget_overview()

        self.mock_facade.overview_use_case.execute.assert_called_once_with()

    def test_show_budget_distribution(self):
        self.controller.show_budget_distribution()

        self.mock_facade.distribution_use_case.execute.assert_called_once_with()

    def test_save_budget(self):
        project_name = 'project'

        self.controller.save_budget(project_name)

        self.mock_facade.save_use_case.execute.assert_called_once_with(project_name)

    def test_load_budget(self):
        project_name = 'project'

        self.controller.load_budget(project_name)

        self.mock_facade.load_use_case.execute.assert_called_once_with(project_name)



if __name__ == '__main__':
    unittest.main()