from llm_guard.input_scanners import Regex


class NNumberScanner(Regex):
    """
    Scanner for N numbers
    N number is a university id number that starts with letter N and is followed by 8 digits
    """

    def __init__(self, *args, **kwargs):
        super().__init__([r"\bN\d{8}\b"], *args, **kwargs)

    def get_name(self):
        return "NNumberScanner"
