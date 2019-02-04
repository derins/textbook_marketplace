import datetime
from users.forms import *
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.test.client import Client
from users.models import CustomUser
from .models import Book

class TestUserModel(TestCase):
    def setUp(self):
        CustomUser.objects.create(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        CustomUser.objects.create(username= 'jh2ab', password = 'dhfj456k', email = 'jh2ab@virginia.edu',)
    def testStrings(self):
        user1 = CustomUser.objects.get(username = 'bfb3ab')
        user2 = CustomUser.objects.get(username = 'bfb3ab')
        user3 = CustomUser.objects.get(username = 'jh2ab')
        self.assertTrue(user1.__str__() == user2.__str__())
        self.assertFalse(user1.__str__() == user3.__str__())
    def create_user(username, password, email):
        return CustomUser.object.create(username = username, password = password, email = email)

class TestBookModel(TestCase):
    def setUp(self):
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',)
        Book.objects.create(name='The other book',author = 'the other author',price = '2', isbn_number = '2')
    def testString(self):
        book1 = Book.objects.get(name='The book')
        book2 = Book.objects.get(name='The book')
        book3 = Book.objects.get(name='The other book')
        self.assertEqual(book1.__str__(),book2.__str__())
        self.assertFalse(book1.__str__() == book3.__str__())
        self.assertEqual('The book',book1.__str__())
    def create_book(name, author, price, isbn_number, date_posted):
        time = timezone.now() + datetime.timedelta(days=days)
        return Book.objects.create(name = name,author = author,price = price,isbn_number = isbn_number,date_posted= time)

class TestBookListView(TestCase):
#    def testNoBook(self):
#        response = self.client.get(reverse('textbookFinder:index'))
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, "TextBook Finder")
    def testBook1(self):
        book1 = Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',)
        response = self.client.get(reverse('textbookFinder:index'))
        self.assertContains(response, 'The book')
    def test2Books(self):
        book1 = Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',)
        book2 = Book.objects.create(name='The story',author = 'the writer',price = '300',isbn_number = '2',)
        response = self.client.get(reverse('textbookFinder:index'))
        self.assertContains(response, 'The book')
        self.assertContains(response, 'The story')
class TestBookCreateView(TestCase):
    def testCreateView(self):
        response = self.client.get(reverse('textbookFinder:create'))
        self.assertEqual(response.status_code, 200)
class TestListingsView(TestCase):
    def testNoBook(self):
        url = reverse('textbookFinder:listing',args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def testOneBook(self):
        book1 = Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',)
        url = reverse('textbookFinder:listing', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book1.name)
    def testMultipleBooks(self):
        book1 = Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',)
        book2 = Book.objects.create(name='Other book', author='other author', price = '21', isbn_number = '2',)
        book3 = Book.objects.create(name='Book 3',author = 'the third author',price = '63',isbn_number = '3',)
        response = self.client.get(reverse('textbookFinder:listing', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, book2.name)
        self.assertContains(response, book1.author)
        response = self.client.get(reverse('textbookFinder:listing', args=(2,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book2.price)
        response = self.client.get(reverse('textbookFinder:listing', args=(3,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book3.price)
class TestLoginView(TestCase):
    def testLoginPage(self):
        url = reverse_lazy('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'password')
class TestSignupView(TestCase):
    def testSignupPage(self):
        url = reverse_lazy('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'email')
class TestAccountView(TestCase):
     def testMyAccount(self):
         self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
         login = self.client.login(username='bfb3ab',password='1234jhj4')
         url = reverse('textbookFinder:account', args=(1,))
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)
         self.assertContains(response,'My Account')
         self.assertContains(response,'Username: ')
         self.assertContains(response, 'Email: ')
         self.assertContains(response,'bfb3ab')
         self.assertContains(response, 'bfb3ab@virginia.edu')
class TestCartView(TestCase):
    def testNoUser(self):
        response = self.client.get('/textbook/cart')
        self.assertContains(response, 'Saved Items')
        self.assertEqual(response.status_code, 200)
    def testEmptyCart(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',)
        Book.objects.create(name='The other book',author = 'the other author',price = '2', isbn_number = '2',)
        book1 = Book.objects.get(name='The book')
        book2 = Book.objects.get(name='The other book')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get('/textbook/cart')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, book1.name)
        self.assertNotContains(response, book2.name)
    def testCartOneItem(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1')
        Book.objects.create(name='The other book',author = 'the other author',price = '2', isbn_number = '2',)
        book1 = Book.objects.get(name='The book')
        book2 = Book.objects.get(name='The other book')
        book1.starred_by.add(self.user)
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get('/textbook/cart')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book1.name)
        self.assertNotContains(response, book2.name)
    def testCartMultipleItems(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1')
        Book.objects.create(name='The other book',author = 'the other author',price = '2', isbn_number = '2')
        Book.objects.create(name='Not gonna be starred',author = 'who cares',price = '1', isbn_number = '2',)
        book1 = Book.objects.get(name='The book')
        book2 = Book.objects.get(name='The other book')
        book3 = Book.objects.get(name='Not gonna be starred')
        book1.starred_by.add(self.user)
        book2.starred_by.add(self.user)
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get('/textbook/cart')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book1.name)
        self.assertContains(response, book2.name)
        self.assertNotContains(response, book3.name)
    def testAddToCart(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1')
        book1 = Book.objects.get(name='The book')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get(reverse('textbookFinder:cart_add', args=(1,)))
        self.assertContains(self.client.get(reverse('textbookFinder:cart')),book1.name)
    def testAddthenRemoveFromCart(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1')
        book1 = Book.objects.get(name='The book')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get(reverse('textbookFinder:cart_add', args=(1,)))
        self.assertContains(self.client.get(reverse('textbookFinder:cart')),book1.name)
        response = self.client.get(reverse('textbookFinder:cart_remove',args=(1,)))
        self.assertNotContains(self.client.get(reverse('textbookFinder:cart')),book1.name)
    def testAddthenRemoveMultiple(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1')
        Book.objects.create(name='The other book',author = 'the other author',price = '2', isbn_number = '2')
        Book.objects.create(name='Not gonna be starred',author = 'who cares',price = '1', isbn_number = '2',)
        book1 = Book.objects.get(name='The book')
        book2 = Book.objects.get(name='The other book')
        book3 = Book.objects.get(name='Not gonna be starred')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get(reverse('textbookFinder:cart_add', args=(1,)))
        response = self.client.get(reverse('textbookFinder:cart_add', args=(2,)))
        response = self.client.get(reverse('textbookFinder:cart_add', args=(3,)))
        self.assertContains(self.client.get(reverse('textbookFinder:cart')),book1.name)
        self.assertContains(self.client.get(reverse('textbookFinder:cart')),book2.name)
        self.assertContains(self.client.get(reverse('textbookFinder:cart')),book3.name)
        response = self.client.get(reverse('textbookFinder:cart_remove',args=(1,)))
        self.assertNotContains(self.client.get(reverse('textbookFinder:cart')),book1.name)
        self.assertContains(self.client.get(reverse('textbookFinder:cart')),book2.name)
        self.assertContains(self.client.get(reverse('textbookFinder:cart')),book3.name)
class TestDeleteView(TestCase):
    def testNoSellingBooks(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1')
        book1 = Book.objects.get(name='The book')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get('/textbook/')
        self.assertContains(response, 'The book')
        response = self.client.get(reverse('textbookFinder:remove_listing', args=(1,)))
        response = self.client.get('/textbook/')
        self.assertContains(response, 'The book')
    def testSellingBooks(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',seller = self.user)
        book1 = Book.objects.get(name='The book')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get('/textbook/')
        self.assertContains(response, 'The book')
        response = self.client.get(reverse('textbookFinder:remove_listing', args=(1,)))
        response = self.client.get('/textbook/')
        self.assertNotContains(response, 'The book')
class TestMarkView(TestCase):
    def testNoSellingBooks(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1')
        book1 = Book.objects.get(name='The book')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        self.assertFalse(Book.objects.get(name = 'The book').is_sold)
        response = self.client.get(reverse('textbookFinder:mark_sold', args=(1,)))
        self.assertFalse(Book.objects.get(name = 'The book').is_sold)
    def testSellingBooks(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',seller = self.user)
        book1 = Book.objects.get(name='The book')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        self.assertFalse(Book.objects.get(name = 'The book').is_sold)
        response = self.client.get(reverse('textbookFinder:mark_sold', args=(book1.id,)))
        self.assertTrue(Book.objects.get(name = 'The book').is_sold)
    def testSellingBooksWarning(self):
        self.user = CustomUser.objects.create_user(username= 'bfb3ab', password = '1234jhj4', email = 'bfb3ab@virginia.edu',)
        Book.objects.create(name='The book',author = 'the author',price = '3',isbn_number = '1',seller = self.user)
        book1 = Book.objects.get(name='The book')
        login = self.client.login(username='bfb3ab',password='1234jhj4')
        response = self.client.get(reverse('textbookFinder:mark_sold', args=(book1.id,)))
        response = self.client.get('/textbook/')
        self.assertContains(response, 'Sold.')
