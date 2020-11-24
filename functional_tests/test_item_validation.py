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
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        self.add_todo('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        self.wait_for(lambda: self.check_for_row_in_table('1: Buy milk'))
        self.wait_for(lambda: self.check_for_row_in_table('2: Make tea'))
