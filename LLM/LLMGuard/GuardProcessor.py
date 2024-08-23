import os
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize import DEFAULT_ENTITY_TYPES
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from llm_guard.input_scanners.anonymize_helpers.regex_patterns import (
    DEFAULT_REGEX_PATTERNS,
)

from llm_guard.vault import Vault
from llm_guard import scan_prompt

from LLM.LLMGuard.InputScanners.IDScanner import IDScanner
from LLM.LLMGuard.InputScanners.NNumberScanner import NNumberScanner
from LLM.LLMGuard.InputScanners.StudentNetIDScanner import StudentNetIDScanner

from llm_guard.output_scanners import Deanonymize


def process_output_with_llmguard(prompt: str, output: str, vault: Vault) -> str:
    """
    Function to process the output with LLMGuard by applying Deanonymize scanner.

    Args:
        prompt (str): The prompt to process.
        output (str): The output to process.
        vault (Vault): The vault object to use for Deanonymize scanner.

    Returns:
        str: The processed output.
    """
    if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
        print(f"[DEV]Output before processing: {output}")

    scanner = Deanonymize(
        vault,
    )

    anonymized_output, is_valid, risk_score = scanner.scan(prompt, output)

    if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
        print(f"[DEV]Output after processing: {anonymized_output}")

    return anonymized_output


def process_input_with_llmguard(input: str, vault: Vault) -> str:
    """
    Function to process the input with LLMGuard by applying the appropriate scanners.

    Args:
        input (str): The input to process.
        vault (Vault): The vault object to use for the scanners.

    Returns:
        str: The processed input.
    """
    if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
        print(f"[DEV]Input before processing: {input}")

    # input_scanners = [
    #     IDScanner(),
    #     NNumberScanner(),
    #     StudentNetIDScanner(),
    # ]

    second_pass = [
        Anonymize(
            vault,
            preamble="Insert before prompt",
            recognizer_conf=BERT_LARGE_NER_CONF,
            regex_patterns=DEFAULT_REGEX_PATTERNS
            + [
                IDScanner().to_anonymize_dict(),
                NNumberScanner().to_anonymize_dict(),
                StudentNetIDScanner().to_anonymize_dict(),
                {
                    "expressions": [r"[a-zA-Z]+\d+(?:@[a-zA-Z]+\.[a-zA-Z]+)?"],
                    "name": "NetID",
                    # "context": ["student", "id"],
                    # "score": 0.85,
                    # "languages": ["en"],
                },
            ],
            entity_types=DEFAULT_ENTITY_TYPES
            + ["IDScanner", "NNumberScanner", "StudentNetIDScanner", "NetID"],
            language="en",
        ),
    ]

    # sanitized_prompt, results_valid, risk_score = scan_prompt(input_scanners, input)
    sanitized_prompt = input

    # if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
    #     print(f"[DEV]Input after processing(1st pass): {sanitized_prompt}")

    sanitized_prompt, results_valid, risk_score = scan_prompt(
        second_pass, sanitized_prompt
    )

    if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
        print(f"[DEV]Input after processing(2nd pass): {sanitized_prompt}")

    return sanitized_prompt
