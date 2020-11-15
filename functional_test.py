from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class VisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # I open to the browser and go to my TO-DO website
        self.browser.get("http://localhost:8000")

        # I check if the web si correct checking the Titles
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)
        # Im searching for an input label
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # ...and insert my First TO-DO
        input_box.send_keys('Buy a peacock feathers')
        input_box.send_keys(Keys.ENTER)
        time.sleep(2)
        # i want add a one more TO-DO
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy a new brain')
        input_box.send_keys(Keys.ENTER)
        time.sleep(2)
        # checking if the TO-DOs were correcly added
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy a peacock feathers', [row.text for row in rows])
        self.assertIn('2: Buy a new brain', [row.text for row in rows])

        self.fail('Test finished is not')
        #[.. rest of comment as before]


if __name__ == '__main__':
    unittest.main(warnings='ignore')