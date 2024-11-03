import unittest
from unittest.mock import Mock
from uuid import uuid4

from finance.application.interface import HistoryPresenterInterface, InputReaderInterface
from finance.application.transaction_interactor import ImportTransactionsUseCase, UpdateTransactionUseCase
from finance.infrastructure.controller import CmdHistoryController
from finance.interface.facade import HistoryUseCaseFacade

class TestCmdBudgetController(unittest.TestCase):

    def setUp(self):
        self.mock_facade = Mock(spec=HistoryUseCaseFacade)
        self.mock_facade.import_use_case = Mock(spec=ImportTransactionsUseCase)
        self.mock_facade.update_use_case = Mock(spec=UpdateTransactionUseCase)
        self.mock_reader = Mock(spec=InputReaderInterface)
        self.mock_presenter = Mock(spec=HistoryPresenterInterface)
        self.controller = CmdHistoryController(self.mock_facade, self.mock_reader, self.mock_presenter)

    def test_import_transaction(self):
        filename = 'filename'

        self.controller.import_transactions(filename)

        self.mock_facade.import_use_case.execute.assert_called_once_with(filename)

    def test_update_transaction(self):
        reference = 'reference'
        data = {
            'category': 'category',
            'month': 8,
            'tag': 'tag',
            'comments': 'comments'
        }

        self.controller.update_transaction(reference, **data)

        self.mock_facade.update_use_case.execute.assert_called_once_with(reference, **data)


    def test_update_category_transaction(self):
        reference = 'reference'
        data = {'category': 'category'}

        self.controller.update_transaction(reference, **data)

        self.mock_facade.update_use_case.execute.assert_called_once_with(reference, **data)


    def test_update_month_transaction(self):
        reference = 'reference'
        data = {'month': 8}

        self.controller.update_transaction(reference, **data)

        self.mock_facade.update_use_case.execute.assert_called_once_with(reference, **data)


    def test_update_tag_transaction(self):
        reference = 'reference'
        data = {'tag': 'tag'}

        self.controller.update_transaction(reference, **data)

        self.mock_facade.update_use_case.execute.assert_called_once_with(reference, **data)


    def test_update_comments_transaction(self):
        reference = 'reference'
        data = {'comments': 'comments'}

        self.controller.update_transaction(reference, **data)

        self.mock_facade.update_use_case.execute.assert_called_once_with(reference, **data)


if __name__ == '__main__':
    unittest.main()
