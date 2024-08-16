import gradio as gr
from LLM.MockLLM import generate_mock_output
from LLM.LLMGuard.GuardProcessor import process_output_with_llmguard, process_input_with_llmguard

def run_llm_guard(prompt):
    # Generate mock LLM output
    mock_output = generate_mock_output(process_input_with_llmguard(prompt))
    
    # Process the output with LLMGuard (placeholder)
    processed_output = process_output_with_llmguard(mock_output)
    
    return processed_output

# Gradio Interface
iface = gr.Interface(
    fn=run_llm_guard,
    inputs="text",
    outputs="text",
    title="LLMGuard Tester",
    description="Enter a prompt to generate mock LLM output and process it with LLMGuard."
)

if __name__ == "__main__":
    iface.launch()
