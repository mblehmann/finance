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

    def test_update_category_success(self):
        reference = 'reference'
        category = 'category'
        args = f'{reference} {category}'
        fields = {'category': category}

        self.ui.do_update_category(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    def test_update_category_more_than_two_parameters_success(self):
        reference = 'reference'
        category = 'category'
        trailer = 'and other words'
        args = f'{reference} {category} {trailer}'
        fields = {'category': category}

        self.ui.do_update_category(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    @patch.object(HistoryCmd, 'do_help')
    def test_update_category_less_than_two_parameters_fails(self, mock_do_help):
        reference = 'reference'
        category = ''
        args = f'{reference} {category}'

        self.ui.do_update_category(args)

        mock_do_help.assert_called_once_with('update_category')

    def test_update_month_success(self):
        reference = 'reference'
        month = 8
        args = f'{reference} {month}'
        fields = {'month': month}

        self.ui.do_update_month(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    def test_update_month_more_than_two_parameters_success(self):
        reference = 'reference'
        month = 8
        trailer = 'and other words'
        args = f'{reference} {month} {trailer}'
        fields = {'month': month}

        self.ui.do_update_month(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    @patch.object(HistoryCmd, 'do_help')
    def test_update_month_less_than_two_parameters_fails(self, mock_do_help):
        reference = 'reference'
        month = ''
        args = f'{reference} {month}'

        self.ui.do_update_month(args)

        mock_do_help.assert_called_once_with('update_month')

    @patch('builtins.print')
    def test_update_month_month_invalid_fails(self, mock_print):
        reference = 'reference'
        month = 'august'
        args = f'{reference} {month}'

        self.ui.do_update_month(args)

        mock_print.assert_called_once_with('The month should be a number. invalid literal for int() with base 10: \'august\'')

    def test_update_tag_success(self):
        reference = 'reference'
        tag = 'tag'
        args = f'{reference} {tag}'
        fields = {'tag': tag}

        self.ui.do_update_tag(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    def test_update_tag_more_than_two_parameters_success(self):
        reference = 'reference'
        tag = 'tag'
        trailer = 'and other words'
        args = f'{reference} {tag} {trailer}'
        fields = {'tag': tag}

        self.ui.do_update_tag(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    @patch.object(HistoryCmd, 'do_help')
    def test_update_tag_less_than_two_parameters_fails(self, mock_do_help):
        reference = 'reference'
        tag = ''
        args = f'{reference} {tag}'

        self.ui.do_update_tag(args)

        mock_do_help.assert_called_once_with('update_tag')

    def test_update_comments_success(self):
        reference = 'reference'
        comments = 'comments'
        args = f'{reference} {comments}'
        fields = {'comments': comments}

        self.ui.do_update_comments(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)
    
    def test_update_comments_more_than_two_parameters_success(self):
        reference = 'reference'
        comments = 'comments'
        trailer = 'and other words'
        args = f'{reference} {comments} {trailer}'
        fields = {'comments': f'{comments} {trailer}'}

        self.ui.do_update_comments(args)

        self.mock_controller.update_transaction.assert_called_once_with(reference, **fields)

    @patch.object(HistoryCmd, 'do_help')
    def test_update_comments_less_than_two_parameters_fails(self, mock_do_help):
        reference = 'reference'
        comments = ''
        args = f'{reference} {comments}'

        self.ui.do_update_comments(args)

        mock_do_help.assert_called_once_with('update_comments')

    def test_ignore_success(self):
        reference = 'reference'
        test_cases = [True, False]

        for ignore in test_cases:
            with self.subTest(ignore=ignore):
                self.mock_controller.reset_mock()
                args = f'{reference} {ignore}'

                self.ui.do_ignore(args)

                self.mock_controller.ignore_transaction.assert_called_once_with(reference, ignore)

    def test_ignore_more_than_two_parameters_success(self):
        reference = 'reference'
        ignore = True
        trailer = 'and more words'
        args = f'{reference} {ignore} {trailer}'

        self.ui.do_ignore(args)

        self.mock_controller.ignore_transaction.assert_called_once_with(reference, ignore)

    @patch.object(HistoryCmd, 'do_help')
    def test_ignore_less_than_two_parameters_fails(self, mock_do_help):
        reference = 'reference'
        ignore = ''
        args = f'{reference} {ignore}'

        self.ui.do_ignore(args)

        mock_do_help.assert_called_once_with('ignore')

    @patch('builtins.print')
    def test_ignore_parameter_invalid_fails(self, mock_print):
        reference = 'reference'
        ignore = 34
        args = f'{reference} {ignore}'

        self.ui.do_ignore(args)

        mock_print.assert_called_once_with('Ignore paramater should be True or False: \'34\'')
    
    def test_list_success(self):
        month = 8
        args = f'{month}'

        self.ui.do_list(args)

        self.mock_controller.list_transactions.assert_called_once_with(month)

    def test_list_more_than_one_parameter_success(self):
        month = 8
        trailer = 'and more words'
        args = f'{month} {trailer}'

        self.ui.do_list(args)

        self.mock_controller.list_transactions.assert_called_once_with(month)

    @patch.object(HistoryCmd, 'do_help')
    def test_list_less_than_one_parameter_fails(self, mock_do_help):
        month = ''
        args = f'{month}'

        self.ui.do_list(args)

        mock_do_help.assert_called_once_with('list')

    @patch('builtins.print')
    def test_list_month_invalid_fails(self, mock_print):
        month = 'august'
        args = f'{month}'

        self.ui.do_list(args)

        mock_print.assert_called_once_with('The month should be a number. invalid literal for int() with base 10: \'august\'')


if __name__ == '__main__':
    unittest.main()