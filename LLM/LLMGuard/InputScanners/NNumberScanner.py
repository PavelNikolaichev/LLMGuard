from llm_guard.input_scanners import Regex
from presidio_anonymizer.core.text_replace_builder import TextReplaceBuilder

from llm_guard.util import get_logger

LOGGER = get_logger()


class NNumberScanner(Regex):
    """
    Scanner for N numbers

    According to NYU info for newcoming students,
    N number is a university id number that starts with letter N and is followed by 8 digits.
    """

    def __init__(self, *args, **kwargs):
        self.string_patterns = [r"N\d{8}"]
        super().__init__(self.string_patterns, *args, **kwargs)

    def get_name(self):
        return "NNumberScanner"

    def to_anonymize_dict(self):
        """
        Returns the anonymize dictionary for the Anonymize scanner.

        Returns:
            dict: The anonymize dictionary, containing the expressions, name, examples, context, score, and languages.
        """
        return {
            "expressions": self.string_patterns,
            "name": self.get_name(),
            "examples": ["N12345678", "N87654321"],
            "context": ["university", "student", "id"],
            "score": 0.85,
            "languages": ["en"],
        }

    def scan(self, prompt: str) -> tuple[str, bool, float]:
        text_replace_builder = TextReplaceBuilder(original_text=prompt)
        for pattern in self._patterns:
            match = self._match_type.match(pattern, prompt)
            if match is None:
                continue

            if self._is_blocked:
                LOGGER.warning("Pattern was detected in the text", pattern=pattern)

                if self._redact:
                    text_replace_builder.replace_text_get_insertion_index(
                        "[OMMITTED_NNUMBER]",
                        match.start(),
                        match.end(),
                    )

                return text_replace_builder.output_text, False, 1.0

            LOGGER.debug("Pattern matched the text", pattern=pattern)
            return text_replace_builder.output_text, True, 0.0

        if self._is_blocked:
            LOGGER.debug("None of the patterns were found in the text")
            return text_replace_builder.output_text, True, 0.0

        LOGGER.warning("None of the patterns matched the text")
        return text_replace_builder.output_text, False, 1.0
