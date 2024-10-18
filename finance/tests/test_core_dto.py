# import unittest

# from finance.application.dto import InteractorResultDto


# class TestInteractorResultDto(unittest.TestCase):

#     def test_creation_success(self):
#         result = InteractorResultDto(success=True, operation='operation', data="data")
#         self.assertTrue(result.success)
#         self.assertEqual(result.operation, 'operation')
#         self.assertEqual(result.data, "data")
#         self.assertIsNone(result.error)

#     def test_creation_failure(self):
#         result = InteractorResultDto(success=False, operation='operation', error="error")
#         self.assertFalse(result.success)
#         self.assertEqual(result.operation, 'operation')
#         self.assertIsNone(result.data)
#         self.assertEqual(result.error, "error")

#     def test_creation_with_optional_data_and_error(self):
#         result = InteractorResultDto(success=True, operation='operation')
#         self.assertTrue(result.success)
#         self.assertEqual(result.operation, 'operation')
#         self.assertIsNone(result.data)
#         self.assertIsNone(result.error)

#     def test_creation_with_all_optional_data(self):
#         result = InteractorResultDto(success=True, operation='operation', data="data", error="error")
#         self.assertTrue(result.success)
#         self.assertEqual(result.operation, 'operation')
#         self.assertEqual(result.data, "data")
#         self.assertEqual(result.error, "error")


# if __name__ == '__main__':
#     unittest.main()
