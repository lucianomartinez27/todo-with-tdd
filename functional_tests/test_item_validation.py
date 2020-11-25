from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_can_not_add_empty_items(self):
        self.browser.get(self.live_server_url)
        self.add_todo('')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'))

        self.add_todo('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.add_todo('') # blank to-do
        self.wait_for(lambda: self.check_for_row_in_table('1: Buy milk'))
        self.add_todo('')  # blank to-do
        self.wait_for(lambda: self.check_for_row_in_table('1: Buy milk'))
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        self.add_todo('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        self.wait_for(lambda: self.check_for_row_in_table('1: Buy milk'))
        self.wait_for(lambda: self.check_for_row_in_table('2: Make tea'))

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.add_todo('Buy wellies')
        self.wait_for(lambda: self.check_for_row_in_table('1: Buy wellies'))

        # Adding a duplicated item
        self.add_todo('Buy wellies')
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector(
            '.has-error').text, "You've already got this in your list"))
