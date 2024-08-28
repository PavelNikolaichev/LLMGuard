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
    if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
        print(f"[DEV]Output before processing: {output}")

    output_scanners = [
        IDScanner(regex_vault),
        NNumberScanner(regex_vault),
        StudentNetIDScanner(regex_vault),
    ]

    sanitized_output = ""

    print(regex_vault)

    for scanner in output_scanners:
        sanitized_output, is_valid, risk_score = scanner.scan(prompt, deanonymize=True)

        if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
            print(f"[DEV]Output after processing: {sanitized_output}")

    scanner = Deanonymize(
        vault,
    )

    # try:
    #     anonymized_output, is_valid, risk_score = scanner.scan(prompt, output)

    #     if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
    #         print(f"[DEV]Output after processing: {anonymized_output}")
    # except Exception as e:
    #     print(f"Error processing output: {e}")
    #     anonymized_output = output

    return output


def process_input_with_llmguard(input: str, vault: Vault, regex_vault: dict) -> str:
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

    input_scanners = [
        IDScanner(regex_vault),
        NNumberScanner(regex_vault),
        StudentNetIDScanner(regex_vault),
    ]

    # Note: custom regex_patterns are not working
    second_pass = [
        Anonymize(
            vault, preamble="Insert before prompt", recognizer_conf=BERT_LARGE_NER_CONF
        ),
    ]

    sanitized_prompt = input

    for scanner in input_scanners:
        sanitized_prompt, is_valid, risk_score = scanner.scan(sanitized_prompt)

    if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
        print(f"[DEV]Input after processing(1st pass): {sanitized_prompt}")

    sanitized_prompt, results_valid, risk_score = scan_prompt(
        second_pass, sanitized_prompt
    )

    if os.getenv("ENVIRONMENT") and os.getenv("ENVIRONMENT") == "development":
        print(f"[DEV]Input after processing(2nd pass): {sanitized_prompt}")

    return sanitized_prompt
