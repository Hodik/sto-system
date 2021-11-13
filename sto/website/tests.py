from django.test import TestCase
from website.models import *

# Create your tests here.

class StoTestCase(TestCase):

    USER_TESTING_EMAIL = "TEST@GMAIL.COM"
    USER_TESTING_PASSWORD = "testPass.1"
    def setUp(self) -> None:
        self.new_user = User.objects.create(email=self.USER_TESTING_EMAIL, password=self.USER_TESTING_PASSWORD)
        self.new_sto = Sto.objects.create(name="First STO", user_id=self.new_user.id)

    def test_sto_set_name(self):
        """ Sto can be created with some name """
        self.assertEqual(self.new_sto.name, "First STO")

    def test_user_got_created(self):
        """ User was created by .objects.create method """
        self.assertEqual(User.objects.filter(email=self.USER_TESTING_EMAIL).exists(), True)

    def test_sto_belongs_to_user(self):
        """ Created STO belongs to a created User """
        self.assertIn(self.new_sto, list(self.new_user.stos.all()))