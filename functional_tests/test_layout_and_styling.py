from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.client.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x']+input_box.size['width'] / 2, 512, delta=10)

        # checking position after post
        self.add_todo('testing')
        self.wait_for(lambda: self.check_for_row_in_table('1: testing'))
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x']+input_box.size['width'] / 2, 512, delta=10)

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