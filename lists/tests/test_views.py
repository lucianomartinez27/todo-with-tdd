from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape

from lists.models import List, Item
from lists.views import home_page


class ListViewTests(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_only_the_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item1', list=correct_list)
        Item.objects.create(text='Item2', list=correct_list)

        incorrect_list = List.objects.create()
        Item.objects.create(text='Another Item1', list=incorrect_list)
        Item.objects.create(text='Another Item2', list=incorrect_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'Item1')
        self.assertContains(response, 'Item2')
        self.assertNotContains(response, 'Another Item1')
        self.assertNotContains(response, 'Another Item2')


        response = self.client.get(f'/lists/{incorrect_list.id}/')

        self.assertContains(response, 'Item1')
        self.assertContains(response, 'Item2')

    def test_passes_correct_list_to_template(self):
        incorrect_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        #self.assertIn('A new list item', response.content.decode())
        #self.assertTemplateUsed(response, 'index.html')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')



    def test_can_save_a_POST_request_to_an_existing_list(self):
        incorrect_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'New To-Do'})

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'New To-Do')
        self.assertEqual(item.list, correct_list)
        self.assertNotEqual(item.list, incorrect_list)

    def test_redirect_to_list_view(self):
        incorrect_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'New To-Do'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')


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
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'not_existing.html')


class NewListTest(TestCase):

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        expected_error = escape("You can't have an empty list")
        self.assertContains(response, expected_error)

    def test_invalid_items_are_not_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)



