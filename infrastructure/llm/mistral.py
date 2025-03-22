from typing import List, Dict, Any
import mistralai
from core.interfaces.llm_provider import LLMProvider
from mistralai import Mistral

from langchain_mistralai import ChatMistralAI
from typing import AsyncGenerator

class MistralProvider(LLMProvider):
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config['api_key']
        self.model = config['model']
        self.client = ChatMistralAI(
            model=self.model,
            temperature=0,
            max_retries=2,
            api_key=self.api_key,
        )

    async def generate_response(self, prompt: str, history: List[Dict[str, str]] = None) -> str:
        """Standard response (non-streaming)."""
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in history or []]
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.client.ainvoke(messages)  
            return response.content
        except Exception as e:
            raise Exception(f"Error generating response from Mistral: {str(e)}")

    async def generate_response_stream(
        self, prompt: str, history: List[Dict[str, str]] = None
    ) -> AsyncGenerator[str, None]:
        """Streaming response."""
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in history or []]
        messages.append({"role": "user", "content": prompt})

        try:
            async for chunk in self.client.astream(messages):
                yield chunk.content 
        except Exception as e:
            raise Exception(f"Error generating response from Mistral: {str(e)}")
    
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": "mistral",
            "model": self.model,
            "capabilities": ["chat", "completion"]
        }