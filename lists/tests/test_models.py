from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


# Create your tests here.

class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

class ItemModelsTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()

        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_only_saves_when_is_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_can_not_save_an_empty_item(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='some text', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text='some text', list=list_)
            #item.full_clean()
            item.save()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='some text')
        item2 = Item(list=list2, text='some text')
        item2.full_clean() # should not raise
        self.assertEqual(item1.text, item2.text)

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')