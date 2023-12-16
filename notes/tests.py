from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note, Category, Notification
from django.utils.text import slugify
from django.utils.translation import activate

# Create your tests here.
class NotesListViewTest(TestCase):
    """
    Tests NoteListView from views.py.
    """
    def setUp(self):
        """ Creating and loging in test user. """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_notes_list_view(self):
        """ Creating test objects and testing the view. """
        category = Category.objects.create(name='Test Category', name_pl='Test Category', slug='test-category')
        note = Note.objects.create(title='Test Note', user=self.user, note_text='Test', members=[self.user], category=category)
        Notification.objects.create(user=self.user, is_read=False, note=note)

        response = self.client.get(reverse('show_notes'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('notes' in response.context)
        self.assertTrue('unread_notifications' in response.context)
        self.assertTrue('categories' in response.context)
        unread_notifications = response.context['unread_notifications']
        self.assertEqual(unread_notifications, 1)
        self.assertTemplateUsed(response, 'notes/show_notes.html')


class CategoryModelTest(TestCase):
    """
    Tests Category model from models.py.
    """
    def setUp(self):
        """ Creating test category. """
        self.category = Category.objects.create(name='Test Category', name_pl='Testowa Kategoria')

    def test_str_method_english(self):
        """ Tests english str method. """
        activate('en')
        self.assertEqual(str(self.category), 'Test Category')

    def test_str_method_polish(self):
        """ Test polish str method. """
        activate('pl')
        self.assertEqual(str(self.category), 'Testowa Kategoria')

    def test_slug_generation(self):
        """ Tests if slug generation is correct. """
        self.assertEqual(self.category.slug, slugify(self.category.name))

    def test_save_method(self):
        """ Tests save() method. """
        new_category = Category(name='New Test Category')
        new_category.save()
        self.assertEqual(new_category.slug, slugify(new_category.name))
        self.assertEqual(Category.objects.count(), 2)

    def test_verbose_name_plural(self):
        """ Tests verbose_name_plural from Meta class. """
        self.assertEqual(str(Category._meta.verbose_name_plural), 'Categories')
