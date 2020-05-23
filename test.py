import unittest
import guess


class TestGame(unittest.TestCase):

    def test_get_scores(self):
        self.assertIsInstance(guess.user_score, dict)

    def test_username(self):
        self.assertNotIn(guess.username, guess.lst)


if __name__ == "__main__":
    unittest.main()
