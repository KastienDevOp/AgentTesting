# Chalice Forged

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Available Providers](#available-providers)
- [Contributing](#contributing)
- [License](#license)

## Overview

Chalice Forged is a provider-agnostic client designed to simplify interactions with various large language model (LLM) providers. It allows you to switch between different providers like OpenAI, Anthropic, Google, and local models like Ollama without modifying your code. This library abstracts away the provider-specific API calls, offering a consistent interface for chat completions, text completions, and streaming responses.

## Features

- **Provider Agnostic:** Supports multiple LLM providers, including OpenAI, Anthropic, Google, Mistral, Cohere, Hugging Face, and Ollama.
- **Easy Configuration:** Uses a simple configuration management system to handle API keys and provider settings.
- **Basic and Advanced Features:** Supports both basic chat and text completion, as well as advanced features like streaming.
- **Local and Remote Models:** Works with both local models (e.g., Ollama) and remote API providers.

## Getting Started

### Prerequisites

- Python 3.7+
- API keys for the providers you wish to use (e.g., OpenAI, Anthropic, Google).
- [Ollama](https://ollama.ai) (for local model usage).

### Installation

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

### Configuration

1.  **API Keys:**
    - Set environment variables for each provider's API key. For example:
      ```bash
      export OPENAI_API_KEY='your-openai-key'
      export ANTHROPIC_API_KEY='your-anthropic-key'
      export GOOGLE_API_KEY='your-google-key'
      ```
    - Alternatively, create a `.env` file in the project root with your API keys:
      ```
      OPENAI_API_KEY=your-openai-key
      ANTHROPIC_API_KEY=your-anthropic-key
      GOOGLE_API_KEY=your-google-key
      ```
    - The `.env` file is gitignored to prevent accidental commits of your keys.

2.  **Ollama (Local Model):**
    - Install Ollama from [https://ollama.ai](https://ollama.ai).
    - Run your desired model:
      ```bash
      ollama run llama2
      ```

## Basic Usage

Here's how to use Chalice Forged with a local Ollama model:

```python
from chalice_forged import create_client

# Create client with any provider
client = create_client("ollama", base_url="http://localhost:11434", model="qwen3", api_key="your-key")
response = client.chat([{"role": "user", "content": "Hello!"}])

for chunk in client.stream_chat([{"role": "user", "content": "Hello!"}]):
    print(chunk["content"], end="", flush=True)
print()
```

## Advanced Features

```python
from chalice_forged import create_client

client = create_client("ollama", model="llama2")

# Text completion
text_response = client.complete("The future of AI is")
print(f"Text completion: {text_response['content'][:50]}...")

# Chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"}
]
chat_response = client.chat(messages)
print(f"Chat completion: {chat_response['content'][:50]}...")

# Streaming
print("Streaming response: ", end="")
for chunk in client.stream_chat(messages):
    if chunk.get("success") and chunk.get("content"):
        print(chunk["content"], end="", flush=True)
        break  # Just show first chunk for demo
print("\n(streaming truncated for demo)")
```

## Available Providers

<details>
  <summary>Supported Providers</summary>

- Anthropic
- Cohere
- Google
- Hugging Face
- Mistral
- Ollama
- OpenAI
</details>

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive commit messages.
4.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
