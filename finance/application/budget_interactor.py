import os
from uuid import UUID, uuid4
from finance.domain.budget import Budget, BudgetItem, BudgetCategory
from finance.domain.exception import BudgetCategoryNotFoundException, BudgetItemExistsException, BudgetItemNotFoundException
from finance.application.dto import BudgetItemDto, InteractorResultDto
from finance.application.interface import BudgetPresenterInterface, BudgetRepositoryInterface


class AddBudgetItemUseCase:

    def __init__(self, budget: Budget, presenter: BudgetPresenterInterface) -> None:
        self.budget = budget
        self.presenter = presenter

    def execute(self, name: str, amount: float, category: str, note: str) -> None:
        result: InteractorResultDto = None
        operation = 'Add Budget Item'
        identifier = uuid4()
        try:
            category = BudgetCategory[category]
        except KeyError:
            error = BudgetCategoryNotFoundException(f'"{category}" is not a valid budget category. The valid categories are: {[member.name for member in BudgetCategory]}')
            result = InteractorResultDto(success=False, operation=operation, error=str(error))
            
        if result is None:
            budget_item = BudgetItem(identifier, name, amount, category, note)
            try:
                response = self.budget.add_budget_item(budget_item)
                result = InteractorResultDto(success=True, operation=operation, data=response.to_dict())
            except BudgetItemExistsException as e:
                result = InteractorResultDto(success=False, operation=operation, error=str(e))

        self.presenter.present_budget_item(result)


class UpdateBudgetItemUseCase:

    def __init__(self, budget: Budget, presenter: BudgetPresenterInterface) -> None:
        self.budget = budget
        self.presenter = presenter

    def execute(self, identifier: UUID, **kwargs) -> None:
        result: InteractorResultDto = None
        operation = 'Update Budget Item'
        if 'category' in kwargs:
            try:
                kwargs['category'] = BudgetCategory[kwargs['category']]
            except KeyError:
                error = BudgetCategoryNotFoundException(f'"{kwargs['category']}" is not a valid budget category. The valid categories are: {[member.name for member in BudgetCategory]}')
                result = InteractorResultDto(success=False, operation=operation, error=str(error))

        if result is None:
            try:
                budget_item = self.budget.get_budget_item(identifier)
                fields = ['name', 'amount', 'category', 'note']
                for field in fields:
                    if field in kwargs:
                        budget_item.__setattr__(field, kwargs[field])
                response = self.budget.update_budget_item(budget_item)
                result = InteractorResultDto(success=True, operation=operation, data=response.to_dict())
            except BudgetItemNotFoundException as e:
                result = InteractorResultDto(success=False, operation=operation, error=str(e))
    
        self.presenter.present_budget_item(result)


class DeleteBudgetItemUseCase:

    def __init__(self, budget: Budget, presenter: BudgetPresenterInterface) -> None:
        self.budget = budget
        self.presenter = presenter

    def execute(self, budget_identifier: UUID) -> None:
        result: InteractorResultDto = None
        operation = 'Delete Budget Item'
        try:
            response = self.budget.delete_budget_item(budget_identifier)
            result = InteractorResultDto(success=True, operation=operation, data=response.to_dict())
        except BudgetItemNotFoundException as e:
            result = InteractorResultDto(success=False, operation=operation, error=str(e))

        self.presenter.present_budget_item(result)


# class GetBudgetItemUseCase:

#     def __init__(self, budget: Budget) -> None:
#         self.budget = budget

#     def execute(self, budget_identifier: UUID) -> InteractorResultDto:
#         try:
#             response = self.budget.get_budget_item(budget_identifier)
#             result = InteractorResultDto(success=True, data=response)
#         except BudgetItemNotFoundException as e:
#             result = InteractorResultDto(success=False, error=str(e))
#         finally:
#             return result


class GetBudgetItemByCategoryUseCase:

    def __init__(self, budget: Budget, presenter: BudgetPresenterInterface) -> None:
        self.budget = budget
        self.presenter = presenter

    def execute(self, category: str) -> None:
        result: InteractorResultDto = None
        operation = 'Get Budget Items'
        try:
            category = BudgetCategory[category]
        except KeyError:
            error = BudgetCategoryNotFoundException(f'"{category}" is not a valid budget category. The valid categories are: {[member.name for member in BudgetCategory]}')
            result = InteractorResultDto(success=False, operation=operation, error=str(error))

        if result is None:
            items = self.budget.get_budget_item_by_category(category)
            response = [item.to_dict() for item in items]
            result = InteractorResultDto(success=True, operation=operation, data=response)
        self.presenter.present_budget_list(result)


class ListBudgetItemsUseCase:

    def __init__(self, budget: Budget, presenter: BudgetPresenterInterface) -> None:
        self.budget = budget
        self.presenter = presenter

    def execute(self) -> None:
        operation = 'List Budget Items'
        items = sorted(self.budget.list_budget_items(), key=lambda x: (x.category.value, -x.amount))
        response = [item.to_dict() for item in items]
        result = InteractorResultDto(success=True, operation=operation, data=response)
        self.presenter.present_budget_list(result)


class ShowBudgetSummaryUseCase:

    def __init__(self, budget: Budget, presenter: BudgetPresenterInterface) -> None:
        self.budget = budget
        self.presenter = presenter

    def execute(self) -> None:
        # TODO get budget statistics: sum income, sum expense, distribution by category, unassigned
        operation = 'Show Budget Summary'
        items = self.budget.list_budget_items()
        response = [item.to_dict() for item in items]
        result = InteractorResultDto(success=True, operation=operation, data=response)
        self.presenter.present_budget_list(result)


class SaveBudgetUseCase:

    def __init__(self, budget: Budget, repository: BudgetRepositoryInterface, presenter: BudgetPresenterInterface) -> None:
        self.budget = budget
        self.repository = repository
        self.presenter = presenter

    def execute(self, project_name: str) -> None:
        operation = 'Save Budget'
        budget_data = [BudgetItemDto.from_dict(item.to_dict()) for item in self.budget.list_budget_items()]
        filename = os.path.join(project_name, 'budget.csv')
        self.repository.save_budget(filename, budget_data)
        result = InteractorResultDto(success=True, operation=operation, data=f'Budget with {len(budget_data)} items saved on {filename}')
        self.presenter.present_success(result)


class LoadBudgetUseCase:

    def __init__(self, budget: Budget, repository: BudgetRepositoryInterface, presenter: BudgetPresenterInterface) -> None:
        self.budget = budget
        self.repository = repository
        self.presenter = presenter

    def execute(self, project_name: str) -> None:
        operation = 'Load Budget'
        filename = os.path.join(project_name, 'budget.csv')
        response = self.repository.load_budget(filename)
        data = [BudgetItem.from_dict(item.to_dict()) for item in response]
        self.budget.items = {item.identifier: item for item in data}
        result = InteractorResultDto(success=True, operation=operation, data=f'Budget loaded from {filename} with {len(data)} items')
        self.presenter.present_success(result)
