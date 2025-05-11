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

    def test_find_all(self):
        user_repository.create(self.user_testi1.username, "salasana123")
        user_repository.create(self.user_testi2.username, "salasana321")

        user1 = user_repository.find_by_username(self.user_testi1.username)
        user2 = user_repository.find_by_username(self.user_testi2.username)

        self.assertIsNotNone(user1)
        self.assertIsNotNone(user2)
        self.assertEqual(user1.username, self.user_testi1.username)
        self.assertEqual(user2.username, self.user_testi2.username)

    def test_find_by_username(self):
        user_repository.create(self.user_testi1.username, "salasana123")

        user = user_repository.find_by_username(self.user_testi1.username)

        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.user_testi1.username)
