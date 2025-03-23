from typing import Dict, List, Optional
from core.interfaces.llm_provider import LLMProvider
from core.database.repository import ChatRepository

class ChatService:
    def __init__(self, llm_provider: LLMProvider, chat_repository: ChatRepository, config: Dict):
        self.llm_provider = llm_provider
        self.chat_repository = chat_repository
        self.max_history = config.get('max_history', 50)
    
    async def create_session(self) -> str:
        """Create a new chat session."""
        return self.chat_repository.create_chat_session()
    
    async def _get_history_and_store(self, session_id: str, message: str):
        self.chat_repository.add_message(session_id, "user", message)
        return self.chat_repository.get_chat_history(session_id, self.max_history)

    async def send_message(self, session_id: str, message: str):
        """Get a full response from LLM (non-streaming)."""
        history = await self._get_history_and_store(session_id, message)
        response = await self.llm_provider.generate_response(message, history)  
        self.chat_repository.add_message(session_id, "assistant", response)
        return response

    async def send_message_stream(self, session_id: str, message: str):
        """Stream response from LLM."""
        history = await self._get_history_and_store(session_id, message)
        response = ""  

        async for chunk in self.llm_provider.generate_response_stream(message, history):
            response += chunk
            yield chunk 
        self.chat_repository.add_message(session_id, "assistant", response)
    
    def get_chat_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get chat history for a session."""
        return self.chat_repository.get_chat_history(session_id, limit or self.max_history)