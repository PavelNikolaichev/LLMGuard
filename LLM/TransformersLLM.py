from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer


# TODO: set appropriate model
def get_transformers_pipeline(model_name: str = "tiiuae/falcon-mamba-7b") -> pipeline:
    """
    Function to get a Transformers pipeline that can be used to generate output.

    Args:
        model_name (str): The name of the model to load. Defaults to "gpt2".

    Returns:
        pipeline: The Transformers pipeline instance.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    return pipeline("text-generation", model=model, tokenizer=tokenizer)


def generate_transformers_output(prompt: str, generator=None) -> str:
    """
    Function to generate an output from the Transformers pipeline.

    Args:
        prompt (str): The prompt to generate the output.
        generator (pipeline | None, optional): The Transformers pipeline to use. Defaults to None. If None, a new pipeline will be created.

    Returns:
        str: The generated output.
    """
    if generator is None:
        generator = get_transformers_pipeline()

    response = generator(prompt, max_length=100, do_sample=True)

    return response[0]["generated_text"]
