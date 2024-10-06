import unittest
import csv
import os
from tempfile import NamedTemporaryFile
from uuid import uuid4
from infrastructure.repository import CsvBudgetRepository

class TestBudgetCsvRepository(unittest.TestCase):
    def setUp(self):
        self.repository = CsvBudgetRepository()

    def test_save_budget(self):
         with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            filename = temp_file.name
            identifier1 = str(uuid4())
            identifier2 = str(uuid4())
            budget = [
                {"identifier": identifier1, "name": "Test", "amount": "100.0", "category": "Savings", "note": "Test Note"},
                {"identifier": identifier2, "name": "Test", "amount": "200.0", "category": "Wants", "note": "Test Note"}
            ]
            # Call the method
            self.repository.save_budget(filename, budget)
            # Assert that the file was written correctly
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                written_data = list(reader)
                expected_data = [[identifier1, "Test", "100.0", "Savings", "Test Note"],
                                 [identifier2, "Test", "200.0", "Wants", "Test Note"]]
                self.assertEqual(written_data, expected_data)

            # Clean up temporary file
            os.unlink(filename) 

    def test_load_budget(self):
        with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            filename = temp_file.name
            identifier1 = str(uuid4())
            identifier2 = str(uuid4())
            budget_data = [
                [identifier1, "Test", "100.0", "Savings", "Test Note"],
                [identifier2, "Test", "200.0", "Wants", "Test Note"]
            ]
            writer = csv.writer(temp_file)
            writer.writerows(budget_data)

        try:
            # Call the method
            result = self.repository.load_budget(filename)
            # Assert that the result matches the expected data
            expected_budget = [
                {"identifier": identifier1, "name": "Test", "amount": "100.0", "category": "Savings", "note": "Test Note"},
                {"identifier": identifier2, "name": "Test", "amount": "200.0", "category": "Wants", "note": "Test Note"}
            ]
            self.assertEqual(result, expected_budget)
        finally:
            # Clean up temporary file
            os.unlink(filename)


if __name__ == '__main__':
    unittest.main()
