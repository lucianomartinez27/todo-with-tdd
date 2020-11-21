from selenium import webdriver

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        self.add_todo('Buy a peacock feathers')
        self.wait_for(lambda: self.check_for_row_in_table('1: Buy a peacock feathers'))
        self.add_todo('Buy a new brain')
        self.wait_for(lambda: self.check_for_row_in_table('2: Buy a new brain'))

    def test_multiple_users_can_start_a_list_at_differents_urls(self):
        self.browser.get(self.live_server_url)
        self.add_todo('Buy peacock feathers')
        self.wait_for(lambda: self.check_for_row_in_table('1: Buy peacock feathers'))
        user_url = self.browser.current_url
        self.assertRegex(user_url, '/lists/.+')

        # New user checking his website
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # There are his To-Do's?
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)


        # New user start a new list
        self.add_todo('Buy milk')

        self.wait_for(lambda: self.check_for_row_in_table('2: Buy milk'))

        # User get his own url
        new_user_url = self.browser.current_url
        self.assertRegex(new_user_url, '/lists/.+')
        self.assertNotEqual(user_url, new_user_url)

        # Checking the list again
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)