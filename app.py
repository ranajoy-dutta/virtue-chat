import asyncio
from config.config_loader import ConfigLoader
from core.interfaces.llm_provider import LLMFactory
from core.services.chat_service import ChatService
from infrastructure.database.repository import ChatRepository
from ui.pages.chat import ChatUI

async def main():
    # Load configuration
    config = ConfigLoader()
    
    # Initialize database
    chat_repository = ChatRepository(config.get_database_config()['url'])
    
    # Initialize LLM provider
    llm_config = config.get_llm_config()
    default_provider = llm_config['default_provider']
    provider_config = llm_config['providers'][default_provider]
    llm_provider = LLMFactory.create(default_provider, provider_config)
    
    # Initialize chat service
    chat_service = ChatService(
        llm_provider=llm_provider,
        chat_repository=chat_repository,
        config=config.get_chat_config()
    )
    
    # Initialize and render UI
    chat_ui = ChatUI(chat_service)
    chat_ui.render()  # removed await as render is synchronous

if __name__ == "__main__":
    asyncio.run(main())