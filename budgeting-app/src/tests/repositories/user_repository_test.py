import unittest
from repositories.user_repository import user_repository
from entities.user import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        user_repository.delete_all()
        self.user_testi1 = User('testi1', 'salasana123')
        self.user_testi2 = User('testi2', 'salasana321')

    def test_create_user(self):
        user_repository.create(self.user_testi1.username, "salasana123")
        user = user_repository.find_by_username(self.user_testi1.username)

        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.user_testi1.username)

    def test_find_all_users(self):
        user_repository.create(self.user_testi1.username, "salasana123")
        user_repository.create(self.user_testi2.username, "salasana321")
        users = user_repository.find_all()
        usernames = [u.username for u in users]
        self.assertIn(self.user_testi1.username, usernames)
        self.assertIn(self.user_testi2.username, usernames)
        self.assertEqual(len(users), 2)

    def test_find_by_username(self):
        user_repository.create(self.user_testi1.username, "salasana123")

        user = user_repository.find_by_username(self.user_testi1.username)

        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.user_testi1.username)

    def test_create_duplicate_user(self):
        user_repository.create(self.user_testi1.username, "salasana123")
        with self.assertRaises(Exception):
            user_repository.create(self.user_testi1.username, "toinensalasana")

    def test_delete_all_users(self):
        user_repository.create(self.user_testi1.username, "salasana123")
        user_repository.delete_all()
        user = user_repository.find_by_username(self.user_testi1.username)
        self.assertIsNone(user)
