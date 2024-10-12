from typing import Protocol

from domain.transaction import History
from finance.domain.budget import Budget
from finance.application.interface import BudgetRepositoryInterface, HistoryRepositoryInterface
from finance.interface.facade import BudgetUseCaseFacadeFactory, HistoryUseCaseFacadeFactory, ReportUseCaseFacadeFactory
from finance.interface.controller import BudgetControllerInterface, HistoryControllerInterface, ReportControllerInterface
from finance.infrastructure.presenter import CmdBudgetPresenter, CmdHistoryPresenter, CmdReportPresenter
from finance.infrastructure.view import CmdBudgetView, CmdHistoryView, CmdReportView
from finance.infrastructure.controller import CmdBudgetController, CmdHistoryController, CmdReportController
from infrastructure.importer import ErsteBankCsvTransactionImporter
from infrastructure.reader import CmdInputReader


class AbstractComponentFactory(Protocol):

    def get_budget_controller(self) -> BudgetControllerInterface:
        ...

    def get_history_controller(self) -> HistoryControllerInterface:
        ...

    def get_report_controller(self) -> ReportControllerInterface:
        ...


class CmdComponentFactory(AbstractComponentFactory):

    def __init__(self) -> None:
        self._budget_controller: BudgetControllerInterface = None
        self._history_controller: HistoryControllerInterface = None
        self._report_controller: ReportControllerInterface = None

    def get_budget_controller(self, budget: Budget, repository: BudgetRepositoryInterface) -> BudgetControllerInterface:
        if not self._budget_controller:
            view = CmdBudgetView()
            presenter = CmdBudgetPresenter(view)
            facade = BudgetUseCaseFacadeFactory.create_facade(budget, repository, presenter)
            self._budget_controller = CmdBudgetController(facade)
        return self._budget_controller

    def get_history_controller(self, history: History, repository: HistoryRepositoryInterface) -> HistoryControllerInterface:
        if not self._history_controller:
            importer = ErsteBankCsvTransactionImporter()
            reader = CmdInputReader()
            view = CmdHistoryView()
            presenter = CmdHistoryPresenter(view)
            facade = HistoryUseCaseFacadeFactory.create_facade(history, importer, repository, presenter)
            self._history_controller = CmdHistoryController(facade, reader, presenter)
        return self._history_controller

    def get_report_controller(self, history: History, budget: Budget) -> ReportControllerInterface:
        if not self._report_controller:
            view = CmdReportView()
            presenter = CmdReportPresenter(view)
            facade = ReportUseCaseFacadeFactory.create_facade(history, budget, presenter)
            self._report_controller = CmdReportController(facade)
        return self._report_controller
