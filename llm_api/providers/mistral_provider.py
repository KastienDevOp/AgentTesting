import os
from typing import List, Dict, Any, Optional
from mistralai import Mistral
from ..interfaces.base_provider import BaseLLMProvider
from ..core.config_manager import ConfigManager
from ..utils.error_handler import handle_provider_errors

class MistralProvider(BaseLLMProvider):
    """
    Mistral AI Provider implementation.
    Supports both chat and code generation models.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Mistral AI provider.
        
        :param config: Configuration dictionary
        """
        self.config = config or ConfigManager.load_config('mistral')
        
        # Prioritize config API key, then environment variable
        api_key = (
            self.config.get('api_key') or 
            os.environ.get('MISTRAL_API_KEY')
        )
        
        if not api_key:
            raise ValueError("Mistral API key must be provided in config or MISTRAL_API_KEY environment variable")
        
        self.client = Mistral(api_key=api_key)
        self.model = self.config.get('model', 'mistral-large-latest')
    
    @handle_provider_errors
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate chat completion using Mistral's Chat API.
        
        :param messages: List of message dictionaries
        :param max_tokens: Maximum number of tokens to generate
        :param temperature: Sampling temperature
        :return: Generated chat response
        """
        # Merge config with passed kwargs
        generation_config = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            **({'max_tokens': max_tokens} if max_tokens else {}),
            **kwargs
        }
        
        response = self.client.chat.complete(**generation_config)
        return response.choices[0].message.content
    
    def generate_text(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text by converting prompt to chat messages.
        
        :param prompt: Input text prompt
        :param max_tokens: Maximum number of tokens to generate
        :param temperature: Sampling temperature
        :return: Generated text response
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(
            messages, 
            max_tokens=max_tokens, 
            temperature=temperature, 
            **kwargs
        )
    
    def get_token_count(self, text: str) -> int:
        """
        Estimate token count for Mistral models.
        Note: This is a rough estimation and may not be 100% accurate.
        
        :param text: Input text to count tokens
        :return: Estimated number of tokens
        """
        # Simple estimation: ~4 characters per token
        return len(text) // 4
