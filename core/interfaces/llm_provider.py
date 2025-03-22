from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate_response(self, prompt: str, history: List[Dict[str, str]] = None) -> str:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        pass


class LLMFactory:
    """Factory class for creating LLM providers."""

    @staticmethod
    def create(provider: str, config: Dict[str, Any]) -> LLMProvider:
        """Create an LLM provider instance based on configuration."""
        from infrastructure.llm.mistral import MistralProvider
        # from infrastructure.llm.openai import OpenAIProvider
        # from infrastructure.llm.gemini import GeminiProvider

        providers = {
            'mistral': MistralProvider,
            # 'openai': OpenAIProvider,
            # 'gemini': GeminiProvider
        }

        if provider not in providers:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        return providers[provider](config)