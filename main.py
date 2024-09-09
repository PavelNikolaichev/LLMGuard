import gradio as gr
from LLM.LLMGuard.GuardProcessor import (
    process_output_with_llmguard,
    process_input_with_llmguard,
)

from dotenv import load_dotenv

from LLM.LLamaLLM import get_pipeline, generate_output

pipeline = None


def run_llm_guard(prompt: str) -> str:
    """
    Run LLMGuard on a prompt. This function processes both input and output with Presidio.

    Args:
        prompt (str): The prompt to process.

    Returns:
        str: The processed prompt.
    """
    regex_vault = {}

    anonymize_result = process_input_with_llmguard(prompt, regex_vault)

    mock_output = generate_output(
        anonymize_result.text,
        pipeline,
    )

    processed_output = process_output_with_llmguard(mock_output, regex_vault)

    return anonymize_result.text, mock_output, processed_output.text


iface = gr.Interface(
    fn=run_llm_guard,
    inputs=gr.Textbox(label="Prompt", lines=1),
    outputs=[
        gr.Textbox(label="Processed Anonymized Prompt", lines=1),
        gr.Textbox(label="Model Output", lines=1),
        gr.Textbox(label="Processed Deanonymized Output", lines=1),
    ],
    title="LLMGuard Tester",
    description="Enter a prompt to generate LLM output and process it with Presidio. Current mode is text generation.",
)

if __name__ == "__main__":
    load_dotenv()

    pipeline = get_pipeline()

    iface.launch()
