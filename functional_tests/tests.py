from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class VisitorTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()
        # I open to the browser and go to my TO-DO website
        self.browser.get(self.live_server_url)
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > self.MAX_WAIT:
                    raise error
                time.sleep(0.5)

    def add_todo(self, todo_to_add):
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(todo_to_add)
        input_box.send_keys(Keys.ENTER)

    def test_the_input_box_is_showed_correctly(self):
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

    def test_the_title_is_the_corresponding(self):
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

    def test_can_start_a_list_for_one_user(self):
        self.add_todo('Buy a peacock feathers')
        self.check_for_row_in_list_table('1: Buy a peacock feathers')
        self.add_todo('Buy a new brain')
        self.check_for_row_in_list_table('2: Buy a new brain')

    def test_multiple_users_can_start_a_list_at_differents_urls(self):
        self.browser.get(self.live_server_url)
        self.add_todo('Buy peacock feathers')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
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
        self.check_for_row_in_list_table('1: Buy milk')

        # User get his own url
        new_user_url = self.browser.current_url
        self.assertRegex(new_user_url, '/lists/.+')
        self.assertNotEqual(user_url, new_user_url)

        # Checking the list again
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        self.client.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x']+input_box.size['width'] / 2, 512, delta=10)

        # checking position after post
        self.add_todo('testing')
        self.check_for_row_in_list_table('1: testing')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x']+input_box.size['width'] / 2, 512, delta=10)
