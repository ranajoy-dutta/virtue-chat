import gradio as gr
import asyncio
from core.services.chat_service import ChatService


class ChatUI:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service
        self.session_id = None

    async def initialize_session(self):
        if not self.session_id:
            self.session_id = await self.chat_service.create_session()
        return self.session_id

    async def chat_function(self, user_message, history):
        session_id = await self.initialize_session()
        response = await self.chat_service.send_message(session_id, user_message) 
        return response  

    async def chat_function_stream(self, user_message, history):
        session_id = await self.initialize_session()
        response = "" 

        async for part in self.chat_service.send_message_stream(session_id, user_message):
            response += part  
            yield response 

    
    def render(self, stream=True):
        chat_fn = self.chat_function_stream if stream else self.chat_function

        demo = gr.ChatInterface(
            chat_fn,
            type="messages",
            save_history=True,
        ).launch()