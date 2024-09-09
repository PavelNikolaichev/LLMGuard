import unittest
from presidio_analyzer import RecognizerResult
from presidio_anonymizer import EngineResult
from GuardProcessor import (
    deanonymize_output,
    recognize_anonymized_tokens,
    process_output_with_llmguard,
    anonymize_input,
    recognize_patterns_in_input,
    process_input_with_llmguard,
)


class TestDeanonymization(unittest.TestCase):
    def test_deanonymize_output(self):
        output = "[OMITTED_StudentNetID_1] is a student."
        recognized_tokens = [
            RecognizerResult(entity_type="AnonymizedToken", start=0, end=24, score=1.0)
        ]
        regex_vault = {"[OMITTED_StudentNetID_1]": "student123"}

        result = deanonymize_output(output, recognized_tokens, regex_vault)

        self.assertIsInstance(result, EngineResult)
        self.assertIn("student123", result.text)

    def test_recognize_anonymized_tokens(self):
        output = "[OMITTED_StudentNetID_1] is a student."
        recognized_tokens = recognize_anonymized_tokens(output)

        self.assertEqual(len(recognized_tokens), 1)
        self.assertEqual(recognized_tokens[0].entity_type, "AnonymizedToken")

    def test_process_output_with_llmguard(self):
        output = "[OMITTED_StudentNetID_1] is a student."
        regex_vault = {"[OMITTED_StudentNetID_1]": "student123"}

        result = process_output_with_llmguard(output, regex_vault)
        self.assertIsInstance(result, EngineResult)
        self.assertIn("student123", result.text)


class TestAnonymization(unittest.TestCase):
    def test_anonymize_input(self):
        input_text = "student123 is a student with N12345678."
        recognized_patterns = [
            RecognizerResult(entity_type="StudentNetID", start=0, end=10, score=1.0),
            RecognizerResult(entity_type="NNumber", start=28, end=37, score=1.0),
        ]
        regex_vault = {}

        result = anonymize_input(input_text, recognized_patterns, regex_vault)

        self.assertIsInstance(result, EngineResult)
        self.assertIn("[OMITTED_StudentNetID_1]", result.text)
        self.assertIn("[OMITTED_NNumber_1]", result.text)
        self.assertIn("[OMITTED_StudentNetID_1]", regex_vault)
        self.assertIn("[OMITTED_NNumber_1]", regex_vault)

    def test_recognize_patterns_in_input(self):
        input_text = "student123 is a student with N12345678."
        recognized_patterns = recognize_patterns_in_input(input_text)

        # Actually netid can catch NNumber as well, so we should have 3 entries
        self.assertEqual(len(recognized_patterns), 3)
        self.assertEqual(recognized_patterns[0].entity_type, "StudentNetID")
        self.assertEqual(recognized_patterns[2].entity_type, "NNumber")

        self.assertEqual(recognized_patterns[0].start, 0)
        self.assertEqual(recognized_patterns[0].end, 10)

        self.assertEqual(recognized_patterns[2].start, 29)
        self.assertEqual(recognized_patterns[2].end, 38)

    def test_process_input_with_llmguard(self):
        input_text = "student123 is a student with N12345678."
        regex_vault = {}

        result = process_input_with_llmguard(input_text, regex_vault)

        self.assertIsInstance(result, EngineResult)
        self.assertIn("[OMITTED_StudentNetID_1]", result.text)
        self.assertIn("[OMITTED_NNumber_1]", result.text)
        self.assertIn("[OMITTED_StudentNetID_1]", regex_vault)
        self.assertIn("[OMITTED_NNumber_1]", regex_vault)


if __name__ == "__main__":
    unittest.main()
