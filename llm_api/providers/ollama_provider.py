from llm_api.interfaces.base_provider import BaseProvider

class OllamaProvider(BaseProvider):
    def __init__(self, config=None):
        super().__init__()
        self.config = config or {}

    def chat_completion(self, messages):
        # Implement chat completion logic
        pass
