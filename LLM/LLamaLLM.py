from llama_cpp import Llama


def get_pipeline(model_name: str = "Qwen/Qwen2-0.5B-Instruct-GGUF"):
    """
    Load the Llama pipeline from the model name

    Args:
        model_name (str): The model name to load

    Returns:
        Llama: The Llama pipeline
    """
    return Llama.from_pretrained(
        repo_id=model_name, filename="*q2_k.gguf", verbose=False
    )


def generate_output(prompt: str, pipeline: Llama) -> str:
    """
    Generate output from the prompt using the Llama pipeline

    Args:
        prompt (str): The prompt to generate the output from
        pipeline (Llama): The pipeline to use

    Returns:
        str: The generated output
    """
    return pipeline.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant in a university environment. Help professors and students with their questions and problems. \n"
                + "You will recieve redacted content inside of square brackets, use it as if you have the information.",
            },
            {"role": "user", "content": prompt},
        ]
    )["choices"][0]["message"]["content"]
