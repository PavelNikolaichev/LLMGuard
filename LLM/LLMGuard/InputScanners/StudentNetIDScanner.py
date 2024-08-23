from llm_guard.input_scanners import Regex
from presidio_anonymizer.core.text_replace_builder import TextReplaceBuilder

from llm_guard.util import get_logger

LOGGER = get_logger()


class StudentNetIDScanner(Regex):
    """
    Scanner for student NetIDs
    NetID is a student's username for logging into university systems.
    NetID is typically your initials and a few random numbers. Optionally it can contain ending as an email address - @<university>.<domain>

    This scanner is used to detect and sanitize student NetIDs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__([r"[a-zA-Z]+\d+(?:@[a-zA-Z]+\.[a-zA-Z]+)?"], *args, **kwargs)

    def get_name(self):
        return "StudentNetIDScanner"

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
                        "[NetID OMMITED]",
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
