from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from config import settings
from logger import logger


@dataclass
class UserContext:
    """Store user conversation context for multi-turn conversations"""
    
    user_id: int
    username: str
    chat_history: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_interaction: datetime = field(default_factory=datetime.now)
    model: str = "deepseek-chat"
    max_history: int = settings.MAX_HISTORY
    reasoning_enabled: bool = True
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.chat_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
        self.last_interaction = datetime.now()
        
        # Keep only last max_history messages
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]
    
    def get_messages(self) -> List[Dict]:
        """Get messages in API format (without timestamps)"""
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.chat_history
        ]
    
    def clear_history(self):
        """Clear conversation history"""
        self.chat_history = []
        logger.info(f"Cleared history for user {self.user_id}")
    
    def get_context_summary(self) -> str:
        """Get summary of current context"""
        return (
            f"👤 کاربر: {self.username} (ID: {self.user_id})\n"
            f"💬 پیام‌ها: {len(self.chat_history)}\n"
            f"🤖 مدل: {self.model}\n"
            f"🧠 استدلال: {'✅ فعال' if self.reasoning_enabled else '❌ غیرفعال'}\n"
            f"⏰ آخرین تعامل: {self.last_interaction.strftime('%H:%M:%S')}"
        )
    
    def is_expired(self, timeout_hours: int = None) -> bool:
        """Check if context has expired"""
        timeout = timeout_hours or (settings.CONTEXT_TIMEOUT / 3600)
        age = (datetime.now() - self.last_interaction).total_seconds() / 3600
        return age > timeout


class UserContextManager:
    """Manage user contexts for multiple users"""
    
    def __init__(self):
        self.contexts: Dict[int, UserContext] = {}
        logger.info("UserContextManager initialized")
    
    def get_context(self, user_id: int, username: str = "Unknown") -> UserContext:
        """Get or create user context"""
        if user_id not in self.contexts:
            self.contexts[user_id] = UserContext(user_id=user_id, username=username)
            logger.info(f"Created new context for user {user_id}")
        return self.contexts[user_id]
    
    def remove_context(self, user_id: int):
        """Remove user context"""
        if user_id in self.contexts:
            del self.contexts[user_id]
            logger.info(f"Removed context for user {user_id}")
    
    def get_all_contexts(self) -> Dict[int, UserContext]:
        """Get all user contexts"""
        return self.contexts
    
    def get_active_users_count(self) -> int:
        """Get number of active users"""
        return len(self.contexts)
    
    def get_total_messages(self) -> int:
        """Get total messages across all users"""
        return sum(len(ctx.chat_history) for ctx in self.contexts.values())
    
    def clear_expired_contexts(self, timeout_hours: int = None):
        """Clear contexts older than timeout"""
        timeout = timeout_hours or (settings.CONTEXT_TIMEOUT / 3600)
        to_remove = []
        
        for user_id, context in self.contexts.items():
            if context.is_expired(timeout):
                to_remove.append(user_id)
        
        for user_id in to_remove:
            self.remove_context(user_id)
        
        if to_remove:
            logger.info(f"Cleared {len(to_remove)} expired contexts")
    
    def get_stats(self) -> dict:
        """Get context manager statistics"""
        return {
            "active_users": self.get_active_users_count(),
            "total_messages": self.get_total_messages(),
            "timestamp": datetime.now().isoformat()
        }


# Global context manager
context_manager = UserContextManager()
