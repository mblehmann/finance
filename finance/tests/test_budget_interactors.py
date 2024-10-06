import unittest
from unittest.mock import Mock
from uuid import uuid4
from application.interface import BudgetPresenterInterface
from finance.domain.budget import Budget, BudgetItem, BudgetCategory
from finance.application.budget_interactor import (
    BudgetRepositoryInterface,
    AddBudgetItemUseCase,
    LoadBudgetUseCase,
    SaveBudgetUseCase,
    UpdateBudgetItemUseCase,
    DeleteBudgetItemUseCase,
    GetBudgetItemUseCase,
    GetBudgetItemByCategoryUseCase,
    ListBudgetItemsUseCase,
)


class TestBudgetUseCases(unittest.TestCase):

    def setUp(self):
        self.budget = Budget()

    def test_add_budget_item_use_case(self):
        name = 'Test Item'
        amount = 100.0
        category = 'Needs'
        note = 'Test Note'
        use_case = AddBudgetItemUseCase(self.budget)
        result = use_case.execute(name, amount, category, note)
        item: BudgetItem = result.data

        self.assertTrue(result.success)
        self.assertIsNotNone(item.identifier)
        self.assertEqual(item.name, name)
        self.assertEqual(item.amount, amount)
        self.assertEqual(item.category, BudgetCategory[category])
        self.assertEqual(item.note, note)
        self.assertIsNone(result.error)

    def test_update_budget_item_use_case(self):
        identifier = uuid4()
        name = 'Another'
        amount = 54.43
        category = 'Savings'
        note = 'Note'
        item = BudgetItem(identifier, 'Test Item', 100.0, BudgetCategory.Wants, 'Test Note')
        self.budget.add_budget_item(item)
        use_case = UpdateBudgetItemUseCase(self.budget)
        result = use_case.execute(identifier, name, amount, category, note)
        response: BudgetItem = result.data

        self.assertTrue(result.success)
        self.assertIsNotNone(item.identifier)
        self.assertEqual(response.identifier, identifier)
        self.assertEqual(response.name, name)
        self.assertEqual(response.amount, amount)
        self.assertEqual(response.category, BudgetCategory[category])
        self.assertEqual(response.note, note)
        self.assertIsNone(result.error)

    def test_update_nonexistent_budget_item_use_case(self):
        identifier = uuid4()
        name = 'Test Item'
        amount = 100.0
        category = 'Needs'
        note = 'Test Note'
        use_case = UpdateBudgetItemUseCase(self.budget)
        result = use_case.execute(identifier, name, amount, category, note)

        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        self.assertEqual(result.error, f'Item with identifier {identifier} does not exist')

    def test_delete_budget_item_use_case(self):
        identifier = uuid4()
        item = BudgetItem(identifier, "Test Item", 100.0, BudgetCategory.Savings, "Test Note")
        self.budget.add_budget_item(item)
        use_case = DeleteBudgetItemUseCase(self.budget)
        result = use_case.execute(identifier)
        
        self.assertTrue(result.success)
        self.assertEqual(result.data, item)
        self.assertIsNone(result.error)

    def test_delete_nonexistent_budget_item_use_case(self):
        identifier = uuid4()
        use_case = DeleteBudgetItemUseCase(self.budget)
        result = use_case.execute(identifier)

        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        self.assertEqual(result.error, f'Item with identifier {identifier} does not exist')

    def test_get_budget_item_use_case(self):
        identifier = uuid4()
        item = BudgetItem(identifier, "Test Item", 100.0, BudgetCategory.Wants, "Test Note")
        self.budget.add_budget_item(item)
        use_case = GetBudgetItemUseCase(self.budget)
        result = use_case.execute(identifier)
        
        self.assertTrue(result.success)
        self.assertEqual(result.data, item)
        self.assertIsNone(result.error)

    def test_get_nonexistent_budget_item_use_case(self):
        identifier = uuid4()
        use_case = GetBudgetItemUseCase(self.budget)
        result = use_case.execute(identifier)
        
        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        self.assertEqual(result.error, f'Item with identifier {identifier} does not exist')

    def test_get_budget_item_by_category_use_case(self):
        category = 'Savings'
        items = [
            BudgetItem(uuid4(), "Test Item 1", 100.0, BudgetCategory.Savings, "Test Note"),
            BudgetItem(uuid4(), "Test Item 2", 200.0, BudgetCategory.Savings, "Test Note")
        ]
        for item in items:
            self.budget.add_budget_item(item)
        use_case = GetBudgetItemByCategoryUseCase(self.budget)
        result = use_case.execute(category)

        self.assertTrue(result.success)
        self.assertEqual(result.data, items)
        self.assertIsNone(result.error)

    def test_list_budget_items_use_case(self):
        items = [
            BudgetItem(uuid4(), "Test Item 1", 100.0, BudgetCategory.Needs, "Test Note"),
            BudgetItem(uuid4(), "Test Item 2", 200.0, BudgetCategory.Income, "Test Note")
        ]
        for item in items:
            self.budget.add_budget_item(item)
        use_case = ListBudgetItemsUseCase(self.budget)
        result = use_case.execute()

        self.assertTrue(result.success)
        self.assertEqual(result.data, items)
        self.assertIsNone(result.error)
    

class TestBudgetPersistenceUseCases(unittest.TestCase):

    def setUp(self):
        self.mock_repository = Mock(spec=BudgetRepositoryInterface)
        self.mock_presenter = Mock(spec=BudgetPresenterInterface)

    def test_save_budget_use_case(self):
        filename = "test_budget.json"
        budget = Budget()
        budget.add_budget_item(BudgetItem(uuid4(), "Test Item 1", 100.0, BudgetCategory.Needs, "Test Note"))
        budget.add_budget_item(BudgetItem(uuid4(), "Test Item 2", 200.0, BudgetCategory.Income, "Test Note"))
        use_case = SaveBudgetUseCase(budget, self.mock_repository, self.mock_presenter)
        result = use_case.execute(filename)

        self.assertTrue(result.success)
        self.assertEqual(result.data, filename)
        self.mock_repository.save_budget.assert_called_once_with(filename, [item.to_dict() for item in budget])

    def test_load_budget_use_case(self):
        filename = "test_budget.json"
        loaded_data = {"items": [{"name": "Item 1", "amount": 100}, {"name": "Item 2", "amount": 200}]}
        self.mock_repository.load_budget.return_value = loaded_data
        use_case = LoadBudgetUseCase(repository=self.mock_repository)
        result = use_case.execute(filename)
        
        self.assertTrue(result.success)
        self.assertEqual(result.data, loaded_data)
        self.mock_repository.load_budget.assert_called_once_with(filename)

if __name__ == '__main__':
    unittest.main()
