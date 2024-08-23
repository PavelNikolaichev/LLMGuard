import sys
import torch
from transformers import (
    pipeline,
    AutoModelForCausalLM,
    AutoTokenizer,
    QuantoConfig,
)

device = "cpu"


def get_transformers_pipeline(model_name: str = "Qwen/Qwen2-0.5B") -> pipeline:
    """
    Function to get a Transformers pipeline that can be used to generate output.

    Args:
        model_name (str): The name of the model to load. Defaults to "Qwen/Qwen2-0.5B".

    Returns:
        pipeline: The Transformers pipeline instance.
    """
    quantization_config = QuantoConfig(weights="int2")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, device_map="cpu", quantization_config=quantization_config
    )

    # Compilation doesn't work with Python 3.12+ yet
    if sys.version_info < (3, 12):
        model.forward = torch.compile(
            model.forward, mode="reduce-overhead", fullgraph=True
        )

    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device_map="auto",
    )


def generate_transformers_output(prompt: str, pipeline: pipeline = None) -> str:
    """
    Function to generate an output from the Transformers pipeline.

    Args:
        prompt (str): The prompt to generate the output.
        pipeline (pipeline | None, optional): The Transformers pipeline to use. Defaults to None. If None, a new pipeline will be created.

    Returns:
        str: The generated output.
    """
    if pipeline is None:
        pipeline = get_transformers_pipeline()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant in a university environment. Help professors and students with their questions and problems.",
        },
        {"role": "user", "content": prompt},
    ]

    response = pipeline(messages, max_new_tokens=100, do_sample=True)

    print(response)

    return response[0]["generated_text"][-1]
