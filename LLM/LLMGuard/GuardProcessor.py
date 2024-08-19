from llm_guard.input_scanners import Anonymize
from llm_guard.vault import Vault
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from llm_guard import scan_prompt

from LLM.LLMGuard.InputScanners.IDScanner import IDScanner
from LLM.LLMGuard.InputScanners.NNumberScanner import NNumberScanner
from LLM.LLMGuard.InputScanners.StudentNetIDScanner import StudentNetIDScanner

from llm_guard.output_scanners import Deanonymize

vault = Vault() # Initialize the vault, TODO: integrate it properly.

def process_output_with_llmguard(prompt, output):
    print(f"Output before processing: {output}")

    # Need to not disclose student id or other sensitive information using LLMGuard

    # Use the LLMGuard to scan the output
    scanner = Deanonymize(
        vault,
    )

    # Anonymize the output
    anonymized_output, is_valid, risk_score = scanner.scan(prompt, output)

    return anonymized_output


def process_input_with_llmguard(input):
    print(f"Input before processing: {input}")

    # Need to not disclose student id or other sensitive information using LLMGuard
    # Use the LLMGuard to scan the output

    input_scanners = [
        IDScanner(),
        NNumberScanner(),
        StudentNetIDScanner(),
        Anonymize(
            vault,
            preamble="Insert before prompt",
            recognizer_conf=BERT_LARGE_NER_CONF,
            language="en",
        ),
    ]

    sanitized_prompt, results_valid, risk_score = scan_prompt(input_scanners, input)

    if any(not result for result in results_valid.values()):
        print(f"Prompt {input} is not valid, scores: {risk_score}")
        return sanitized_prompt

    return sanitized_prompt
