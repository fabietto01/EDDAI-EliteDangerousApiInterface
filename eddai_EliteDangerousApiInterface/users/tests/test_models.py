from django.test import TestCase
from users.models import User

from django.conf import settings

# Create your tests here.

class UserTestCase(TestCase):

    databases = '__all__'

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
        istance.delete()
        self.assertFalse(User.objects.filter(username="test_delete_user").exists(), f"User {istance.username} exists")
    
    def test_create_user_in_all_dbs(self):
        istance = User.objects.create_user(
            username="test_create_user_in_all_dbs",
        )
        dbs = settings.DATABASES_FOR_USERS_MODEL
        for db in dbs:
            self.assertTrue(User.objects.using(db).filter(username="test_create_user_in_all_dbs").exists(), f"User {istance.username} does not exists in db {db}")

    def test_delete_user_in_all_dbs(self):
        istance:User = User.objects.create_user(
            username="test_delete_user_in_all_dbs",
        )
        dbs = settings.DATABASES_FOR_USERS_MODEL
        istance.delete()
        for db in dbs:
            self.assertFalse(User.objects.using(db).filter(username="test_delete_user_in_all_dbs").exists(), f"User {istance.username} exists in db {db}")
