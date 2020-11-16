from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase

class VisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # I open to the browser and go to my TO-DO website
        self.browser.get(self.live_server_url)
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def add_todo(self, todo_to_add):
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(todo_to_add)
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)

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

    def test_todo_can_be_added_correctly(self):
        self.add_todo('Buy a peacock feathers')
        self.check_for_row_in_list_table('1: Buy a peacock feathers')
        self.add_todo('Buy a new brain')
        self.check_for_row_in_list_table('2: Buy a new brain')
