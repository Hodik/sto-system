from django.test import TestCase
from website.models import *
from website.serializers import *
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


class ReviewsTestCase(TestCase):
    """ Testing Sto serializer along with rating serializer  """
    USER_TESTING_EMAIL = "TEST@GMAIL.COM"
    USER_TESTING_PASSWORD = "testPass.1"
    STO_NAME = "Test STo"
    REVIEW_TEXT = "TEST REVIEW"
    REVIEW_RATING = 5
    def setUp(self) -> None:
        self.new_user = User.objects.create(email=self.USER_TESTING_EMAIL, password=self.USER_TESTING_PASSWORD)
        self.new_sto = Sto.objects.create(name=self.STO_NAME, user_id=self.new_user.id)
        Review.objects.create(user=self.new_user, sto=self.new_sto, text=self.REVIEW_TEXT, rating=self.REVIEW_RATING)

    def test_review_was_assigned(self):
        """ Review was assigned to STO """
        self.assertEqual(Sto.objects.filter(name=self.STO_NAME).first().sto_reviews.exists(), True)

class StoSerializerTestCase(TestCase):
    """ Testing Sto serializer along with rating serializer  """
    USER_TESTING_EMAIL = "TEST@GMAIL.COM"
    USER_TESTING_PASSWORD = "testPass.1"
    STO_NAME = "Test STo"
    REVIEW_TEXT = "TEST REVIEW"
    REVIEW_RATING = 5
    def setUp(self) -> None:
        self.new_user = User.objects.create(email=self.USER_TESTING_EMAIL, password=self.USER_TESTING_PASSWORD)
        self.new_sto = Sto.objects.create(name=self.STO_NAME, user_id=self.new_user.id)
        Review.objects.create(user=self.new_user, sto=self.new_sto, text=self.REVIEW_TEXT, rating=self.REVIEW_RATING)

    def test_serialized_sto(self):
        """ Sto object was correctly serialized """
        should_be = {'sto_reviews': [{'id': '2', 'created_at': '2021-11-23 19:08:09.203412+00:00', 'updated_at': '2021-11-23 19:08:09.203438+00:00', 'user': '', 'sto': 'Sto object (2)', 'text': 'TEST REVIEW', 'rating': '5'}], 'id': '2', 'created_at': '2021-11-23 19:08:09.202716+00:00', 'updated_at': '2021-11-23 19:08:09.202744+00:00', 'name': 'Test STo', 'user': '', 'location': '', 'discription': '', 'website': '', 'average_rating': '5.0'}
        self.assertEqual(StoSerializer(self.new_sto, many=False).serialized['average_rating'], should_be['average_rating'])
