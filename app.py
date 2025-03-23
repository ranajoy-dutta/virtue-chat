import asyncio
from config.config_loader import ConfigLoader
from core.interfaces.llm_provider import LLMFactory
from core.services.chat_service import ChatService
from core.database.repository import ChatRepository
from ui.pages.chat import ChatUI

async def main():
    # Load configuration
    config = ConfigLoader()
    
    # Initialize database
    chat_repository = ChatRepository(config.database.url)
    
    # Initialize LLM provider
    default_provider = config.llm.default_provider
    provider_config = config.llm.providers[default_provider]
    llm_provider = LLMFactory.create(default_provider, provider_config)
    
    # Initialize chat service
    chat_service = ChatService(
        llm_provider=llm_provider,
        chat_repository=chat_repository,
        config=config.chat 
    )
    
    # Initialize and render UI
    chat_ui = ChatUI(chat_service)
    chat_ui.render() 

if __name__ == "__main__":
    asyncio.run(main())