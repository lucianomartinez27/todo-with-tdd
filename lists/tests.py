from django.test import TestCase
from .views import home_page
from .models import Item
from django.urls import resolve
# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateNotUsed(response, 'not_existing.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        #self.assertIn('A new list item', response.content.decode())
        #self.assertTemplateUsed(response, 'index.html')
    def test_redirect_after_post(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_mutiples_items_can_be_displayed(self):
        Item.objects.create(text="Item1")
        Item.objects.create(text="Item2")

        response = self.client.get('/')

        self.assertIn("Item1", response.content.decode())
        self.assertIn("Item2", response.content.decode())

class ModelItemTest(TestCase):
    def test_saving_and_retriving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) item list'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) item list')
        self.assertEqual(second_saved_item.text, 'The second item')

    def test_only_saves_when_is_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)
