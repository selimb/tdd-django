from django.test import TestCase

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


class TestItemForm(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={"text": ""})
        self.assertEqual(form.errors, {"text": [EMPTY_ITEM_ERROR]})

    def test_form_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={"text": "do me"})
        new_item = form.save(for_list=list_)
        self.assertEqual((new_item.text, new_item.list), ("do me", list_))
        self.assertEqual(list(Item.objects.all()), [new_item])
