from presidio_analyzer import PatternRecognizer, Pattern, RecognizerResult
from presidio_anonymizer import (
    AnonymizerEngine,
    EngineResult,
    OperatorConfig,
)
from typing import Dict, List


def deanonymize_output(
    output: str, recognized_tokens: List[RecognizerResult], regex_vault: Dict[str, str]
) -> EngineResult:
    """
    Deanonymize the provided output using the recognized tokens and regex vault.

    Args:
        output (str): The anonymized output text.
        recognized_tokens: Tokens recognized for anonymization.
        regex_vault (dict): Dictionary for mapping anonymized tokens to their original values.

    Returns:
        str: The deanonymized output text.
    """
    engine = AnonymizerEngine()

    def deanonymize_operator(anonymized_text: str) -> str:
        return regex_vault.get(anonymized_text, anonymized_text)

    result = engine.anonymize(
        text=output,
        analyzer_results=recognized_tokens,
        operators={
            "AnonymizedToken": OperatorConfig(
                "custom", {"lambda": deanonymize_operator}
            )
        },
    )

    return result


def recognize_anonymized_tokens(output: str) -> List[RecognizerResult]:
    """
    Recognize anonymized tokens in the output using a predefined pattern.

    Args:
        output (str): The text to analyze.

    Returns:
        list: Recognized anonymized tokens in the output.
    """
    anonymized_pattern = Pattern(
        name="AnonymizedToken", regex=r"\[OMITTED_[A-Za-z]+_\d+\]", score=1.0
    )
    recognizer = PatternRecognizer(
        supported_entity="AnonymizedToken", patterns=[anonymized_pattern]
    )

    return recognizer.analyze(text=output, entities=["AnonymizedToken"])


def process_output_with_llmguard(
    output: str, regex_vault: Dict[str, str]
) -> EngineResult:
    """
    Process the output with Presidio by applying the deanonymization scanner.

    Args:
        output (str): The anonymized output to process.
        regex_vault (dict): The vault to use for deanonymization.

    Returns:
        EngineResult: The deanonymized output.
    """
    recognized_anonymized_tokens = recognize_anonymized_tokens(output)
    deanonymized_output = deanonymize_output(
        output, recognized_anonymized_tokens, regex_vault
    )

    return deanonymized_output


def anonymize_input(
    input_text: str,
    recognized_patterns: List[RecognizerResult],
    regex_vault: Dict[str, str],
) -> EngineResult:
    """
    Anonymize input text using predefined patterns and update the regex vault.

    Args:
        input_text (str): The input text to anonymize.
        recognized_patterns: Recognized patterns for sensitive information.
        regex_vault (dict): The vault to store the anonymized values.

    Returns:
        EngineResult: The result of the anonymization process.
    """
    engine = AnonymizerEngine()
    entity_counters = {}  # Store counters for each entity type

    def store_record(record: str, entity_type: str) -> str:
        # I am not sure why some of the entries are just PII, so we actually should skip them
        if record == "PII":
            return record

        nonlocal entity_counters
        # Initialize counter for entity type if not set
        if entity_type not in entity_counters:
            entity_counters[entity_type] = 0
        entity_counters[entity_type] += 1

        # Create token in the format [OMITTED_<EntityType>_<Counter>]
        token = f"[OMITTED_{entity_type}_{entity_counters[entity_type]}]"
        regex_vault[token] = record
        return token

    # Anonymize the input using specific entities and descriptive tokens
    result = engine.anonymize(
        text=input_text,
        analyzer_results=recognized_patterns,
        operators={
            "StudentNetID": OperatorConfig(
                "custom", {"lambda": lambda x: store_record(x, "StudentNetID")}
            ),
            "NNumber": OperatorConfig(
                "custom", {"lambda": lambda x: store_record(x, "NNumber")}
            ),
            "ID": OperatorConfig("custom", {"lambda": lambda x: store_record(x, "ID")}),
        },
    )

    return result


def recognize_patterns_in_input(input_text: str) -> List[RecognizerResult]:
    """
    Recognize sensitive patterns in the input text using predefined patterns.

    Args:
        input_text (str): The input text to scan for sensitive information.

    Returns:
        list: Recognized patterns in the input.
    """
    patterns = [
        Pattern(
            name="StudentNetID",
            regex=r"[a-zA-Z]+\d+(?:@[a-zA-Z]+\.[a-zA-Z]+)?",
            score=1.0,
        ),
        Pattern(name="NNumber", regex=r"N\d{8}\b", score=1.0),
        Pattern(
            name="ID",
            regex=r"\b((([A-Za-z]{2})( +))|([A-Za-z]{2}))?\d{6,10}\b",
            score=1,
        ),
    ]

    recognized_results = []
    for pattern in patterns:
        recognizer = PatternRecognizer(
            supported_entity=pattern.name, patterns=[pattern]
        )
        recognized_results.extend(
            recognizer.analyze(text=input_text, entities=[pattern.name])
        )

    return recognized_results


def process_input_with_llmguard(
    input_text: str, regex_vault: Dict[str, str]
) -> EngineResult:
    """
    Process the input text with Presidio by applying anonymization.

    Args:
        input_text (str): The input to process.
        regex_vault (dict): The vault to store anonymized information.

    Returns:
        EngineResult: The processed input.
    """
    recognized_patterns = recognize_patterns_in_input(input_text)
    sanitized_prompt = anonymize_input(input_text, recognized_patterns, regex_vault)

    return sanitized_prompt
