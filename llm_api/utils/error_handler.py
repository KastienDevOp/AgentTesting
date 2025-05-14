import logging
from typing import Callable, Any

class LLMProviderError(Exception):
    """
    Custom exception for LLM provider-related errors.
    """
    pass

def handle_provider_errors(func: Callable) -> Callable:
    """
    Decorator to handle errors in LLM provider methods.
    
    :param func: Function to wrap
    :return: Wrapped function with error handling
    """
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"LLM Provider Error: {e}")
            raise LLMProviderError(f"Error in {func.__name__}: {str(e)}") from e
    return wrapper
