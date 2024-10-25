import unittest
from uuid import UUID

from finance.application.budget_interactor import AddBudgetItemUseCase, DeleteBudgetItemUseCase, GetBudgetItemByCategoryUseCase, ListBudgetItemsUseCase, LoadBudgetUseCase, SaveBudgetUseCase, ShowBudgetDistributionUseCase, ShowBudgetOverviewUseCase, UpdateBudgetItemUseCase
from finance.interface.facade import BudgetUseCaseFacadeFactory
from finance.interface.view import BudgetErrorViewModel, BudgetItemViewModel


class TestBudgetItemViewModel(unittest.TestCase):

    def test_budget_item_data(self):
        identifier = 'identifier'
        name = 'name'
        amount = 'amount'
        category = 'category'
        note = 'note'
        item = BudgetItemViewModel(identifier, name, amount, category, note)

        self.assertEqual(identifier, item.identifier)
        self.assertEqual(name, item.name)
        self.assertEqual(amount, item.amount)
        self.assertEqual(category, item.category)
        self.assertEqual(note, item.note)

    def test_budget_item_from_dict(self):
        identifier = '88f0f4e2-ba3b-4bf5-93bd-0eda2f17f45d'
        name = 'name'
        amount = '3.14'
        category = 'category'
        note = 'note'
        data = {
            'identifier': UUID(identifier),
            'name': 'name',
            'amount': float(amount),
            'category': 'category',
            'note': 'note',
        }
        item = BudgetItemViewModel.from_dict(data)

        self.assertEqual(identifier, item.identifier)
        self.assertEqual(name, item.name)
        self.assertEqual(amount, item.amount)
        self.assertEqual(category, item.category)
        self.assertEqual(note, item.note)

    def test_budget_item_to_dict(self):
        identifier = 'identifier'
        name = 'name'
        amount = 'amount'
        category = 'category'
        note = 'note'
        item = BudgetItemViewModel(identifier, name, amount, category, note)
        data = item.to_dict()

        self.assertEqual(identifier, data['identifier'])
        self.assertEqual(name, data['name'])
        self.assertEqual(amount, data['amount'])
        self.assertEqual(category, data['category'])
        self.assertEqual(note, data['note'])


class TestBudgetErrorViewModel(unittest.TestCase):

    def test_error_data(self):
        command = 'cmd'
        message = 'msg'
        error = BudgetErrorViewModel(command, message)

        self.assertEqual(command, error.command)
        self.assertEqual(message, error.message)


class TestBudgetUseCaseFacade(unittest.TestCase):

    def test_budget_use_case_facade_factory(self):
        budget_use_case_facade = BudgetUseCaseFacadeFactory.create_facade(None, None, None)
        
        self.assertEqual(AddBudgetItemUseCase, type(budget_use_case_facade.add_use_case))
        self.assertEqual(UpdateBudgetItemUseCase, type(budget_use_case_facade.update_use_case))
        self.assertEqual(DeleteBudgetItemUseCase, type(budget_use_case_facade.delete_use_case))
        self.assertEqual(GetBudgetItemByCategoryUseCase, type(budget_use_case_facade.get_by_category_use_case))
        self.assertEqual(ListBudgetItemsUseCase, type(budget_use_case_facade.list_use_case))
        self.assertEqual(ShowBudgetOverviewUseCase, type(budget_use_case_facade.overview_use_case))
        self.assertEqual(ShowBudgetDistributionUseCase, type(budget_use_case_facade.distribution_use_case))
        self.assertEqual(SaveBudgetUseCase, type(budget_use_case_facade.save_use_case))
        self.assertEqual(LoadBudgetUseCase, type(budget_use_case_facade.load_use_case))


if __name__ == '__main__':
    unittest.main()