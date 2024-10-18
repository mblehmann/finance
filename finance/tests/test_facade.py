# import unittest
# from unittest.mock import Mock
# from finance.application.dto import InteractorResultDto
# from interface.facade import BudgetUseCaseFacade
# from finance.application.budget_interactor import (
#     AddBudgetItemUseCase,
#     LoadBudgetUseCase,
#     SaveBudgetUseCase,
#     UpdateBudgetItemUseCase,
#     DeleteBudgetItemUseCase,
#     GetBudgetItemUseCase,
#     GetBudgetItemByCategoryUseCase,
#     ListBudgetItemsUseCase,
#     BudgetItem,
#     BudgetCategory
# )

# class TestBudgetUseCaseFacade(unittest.TestCase):

#     def setUp(self):
#         # Mocking each use case
#         self.mock_add_use_case = Mock(spec=AddBudgetItemUseCase)
#         self.mock_update_use_case = Mock(spec=UpdateBudgetItemUseCase)
#         self.mock_delete_use_case = Mock(spec=DeleteBudgetItemUseCase)
#         self.mock_select_use_case = Mock(spec=GetBudgetItemUseCase)
#         self.mock_select_by_category_use_case = Mock(spec=GetBudgetItemByCategoryUseCase)
#         self.mock_list_use_case = Mock(spec=ListBudgetItemsUseCase)
#         self.mock_save_use_case = Mock(spec=SaveBudgetUseCase)
#         self.mock_load_use_case = Mock(spec=LoadBudgetUseCase)

#         # Creating the facade instance with mocked use cases
#         self.facade = BudgetUseCaseFacade(
#             add_use_case=self.mock_add_use_case,
#             update_use_case=self.mock_update_use_case,
#             delete_use_case=self.mock_delete_use_case,
#             get_use_case=self.mock_select_use_case,
#             get_by_category_use_case=self.mock_select_by_category_use_case,
#             list_use_case=self.mock_list_use_case,
#             save_use_case=self.mock_save_use_case,
#             load_use_case=self.mock_load_use_case
#         )

#     def test_add_budget_item(self):
#         name = 'Test'
#         amount = 100.0
#         category = 'Needs'
#         note = 'Test Note'
#         response = InteractorResultDto(success=True)
#         self.mock_add_use_case.execute.return_value = response
#         result = self.facade.add_use_case.execute(name, amount, category, note)

#         self.assertTrue(result.success)
#         self.mock_add_use_case.execute.assert_called_once_with(name, amount, category, note)

#     def test_update_budget_item(self):
#         identifier = '123'
#         name = 'Test'
#         amount = 100.0
#         category = 'Needs'
#         note = 'Test Note'
#         response = InteractorResultDto(success=True)
#         self.mock_update_use_case.execute.return_value = response
#         result = self.facade.update_use_case.execute(identifier, name, amount, category, note)
        
#         self.assertTrue(result.success)
#         self.mock_update_use_case.execute.assert_called_once_with(identifier, name, amount, category, note)

#     def test_delete_budget_item(self):
#         identifier = "123"
#         response = InteractorResultDto(success=True)
#         self.mock_delete_use_case.execute.return_value = response
#         result = self.facade.delete_use_case.execute(identifier)

#         self.assertTrue(result.success)
#         self.mock_delete_use_case.execute.assert_called_once_with(identifier)

#     def test_get_budget_item(self):
#         identifier = "123"
#         response = InteractorResultDto(success=True)
#         self.mock_select_use_case.execute.return_value = response
#         result = self.facade.get_use_case.execute(identifier)

#         self.assertTrue(result.success)
#         self.mock_select_use_case.execute.assert_called_once_with(identifier)

#     def test_get_by_category_budget_item(self):
#         category = 'Needs'
#         items = [
#             BudgetItem("123", "Test", 100.0, BudgetCategory.Needs, "Test Note"),
#             BudgetItem("456", "Test", 200.0, BudgetCategory.Needs, "Test Note")
#         ]
#         response = InteractorResultDto(success=True)
#         self.mock_select_by_category_use_case.execute.return_value = response
#         result = self.facade.get_by_category_use_case.execute(category)

#         self.assertTrue(result.success)
#         self.mock_select_by_category_use_case.execute.assert_called_once_with(category)

#     def test_list_budget_items(self):
#         response = InteractorResultDto(success=True)
#         self.mock_list_use_case.execute.return_value = response
#         result = self.facade.list_use_case.execute()

#         self.assertTrue(result.success)
#         self.mock_list_use_case.execute.assert_called_once()

#     def test_save_budget(self):
#         filename = "test_budget.csv"
#         items = [
#             BudgetItem("123", "Test", 100.0, BudgetCategory.Savings, "Test Note"),
#             BudgetItem("456", "Test", 200.0, BudgetCategory.Wants, "Test Note")
#         ]
#         response = InteractorResultDto(success=True)
#         self.mock_save_use_case.execute.return_value = response
#         result = self.facade.save_use_case.execute(filename, items)

#         self.assertTrue(result.success)
#         self.mock_save_use_case.execute.assert_called_once_with(filename, items)

#     def test_load_budget(self):
#         filename = "test_budget.csv"
#         response = InteractorResultDto(success=True)
#         self.mock_load_use_case.execute.return_value = response
#         result = self.facade.load_use_case.execute(filename)

#         self.assertTrue(result.success)
#         self.mock_load_use_case.execute.assert_called_once_with(filename)

# if __name__ == '__main__':
#     unittest.main()
