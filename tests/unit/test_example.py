"""Contains tests for the example module"""

import unittest

from crma_api_client.example import foo


class ExampleTests(unittest.TestCase):
    """Tests showing an example"""

    def test_example(self):
        """Should be true"""
        self.assertEqual(foo(), "bar")
