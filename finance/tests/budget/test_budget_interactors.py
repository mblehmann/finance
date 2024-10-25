import unittest
from unittest.mock import ANY, Mock, call
from uuid import uuid4

from finance.application.dto import BudgetItemDto, InteractorResultDto, TableDto
from finance.application.interface import BudgetPresenterInterface
from finance.domain.budget import Budget, BudgetItem, BudgetCategory
from finance.application.budget_interactor import (
    BudgetRepositoryInterface,
    AddBudgetItemUseCase,
    LoadBudgetUseCase,
    SaveBudgetUseCase,
    ShowBudgetDistributionUseCase,
    ShowBudgetOverviewUseCase,
    UpdateBudgetItemUseCase,
    DeleteBudgetItemUseCase,
    GetBudgetItemByCategoryUseCase,
    ListBudgetItemsUseCase,
)


class TestBudgetItemDto(unittest.TestCase):

    def test_from_dict(self):
        identifier = uuid4()
        data = {
            'identifier': identifier,
            'name': 'name',
            'amount': 7.42,
            'category': BudgetCategory.Income.name,
            'note': 'a lot of notes'
        }

        dto = BudgetItemDto.from_dict(data)
        self.assertEqual(str(identifier), dto.identifier)
        self.assertEqual('name', dto.name)
        self.assertEqual('7.42', dto.amount)
        self.assertEqual('Income', dto.category)
        self.assertEqual('a lot of notes', dto.note)

    def test_from_dict_budget_item(self):
        identifier = uuid4()
        item = BudgetItem(identifier, 'budget', 1400.84, BudgetCategory.Empty, 'nothing to add')

        dto = BudgetItemDto.from_dict(item.to_dict())
        self.assertEqual(str(identifier), dto.identifier)
        self.assertEqual('budget', dto.name)
        self.assertEqual('1400.84', dto.amount)
        self.assertEqual('Empty', dto.category)
        self.assertEqual('nothing to add', dto.note)

    def test_to_dict(self):
        dto = BudgetItemDto('identifier', 'item', '10.08', 'Savings', 'notes')

        data = dto.to_dict()
        self.assertEqual('identifier', data['identifier'])
        self.assertEqual('item', data['name'])
        self.assertEqual('10.08', data['amount'])
        self.assertEqual('Savings', data['category'])
        self.assertEqual('notes', data['note'])


class TestBudgetUseCases(unittest.TestCase):

    def setUp(self):
        self.budget = Budget()
        self.mock_presenter = Mock(spec=BudgetPresenterInterface)

    def test_add_budget_item_use_case(self):
        name = 'Test Item'
        amount = 100.0
        category = 'Needs'
        note = 'Test Note'
        response = {
            'identifier': ANY,
            'name': name,
            'amount': amount,
            'category': category,
            'note': note
        }
        result = InteractorResultDto(success=True, operation="Add Budget Item", data=response)

        use_case = AddBudgetItemUseCase(self.budget, self.mock_presenter)
        
        use_case.execute(name, amount, category, note)

        self.mock_presenter.present_budget_item.assert_called_once_with(result)

    def test_add_budget_item_invalid_category_returns_error(self):
        name = 'Test Item'
        amount = 100.0
        category = 'Needings'
        note = 'Test Note'
        error = f'"{category}" is not a valid budget category. The valid categories are: {[member.name for member in BudgetCategory]}'
        result = InteractorResultDto(success=False, operation="Add Budget Item", error=error)

        use_case = AddBudgetItemUseCase(self.budget, self.mock_presenter)
        
        use_case.execute(name, amount, category, note)

        self.mock_presenter.present_budget_item.assert_called_once_with(result)

    def test_update_budget_item(self):
        identifier = uuid4()

        test_cases = [
            {'name': 'Another', 'amount': 54.43, 'category': 'Savings', 'note': 'Note'},
            {'name': 'Another'},
            {'amount': 54.43},
            {'category': 'Savings'},
            {'note': 'Note'},
        ]

        for update in test_cases:
            with self.subTest(fields=list(update.keys())):
                self.budget = Budget()
                self.mock_presenter.reset_mock()
                item = BudgetItem(identifier, 'Test Item', 100.0, BudgetCategory.Wants, 'Test Note')
                self.budget.add_budget_item(item)

                response = item.to_dict()
                response.update(update)
                result = InteractorResultDto(success=True, operation='Update Budget Item', data=response)
                use_case = UpdateBudgetItemUseCase(self.budget, self.mock_presenter)

                use_case.execute(identifier, **update)

                self.mock_presenter.present_budget_item.assert_called_once_with(result)

    def test_update_budget_item_invalid_category_returns_error(self):
        category = 'Abc'
        update = {'category': category}
        error = f'"{category}" is not a valid budget category. The valid categories are: {[member.name for member in BudgetCategory]}'
        result = InteractorResultDto(success=False, operation="Update Budget Item", error=error)

        use_case = UpdateBudgetItemUseCase(self.budget, self.mock_presenter)

        use_case.execute(uuid4(), **update)

        self.mock_presenter.present_budget_item.assert_called_once_with(result)

    def test_update_non_existing_budget_item_returns_error(self):
        identifier = uuid4()
        update = {'name': 'name'}
        error = f'Failed to get a budget item. Item with identifier "{identifier}" does not exist'
        result = InteractorResultDto(success=False, operation="Update Budget Item", error=error)

        use_case = UpdateBudgetItemUseCase(self.budget, self.mock_presenter)

        use_case.execute(identifier, **update)

        self.mock_presenter.present_budget_item.assert_called_once_with(result)

    def test_delete_budget_item_use_case(self):
        identifier = uuid4()
        item = BudgetItem(identifier, "Test Item", 100.0, BudgetCategory.Savings, "Test Note")
        self.budget.add_budget_item(item)

        response = item.to_dict()
        result = InteractorResultDto(success=True, operation='Delete Budget Item', data=response)
        use_case = DeleteBudgetItemUseCase(self.budget, self.mock_presenter)

        use_case.execute(identifier)

        self.mock_presenter.present_budget_item.assert_called_once_with(result)

    def test_delete_nonexistent_budget_item_use_case(self):
        identifier = uuid4()
        
        error = f'Failed to delete a budget item. Item with identifier "{identifier}" does not exist'
        result = InteractorResultDto(success=False, operation='Delete Budget Item', error=error)
        use_case = DeleteBudgetItemUseCase(self.budget, self.mock_presenter)

        use_case.execute(identifier)

        self.mock_presenter.present_budget_item.assert_called_once_with(result)

    def test_get_budget_item_use_case(self):
        item1 = BudgetItem(uuid4(), 'Test Item', 100.0, BudgetCategory.Wants, 'Test Note')
        item2 = BudgetItem(uuid4(), 'Test Item2', 200.0, BudgetCategory.Wants, 'Test Note3')
        self.budget.add_budget_item(item1)
        self.budget.add_budget_item(item2)

        response = [item1.to_dict(), item2.to_dict()]
        result = InteractorResultDto(success=True, operation='Get Budget Items', data=response)
        use_case = GetBudgetItemByCategoryUseCase(self.budget, self.mock_presenter)

        use_case.execute('Wants')

        self.mock_presenter.present_budget_list.assert_called_once_with(result)

    def test_get_budget_item_empty_list(self):
        response = []
        result = InteractorResultDto(success=True, operation='Get Budget Items', data=response)
        use_case = GetBudgetItemByCategoryUseCase(self.budget, self.mock_presenter)

        use_case.execute('Income')

        self.mock_presenter.present_budget_list.assert_called_once_with(result)

    def test_get_budget_item_invalid_category_returns_error(self):
        category = 'Alguma'
        error = f'"{category}" is not a valid budget category. The valid categories are: {[member.name for member in BudgetCategory]}'
        result = InteractorResultDto(success=False, operation='Get Budget Items', error=error)
        use_case = GetBudgetItemByCategoryUseCase(self.budget, self.mock_presenter)

        use_case.execute(category)

        self.mock_presenter.present_budget_list.assert_called_once_with(result)

    def test_list_budget_items_use_case(self):
        item1 = BudgetItem(uuid4(), "Test Item 1", 100.0, BudgetCategory.Needs, "Test Note")
        item2 = BudgetItem(uuid4(), "Test Item 2", 200.0, BudgetCategory.Income, "Test Note")
        item3 = BudgetItem(uuid4(), "Test Item 3", 300.0, BudgetCategory.Empty, "Test Note")
        item4 = BudgetItem(uuid4(), "Test Item 4", 400.0, BudgetCategory.Savings, "Test Note")
        item5 = BudgetItem(uuid4(), "Test Item 5", 500.0, BudgetCategory.Wants, "Test Note")
        item6 = BudgetItem(uuid4(), "Test Item 6", 600.0, BudgetCategory.Wants, "Test Note")
        self.budget.add_budget_item(item1)
        self.budget.add_budget_item(item2)
        self.budget.add_budget_item(item3)
        self.budget.add_budget_item(item4)
        self.budget.add_budget_item(item5)
        self.budget.add_budget_item(item6)

        response = [item3.to_dict(), item2.to_dict(), item1.to_dict(), item6.to_dict(), item5.to_dict(), item4.to_dict()]
        result = InteractorResultDto(success=True, operation='List Budget Items', data=response)
        use_case = ListBudgetItemsUseCase(self.budget, self.mock_presenter)

        use_case.execute()

        self.mock_presenter.present_budget_list.assert_called_once_with(result)    

    def test_show_budget_overview_use_case(self):
        item1 = BudgetItem(uuid4(), "Test Item 1", 100.0, BudgetCategory.Needs, "Test Note")
        item2 = BudgetItem(uuid4(), "Test Item 2", 200.0, BudgetCategory.Income, "Test Note")
        item3 = BudgetItem(uuid4(), "Test Item 3", 300.0, BudgetCategory.Empty, "Test Note")
        item4 = BudgetItem(uuid4(), "Test Item 4", 400.0, BudgetCategory.Savings, "Test Note")
        item5 = BudgetItem(uuid4(), "Test Item 5", 500.0, BudgetCategory.Wants, "Test Note")
        item6 = BudgetItem(uuid4(), "Test Item 6", 600.8, BudgetCategory.Wants, "Test Note")
        self.budget.add_budget_item(item1)
        self.budget.add_budget_item(item2)
        self.budget.add_budget_item(item3)
        self.budget.add_budget_item(item4)
        self.budget.add_budget_item(item5)
        self.budget.add_budget_item(item6)

        category_overview = TableDto(
            fields=['Category', 'Amount'],
            rows=[
                ['Income', '200.00'],
                ['Expenses', '1,600.80'],
                ['Result', '-1,400.80'],
                ['Unassigned', '300.00']
            ]
        )
        overview_result = InteractorResultDto(success=True, operation='Show Budget Overview', data=category_overview)
        
        category_distribution = TableDto(
            fields=['Category', 'Amount', 'Percentage'],
            rows=[
                ['Empty', '300.00', '-'],
                ['Income', '200.00', '-'],
                ['Needs', '100.00', '6.25%'],
                ['Wants', '1,100.80', '68.77%'],
                ['Savings', '400.00', '24.99%'],
            ]
        )
        distribution_result = InteractorResultDto(success=True, operation='Show Budget Overview', data=category_distribution)
        expected_calls = [call(overview_result), call(distribution_result)]

        use_case = ShowBudgetOverviewUseCase(self.budget, self.mock_presenter)

        use_case.execute()

        self.assertEqual(self.mock_presenter.present_budget_table.call_count, 2)
        self.assertEqual(self.mock_presenter.present_budget_table.call_args_list, expected_calls)

    def test_show_budget_distribution_use_case(self):
        item1 = BudgetItem(uuid4(), "Test Item 1", 100.0, BudgetCategory.Needs, "Test Note1")
        item2 = BudgetItem(uuid4(), "Test Item 2", 200.77, BudgetCategory.Income, "Test Note2")
        item3 = BudgetItem(uuid4(), "Test Item 3", 0.0, BudgetCategory.Savings, "Test Note3")
        item4 = BudgetItem(uuid4(), "Test Item 4", 500.0, BudgetCategory.Wants, "Test Note4")
        item5 = BudgetItem(uuid4(), "Test Item 5", 1600.0, BudgetCategory.Wants, "Test Note5")
        self.budget.add_budget_item(item1)
        self.budget.add_budget_item(item2)
        self.budget.add_budget_item(item3)
        self.budget.add_budget_item(item4)
        self.budget.add_budget_item(item5)

        income_distribution = TableDto(
            fields=['category', 'name', 'note', 'amount', 'percentage'],
            rows=[
                ['Income', 'Test Item 2', 'Test Note2', '200.77', '100.00%'],
                ['Income', 'Total', '', '200.77', '100.00%'],
            ]
        )
        needs_distribution = TableDto(
            fields=['category', 'name', 'note', 'amount', 'percentage'],
            rows=[
                ['Needs', 'Test Item 1', 'Test Note1', '100.00', '100.00%'],
                ['Needs', 'Total', '', '100.00', '100.00%'],
            ]
        )
        wants_distribution = TableDto(
            fields=['category', 'name', 'note', 'amount', 'percentage'],
            rows=[
                ['Wants', 'Test Item 5', 'Test Note5', '1,600.00', '76.19%'],
                ['Wants', 'Test Item 4', 'Test Note4', '500.00', '23.81%'],
                ['Wants', 'Total', '', '2,100.00', '100.00%'],
            ]
        )
        savings_distribution = TableDto(
            fields=['category', 'name', 'note', 'amount', 'percentage'],
            rows=[
                ['Savings', 'Test Item 3', 'Test Note3', '0.00', '0.00%'],
                ['Savings', 'Total', '', '0.00', '100.00%'],
            ]
        )
        
        income_result = InteractorResultDto(success=True, operation='Show Budget Distribution - Income', data=income_distribution)
        needs_result = InteractorResultDto(success=True, operation='Show Budget Distribution - Needs', data=needs_distribution)
        wants_result = InteractorResultDto(success=True, operation='Show Budget Distribution - Wants', data=wants_distribution)
        savings_result = InteractorResultDto(success=True, operation='Show Budget Distribution - Savings', data=savings_distribution)
        
        expected_calls = [call(income_result), call(needs_result), call(wants_result), call(savings_result)]

        use_case = ShowBudgetDistributionUseCase(self.budget, self.mock_presenter)

        use_case.execute()

        self.assertEqual(self.mock_presenter.present_budget_table.call_count, 4)
        self.assertEqual(self.mock_presenter.present_budget_table.call_args_list, expected_calls)

class TestBudgetPersistenceUseCases(unittest.TestCase):

    def setUp(self):
        self.budget = Budget()
        self.mock_repository = Mock(spec=BudgetRepositoryInterface)
        self.mock_presenter = Mock(spec=BudgetPresenterInterface)

    def test_save_budget_use_case(self):
        project = 'budget_project'
        self.budget.add_budget_item(BudgetItem(uuid4(), 'Test Item 1', 100.0, BudgetCategory.Needs, 'Test Note'))
        self.budget.add_budget_item(BudgetItem(uuid4(), 'Test Item 2', 200.0, BudgetCategory.Income, 'Another note'))
        
        budget_data = [BudgetItemDto.from_dict(item.to_dict()) for item in self.budget.list_budget_items()]
        filename = project + '/budget.csv'
        result = InteractorResultDto(success=True, operation='Save Budget', data=f'Budget with 2 items saved on {filename}')
        use_case = SaveBudgetUseCase(self.budget, self.mock_repository, self.mock_presenter)
        
        use_case.execute(project)

        self.mock_repository.save_budget.assert_called_once_with(filename, budget_data)
        self.mock_presenter.present_success.assert_called_once_with(result)

    def test_load_budget_use_case(self):
        project = 'budget_project'
        items = [
            BudgetItem(uuid4(), "Test Item 1", 100.0, BudgetCategory.Needs, "Test Note"),
            BudgetItem(uuid4(), "Test Item 2", 200.0, BudgetCategory.Income, "Test Note2")
        ]
        loaded_data = [BudgetItemDto.from_dict(item.to_dict()) for item in items]
        self.mock_repository.load_budget.return_value = loaded_data

        filename = project + '/budget.csv'
        result = InteractorResultDto(success=True, operation='Load Budget', data=f'Budget loaded from {filename} with 2 items')
        use_case = LoadBudgetUseCase(self.budget, self.mock_repository, self.mock_presenter)

        use_case.execute(project)
        
        self.mock_repository.load_budget.assert_called_once_with(filename)
        self.mock_presenter.present_success.assert_called_once_with(result)


if __name__ == '__main__':
    unittest.main()
