class BudgetItemExistsException(Exception):
    pass


class BudgetItemNotFoundException(Exception):
    pass


class BudgetCategoryNotFoundException(Exception):
    pass


class TransactionExistsException(Exception):
    pass


class TransactionNotFoundException(Exception):
    pass


class TransactionUpdateException(Exception):
    pass
