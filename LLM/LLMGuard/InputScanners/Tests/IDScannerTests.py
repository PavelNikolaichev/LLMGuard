import unittest

import sys
import os

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR + "/../"))


from IDScanner import *


# TODO: Add more test cases, check regex matching itself.
class TestIDScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = IDScanner()
        
    def test_get_name(self):
        self.assertEqual(self.scanner.get_name(), "IDScanner")

    def test_scan_wrong_format(self):
        test_input = "My university ID is N12345678."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)

    def test_scan_no_match(self):
        test_input = "This is a test string."
        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)

    def test_scan_risk(self):
        test_input = "My ID is NB1234567."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertNotEqual(sanitized, test_input)

    def test_scan_us_id(self):
        test_input = "My ID is 123456789."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertNotEqual(sanitized, test_input)
    
    def test_scan_us_id_2(self):
        test_input = "My ID is US123456789."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertNotEqual(sanitized, test_input)
    
    def test_scan_large_number(self):
        test_input = "My ID is 12345678901234567890."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR + "/../"))

    unittest.main()
