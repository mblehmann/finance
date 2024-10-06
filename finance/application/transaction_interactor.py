import os
from typing import List
from application.dto import InteractorResultDto, TransactionDto
from application.interface import HistoryPresenterInterface, HistoryRepositoryInterface, TransactionImporterInterface
from domain.exception import TransactionExistsException, TransactionNotFoundException, TransactionUpdateException
from domain.transaction import History, Transaction


class ImportTransactionsUseCase:

    def __init__(self, history: History, importer: TransactionImporterInterface, presenter: HistoryPresenterInterface) -> None:
        self.history = history
        self.importer = importer
        self.presenter = presenter

    def execute(self, filename: str) -> None:
        result: InteractorResultDto = None
        operation = 'Import Transactions'
        try:
            transaction_dto_list = self.importer.import_transactions(filename)
        except Exception as e:
            print('exception')
            result = InteractorResultDto(success=False, operation=operation, error=str(e))

        response = {'imported': [], 'duplicated': []}
        if result is None:
            for transaction_dto in transaction_dto_list:
                transaction = Transaction.from_dict(transaction_dto.to_dict())
                try:
                    self.history.add_transaction(transaction)
                    response['imported'].append(transaction.to_dict())
                except TransactionExistsException as e:
                    response['duplicated'].append(str(e))
            result = InteractorResultDto(success=True, operation=operation, data=response)

        self.presenter.present_import_transactions(result)
    

class UpdateTransactionUseCase:

    def __init__(self, history: History, presenter: HistoryPresenterInterface) -> None:
        self.history = history
        self.presenter = presenter

    def execute(self, reference: str, category: str, comments: str) -> None:        
        result: InteractorResultDto = None
        operation = 'Update Transaction'
        
        try:
            transaction = self.history.get_transaction(reference)
        except TransactionNotFoundException as e:
            result = InteractorResultDto(success=False, operation=operation, error=str(e))

        if result is None:
            transaction.category = category
            transaction.comments = comments

            try:
                response = self.history.update_transaction(transaction)
                result = InteractorResultDto(success=True, operation=operation, data=response.to_dict())
            except (TransactionNotFoundException, TransactionUpdateException) as e:
                result = InteractorResultDto(success=False, operation=operation, error=str(e))
    
        self.presenter.present_transaction(result)


class DeleteTransactionUseCase:

    def __init__(self, history: History, presenter: HistoryPresenterInterface) -> None:
        self.history = history
        self.presenter = presenter

    def execute(self, reference: str) -> None:
        result: InteractorResultDto = None
        operation = 'Delete Transaction'
        try:
            response = self.history.delete_transaction(reference)
            result = InteractorResultDto(success=True, operation=operation, data=response.to_dict())
        except TransactionNotFoundException as e:
            result = InteractorResultDto(success=False, operation=operation, error=str(e))

        self.presenter.present_transaction(result)


class GetUnreviewedTransactionsUseCase:

    def __init__(self, history: History, presenter: HistoryPresenterInterface) -> None:
        self.history = history
        self.presenter = presenter

    def execute(self) -> List[TransactionDto]:
        result: InteractorResultDto = None
        operation = 'Review Transactions'
        transactions = self.history.get_unreviewed_transactions()
        response = [TransactionDto.from_dict(item.to_dict()) for item in transactions]

        result = InteractorResultDto(success=True, operation=operation, data=response)
        self.presenter.present_review_transactions(result)
        return response



class SaveHistoryUseCase:

    def __init__(self, history: History, repository: HistoryRepositoryInterface, presenter: HistoryPresenterInterface) -> None:
        self.history = history
        self.repository = repository
        self.presenter = presenter

    def execute(self, project_name: str) -> None:
        operation = 'Save Budget'
        history_data = [TransactionDto.from_dict(item.to_dict()) for item in self.history.list_transactions()]
        filename = os.path.join(project_name, 'history.csv')
        self.repository.save_history(filename, history_data)
        result = InteractorResultDto(success=True, operation=operation, data=f'History with {len(history_data)} transactions saved on {filename}')
        self.presenter.present_success(result)


class LoadHistoryUseCase:

    def __init__(self, history: History, repository: HistoryRepositoryInterface, presenter: HistoryPresenterInterface) -> None:
        self.history = history
        self.repository = repository
        self.presenter = presenter

    def execute(self, project_name: str) -> None:
        operation = 'Load Budget'
        filename = os.path.join(project_name, 'history.csv')
        response = self.repository.load_history(filename)
        data = [Transaction.from_dict(item.to_dict()) for item in response]
        self.history.items = {item.reference: item for item in data}
        result = InteractorResultDto(success=True, operation=operation, data=f'History loaded from {filename} with {len(data)} transactions')
        self.presenter.present_success(result)