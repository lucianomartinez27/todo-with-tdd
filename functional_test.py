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
        self.browser.get("http://localhost:8000")

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        input_box.send_keys('Buy a peacock feathers')

        input_box.send_keys((Keys.ENTER))
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )
        self.fail('Test finished is not')
        #[.. rest of comment as before]


if __name__ == '__main__':
    unittest.main(warnings='ignore')