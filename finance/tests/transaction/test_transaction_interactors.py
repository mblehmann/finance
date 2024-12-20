from datetime import date, datetime
import unittest
from unittest.mock import ANY, Mock, call
from uuid import uuid4

from finance.application.transaction_interactor import IgnoreTransactionUseCase, ImportTransactionsUseCase, ListTransactionsUseCase, UpdateTransactionUseCase
from finance.application.dto import InteractorResultDto, TransactionDto
from finance.application.interface import HistoryPresenterInterface, TransactionImporterInterface
from finance.domain.transaction import History, Transaction


class TestTransactionDto(unittest.TestCase):

    def test_from_dict(self):
        day = date(2024, 10, 8)
        data = {
            'reference': 'reference',
            'day': day.isoformat(),
            'source': 'source',
            'amount': '12.67',
            'notes': 'a lot of notes',
            'category': '',
            'month': str(8),
            'tag': 'holiday',
            'comments': 'none',
            'ignore': str(False),
        }

        dto = TransactionDto.from_dict(data)
        self.assertEqual('reference', dto.reference)
        self.assertEqual('2024-10-08', dto.day)
        self.assertEqual('source', dto.source)
        self.assertEqual('12.67', dto.amount)
        self.assertEqual('a lot of notes', dto.notes)
        self.assertEqual('', dto.category)
        self.assertEqual('8', dto.month)
        self.assertEqual('holiday', dto.tag)
        self.assertEqual('none', dto.comments)
        self.assertEqual('False', dto.ignore)

    def test_from_dict_budget_item(self):
        day = date(2024, 10, 8)
        item = Transaction('reference', day, 'source', 1400.84, 'nothing to add', 'category', 8, 'birthday', 'comments', True)

        dto = TransactionDto.from_dict(item.to_dict())
        self.assertEqual('reference', dto.reference)
        self.assertEqual('2024-10-08', dto.day)
        self.assertEqual('source', dto.source)
        self.assertEqual('1400.84', dto.amount)
        self.assertEqual('nothing to add', dto.notes)
        self.assertEqual('category', dto.category)
        self.assertEqual('8', dto.month)
        self.assertEqual('birthday', dto.tag)
        self.assertEqual('comments', dto.comments)
        self.assertEqual('True', dto.ignore)

    def test_to_dict(self):
        dto = TransactionDto('reference', '2024-10-08', 'source', '1400.84', 'nothing to add', 'category', '8', 'gift', 'comments', 'False')

        data = dto.to_dict()
        self.assertEqual('reference', data['reference'])
        self.assertEqual('2024-10-08', data['day'])
        self.assertEqual('source', data['source'])
        self.assertEqual('1400.84', data['amount'])
        self.assertEqual('nothing to add', data['notes'])
        self.assertEqual('category', data['category'])
        self.assertEqual('8', data['month'])
        self.assertEqual('gift', data['tag'])
        self.assertEqual('comments', data['comments'])
        self.assertEqual('False', data['ignore'])


class TestHistoryUseCases(unittest.TestCase):

    def setUp(self):
        self.history = History()
        self.mock_importer = Mock(spec=TransactionImporterInterface)
        self.mock_presenter = Mock(spec=HistoryPresenterInterface)

    def test_import_transaction_no_transactions_use_case(self):
        filename = 'filename'
        self.mock_importer.import_transactions.return_value = []
        response = {
            'imported': [],
            'duplicated': []
        }
        result = InteractorResultDto(success=True, operation="Import Transactions", data=response)

        use_case = ImportTransactionsUseCase(self.history, self.mock_importer, self.mock_presenter)
        
        use_case.execute(filename)

        self.assertEqual(0, len(self.history.items))
        self.mock_presenter.present_import_transactions.assert_called_once_with(result)

    def test_import_transaction_use_case(self):
        filename = 'filename'
        transaction_dto = TransactionDto('reference', '2024-10-08', 'source', '1400.84', 'nothing to add', 'category', '8', 'gift', 'comments', 'False')
        transaction_dto2 = TransactionDto('reference2', '2024-10-08', 'source', '1400.84', 'nothing to add', 'category', '8', 'gift', 'comments', 'False')
        transaction_dto3 = TransactionDto('reference3', '2024-10-08', 'source', '1400.84', 'nothing to add', 'category', '8', 'gift', 'comments', 'False')

        self.mock_importer.import_transactions.return_value = [transaction_dto, transaction_dto2, transaction_dto3]
        response = {
            'imported': [
                Transaction.from_dict(transaction_dto.to_dict()).to_dict(),
                Transaction.from_dict(transaction_dto2.to_dict()).to_dict(),
                Transaction.from_dict(transaction_dto3.to_dict()).to_dict()
            ],
            'duplicated': []
        }
        result = InteractorResultDto(success=True, operation="Import Transactions", data=response)

        use_case = ImportTransactionsUseCase(self.history, self.mock_importer, self.mock_presenter)
        
        use_case.execute(filename)

        self.assertEqual(3, len(self.history.items))
        self.mock_presenter.present_import_transactions.assert_called_once_with(result)

    def test_import_transaction_duplicate_items_use_case(self):
        filename = 'filename'
        transaction_dto = TransactionDto('reference', '2024-10-08', 'source', '1400.84', 'nothing to add', 'category', '8', 'gift', 'comments', 'False')

        self.mock_importer.import_transactions.return_value = [transaction_dto, transaction_dto, transaction_dto]
        response = {
            'imported': [Transaction.from_dict(transaction_dto.to_dict()).to_dict()],
            'duplicated': [
                'Failed to add transaction. Transaction with reference "reference" already exists',
                'Failed to add transaction. Transaction with reference "reference" already exists'
            ]
        }
        result = InteractorResultDto(success=True, operation="Import Transactions", data=response)

        use_case = ImportTransactionsUseCase(self.history, self.mock_importer, self.mock_presenter)
        
        use_case.execute(filename)

        self.assertEqual(1, len(self.history.items))
        self.mock_presenter.present_import_transactions.assert_called_once_with(result)

    def test_import_transaction_non_existing_file_use_case(self):
        filename = 'filename'

        self.mock_importer.import_transactions.side_effect = Exception(f'No such file {filename}')
        result = InteractorResultDto(success=False, operation="Import Transactions", error='No such file filename')

        use_case = ImportTransactionsUseCase(self.history, self.mock_importer, self.mock_presenter)
        
        use_case.execute(filename)

        self.assertEqual(0, len(self.history.items))
        self.mock_presenter.present_import_transactions.assert_called_once_with(result)

    def test_update_transaction_use_case(self):
        reference = 'reference'

        test_cases = [
            {'category': 'category', 'month': 8, 'tag': 'tag', 'comments': 'comments'},
            {'category': 'category'},
            {'month': 8},
            {'tag': 'tag'},
            {'comments': 'comments'},
        ]

        for update in test_cases:
            with self.subTest(fields=list(update.keys())):
                self.history = History()
                self.mock_presenter.reset_mock()
                transaction = Transaction(reference, date(2024, 10, 8), 'source', 1400.84, 'nothing to add', 'vacation', 4, 'gift', 'testing', False)
                self.history.add_transaction(transaction)

                response = transaction.to_dict()
                response.update(update)
                result = InteractorResultDto(success=True, operation='Update Transaction', data=response)
                use_case = UpdateTransactionUseCase(self.history, self.mock_presenter)

                use_case.execute(reference, **update)

                for key, value in update.items():
                    self.assertEqual(value, self.history.items[reference].__getattribute__(key))
                self.mock_presenter.present_transaction.assert_called_once_with(result)

    def test_update_non_existing_transaction_returns_error(self):
        reference = 'reference'
        update = {'category': 'category', 'month': 8, 'tag': 'tag', 'comments': 'comments'}
        error = f'Failed to get transaction. Transaction with reference "reference" does not exist'
        result = InteractorResultDto(success=False, operation="Update Transaction", error=error)

        use_case = UpdateTransactionUseCase(self.history, self.mock_presenter)

        use_case.execute(reference, **update)

        self.assertNotIn(reference, self.history.items)
        self.mock_presenter.present_transaction.assert_called_once_with(result)

    def test_ignore_transaction_use_case(self):
        reference = 'reference'
        test_cases = [True, False]

        for ignore in test_cases:
            with self.subTest(ignore=ignore):
                self.history = History()
                self.mock_presenter.reset_mock()
                transaction = Transaction(reference, date(2024, 10, 8), 'source', 1400.84, 'nothing to add', 'vacation', 4, 'gift', 'testing', not ignore)
                self.history.add_transaction(transaction)

                response = transaction.to_dict()
                response['ignore'] = ignore
                result = InteractorResultDto(success=True, operation='Ignore Transaction', data=response)
                use_case = IgnoreTransactionUseCase(self.history, self.mock_presenter)

                use_case.execute(reference, ignore)

                self.assertEqual(ignore, self.history.items[reference].ignore)
                self.mock_presenter.present_transaction.assert_called_once_with(result)
    
    def test_ignore_non_existing_transaction_returns_error(self):
        reference = 'reference'
        ignore = True
        error = f'Failed to get transaction. Transaction with reference "reference" does not exist'
        result = InteractorResultDto(success=False, operation="Ignore Transaction", error=error)

        use_case = IgnoreTransactionUseCase(self.history, self.mock_presenter)

        use_case.execute(reference, ignore)

        self.assertNotIn(reference, self.history.items)
        self.mock_presenter.present_transaction.assert_called_once_with(result)

    def test_list_transactions_use_case(self):
        transaction1 = Transaction('ref1', date(2024, 8, 10), 'source1', 1400.84, 'nothing to add1', 'vacation', 8, 'gift', 'testing1', False)
        transaction2 = Transaction('ref2', date(2024, 8, 1), 'source2', 10.33, 'nothing to add2', 'groceries', 8, 'lidl', 'testing2', False)
        transaction3 = Transaction('ref3', date(2024, 8, 20), 'source3', 22.05, 'nothing to add3', 'eatingout', 8, 'tgtg', 'testing3', True)
        transaction4 = Transaction('ref4', date(2024, 8, 30), 'source4', 132.47, 'nothing to add4', 'coinsurance', 9, 'oegk', 'testing4', False)
        transaction5 = Transaction('ref5', date(2024, 8, 15), 'source5', 5.23, 'nothing to add5', 'groceries', 8, 'hofer', 'testing5', False)
        self.history.add_transaction(transaction1)
        self.history.add_transaction(transaction2)
        self.history.add_transaction(transaction3)
        self.history.add_transaction(transaction4)
        self.history.add_transaction(transaction5)
        month = 8

        response = [transaction2.to_dict(), transaction1.to_dict(), transaction5.to_dict(), transaction3.to_dict()]
        result = InteractorResultDto(success=True, operation='List Transactions', data=response)
        use_case = ListTransactionsUseCase(self.history, self.mock_presenter)

        use_case.execute(month)

        self.mock_presenter.present_history.assert_called_once_with(result)


if __name__ == '__main__':
    unittest.main()
