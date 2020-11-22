from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


# Create your tests here.


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
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

    def test_can_not_save_an_empty_item(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()