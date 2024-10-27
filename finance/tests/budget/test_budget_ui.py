import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from infrastructure.ui import BudgetCmd
from interface.controller import BudgetControllerInterface


class TestBudgetCmd(unittest.TestCase):

    def setUp(self):
        self.mock_controller = Mock(spec=BudgetControllerInterface)
        self.ui = BudgetCmd(self.mock_controller)

    def test_prompt(self):
        self.assertEqual('budget> ', self.ui.prompt)

    def test_add_success(self):
        name = 'name'
        amount = 3.14
        category = 'category'
        note = 'note'
        args = f'{name} {amount} {category} {note}'

        self.ui.do_add(args)

        self.mock_controller.add_budget_item.assert_called_once_with(name, amount, category, note)

    def test_add_more_than_four_parameters_success(self):
        name = 'name'
        amount = 3.14
        category = 'category'
        note = 'longer note than one word'
        args = f'{name} {amount} {category} {note}'

        self.ui.do_add(args)

        self.mock_controller.add_budget_item.assert_called_once_with(name, amount, category, note)

    @patch.object(BudgetCmd, 'do_help')
    def test_add_less_than_four_parameters_fails(self, mock_do_help):
        name = 'name'
        amount = 3.14
        category = 'category'
        note = ''
        args = f'{name} {amount} {category} {note}'

        self.ui.do_add(args)

        mock_do_help.assert_called_once_with('add')

    @patch('builtins.print')
    def test_add_amount_invalid_fails(self, mock_print):
        name = 'name'
        amount = '3,14'
        category = 'category'
        note = 'note'
        args = f'{name} {amount} {category} {note}'

        self.ui.do_add(args)

        mock_print.assert_called_once_with('The amount should be a number. could not convert string to float: \'3,14\'')

    def test_update_success(self):
        identifier = uuid4()
        name = 'name'
        amount = 3.14
        category = 'category'
        note = 'note'
        args = f'{identifier} {name} {amount} {category} {note}'
        fields = {'name': name, 'amount': amount, 'category': category, 'note': note}

        self.ui.do_update(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    def test_update_more_than_five_parameters_success(self):
        identifier = uuid4()
        name = 'name'
        amount = 3.14
        category = 'category'
        note = 'longer note than one word'
        args = f'{identifier} {name} {amount} {category} {note}'
        fields = {'name': name, 'amount': amount, 'category': category, 'note': note}

        self.ui.do_update(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    @patch.object(BudgetCmd, 'do_help')
    def test_update_less_than_five_parameters_fails(self, mock_do_help):
        identifier = uuid4()
        name = 'name'
        amount = 3.14
        category = 'category'
        note = ''
        args = f'{identifier} {name} {amount} {category} {note}'

        self.ui.do_update(args)

        mock_do_help.assert_called_once_with('update')

    @patch('builtins.print')
    def test_update_identifier_invalid_fails(self, mock_print):
        identifier = 'identifier'
        name = 'name'
        amount = 3.14
        category = 'category'
        note = 'note'
        args = f'{identifier} {name} {amount} {category} {note}'

        self.ui.do_update(args)

        mock_print.assert_called_once_with('The identifier should be a valid UUID. badly formed hexadecimal UUID string: "identifier"')

    @patch('builtins.print')
    def test_update_amount_invalid_fails(self, mock_print):
        identifier = uuid4()
        name = 'name'
        amount = '3.14a'
        category = 'category'
        note = 'note'
        args = f'{identifier} {name} {amount} {category} {note}'

        self.ui.do_update(args)

        mock_print.assert_called_once_with('The amount should be a number. could not convert string to float: \'3.14a\'')

    def test_update_name_success(self):
        identifier = uuid4()
        name = 'name'
        args = f'{identifier} {name}'
        fields = {'name': name}

        self.ui.do_update_name(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    def test_update_name_more_than_two_parameters_success(self):
        identifier = uuid4()
        name = 'name'
        trailer = 'and other words'
        args = f'{identifier} {name} {trailer}'
        fields = {'name': name}

        self.ui.do_update_name(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    @patch.object(BudgetCmd, 'do_help')
    def test_update_name_less_than_two_parameters_fails(self, mock_do_help):
        identifier = uuid4()
        name = ''
        args = f'{identifier} {name}'

        self.ui.do_update_name(args)

        mock_do_help.assert_called_once_with('update_name')

    @patch('builtins.print')
    def test_update_name_identifier_invalid_fails(self, mock_print):
        identifier = 'identifier'
        name = 'name'
        args = f'{identifier} {name}'

        self.ui.do_update_name(args)

        mock_print.assert_called_once_with('The identifier should be a valid UUID. badly formed hexadecimal UUID string: "identifier"')

    def test_update_amount_success(self):
        identifier = uuid4()
        amount = 10.08
        args = f'{identifier} {amount}'
        fields = {'amount': amount}

        self.ui.do_update_amount(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    def test_update_amount_more_than_two_parameters_success(self):
        identifier = uuid4()
        amount = 10.08
        trailer = 'and other words'
        args = f'{identifier} {amount} {trailer}'
        fields = {'amount': amount}

        self.ui.do_update_amount(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    @patch.object(BudgetCmd, 'do_help')
    def test_update_amount_less_than_two_parameters_fails(self, mock_do_help):
        identifier = uuid4()
        amount = ''
        args = f'{identifier} {amount}'

        self.ui.do_update_amount(args)

        mock_do_help.assert_called_once_with('update_amount')

    @patch('builtins.print')
    def test_update_amount_identifier_invalid_fails(self, mock_print):
        identifier = uuid4()
        amount = '3.14.23'
        args = f'{identifier} {amount}'

        self.ui.do_update_amount(args)

        mock_print.assert_called_once_with('The amount should be a number. could not convert string to float: \'3.14.23\'')

    @patch('builtins.print')
    def test_update_amount_amount_invalid_fails(self, mock_print):
        identifier = 'identifier'
        amount = 3.14
        args = f'{identifier} {amount}'

        self.ui.do_update_amount(args)

        mock_print.assert_called_once_with('The identifier should be a valid UUID. badly formed hexadecimal UUID string: "identifier"')

    def test_update_category_success(self):
        identifier = uuid4()
        category = 'category'
        args = f'{identifier} {category}'
        fields = {'category': category}

        self.ui.do_update_category(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    def test_update_category_more_than_two_parameters_success(self):
        identifier = uuid4()
        category = 'category'
        trailer = 'and other words'
        args = f'{identifier} {category} {trailer}'
        fields = {'category': category}

        self.ui.do_update_category(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    @patch.object(BudgetCmd, 'do_help')
    def test_update_category_less_than_two_parameters_fails(self, mock_do_help):
        identifier = uuid4()
        category = ''
        args = f'{identifier} {category}'

        self.ui.do_update_category(args)

        mock_do_help.assert_called_once_with('update_category')

    @patch('builtins.print')
    def test_update_category_identifier_invalid_fails(self, mock_print):
        identifier = 'identifier'
        category = 'category'
        args = f'{identifier} {category}'

        self.ui.do_update_category(args)

        mock_print.assert_called_once_with('The identifier should be a valid UUID. badly formed hexadecimal UUID string: "identifier"')

    def test_update_note_success(self):
        identifier = uuid4()
        note = 'note'
        args = f'{identifier} {note}'
        fields = {'note': note}

        self.ui.do_update_note(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    def test_update_note_more_than_two_parameters_success(self):
        identifier = uuid4()
        note = 'note'
        trailer = 'and other words'
        args = f'{identifier} {note} {trailer}'
        fields = {'note': f'{note} {trailer}'}

        self.ui.do_update_note(args)

        self.mock_controller.update_budget_item.assert_called_once_with(identifier, **fields)

    @patch.object(BudgetCmd, 'do_help')
    def test_update_note_less_than_two_parameters_fails(self, mock_do_help):
        identifier = uuid4()
        note = ''
        args = f'{identifier} {note}'

        self.ui.do_update_note(args)

        mock_do_help.assert_called_once_with('update_note')

    @patch('builtins.print')
    def test_update_note_identifier_invalid_fails(self, mock_print):
        identifier = 'identifier'
        note = 'note'
        args = f'{identifier} {note}'

        self.ui.do_update_note(args)

        mock_print.assert_called_once_with('The identifier should be a valid UUID. badly formed hexadecimal UUID string: "identifier"')

    def test_get_success(self):
        category = 'category'
        args = f'{category}'

        self.ui.do_get(args)

        self.mock_controller.get_budget_items.assert_called_once_with(category)

    def test_get_more_than_one_parameter_success(self):
        category = 'category'
        trailer = 'and other words'
        args = f'{category} {trailer}'

        self.ui.do_get(args)

        self.mock_controller.get_budget_items.assert_called_once_with(category)

    @patch.object(BudgetCmd, 'do_help')
    def test_get_less_than_one_parameter_fails(self, mock_do_help):
        category = ''
        args = f'{category}'

        self.ui.do_get(args)

        mock_do_help.assert_called_once_with('get')

    def test_delete_success(self):
        identifier = uuid4()
        args = f'{identifier}'

        self.ui.do_delete(args)

        self.mock_controller.delete_budget_item.assert_called_once_with(identifier)

    def test_delete_more_than_one_parameter_success(self):
        identifier = uuid4()
        trailer = 'and other words'
        args = f'{identifier} {trailer}'

        self.ui.do_delete(args)

        self.mock_controller.delete_budget_item.assert_called_once_with(identifier)

    @patch.object(BudgetCmd, 'do_help')
    def test_delete_less_than_one_parameter_fails(self, mock_do_help):
        identifier = ''
        args = f'{identifier}'

        self.ui.do_delete(args)

        mock_do_help.assert_called_once_with('delete')

    @patch('builtins.print')
    def test_delete_identifier_invalid_fails(self, mock_print):
        identifier = 'identifier'
        args = f'{identifier}'

        self.ui.do_delete(args)

        mock_print.assert_called_once_with('The identifier should be a valid UUID. badly formed hexadecimal UUID string: "identifier"')

    def test_list_success(self):
        args = ''

        self.ui.do_list(args)

        self.mock_controller.list_budget_items.assert_called_once_with()

    def test_list_with_parameters_success(self):
        args = 'args'

        self.ui.do_list(args)

        self.mock_controller.list_budget_items.assert_called_once_with()

    def test_show_overview_success(self):
        args = ''

        self.ui.do_show_overview(args)

        self.mock_controller.show_budget_overview.assert_called_once_with()

    def test_show_overview_with_parameters_success(self):
        args = 'args'

        self.ui.do_show_overview(args)

        self.mock_controller.show_budget_overview.assert_called_once_with()

    def test_show_distribution_success(self):
        args = ''

        self.ui.do_show_distribution(args)

        self.mock_controller.show_budget_distribution.assert_called_once_with()

    def test_show_distribution_with_parameters_success(self):
        args = 'args'

        self.ui.do_show_distribution(args)

        self.mock_controller.show_budget_distribution.assert_called_once_with()

    @patch('os.makedirs')
    def test_save_success(self, mock_os_makedirs):
        project_name = 'project'
        args = f'{project_name}'

        self.ui.do_save(args)

        mock_os_makedirs.assert_called_once_with(project_name, exist_ok=True)
        self.mock_controller.save_budget.assert_called_once_with(project_name)

    @patch('os.makedirs')
    def test_save_more_than_one_parameter_success(self, mock_os_makedirs):
        project_name = 'project'
        trailer = 'and other words'
        args = f'{project_name} {trailer}'

        self.ui.do_save(args)

        mock_os_makedirs.assert_called_once_with(project_name, exist_ok=True)
        self.mock_controller.save_budget.assert_called_once_with(project_name)

    @patch('os.makedirs')
    @patch.object(BudgetCmd, 'do_help')
    def test_save_less_than_one_parameter_fails(self, mock_do_help, mock_os_makedirs):
        project_name = ''
        args = f'{project_name}'

        self.ui.do_save(args)

        mock_os_makedirs.assert_not_called()
        mock_do_help.assert_called_once_with('save')

    def test_load_success(self):
        project_name = 'project'
        args = f'{project_name}'

        self.ui.do_load(args)

        self.mock_controller.load_budget.assert_called_once_with(project_name)

    def test_load_more_than_one_parameter_success(self):
        project_name = 'project'
        trailer = 'and other words'
        args = f'{project_name} {trailer}'

        self.ui.do_load(args)

        self.mock_controller.load_budget.assert_called_once_with(project_name)

    @patch.object(BudgetCmd, 'do_help')
    def test_load_less_than_one_parameter_fails(self, mock_do_help):
        project_name = ''
        args = f'{project_name}'

        self.ui.do_load(args)

        mock_do_help.assert_called_once_with('load')
    
    def test_quit_success(self):
        args = ''

        self.assertEqual(True, self.ui.do_quit(args))

    def test_quit_with_parameters_success(self):
        args = 'args'

        self.assertEqual(True, self.ui.do_quit(args))


if __name__ == '__main__':
    unittest.main()