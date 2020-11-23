from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os


class FunctionalTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'https://' + staging_server
        # I open to the browser and go to my TO-DO website
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        return

    def wait_for(self, function):
        start_time = time.time()
        while True:
            try:
                return function()
            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > self.MAX_WAIT:
                    raise error
                time.sleep(0.5)

    def add_todo(self, todo_to_add):
        self.get_item_input_box().send_keys(todo_to_add+Keys.ENTER)

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')


