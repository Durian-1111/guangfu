"""
核心模块
包含对话管理、知识库等核心功能
"""

from .conversation_manager import ConversationManager
from .knowledge_base import KnowledgeBase

__all__ = [
    "ConversationManager",
    "KnowledgeBase"
]

