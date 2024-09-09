---
title: Student LLM Guard
emoji: ⚡
colorFrom: gray
colorTo: purple
sdk: gradio
sdk_version: 4.41.0
app_file: main.py
pinned: false
---

# LLMGuard

LLMGuard is a project that utilizes Presidio to protect users from leaking personal information in a university-like environment.
Our project aims to hide sensitive info for NYU students in particular, so some of the functionality might require additional changes if you want to use it for another university.
In this repo, Gradio is utilized to showcase the functionality provided.

## Demo

You can test functionality via [HuggingFace Spaces](https://huggingface.co/spaces/retereum/student-llm-guard)

## Installation

To install LLMGuard, follow these steps:

1. Clone the repository: `git clone https://github.com/PavelNikolaichev/LLMGuard.git`
2. Install the required dependencies:
   ```python
   pip install -r requirements.txt
   ```

## Usage

To run this project, follow these steps:

1. Run `main.py`: `python main.py`
2. Open the provided link in your browser
