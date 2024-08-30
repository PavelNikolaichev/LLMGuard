from presidio_analyzer import (
    PatternRecognizer,
    Pattern,
)
from presidio_anonymizer import (
    AnonymizerEngine,
    EngineResult,
    OperatorConfig,
)

import re


def process_output_with_llmguard(prompt: str, output: str, regex_vault: dict) -> str:
    """
    Function to process the output with LLMGuard by applying Deanonymize scanner.

    Args:
        prompt (str): The prompt to process.
        output (str): The output to process.
        vault (Vault): The vault object to use for Deanonymize scanner.

    Returns:
        str: The processed output.
    """
    regex = r"\[OMITTED_\d+\]"

    def check(x: re.Match):
        res = regex_vault.get(x.group(), "")
        return res

    # Deanonymize engine in presidio does not support custom behavior unless we would override it's sources, according to documentation
    result = output
    result = re.sub(regex, check, result)

    return result


counter = 0


def process_input_with_llmguard(input: str, regex_vault: dict) -> EngineResult:
    """
    Function to process the input with LLMGuard by applying the appropriate scanners.

    Args:
        input (str): The input to process.
    Returns:
        str: The processed input.
    """
    global counter
    counter = 0

    patterns = [
        Pattern(
            name="StudentNetID",
            regex="[a-zA-Z]+\\d+(?:@[a-zA-Z]+\\.[a-zA-Z]+)?",
            score=1.0,
        ),
        Pattern(name="NNumber", regex="N\\d{8}\\b", score=1.0),
        Pattern(
            name="ID",
            regex="\\b((([A-Za-z]{2,4})( +))|([A-Za-z]{2,4}))?\\d{6,10}\b",
            score=1.0,
        ),
    ]

    recognizer = PatternRecognizer(supported_entity="TITLE", patterns=patterns)

    entries = recognizer.analyze(text=input, entities=["TITLE"])

    engine = AnonymizerEngine()

    def set_record(record):
        global counter

        counter += 1

        regex_vault[f"[OMITTED_{counter}]"] = record

        return f"[OMITTED_{counter}]"

    sanitized_prompt = engine.anonymize(
        text=input,
        analyzer_results=entries,
        operators={
            "TITLE": OperatorConfig("custom", {"lambda": lambda x: set_record(x)})
        },
    )

    print(f"Sanitized prompt: {sanitized_prompt}")

    return sanitized_prompt
