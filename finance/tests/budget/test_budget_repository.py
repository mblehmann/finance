import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from finance.application.dto import BudgetItemDto
from finance.infrastructure.repository import CsvBudgetRepository


class TestBudgetItem(unittest.TestCase):

    def setUp(self) -> None:
        self.repository = CsvBudgetRepository()

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.writer")
    def test_save_budget(self, mock_csv_writer, mock_file) -> None:
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer

        filename = 'budget.csv'
        item1 = BudgetItemDto('identifier1', 'name1', '1.00', 'category1', 'note1')
        item2 = BudgetItemDto('identifier2', 'name2', '2.00', 'category2', 'note2')
        expected_calls = [
            call(list(item1.to_dict().values())),
            call(list(item2.to_dict().values()))
        ]

        self.repository.save_budget(filename, [item1, item2])

        mock_file.assert_called_once_with(filename, 'w', newline='')
        self.assertEqual(mock_writer.writerow.call_count, 2)
        self.assertEqual(mock_writer.writerow.call_args_list, expected_calls)

    @patch("builtins.open", new_callable=mock_open, read_data="identifier1,name1,1.00,category1,note1\nidentifier2,name2,2.00,category2,note2\n")
    def test_load_budget(self, mock_file) -> None:
        filename = 'budget.csv'
        items = self.repository.load_budget(filename)

        mock_file.assert_called_once_with(filename, 'r')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].identifier, 'identifier1')
        self.assertEqual(items[0].name, 'name1')
        self.assertEqual(items[0].amount, '1.00')
        self.assertEqual(items[0].category, 'category1')
        self.assertEqual(items[0].note, 'note1')

        self.assertEqual(items[1].identifier, 'identifier2')
        self.assertEqual(items[1].name, 'name2')
        self.assertEqual(items[1].amount, '2.00')
        self.assertEqual(items[1].category, 'category2')
        self.assertEqual(items[1].note, 'note2')


if __name__ == '__main__':
    unittest.main()
