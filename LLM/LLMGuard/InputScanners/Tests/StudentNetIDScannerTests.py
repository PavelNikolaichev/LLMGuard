import unittest

import sys
import os

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR + "/../"))


from StudentNetIDScanner import *


# TODO: Add more test cases, check regex matching itself.
class TestStudentNetIDScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = StudentNetIDScanner()

    def test_valid_netid(self):
        test_input = "My NetID is ab1234."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertNotEqual(sanitized, test_input)

    def test_invalid_netid(self):
        test_input = "My NetID is abcdef."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)

    def test_multiple_netids(self):
        # TODO: check all the matches in this case
        test_input = "NetIDs: ab1234, cd5678."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)

        self.assertNotEqual(sanitized, test_input)

    def test_no_netid(self):
        test_input = "This sentence has no NetID."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)

    def test_edge_cases(self):
        test_input = "ab1230495 is not valid because digits are limitless."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertNotEqual(sanitized, test_input)

    def test_email_netid(self):
        test_input = "My NetID is ab1234@example.com"
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertNotEqual(sanitized, test_input)


if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR + "/../"))

    unittest.main()
