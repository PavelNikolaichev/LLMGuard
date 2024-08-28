import unittest

import sys
import os

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR + "/../"))


from NNumberScanner import *


class TestNNumberScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = NNumberScanner()

    def test_valid_n_number(self):
        test_input = "My university ID is N12345678."
        test_output = "My university ID is [OMITTED_NNUMBER_1]."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertEqual(sanitized, test_output)

    def test_invalid_n_number(self):
        test_input = "My ID is X12345678."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)

    def test_multiple_n_numbers(self):
        test_input = "IDs: N12345678, N87654321."
        test_output = "IDs: [OMITTED_NNUMBER_1], [OMITTED_NNUMBER_2]."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertEqual(sanitized, test_output)

        desanitized, _, _ = self.scanner.scan(sanitized, True)

        self.assertEqual(desanitized, test_input)

    def test_no_n_number(self):
        test_input = "This sentence has no N number."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)

    def test_edge_cases(self):
        test_input = "N123456789 is not valid because it has 9 digits."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)


if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR + "/../"))

    unittest.main()
