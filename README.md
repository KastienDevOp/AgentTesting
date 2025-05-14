# LLM API Client

## Overview
A Python client for interacting with various language models, supporting both chat and code generation.

## Features
- Easy interaction with multiple language models
- Support for various models (Mistral, Ollama, etc.)
- Simple configuration and usage
- Error handling

## Usage Example

### Mistral Provider
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

### Ollama Provider
```python
import os
from llm_api.providers.ollama_provider import OllamaProvider

# Set your API key
os.environ['OLLAMA_API_KEY'] = 'your-api-key-here'

# Initialize Ollama Provider
ollama = OllamaProvider()

# Chat Completion
messages = [
    {"role": "user", "content": "What is the best French cheese?"}
]
response = ollama.chat_completion(messages)
print(response)

# Code Generation with Ollama
code_messages = [
    {"role": "user", "content": "Write a Python function to calculate Fibonacci"}
]
ollama_code = OllamaProvider(config={'model': 'ollama-code-latest'})
code_response = ollama_code.chat_completion(code_messages)
print(code_response)
```

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
- Set `MISTRAL_API_KEY` or `OLLAMA_API_KEY` environment variable
- Optionally specify model in configuration dictionary

## Models Supported
- Mistral: `mistral-large-latest`, `codestral-latest`
- Ollama: `ollama-chat-latest`, `ollama-code-latest`

## Contributing
Contributions welcome! Ensure code follows existing patterns.
