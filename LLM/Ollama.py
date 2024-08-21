from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


def get_ollama_llm() -> ChatPromptTemplate | OllamaLLM:
    """
    Function to get an Ollama langchain that can be used to generate output.

    Returns:
        ChatPromptTemplate | OllamaLLM: The OllamaLLM instance.
    """
    template = """Question: {question} Answer: Let's think step by step."""

    prompt = ChatPromptTemplate.from_template(template)

    model = OllamaLLM(model="gemma2:2b")

    chain = prompt | model

    return chain


def generate_ollama_output(prompt: str, llm: ChatPromptTemplate | None = None) -> str:
    """
    Function to generate an output from the Ollama langchain.

    Args:
        prompt (str): The prompt to generate the output.
        llm (ChatPromptTemplate | None, optional): The Ollama langchain to use. Defaults to None. If None, a new langchain will be created.
    Returns:
        str: The generated output.
    """
    if llm is None:
        llm = get_ollama_llm()

    return llm.invoke({"question": prompt})
