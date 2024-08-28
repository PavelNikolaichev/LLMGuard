import os
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF

from llm_guard.vault import Vault
from llm_guard import scan_prompt

from LLM.LLMGuard.InputScanners.IDScanner import IDScanner
from LLM.LLMGuard.InputScanners.NNumberScanner import NNumberScanner
from LLM.LLMGuard.InputScanners.StudentNetIDScanner import StudentNetIDScanner

from llm_guard.output_scanners import Deanonymize


def process_output_with_llmguard(
    prompt: str, output: str, vault: Vault, regex_vault: dict
) -> str:
    """
    Function to process the output with LLMGuard by applying Deanonymize scanner.

    Args:
        prompt (str): The prompt to process.
        output (str): The output to process.
        vault (Vault): The vault object to use for Deanonymize scanner.

    Returns:
        str: The processed output.
    """
    output_scanners = [
        NNumberScanner(regex_vault),
        StudentNetIDScanner(regex_vault),
        IDScanner(regex_vault),
    ]

    desanitized_output = ""

    desanitized_output = output
    for scanner in output_scanners:
        desanitized_output, is_valid, risk_score = scanner.scan(
            desanitized_output, deanonymize=True
        )

    scanner = Deanonymize(vault)

    try:
        desanitized_output, is_valid, risk_score = scanner.scan(
            prompt, desanitized_output
        )
    except Exception as e:
        print(f"Error during Deanonimyze scanner output: {e}")

    return desanitized_output


def process_input_with_llmguard(input: str, vault: Vault, regex_vault: dict) -> str:
    """
    Function to process the input with LLMGuard by applying the appropriate scanners.

    Args:
        input (str): The input to process.
        vault (Vault): The vault object to use for the scanners.

    Returns:
        str: The processed input.
    """
    input_scanners = [
        NNumberScanner(regex_vault),
        StudentNetIDScanner(regex_vault),
        IDScanner(regex_vault),
    ]

    # Note: custom regex_patterns are not working, so we are using 2 passes
    second_pass = [
        Anonymize(
            vault, preamble="Insert before prompt", recognizer_conf=BERT_LARGE_NER_CONF
        ),
    ]

    sanitized_prompt = input
    for scanner in input_scanners:
        sanitized_prompt, is_valid, risk_score = scanner.scan(sanitized_prompt)

    sanitized_prompt, results_valid, risk_score = scan_prompt(
        second_pass, sanitized_prompt
    )

    return sanitized_prompt
