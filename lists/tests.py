from django.test import TestCase
from .views import home_page
from .models import Item, List
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


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retriving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) item list'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) item list')
        self.assertEqual(second_saved_item.text, 'The second item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.list, list_)

    def test_only_saves_when_is_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)


class ListViewTests(TestCase):

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item1', list=list_)
        Item.objects.create(text='Item2', list=list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'Item1')
        self.assertContains(response, 'Item2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        #self.assertIn('A new list item', response.content.decode())
        #self.assertTemplateUsed(response, 'index.html')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')