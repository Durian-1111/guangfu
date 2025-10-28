"""
对话管理器
负责管理用户与智能体的对话历史
"""

from typing import Dict, List, Any, Optional
import json
import asyncio
from datetime import datetime
import sqlite3
import os

class ConversationManager:
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建对话表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                agent_response TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建会话表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def save_conversation(self, session_id: str, user_message: str, 
                              agent_response: str, agent_type: str) -> bool:
        """保存对话记录"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conversations (session_id, user_message, agent_response, agent_type)
                VALUES (?, ?, ?, ?)
            """, (session_id, user_message, agent_response, agent_type))
            
            # 更新会话活动时间
            cursor.execute("""
                INSERT OR REPLACE INTO sessions (id, last_activity)
                VALUES (?, CURRENT_TIMESTAMP)
            """, (session_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"保存对话记录失败: {e}")
            return False
    
    async def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取对话历史"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_message, agent_response, agent_type, timestamp
                FROM conversations
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (session_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            conversations = []
            for row in rows:
                conversations.append({
                    "user_message": row[0],
                    "agent_response": row[1],
                    "agent_type": row[2],
                    "timestamp": row[3]
                })
            
            return conversations
            
        except Exception as e:
            print(f"获取对话历史失败: {e}")
            return []
    
    async def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取会话信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT created_at, last_activity
                FROM sessions
                WHERE id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "session_id": session_id,
                    "created_at": row[0],
                    "last_activity": row[1]
                }
            return None
            
        except Exception as e:
            print(f"获取会话信息失败: {e}")
            return None
    
    async def create_session(self, session_id: str) -> bool:
        """创建新会话"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO sessions (id, created_at, last_activity)
                VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (session_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"创建会话失败: {e}")
            return False
    
    async def get_active_sessions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取活跃会话列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT s.id, s.created_at, s.last_activity, COUNT(c.id) as message_count
                FROM sessions s
                LEFT JOIN conversations c ON s.id = c.session_id
                GROUP BY s.id, s.created_at, s.last_activity
                ORDER BY s.last_activity DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            sessions = []
            for row in rows:
                sessions.append({
                    "session_id": row[0],
                    "created_at": row[1],
                    "last_activity": row[2],
                    "message_count": row[3]
                })
            
            return sessions
            
        except Exception as e:
            print(f"获取活跃会话失败: {e}")
            return []
    
    async def delete_session(self, session_id: str) -> bool:
        """删除会话"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 删除对话记录
            cursor.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
            
            # 删除会话记录
            cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"删除会话失败: {e}")
            return False
    
    async def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户的所有对话记录（返回活跃会话列表）"""
        return await self.get_active_sessions()

