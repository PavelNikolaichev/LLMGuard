LLMGuard is a project that utilizes Gradio and LLMGuard to protect users from leaking personal information in a university environment.
Our project aims to hide sensitive info for NYU students in particular, so some of the scanners might require additional changes if you want to use it for another university.

## Installation

To install LLMGuard, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/LLMGuard.git`
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage

To run this project, follow these steps:

1. Run `main.py`: `python main.py`

## TODO

- [ ] Implement scanners to detect personal information leakage. :mag: - in progress
- [x] Consider using regex scanner for more accurate detection. :dart:
- [ ] Implement real LLM (Leakage Limiting Mechanism) instead of the mock version. :gear:
- [x] Generate tests to automate the testing process. :test_tube:
