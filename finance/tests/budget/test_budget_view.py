from io import StringIO
import unittest
from unittest.mock import patch

from infrastructure.view import CmdBudgetView
from interface.view import BudgetErrorViewModel, BudgetItemViewModel, TableViewModel


class TestBudgetItem(unittest.TestCase):

    def setUp(self) -> None:
        self.view = CmdBudgetView()

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_item(self, mock_stdout) -> None:
        command = 'Show Item'
        identifier = 'identifier'
        name = 'name'
        amount = '3.90'
        category = 'category'
        note = 'note'
        item = BudgetItemViewModel(identifier, name, amount, category, note)
        expected_output = f'{command}\n\tidentifier: {identifier}\n\tname: {name}\n\tamount: {amount}\n\tcategory: {category}\n\tnote: {note}\n\n'

        self.view.show_item(command, item)
        output = mock_stdout.getvalue()
        self.assertEqual(expected_output, output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_list(self, mock_stdout) -> None:
        command = 'Show List'
        data = [
            ('identifier1', 'name1', '1.00', 'category1', 'note1'),
            ('identifier2', 'name2', '2.00', 'category2', 'note2'),
        ]
        item1 = BudgetItemViewModel(*data[0])
        item2 = BudgetItemViewModel(*data[1])

        self.view.show_list(command, [item1, item2])
        output = mock_stdout.getvalue().split('\n')
        self.assertEqual(command, output[0])
        for field in item1.to_dict().keys():
            self.assertIn(field, output[2])
        for value in data[0]:
            self.assertIn(value, output[4])
        for value in data[1]:
            self.assertIn(value, output[5])

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_table(self, mock_stdout) -> None:
        command = 'Show Table'
        fields = ['f1', 'f2']
        r1 = ['v1', 'v2']
        r2 = ['a3', 'a4']
        r3 = ['c5', 'c6']
        table = TableViewModel(fields, [r1, r2, r3])
        
        self.view.show_table(command, table)

        output = mock_stdout.getvalue().split('\n')
        self.assertEqual(command, output[0])
        for field in fields:
            self.assertIn(field, output[2])
        for value in r1:
            self.assertIn(value, output[4])
        for value in r2:
            self.assertIn(value, output[5])
        for value in r3:
            self.assertIn(value, output[6])

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_failure(self, mock_stdout) -> None:
        command = 'command'
        message = 'message'
        error = BudgetErrorViewModel(command, message)
        expected_output = f'{command}\n\t{message}\n\n'

        self.view.show_failure(error)
        output = mock_stdout.getvalue()
        self.assertEqual(expected_output, output)


if __name__ == '__main__':
    unittest.main()
