import gradio as gr
from LLM.MockLLM import generate_mock_output
from LLM.LLMGuard.GuardProcessor import (
    process_output_with_llmguard,
    process_input_with_llmguard,
)
from LLM.Ollama import generate_ollama_output

from LLM.TransformersLLM import generate_transformers_output

from llm_guard.vault import Vault


def run_llm_guard(prompt):
    """
    Run LLMGuard on a prompt. This function processes both input and output with LLMGuard.

    Args:
        prompt (str): The prompt to process.

    Returns:
        str: The processed prompt.
    """

    vault = Vault()

    # Generate mock LLM output based on the preprocessed input
    # mock_output = generate_mock_output(process_input_with_llmguard(prompt))
    mock_output = generate_transformers_output(process_input_with_llmguard(prompt, vault))

    # Process the output with LLMGuard
    processed_output = process_output_with_llmguard(prompt, mock_output, vault)

    return processed_output


# Gradio Interface
iface = gr.Interface(
    fn=run_llm_guard,
    inputs="text",
    outputs="text",
    title="LLMGuard Tester",
    description="Enter a prompt to generate mock LLM output and process it with LLMGuard.",
)

if __name__ == "__main__":
    iface.launch()
