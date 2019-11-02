from ..models import My_custom_user

from django.test.testcases import LiveServerTestCase
from django.test import TestCase

class Test_models(TestCase):

    def test_custom_user(self):
        custom_user = My_custom_user.objects.create('username'='test_user', 'email'='test@gmail.com')
        user_created = My_custom_user.objects.first()
        self.assertEqual(user_created.username, 'test_user')