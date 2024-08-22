import sys
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer


# TODO: set appropriate model
def get_transformers_pipeline(model_name: str = "facebook/opt-350m") -> pipeline:
    """
    Function to get a Transformers pipeline that can be used to generate output.

    Args:
        model_name (str): The name of the model to load. Defaults to "facebook/opt-350m".

    Returns:
        pipeline: The Transformers pipeline instance.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

    # Compilation doesn't work with Python 3.12+ yet
    if sys.version_info < (3, 12):
        model.forward = torch.compile(
            model.forward, mode="reduce-overhead", fullgraph=True
        )

    return pipeline("text-generation", model=model, tokenizer=tokenizer)


def generate_transformers_output(prompt: str, pipeline=None) -> str:
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

    response = pipeline(prompt, max_length=100, do_sample=True)

    return response[0]["generated_text"]
