from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from lists.models import Item
from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_uses_home_template(self):
    	response = self.client.get('/')
    	self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):

	def test_can_save_a_post_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')


	def test_redirects_after_post(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):

		first_item = Item()
		first_item.text = 'The first (ever) listed item'
		first_item.save()

		second_item = Item()
		second_item.text = 'The second item'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) listed item')
		self.assertEqual(second_saved_item.text, 'The second item')


class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'lists.html')

	def test_displays_all_items(self):
		Item.objects.create(text='Item 1')
		Item.objects.create(text='Item 2')

		response = self.client.get('/lists/the-only-list-in-the-world/', follow=True)

		# assertContains decodes the response object and looks at the data thats passed in
		# the bytes to see if the passed argument is inside
		self.assertContains(response, 'Item 1')
		self.assertContains(response, 'Item 2')





