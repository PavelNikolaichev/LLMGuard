import gradio as gr
from LLM.LLMGuard.GuardProcessor import (
    process_output_with_llmguard,
    process_input_with_llmguard,
)
from llm_guard.vault import Vault

from dotenv import load_dotenv

from LLM.LLamaLLM import get_pipeline, generate_output

pipeline = None
vault = Vault()


def run_llm_guard(prompt: str) -> str:
    """
    Run LLMGuard on a prompt. This function processes both input and output with LLMGuard.

    Args:
        prompt (str): The prompt to process.

    Returns:
        str: The processed prompt.
    """

    mock_output = generate_output(
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
    load_dotenv()

    pipeline = get_pipeline()

    iface.launch()
