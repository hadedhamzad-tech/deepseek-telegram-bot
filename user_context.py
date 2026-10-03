from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from config import settings
from logger import logger


@dataclass
class UserContext:
    user_id: int
    username: str
    chat_history: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_interaction: datetime = field(default_factory=datetime.now)
    model: str = "deepseek-chat"
    reasoning_enabled: bool = True
    max_history: int = settings.MAX_HISTORY
    
    def add_message(self, role: str, content: str):
        self.chat_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
        self.last_interaction = datetime.now()
        
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]
    
    def get_messages(self):
        return [{"role": m["role"], "content": m["content"]} for m in self.chat_history]
    
    def clear_history(self):
        self.chat_history = []
        logger.info(f"Cleared history for user {self.user_id}")
    
    def is_expired(self):
        age_seconds = (datetime.now() - self.last_interaction).total_seconds()
        return age_seconds > settings.CONTEXT_TIMEOUT


class UserContextManager:
    def __init__(self):
        self.contexts: Dict[int, UserContext] = {}
        logger.info("UserContextManager initialized")
    
    def get_context(self, user_id: int, username: str = "Unknown") -> UserContext:
        if user_id not in self.contexts:
            self.contexts[user_id] = UserContext(user_id=user_id, username=username)
            logger.info(f"Created context for user {user_id}")
        return self.contexts[user_id]
    
    def clear_context(self, user_id: int):
        if user_id in self.contexts:
            del self.contexts[user_id]
            logger.info(f"Cleared context for user {user_id}")
    
    def clear_expired(self):
        expired = [uid for uid, ctx in self.contexts.items() if ctx.is_expired()]
        for uid in expired:
            del self.contexts[uid]
        if expired:
            logger.info(f"Cleared {len(expired)} expired contexts")
    
    def stats(self):
        return {
            "active_users": len(self.contexts),
            "total_messages": sum(len(ctx.chat_history) for ctx in self.contexts.values()),
        }


context_manager = UserContextManager()
