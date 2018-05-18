

# Create your tests here.
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 09:29:06 2018

@author: Administrator
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders
from rango.models import Category
from django.urls import reverse
# Thanks to Enzo Roiz https://github.com/enzoroiz who made these tests during an internship with us

class CategoryMethodTest(TestCase):
    """docstring for CategoryMethodTest"""
    def test_ensure_views_are_positive(self):
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views>=0),True)
        

    def test_slug_line_creation(self):
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


class IndexViewTest(TestCase):
    """docstring for IndexViewTest"""
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"There are no categories present")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('test temp tmp',1,1)
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test temp tmp')

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats,4)

        
        









class GeneralTests(TestCase):
    def test_serving_static_files(self):
        # If using static media properly result is not NONE once it finds rango.jpg
        result = finders.find('rango/images/TheWorld.jpg')
        self.assertIsNotNone(result)


class IndexPageTests(TestCase):
        
    def test_index_contains_hello_message(self):
        # Check if there is the message 'Rango Says'
        # Chapter 4
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'Rango says', response.content)
         
    def test_index_using_template(self):
        # Check the template used to render index page
        # Chapter 4
        response = self.client.get(reverse('rango:index'))
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_rango_picture_displayed(self):
        # Check if is there an image called 'rango.jpg' on the index page
        # Chapter 4
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'img src="/static/rango/images/TheWorld.jpg', response.content)
    
    def test_index_has_title(self):
        # Check to make sure that the title tag has been used
        # And that the template contains the HTML from Chapter 4 
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'<title>', response.content)
        self.assertIn(b'</title>', response.content)


class AboutPageTests(TestCase):
        
    def test_about_contains_create_message(self):
        # Check if in the about page is there - and contains the specified message
        # Exercise from Chapter 4
        response = self.client.get(reverse('rango:about'))
        self.assertIn(b'This tutorial has been put together by', response.content)
        
        
    def test_about_contain_image(self):
        # Check if is there an image on the about page
        # Chapter 4
        response = self.client.get(reverse('rango:about'))
        self.assertIn(b'img src="/media/', response.content)

    def test_about_using_template(self):
        # Check the template used to render index page
        # Exercise from Chapter 4 
        response = self.client.get(reverse('rango:about'))

        self.assertTemplateUsed(response, 'rango/about.html')
        
        
        
class ModelTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')
        
        
    def get_category(self, name):
        
        from rango.models import Category
        try:                  
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:    
            cat = None
        return cat
        
    def test_python_cat_added(self):
        cat = self.get_category('Python')  
        self.assertIsNotNone(cat)
         
    def test_python_cat_with_views(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.views, 128)
        
    def test_python_cat_with_likes(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)
        

class Chapter4ViewTests(TestCase):
    def test_index_contains_hello_message(self):
        # Check if there is the message 'hello world!'
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'Rango says', response.content)

    def test_does_index_contain_img(self):
        # Check if the index page contains an img
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'img', response.content)

    def test_about_using_template(self):
        # Check the template used to render index page
        # Exercise from Chapter 4
        response = self.client.get(reverse('rango:about'))

        self.assertTemplateUsed(response, 'rango/about.html')

    def test_does_about_contain_img(self):
        # Check if in the about page contains an image
        response = self.client.get(reverse('rango:about'))
        self.assertIn(b'img', response.content)

    def test_about_contains_create_message(self):
        # Check if in the about page contains the message from the exercise
        response = self.client.get(reverse('rango:about'))
        self.assertIn(b'This tutorial has been put together by', response.content)


class Chapter5ViewTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')


    def get_category(self, name):

        from rango.models import Category
        try:
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:
            cat = None
        return cat

    def test_python_cat_added(self):
        cat = self.get_category('Python')
        self.assertIsNotNone(cat)

    def test_python_cat_with_views(self):
        cat = self.get_category('Python')

        self.assertEquals(cat.views, 128)

    def test_python_cat_with_likes(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)

    def test_view_has_title(self):
        response = self.client.get(reverse('rango:index'))

        #Check title used correctly
        self.assertIn(b'<title>', response.content)
        self.assertIn(b'</title>', response.content)

    # Need to add tests to:
    # check admin interface - is it configured and set up

    def test_admin_interface_page_view(self):
        from rango.admin import PageAdmin
        self.assertIn('category', PageAdmin.list_display)
        self.assertIn('url', PageAdmin.list_display)


class Chapter6ViewTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')


    # are categories displayed on index page?

    # does the category model have a slug field?


    # test the slug field works..
    def test_does_slug_field_work(self):
        from rango.models import Category
        cat = Category(name='how do i create a slug in django')
        cat.save()
        self.assertEqual(cat.slug,'how-do-i-create-a-slug-in-django')

    # test category view does the page exist?


    # test whether you can navigate from index to a category page


    # test does index page contain top five pages?

    # test does index page contain the words "most liked" and "most viewed"

    # test does category page contain a link back to index page?


class Chapter7ViewTests(TestCase):

    def setUp(self):
        try:
            from forms import PageForm
            from forms import CategoryForm

        except ImportError:
            print('The module forms does not exist')
        except NameError:
            print('The class PageForm does not exist or is not correct')
        except:
            print('Something else went wrong :-(')

    pass
    # test is there a PageForm in rango.forms

    # test is there a CategoryForm in rango.forms

    # test is there an add page page?

    # test is there an category page?


    # test if index contains link to add category page
    #<a href="/rango/add_category/">Add a New Category</a><br />


    # test if the add_page.html template exists.