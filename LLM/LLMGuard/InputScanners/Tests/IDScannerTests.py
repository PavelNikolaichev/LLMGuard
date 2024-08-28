import unittest

import sys
import os

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR + "/../"))


from IDScanner import *


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
        test_output = "My ID is [OMITTED_ID_1]."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertEqual(sanitized, test_output)

    def test_scan_us_id(self):
        test_input = "My ID is 123456789."
        test_output = "My ID is [OMITTED_ID_1]."
        test_output_2 = "My ID [OMITTED_ID_1]."  # alternative if the scanner is capturing passport serties with a space

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertTrue(sanitized == test_output or sanitized == test_output_2)

        desanitize, _, _ = self.scanner.scan(sanitized, deanonymize=True)

        self.assertEqual(desanitize, test_input)

    def test_scan_us_id_2(self):
        test_input = "My ID is US123456789."
        test_output = "My ID is [OMITTED_ID_1]."
        test_output_2 = "My ID [OMITTED_ID_1]."  # alternative if the scanner is capturing passport serties with a space

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertTrue(sanitized == test_output or sanitized == test_output_2)

        desanitize, _, _ = self.scanner.scan(sanitized, deanonymize=True)

        self.assertEqual(desanitize, test_input)

    def test_scan_large_number(self):
        test_input = "My ID is 12345678901234567890."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, True)
        self.assertEqual(sanitized, test_input)

    def test_scan_multiple_ids(self):
        test_input = "IDs: 123456789, 987654321."
        test_output = "IDs: [OMITTED_ID_1], [OMITTED_ID_2]."

        sanitized, isValid, risk = self.scanner.scan(test_input)

        self.assertEqual(isValid, False)
        self.assertEqual(sanitized, test_output)

        desanitize, _, _ = self.scanner.scan(sanitized, deanonymize=True)

        self.assertEqual(desanitize, test_input)


if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR + "/../"))

    unittest.main()
