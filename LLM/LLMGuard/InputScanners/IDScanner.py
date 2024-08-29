import re
from llm_guard.input_scanners import Regex
from presidio_anonymizer.core.text_replace_builder import TextReplaceBuilder

from llm_guard.util import get_logger

LOGGER = get_logger()


class IDScanner(Regex):
    def __init__(self, regex_vault={}, *args, **kwargs):
        self.string_patterns = [r"\b((([A-Za-z]{2,4})( +))|([A-Za-z]{2,4}))?\d{6,10}\b"]
        self.storage_dict = regex_vault
        self.counter = 0
        super().__init__(self.string_patterns, *args, **kwargs)

    def get_name(self):
        return "IDScanner"

    def scan(self, prompt: str, deanonymize=False) -> tuple[str, bool, float]:
        text_replace_builder = TextReplaceBuilder(original_text=prompt)

        if deanonymize:
            return self._deanonymize(text_replace_builder)

        isValid = True
        for pattern in self._patterns:
            matches = list(re.finditer(pattern, prompt))[::-1]
            self.counter += len(matches) + 1
            for match in matches:
                original_data = match.group(0)
                self.counter -= 1
                key = f"ID_{self.counter}"
                self.storage_dict[key] = original_data
                anonymized_data = f"[OMITTED_{key}]"

                LOGGER.warning("Pattern was detected and anonymized", pattern=pattern)
                text_replace_builder.replace_text_get_insertion_index(
                    anonymized_data,
                    match.start(),
                    match.end(),
                )

                prompt = text_replace_builder.output_text

                isValid = False

        if isValid:
            LOGGER.warning("None of the patterns matched the text")
            return text_replace_builder.output_text, True, 1.0

        return text_replace_builder.output_text, False, 1.0

    def _deanonymize(
        self, text_replace_builder: TextReplaceBuilder
    ) -> tuple[str, bool, float]:
        prompt = text_replace_builder.output_text
        for match in list(re.finditer(r"\[OMITTED_ID_\d+\]", prompt))[::-1]:
            key = match.group(0)[9:-1]
            original_data = self.storage_dict.get(key)
            if original_data:
                text_replace_builder.replace_text_get_insertion_index(
                    original_data,
                    match.start(),
                    match.end(),
                )
                LOGGER.debug("Deanonymized the data back", id=key)

            prompt = text_replace_builder.output_text

        return text_replace_builder.output_text, True, 0.0
