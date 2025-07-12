from django.test import TestCase
from users.models import User

# Create your tests here.

class UserTestCase(TestCase):

    def test_create_user(self):
        istance = User.objects.create_user(
            username="test_create_user",
        )
        self.assertEqual(type(istance), User, f"User {istance.username} is not an instance of User")
        self.assertEqual(istance.username, "test_create_user", f"User {istance.username} is not the expected user")

    def test_delete_user(self):
        istance:User = User.objects.create_user(
            username="test_delete_user",
        )
        User.objects.filter(username="test_delete_user").delete()
        self.assertFalse(User.objects.filter(username="test_delete_user").exists(), f"User {istance.username} exists")