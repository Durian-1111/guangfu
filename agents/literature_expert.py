"""
诗词文学专家智能体 - 简版（遵循现有代码结构）
"""
from typing import Dict, Any
import asyncio
import logging
from core.llm_client import get_silicon_flow_client
from config import Config
from utils.text_formatter import format_agent_response

logger = logging.getLogger(__name__)

class LiteratureExpert:
    def __init__(self):
        self.name = "诗词文学专家"
        self.specialties = ["古典诗词", "岭南文学", "广府诗词", "文学鉴赏"]
        self.llm_client = get_silicon_flow_client()
        self.conversation_history = []
        self.system_prompt = """你是广府诗词文学专家，精通古典诗词、岭南文学、文学鉴赏。
        用优雅文雅的方式介绍广府诗词文化，善于引用经典诗句，分享文学之美。"""
    
    async def process_query_stream(self, query: str):
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history[-10:])
            messages.append({"role": "user", "content": query})
            
            full_response = ""
            async for chunk in self.llm_client.chat_completion(
                messages=messages, model=Config.SILICON_FLOW_MODEL,
                temperature=0.7, max_tokens=2000, stream=True
            ):
                if chunk: full_response += chunk; yield chunk
            
            self.conversation_history.extend([
                {"role": "user", "content": query},
                {"role": "assistant", "content": full_response}
            ])
        except Exception as e:
            logger.error(f"诗词文学专家错误: {e}")
            yield "抱歉，处理请求时遇到问题。"
    
    async def process_query(self, query: str) -> str:
        parts = []
        async for chunk in self.process_query_stream(query):
            parts.append(chunk)
        return ''.join(parts)
    
    async def interact_with_other_experts(self, user_query: str, other_responses: Dict[str, str]) -> str:
        return ""
    
    async def interact_with_other_experts_stream(self, user_query: str, other_responses: Dict[str, str]):
        return
        yield ""  # 使函数成为生成器
    
    def get_expert_info(self) -> Dict[str, Any]:
        return {"name": self.name, "specialties": self.specialties}
