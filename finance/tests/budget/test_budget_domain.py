import unittest
from unittest.mock import Mock
from uuid import UUID, uuid4

from finance.domain.budget import BudgetCategory, BudgetItem, Budget, BudgetItemExistsException, BudgetItemNotFoundException


class TestBudgetItem(unittest.TestCase):
    
    def test_budget_item_constructor(self) -> None:
        identifier = uuid4()
        name = 'Test Budget Item'
        amount = 100.0
        category = BudgetCategory.Needs
        note = 'This is a test budget item'

        budget_item = BudgetItem(identifier=identifier, name=name, amount=amount, category=category, note=note)

        self.assertEqual(budget_item.identifier, identifier)
        self.assertEqual(budget_item.name, name)
        self.assertEqual(budget_item.amount, amount)
        self.assertEqual(budget_item.category, category)
        self.assertEqual(budget_item.note, note)

    def test_budget_item_different_fields_is_not_equal(self):
        identifier1 = uuid4()
        identifier2 = uuid4()
        name1 = 'Test Budget Item 1'
        name2 = 'Test Budget Item 2'
        amount1 = 100.0
        amount2 = 200.0
        category1 = BudgetCategory.Needs
        category2 = BudgetCategory.Wants
        note1 = 'This is a test budget item 1'
        note2 = 'This is a test budget item 2'

        budget_item1 = BudgetItem(identifier=identifier1, name=name1, amount=amount1, category=category1, note=note1)
        budget_item2 = BudgetItem(identifier=identifier2, name=name2, amount=amount2, category=category2, note=note2)

        self.assertNotEqual(budget_item1, budget_item2)

    def test_budget_item_same_id_is_equal(self):
        identifier = uuid4()
        name1 = 'Test Budget Item 1'
        name2 = 'Test Budget Item 2'
        amount1 = 100.0
        amount2 = 200.0
        category1 = BudgetCategory.Needs
        category2 = BudgetCategory.Wants
        note1 = 'This is a test budget item 1'
        note2 = 'This is a test budget item 2'

        budget_item1 = BudgetItem(identifier=identifier, name=name1, amount=amount1, category=category1, note=note1)
        budget_item2 = BudgetItem(identifier=identifier, name=name2, amount=amount2, category=category2, note=note2)

        self.assertEqual(budget_item1, budget_item2)

    def test_budget_item_same_fields_but_different_id_is_not_equal(self):
        identifier1 = uuid4()
        identifier2 = uuid4()
        name = 'Test Budget Item'
        amount = 100.0
        category = BudgetCategory.Needs
        note = 'This is a test budget item'

        budget_item1 = BudgetItem(identifier=identifier1, name=name, amount=amount, category=category, note=note)
        budget_item2 = BudgetItem(identifier=identifier2, name=name, amount=amount, category=category, note=note)

        self.assertNotEqual(budget_item1, budget_item2)

    def test_to_dict(self):
        identifier = uuid4()
        name = "Test"
        amount = 100.0
        category = BudgetCategory.Savings
        note = "Test Note"

        budget_item = BudgetItem(identifier=identifier, name=name, amount=amount, category=category, note=note)
        expected_dict = {
            'identifier': identifier,
            'name': name,
            'amount': amount,
            'category': category.name,
            'note': note
        }
        self.assertEqual(budget_item.to_dict(), expected_dict)

    def test_from_dict(self):
        identifier_str = str(uuid4())
        name = "Test"
        amount_str = "100.0"
        category_str = "Savings"
        note = "Test Note"

        data = {
            'identifier': identifier_str,
            'name': name,
            'amount': amount_str,
            'category': category_str,
            'note': note
        }
        expected_identifier = UUID(identifier_str)
        expected_amount = 100.0
        expected_category = BudgetCategory.Savings

        budget_item = BudgetItem.from_dict(data)
        self.assertEqual(budget_item.identifier, expected_identifier)
        self.assertEqual(budget_item.name, name)
        self.assertEqual(budget_item.amount, expected_amount)
        self.assertEqual(budget_item.category, expected_category)
        self.assertEqual(budget_item.note, note)


class TestBudget(unittest.TestCase):

    def setUp(self):
        self.budget = Budget()

    def test_add_budget_item(self):
        budget_item = Mock(identifier=uuid4())

        item = self.budget.add_budget_item(budget_item)

        self.assertEqual(item, budget_item)
        self.assertEqual(len(self.budget.items), 1)
        self.assertIn(budget_item.identifier, self.budget.items)

    def test_add_existing_budget_item_raises_exception(self):
        budget_item = Mock(identifier=uuid4())
        self.budget.add_budget_item(budget_item)

        with self.assertRaises(BudgetItemExistsException):
            self.budget.add_budget_item(budget_item)

    def test_update_budget_item(self):
        budget_item = Mock(identifier=uuid4())
        updated_budget_item = Mock(identifier=budget_item.identifier)
        self.budget.add_budget_item(budget_item)

        item = self.budget.update_budget_item(updated_budget_item)

        self.assertEqual(item, updated_budget_item)
        self.assertEqual(len(self.budget.items), 1)
        self.assertIn(updated_budget_item.identifier, self.budget.items)

    def test_update_non_existing_item_raises_exception(self):
        non_existing_budget_item = Mock(identifier=uuid4())
        with self.assertRaises(BudgetItemNotFoundException):
            self.budget.update_budget_item(non_existing_budget_item)

    def test_delete_budget_item(self):
        budget_item = Mock(identifier=uuid4())
        self.budget.add_budget_item(budget_item)

        item = self.budget.delete_budget_item(budget_item.identifier)

        self.assertEqual(item, budget_item)
        self.assertEqual(len(self.budget.items), 0)
        self.assertNotIn(budget_item.identifier, self.budget.items)

    def test_delete_non_existing_item_raises_exception(self):
        non_existing_budget_item = Mock(identifier=uuid4())
        with self.assertRaises(BudgetItemNotFoundException):
            self.budget.delete_budget_item(non_existing_budget_item.identifier)

    def test_get_budget_item(self):
        budget_item = Mock(identifier=uuid4())
        self.budget.add_budget_item(budget_item)

        item = self.budget.get_budget_item(budget_item.identifier)

        self.assertEqual(item, budget_item)

    def test_get_non_existing_item_raises_exception(self):
        non_existing_budget_item = Mock(identifier=uuid4())
        with self.assertRaises(BudgetItemNotFoundException):
            self.budget.get_budget_item(non_existing_budget_item.identifier)

    def test_get_budget_item_by_name(self):
        name = 'item'
        budget_item = Mock(identifier=uuid4())
        budget_item.name = name
        self.budget.add_budget_item(budget_item)

        item = self.budget.get_budget_item_by_name(name)

        self.assertEqual(item, budget_item)
        
    def test_get_non_existing_budget_item_by_name_raises_exception(self):
        name = 'item'
        with self.assertRaises(BudgetItemNotFoundException):
            self.budget.get_budget_item_by_name(name)

    def test_get_budget_item_by_category(self):
        budget_item1 = Mock(identifier=uuid4(), category=BudgetCategory.Needs)
        budget_item2 = Mock(identifier=uuid4(), category=BudgetCategory.Needs)
        budget_item3 = Mock(identifier=uuid4(), category=BudgetCategory.Needs)
        self.budget.add_budget_item(budget_item1)
        self.budget.add_budget_item(budget_item2)
        self.budget.add_budget_item(budget_item3)

        items = self.budget.get_budget_item_by_category(BudgetCategory.Needs)

        self.assertEqual(items, [budget_item1, budget_item2, budget_item3])

    def test_get_budget_item_by_category_no_items(self):
        items = self.budget.get_budget_item_by_category(BudgetCategory.Needs)

        self.assertEqual(items, [])

    def test_list_budget_items(self):
        budget_item1 = Mock(identifier=uuid4())
        budget_item2 = Mock(identifier=uuid4())
        budget_item3 = Mock(identifier=uuid4())
        self.budget.add_budget_item(budget_item1)
        self.budget.add_budget_item(budget_item2)
        self.budget.add_budget_item(budget_item3)

        self.assertEqual(self.budget.list_budget_items(), [budget_item1, budget_item2, budget_item3])


if __name__ == '__main__':
    unittest.main()
