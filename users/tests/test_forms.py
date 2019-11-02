from ..forms import Custom_User_Creation_form, Custom_User_Change_form
from ..models import My_custom_user

from django.test.testcases import LiveServerTestCase
from django.test import TestCase

class Test_forms(TestCase):

    def test_user_creation_form(self):
        form = Custom_User_Change_form(data={'username':'test_user', 
             'email': 'test@gmail.com', 'password1':'Test123!test', 'password2': 'Test123!test',})
        form.save()
        user_created = My_custom_user.objects.first()
        self.assertEqual(user_created.id, 1)
        self.assertEqual(user_created.username, 'test_user')
        self.assertEqual(user_created.password1, 'test123!test')
        self.assertEqual(user_created.email, 'test@gmail.com')
        self.assertEqual(user_created.total_points, 0)
