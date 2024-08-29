import glob
from typing import List
import pprint

from numpy import rec
from presidio_analyzer import (
    AnalyzerEngine,
    PatternRecognizer,
    EntityRecognizer,
    Pattern,
    RecognizerResult,
)
from presidio_analyzer.recognizer_registry import RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngine, SpacyNlpEngine, NlpArtifacts
from presidio_analyzer.context_aware_enhancers import LemmaContextAwareEnhancer
from presidio_anonymizer import (
    AnonymizerEngine,
    DeanonymizeEngine,
    EngineResult,
    OperatorConfig,
)
import regex


def process_output_with_llmguard(
    prompt: str, output: str, regex_vault: dict
) -> EngineResult:
    """
    Function to process the output with LLMGuard by applying Deanonymize scanner.

    Args:
        prompt (str): The prompt to process.
        output (str): The output to process.
        vault (Vault): The vault object to use for Deanonymize scanner.

    Returns:
        str: The processed output.
    """
    engine = DeanonymizeEngine()

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
        Pattern(name="Omitted", regex="\\[TITLE_\\d+\\]", score=1.0),
    ]

    recognizer = PatternRecognizer(supported_entity="TITLE", patterns=patterns)

    entries = recognizer.analyze(text=output, entities=["TITLE"])

    print(regex_vault)

    def check(x):
        print("pattern", x)
        res = regex_vault.gex(x, "")
        print(res)
        return res

    result = engine.deanonymize(
        text=output,
        entities=entries,
        operators={"TITLE": OperatorConfig("custom", {"lambda": lambda x: check(x)})},
    )

    return result

    # output_scanners = [
    #     NNumberScanner(regex_vault),
    #     StudentNetIDScanner(regex_vault),
    #     IDScanner(regex_vault),
    # ]

    # desanitized_output = ""

    # desanitized_output = output
    # for scanner in output_scanners:
    #     desanitized_output, is_valid, risk_score = scanner.scan(
    #         desanitized_output, deanonymize=True
    #     )

    # scanner = Deanonymize(vault)

    # try:
    #     desanitized_output, is_valid, risk_score = scanner.scan(
    #         prompt, desanitized_output
    #     )
    # except Exception as e:
    #     print(f"Error during Deanonimyze scanner output: {e}")

    # return desanitized_output


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

    print("Result:")
    print(entries)

    engine = AnonymizerEngine()

    def set_record(record):
        global counter

        counter += 1

        regex_vault[f"[TITLE_{counter}]"] = record

        return f"[TITLE_{counter}]"

    sanitized_prompt = engine.anonymize(
        text=input,
        analyzer_results=entries,
        operators={
            "TITLE": OperatorConfig("custom", {"lambda": lambda x: set_record(x)})
        },
    )

    print(f"Sanitized prompt: {sanitized_prompt}")

    return sanitized_prompt
