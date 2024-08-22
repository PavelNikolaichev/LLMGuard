import gradio as gr
from LLM.LLMGuard.GuardProcessor import (
    process_output_with_llmguard,
    process_input_with_llmguard,
)
from llm_guard.vault import Vault

from LLM.TransformersLLM import get_transformers_pipeline, generate_transformers_output

pipeline = None


def run_llm_guard(prompt: str) -> str:
    """
    Run LLMGuard on a prompt. This function processes both input and output with LLMGuard.

    Args:
        prompt (str): The prompt to process.

    Returns:
        str: The processed prompt.
    """
    vault = Vault()

    mock_output = generate_transformers_output(
        process_input_with_llmguard(prompt, vault),
        pipeline,
    )

    processed_output = process_output_with_llmguard(prompt, mock_output, vault)

    return processed_output


iface = gr.Interface(
    fn=run_llm_guard,
    inputs="text",
    outputs="text",
    title="LLMGuard Tester",
    description="Enter a prompt to generate LLM output and process it with LLMGuard. Current mode is text generation.",
)

if __name__ == "__main__":
    pipeline = get_transformers_pipeline()

    iface.launch()
