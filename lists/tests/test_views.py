from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape

from lists.models import List, Item
from lists.views import home_page

from lists.forms import ItemForm
from lists.forms import EMPTY_ITEM_ERROR

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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_POST_redirect_to_list_view(self):
        incorrect_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text': 'A new item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_render_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'not_existing.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class NewListTest(TestCase):

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_items_are_not_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.client.post('/lists/new', data={'text': ''})
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)



