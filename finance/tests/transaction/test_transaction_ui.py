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


if __name__ == '__main__':
    unittest.main()