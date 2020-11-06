from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse

import http.client
import urllib


from .models import Category, Product, ProductReview
# Create your tests here.
class NewUserTestCase(TestCase):
    """ tests an Anonymous user browing the pages of the site """
    def setUp(self):
        self.client = Client()
        logged_in = self.client.session.has_key(SESSION_KEY)
        self.assertFalse(logged_in)

    def test_view_homepage(self):
        home_url =  reverse('home-page')
        response = self.client.get(home_url)
        # check that we did get a response
        self.failUnless(response)
        # check that status code of response was success
        self.assertEqual(response.status_code, http.client.OK)