from llm_guard.input_scanners import Regex
from presidio_anonymizer.core.text_replace_builder import TextReplaceBuilder

from llm_guard.util import get_logger

LOGGER = get_logger()


class IDScanner(Regex):
    """
    A scanner for the passpor/ID numbers, it tries to find the ID number based on ICAO 9303 standard with small changes to be able to detect more cornercases.
    """

    def __init__(self, *args, **kwargs):
        self.string_patterns = [r"([A-Z]{2,4})?\d{6,10}"]
        super().__init__(self.string_patterns, *args, **kwargs)

    def get_name(self):
        return "IDScanner"

    def to_anonymize_dict(self):
        """
        Returns the anonymize dictionary for the Anonymize scanner.

        Returns:
            dict: The anonymize dictionary, containing the expressions, name, examples, context, score, and languages.
        """
        return {
            "expressions": self.string_patterns,
            "name": self.get_name(),
            "examples": ["ND22848814", "1234567890"],
            "context": ["id", "passport", "identity"],
            "score": 0.9,
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
                        "[OMMITED_ID]",
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
