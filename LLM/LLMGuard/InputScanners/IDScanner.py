from llm_guard.input_scanners import Regex


class IDScanner(Regex):
    """
    A dummy for future IDScanner class. for now contains some boilerplate code
    """

    def __init__(self):
        super().__init__(r'\b\d{9}\b')