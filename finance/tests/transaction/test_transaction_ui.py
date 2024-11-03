import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from finance.infrastructure.ui import HistoryCmd
from finance.interface.controller import HistoryControllerInterface


class TestHistoryCmd(unittest.TestCase):

    def setUp(self):
        self.mock_controller = Mock(spec=HistoryControllerInterface)
        self.ui = HistoryCmd(self.mock_controller)

    def test_prompt(self):
        self.assertEqual('history> ', self.ui.prompt)

    def test_import_success(self):
        filename = 'filename'
        args = f'{filename}'

        self.ui.do_import(args)

        self.mock_controller.import_transactions.assert_called_once_with(filename)

    def test_import_more_than_one_parameter_success(self):
        filename = 'filename'
        trailer = 'and more words'
        args = f'{filename} {trailer}'

        self.ui.do_import(args)

        self.mock_controller.import_transactions.assert_called_once_with(filename)

    @patch.object(HistoryCmd, 'do_help')
    def test_import_less_than_one_parameter_fails(self, mock_do_help):
        filename = ''
        args = f'{filename}'

        self.ui.do_import(args)

        mock_do_help.assert_called_once_with('import')

    def test_update_success(self):
        reference = 'reference'
        category = 'category'
        month = 8
        tag = 'tag'
        comments = 'comments'
        args = f'{reference} {category} {month} {tag} {comments}'
        fields = {'category': category, 'month': month, 'tag': tag, 'comments': comments}

        self.ui.do_update(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    def test_update_more_than_five_parameters_success(self):
        reference = 'reference'
        category = 'category'
        month = 8
        tag = 'tag'
        comments = 'comments more than one word'
        args = f'{reference} {category} {month} {tag} {comments}'
        fields = {'category': category, 'month': month, 'tag': tag, 'comments': comments}

        self.ui.do_update(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    @patch.object(HistoryCmd, 'do_help')
    def test_update_less_than_five_parameters_fails(self, mock_do_help):
        reference = 'reference'
        category = 'category'
        month = 8
        tag = 'tag'
        comments = ''
        args = f'{reference} {category} {month} {tag} {comments}'

        self.ui.do_update(args)

        mock_do_help.assert_called_once_with('update')

    @patch('builtins.print')
    def test_update_month_invalid_fails(self, mock_print):
        reference = 'reference'
        category = 'category'
        month = 'august'
        tag = 'tag'
        comments = 'comments'
        args = f'{reference} {category} {month} {tag} {comments}'

        self.ui.do_update(args)

        mock_print.assert_called_once_with('The month should be a number. invalid literal for int() with base 10: \'august\'')


if __name__ == '__main__':
    unittest.main()