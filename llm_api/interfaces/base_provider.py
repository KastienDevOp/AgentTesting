from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLMProvider(ABC):
    """
    Base class for Mistral AI language models.
    Defines the core interface for text generation and chat completion.
    """
    
    @abstractmethod
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate a chat completion response.
        
        :param messages: List of message dictionaries with 'role' and 'content'
        :param max_tokens: Maximum number of tokens to generate
        :param temperature: Sampling temperature for text generation
        :return: Generated chat response
        """
        pass
    
    def generate_text(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text by converting prompt to a chat message.
        
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
        
        :param text: Input text to count tokens
        :return: Estimated number of tokens
        """
        # Simple estimation: ~4 characters per token
        return len(text) // 4
