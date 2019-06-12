import unittest


class MyTestCase(unittest.TestCase):
    def test_single(self):
        self.assertEqual(True, False)