"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text
Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch
TIP: for testing builtin input() function create another function which return input()
and mock returned value
"""
from unittest.mock import patch
import unittest
from task_input_output import read_numbers


class TestInputOutput(unittest.TestCase):
    @patch('builtins.input', side_effect=[1, 2, 3, 4])
    def test_read_numbers_without_text_input(self, mock_inputs):
        self.assertEqual(read_numbers(4), 2.5)

    @patch('builtins.input', side_effect=[1, 2, 'Text'])
    def test_read_numbers_with_text_input(self, mock_inputs):
        self.assertEqual(read_numbers(3), 1.5)

    @patch('builtins.input', side_effect=['ja', 'ty', 'on', 'ona', 'drzewo'])
    def test_test_number_with_text_input_2(self, mock_inputs):
        self.assertIsNone(read_numbers(5))
