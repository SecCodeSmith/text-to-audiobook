# Contributing to text-to-audiobook

First off, thanks for taking the time to contribute! 🎉

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (OS, Python version, GPU type, etc.)
* **Include relevant logs** from `logs/pipeline.log`

### Suggesting Enhancements

When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and what the expected behavior would be**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Styleguides

### Python Styleguide

* Use [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use meaningful variable names
* Keep functions focused and single-purpose
* Add docstrings to public functions
* Use type hints where applicable

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Documentation Styleguide

* Use Markdown for documentation
* Reference code blocks with triple backticks (```)
* Add code examples for new features
* Keep documentation up-to-date with code changes

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ai-tts-v7.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install dev dependencies: `pip install -r requirements.txt && pip install pytest pytest-cov`
6. Create a branch for your changes: `git checkout -b my-feature-branch`

## Testing

* Write tests for new features
* Ensure all existing tests pass: `pytest -v`
* Check test coverage: `pytest --cov=src`
* Run the full test suite before submitting a PR

## Running Tests Locally

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_gui.py

# Run specific test
pytest tests/test_gui.py::test_gui_launch
```

## Before You Submit

* Check your code against PEP 8
* Run the test suite
* Update the README.md if you've changed functionality
* Add tests for new functionality
* Ensure your branch is up-to-date with main

## Additional Notes

* Ask any questions in discussions before starting work on significant changes
* Consider opening an issue first to discuss major changes
* Be respectful and constructive in all interactions

Thank you for contributing to text-to-audiobook! 🚀
