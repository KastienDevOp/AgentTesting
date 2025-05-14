# Mistral AI Python Client

## Overview
A Python client for interacting with Mistral AI's language models, supporting both chat and code generation.

## Features
- Easy interaction with Mistral's chat models
- Support for multiple models (mistral-large-latest, codestral-latest)
- Simple configuration and usage
- Error handling

## Usage Example

```python
import os
from llm_api.providers.mistral_provider import MistralProvider

# Set your API key
os.environ['MISTRAL_API_KEY'] = 'your-api-key-here'

# Initialize Mistral Provider
mistral = MistralProvider()

# Chat Completion
messages = [
    {"role": "user", "content": "What is the best French cheese?"}
]
response = mistral.chat_completion(messages)
print(response)

# Code Generation with Codestral
code_messages = [
    {"role": "user", "content": "Write a Python function to calculate Fibonacci"}
]
mistral_code = MistralProvider(config={'model': 'codestral-latest'})
code_response = mistral_code.chat_completion(code_messages)
print(code_response)
```

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
- Set `MISTRAL_API_KEY` environment variable
- Optionally specify model in configuration dictionary

## Models Supported
- `mistral-large-latest`
- `codestral-latest`

## Contributing
Contributions welcome! Ensure code follows existing patterns.
