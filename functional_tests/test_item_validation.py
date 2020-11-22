from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_can_not_add_empty_items(self):
        self.browser.get(self.live_server_url)
        self.add_todo('')
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_class_name('has-error').text, 'You can\'t have an empty list'))

        self.add_todo('Buy milk')
        self.wait_for(lambda: self.check_for_row_in_table('1: Buy milk'))
        self.add_todo('')
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_class_name('has-error').text, 'You can\'t have an empty list item'))
        self.add_todo('Buy another thing')
        self.wait_for(lambda : self.check_for_row_in_table('1: Buy milk'))
        self.wait_for(lambda : self.check_for_row_in_table('2: Buy another thing'))
