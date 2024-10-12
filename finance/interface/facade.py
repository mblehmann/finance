from dataclasses import dataclass
from typing import Self

from application.interface import BudgetPresenterInterface, BudgetRepositoryInterface, HistoryPresenterInterface, HistoryRepositoryInterface, ReportPresenterInterface, TransactionImporterInterface
from application.report_interactor import AllCategoryReportUseCase, CategoryReportUseCase, MonthResultUseCase
from application.transaction_interactor import DeleteTransactionUseCase, GetUnreviewedTransactionsUseCase, IgnoreTransactionUseCase, ImportTransactionsUseCase, LoadHistoryUseCase, ReviewTransactionsUseCase, SaveHistoryUseCase, UpdateTransactionUseCase
from domain.transaction import History
from finance.domain.budget import Budget
from finance.application.budget_interactor import (
    AddBudgetItemUseCase,
    DeleteBudgetItemUseCase,
    ListBudgetItemsUseCase,
    GetBudgetItemByCategoryUseCase,
    LoadBudgetUseCase,
    SaveBudgetUseCase,
    ShowBudgetDistributionUseCase,
    ShowBudgetOverviewUseCase,
    UpdateBudgetItemUseCase
)

@dataclass
class BudgetUseCaseFacade:
    add_use_case: AddBudgetItemUseCase
    update_use_case: UpdateBudgetItemUseCase
    delete_use_case: DeleteBudgetItemUseCase
    get_by_category_use_case: GetBudgetItemByCategoryUseCase
    list_use_case: ListBudgetItemsUseCase
    overview_use_case: ShowBudgetOverviewUseCase
    distribution_use_case: ShowBudgetDistributionUseCase
    save_use_case: SaveBudgetUseCase
    load_use_case: LoadBudgetUseCase


class BudgetUseCaseFacadeFactory:

    @classmethod
    def create_facade(cls, budget: Budget, repository: BudgetRepositoryInterface, presenter: BudgetPresenterInterface) -> Self:
        return BudgetUseCaseFacade(AddBudgetItemUseCase(budget, presenter),
                                   UpdateBudgetItemUseCase(budget, presenter),
                                   DeleteBudgetItemUseCase(budget, presenter),
                                   GetBudgetItemByCategoryUseCase(budget, presenter),
                                   ListBudgetItemsUseCase(budget, presenter),
                                   ShowBudgetOverviewUseCase(budget, presenter),
                                   ShowBudgetDistributionUseCase(budget, presenter),
                                   SaveBudgetUseCase(budget, repository, presenter),
                                   LoadBudgetUseCase(budget, repository, presenter))



@dataclass
class HistoryUseCaseFacade:
    import_use_case: ImportTransactionsUseCase
    review_use_case: ReviewTransactionsUseCase
    update_use_case: UpdateTransactionUseCase
    ignore_use_case: IgnoreTransactionUseCase
    delete_use_case: DeleteTransactionUseCase
    save_use_case: SaveHistoryUseCase
    load_use_case: LoadHistoryUseCase


class HistoryUseCaseFacadeFactory:

    @classmethod
    def create_facade(cls, history: History, importer: TransactionImporterInterface, repository: HistoryRepositoryInterface, presenter: HistoryPresenterInterface) -> Self:
        return HistoryUseCaseFacade(ImportTransactionsUseCase(history, importer, presenter),
                                    ReviewTransactionsUseCase(history, presenter),
                                    UpdateTransactionUseCase(history, presenter),
                                    IgnoreTransactionUseCase(history, presenter),
                                    DeleteTransactionUseCase(history, presenter),
                                    SaveHistoryUseCase(history, repository, presenter),
                                    LoadHistoryUseCase(history, repository, presenter))


@dataclass
class ReportUseCaseFacade:
    category_report: CategoryReportUseCase
    all_category_report: AllCategoryReportUseCase
    month_report: MonthResultUseCase


class ReportUseCaseFacadeFactory:

    @classmethod
    def create_facade(cls, history: History, budget: Budget, presenter: ReportPresenterInterface):
        category_report = CategoryReportUseCase(budget, history, presenter)
        return ReportUseCaseFacade(category_report,
                                   AllCategoryReportUseCase(budget, category_report),
                                   MonthResultUseCase(budget, history, presenter))
    