from llm_guard.input_scanners import Anonymize
from llm_guard.vault import Vault
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF


def process_output_with_llmguard(output):
    print(f"Processed with LLMGuard: {output}")

    # Need to not disclose student id or other sensitive information using LLMGuard
    
    # Use the LLMGuard to scan the output
    vault = Vault()
    scanner = Anonymize(vault, preamble="Insert before prompt", recognizer_conf=BERT_LARGE_NER_CONF, language="en")

    # Anonymize the output
    anonymized_output, is_valid, risk_score = scanner.scan(output)

    return anonymized_output


def process_input_with_llmguard(input):
    print(f"Processed with LLMGuard: {input}")

    # Need to not disclose student id or other sensitive information using LLMGuard
    
    # Use the LLMGuard to scan the output
    vault = Vault()
    scanner = Anonymize(vault, preamble="Insert before prompt", recognizer_conf=BERT_LARGE_NER_CONF, language="en")

    # Anonymize the output
    anonymized_output, is_valid, risk_score = scanner.scan(input)

    return anonymized_output
