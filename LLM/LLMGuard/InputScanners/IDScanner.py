from llm_guard.input_scanners import Regex


class IDScanner(Regex):
    """
    A scanner for the passpor/ID numbers, it tries to find the ID number based on ICAO 9303 standard with small changes to be able to detect more cornercases.
    """

    def __init__(self, *args, **kwargs):
        super().__init__([r'\b([A-Z]{2,4})?\d{6,10}\b'], *args, **kwargs)

    def get_name(self):
        return "IDScanner"