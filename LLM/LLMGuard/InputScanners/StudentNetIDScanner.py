from llm_guard.input_scanners import Regex


class StudentNetIDScanner(Regex):
    """
    Scanner for student NetIDs
    NetID is a student's username for logging into university systems.
    NetID is typically your initials and a few random numbers. Optionally it can contain ending as an email address - @<university>.<domain>

    This scanner is used to detect and sanitize student NetIDs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            [r"\b[a-zA-Z]{2,3}\d{3,5}(?:@[a-zA-Z]+\.[a-zA-Z]+)?\b"], *args, **kwargs
        )

    def get_name(self):
        return "StudentNetIDScanner"
