from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from .models import ChatSession, ChatMessage


class ChatRepository:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def create_chat_session(self) -> str:
        """Create a new chat session and return its ID."""
        with self.get_session() as session:
            chat_session = ChatSession(session_id=str(uuid.uuid4()))
            session.add(chat_session)
            session.commit()
            return chat_session.session_id
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to a chat session."""
        with self.get_session() as session:
            if not session.query(ChatSession).filter_by(session_id=session_id).first():
                raise ValueError(f"Chat session {session_id} not found")
            message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content
            )
            session.add(message)
            session.commit()
    
    def get_chat_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get chat history for a session."""
        with self.get_session() as session:
            chat_session = session.query(ChatSession).filter_by(session_id=session_id).first()
            if not chat_session:
                return []
            
            query = session.query(ChatMessage).filter_by(session_id=chat_session.id).order_by(ChatMessage.created_at)
            if limit:
                query = query.limit(limit)
            
            messages = query.all()
            return [{"role": msg.role, "content": msg.content} for msg in messages]
    
    def delete_chat_session(self, session_id: str) -> None:
        """Delete a chat session and all its messages."""
        with self.get_session() as session:
            chat_session = session.query(ChatSession).filter_by(session_id=session_id).first()
            if chat_session:
                session.delete(chat_session)
                session.commit()