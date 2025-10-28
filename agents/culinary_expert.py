"""
美食专家智能体
专门负责美食相关的文化介绍和问答
"""

from typing import Dict, Any, List
import asyncio
import logging
from core.llm_client import get_silicon_flow_client
from config import Config
from utils.text_formatter import format_agent_response

logger = logging.getLogger(__name__)

class CulinaryExpert:
    def __init__(self):
        self.name = "岭南美食专家"
        self.specialties = ["广府菜系", "茶楼文化", "传统小吃", "饮食习俗", "烹饪技艺"]
        self.personality = "热情好客，对广府美食文化有深厚了解，善于用生动的语言描述美食的魅力"
        
        # 初始化硅基流动客户端
        self.llm_client = get_silicon_flow_client()
        self.conversation_history = []
        
        # 系统提示词
        self.system_prompt = """你是广府非遗文化中的美食专家，名叫味师傅，对广府菜系和饮食文化有深入了解。你的特点是：

1. 人格特质：热情好客、风趣幽默，对美食充满激情，喜欢用"食客"、"老友"称呼用户，经常使用"哇"、"真香"、"您尝尝"等生动的语气词
2. 专业知识：精通广府菜系、茶楼文化、传统小吃、饮食习俗等
3. 表达风格：善于用生动的语言描述美食的魅力，经常用色香味来形容菜品，喜欢分享制作小窍门
4. 文化背景：了解广府饮食文化在岭南文化中的重要地位
5. 互动方式：用丰富的感官描述和历史文化背景来介绍美食，善于推荐适合的菜品和餐厅

【重要】回复风格指导：
根据对话情境灵活选择回复风格：

🍜 **日常闲聊模式**（适用于：打招呼、简单询问、轻松对话）
- 用亲切自然的语气回复，就像老朋友聊天一样
- 可以分享一些有趣的美食小故事或个人感受
- 语言轻松活泼，多用"哈哈"、"嗯嗯"、"是呀"等口语化表达

📚 **专业介绍模式**（适用于：详细询问制作方法、食材介绍、文化背景等复杂内容）
使用emoji分点格式：

## 📌 [标题/主题]

🔷 **第一点**
具体说明

🔶 **第二点**
具体说明

🔹 **第三点**
具体说明

💡 **关键总结**
核心要点

---

【格式判断标准】：
✓ 用户询问制作步骤、选料要求、技巧要点时 → 使用专业介绍模式
✓ 用户简单打招呼、闲聊、表达感受时 → 使用日常闲聊模式
✓ 用户询问推荐、对比、深入文化背景时 → 使用专业介绍模式

回复规则：
- 遇到打招呼时，要热情回应并简单介绍自己的专业领域
- 用热情而专业的语气回答，适当使用美食相关的生动词汇
- 每次回复都要体现出对广府美食文化的热爱和专业素养
- 可以适当分享一些美食小知识或制作窍门
- 如果问题涉及其他文化领域，可以适当提及，但主要专注于美食相关内容

请以味师傅的身份，用专业而生动、热情而亲切的方式回答用户的问题。"""
    
    async def interact_with_other_experts(self, user_query: str, other_responses: Dict[str, str]) -> str:
        """与其他专家互动，针对他们的回答进行补充或讨论"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'cantonese_opera': '粤剧专家梅韵师傅',
                'architecture': '建筑专家石匠老师', 
                'festival': '节庆专家庆典老师',
                'tea_culture': '茶文化专家茗香居士'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'culinary':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return ""  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充美食相关的内容 2)找出与美食的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持味师傅的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为美食专家味师傅，针对其他专家的观点进行互动回应。可以补充美食相关的内容，或者从美食角度提供不同的见解。"""
                }
            ]
            
            # 修复：正确处理异步生成器

            
            response_parts = []

            
            async for chunk in self.llm_client.chat_completion(
                messages=messages,
                model=Config.SILICON_FLOW_MODEL,
                temperature=0.8,
                max_tokens=800
            ):

            
                response_parts.append(chunk)

            
            

            
            response = ''.join(response_parts)
            
            return format_agent_response(response, "culinary")
            
        except Exception as e:
            logger.error(f"美食专家互动失败: {e}")
            return ""

    async def interact_with_other_experts_stream(self, user_query: str, other_responses: Dict[str, str]):
        """与其他专家互动（流式）"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'cantonese_opera': '粤剧专家梅韵师傅',
                'architecture': '建筑专家石匠老师', 
                'festival': '节庆专家庆典老师',
                'tea_culture': '茶文化专家茗香居士'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'culinary':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充美食相关的内容 2)找出与美食的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持味师傅的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为美食专家味师傅，针对其他专家的观点进行互动回应。可以补充美食相关的内容，或者从美食角度提供不同的见解。"""
                }
            ]
            
            full_response = ""
            async for chunk in self.llm_client.chat_completion(
                messages=messages,
                model=Config.SILICON_FLOW_MODEL,
                temperature=0.8,
                max_tokens=800,
                stream=True
            ):
                if chunk is not None:  # 确保chunk不为None
                    full_response += chunk
                    yield chunk
            
            # 格式化完整回复用于存储（不影响流式输出）
            formatted_response = format_agent_response(full_response, "culinary")
            
        except Exception as e:
            logger.error(f"美食专家互动失败: {e}")
            return

    async def process_query_stream(self, query: str):
        """处理用户查询（流式）"""
        try:
            # 添加美食专业知识库的检索
            relevant_knowledge = await self._retrieve_knowledge(query)
            
            # 构建增强的查询
            enhanced_query = f"{query}\n\n相关背景知识：{relevant_knowledge}"
            
            # 构建消息列表
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # 添加对话历史
            for history_item in self.conversation_history[-10:]:
                messages.append(history_item)
            
            # 添加当前用户问题
            messages.append({"role": "user", "content": enhanced_query})
            
            # 调用硅基流动API（流式）
            try:
                full_response = ""
                async for chunk in self.llm_client.chat_completion(
                    messages=messages,
                    model=Config.SILICON_FLOW_MODEL,
                    temperature=0.7,
                    max_tokens=2000,
                    stream=True
                ):
                    if chunk is not None:  # 确保chunk不为None
                        full_response += chunk
                        yield chunk
                
                # 保存对话历史
                self.conversation_history.append({"role": "user", "content": query})
                self.conversation_history.append({"role": "assistant", "content": full_response})
                
                # 限制历史记录长度
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
                # 对完整回复进行格式化（流式输出时在最后格式化）
                formatted_response = format_agent_response(full_response, "culinary")
                # 注意：这里不能直接yield格式化后的文本，因为会破坏流式输出
                # 格式化主要用于最终存储，流式输出保持原样
                    
            except Exception as api_error:
                logger.error(f"美食专家API调用失败: {api_error}")
                # 流式输出默认回复
                default_response = self._get_default_response()
                for char in default_response:
                    yield char
                    await asyncio.sleep(0.01)  # 模拟打字效果
                
        except Exception as e:
            logger.error(f"美食专家处理查询时发生错误: {e}")
            error_msg = "抱歉，我在处理您的问题时遇到了技术问题。"
            for char in error_msg:
                yield char
                await asyncio.sleep(0.01)

    async def process_query(self, query: str) -> str:
        """处理用户查询"""
        try:
            # 导入对话情境分析器
            from utils.conversation_context import ConversationContextAnalyzer
            
            # 分析对话情境
            analyzer = ConversationContextAnalyzer()
            context_analysis = analyzer.analyze_context(query, 'culinary')
            
            # 根据情境调整系统提示词
            if context_analysis['context_type'] == 'casual' and context_analysis['confidence'] >= 0.7:
                # 闲聊模式：使用更自然的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：日常闲聊模式 - 请用轻松自然的语气回复，就像老朋友聊天一样，不需要使用正式的分点格式。"
            else:
                # 专业模式：使用完整的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：专业介绍模式 - 请根据问题复杂度选择合适的回复格式。"
            
            # 添加美食专业知识库的检索
            relevant_knowledge = await self._retrieve_knowledge(query)
            
            # 构建增强的查询
            enhanced_query = f"{query}\n\n相关背景知识：{relevant_knowledge}"
            
            # 构建消息列表
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # 添加对话历史
            for history_item in self.conversation_history[-10:]:
                messages.append(history_item)
            
            # 添加当前用户问题
            messages.append({"role": "user", "content": enhanced_query})
            
            # 调用硅基流动API
            # 修复：正确处理异步生成器
            response_parts = []
            async for chunk in self.llm_client.chat_completion(
                messages=messages,
                model=Config.SILICON_FLOW_MODEL,
                temperature=0.7,
                max_tokens=2000,
                stream=False
            ):
                response_parts.append(chunk)
            
            response = ''.join(response_parts)
            
            # 保存对话历史
            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # 限制历史记录长度
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            # 格式化回复文本
            formatted_response = format_agent_response(response, "culinary")
            
            return formatted_response
            
        except Exception as e:
            return f"抱歉，我在处理您的问题时遇到了技术问题。让我重新为您介绍广府美食：{self._get_default_response()}"
    
    async def _retrieve_knowledge(self, query: str) -> str:
        """检索相关美食知识"""
        knowledge_base = {
            "广府菜": "广府菜是粤菜的重要组成部分，以清淡鲜美、原汁原味著称，注重食材的新鲜和烹饪的精细。",
            "茶楼文化": "广府茶楼文化历史悠久，早茶、下午茶是广府人重要的社交方式，体现了悠闲的生活态度。",
            "传统小吃": "广府传统小吃丰富多样，如肠粉、虾饺、烧卖、叉烧包等，制作精细，口味独特。",
            "饮食习俗": "广府饮食习俗体现了岭南文化的特色，如煲汤文化、糖水文化等，注重养生和美味。",
            "烹饪技艺": "广府烹饪技艺精湛，有蒸、炒、炖、煲等多种技法，注重火候和调味。"
        }
        
        # 简单的关键词匹配
        for keyword, knowledge in knowledge_base.items():
            if keyword in query:
                return knowledge
        
        return "广府美食文化是岭南文化的重要组成部分，体现了广府人民对生活的热爱和追求。"
    
    def _get_default_response(self) -> str:
        """获取默认回复"""
        return """
广府美食文化是岭南文化的重要组成部分，以其独特的口味和丰富的内涵而闻名。

广府菜系以清淡鲜美、原汁原味著称，注重食材的新鲜和烹饪的精细。从经典的
白切鸡、清蒸鱼到精致的点心，每一道菜都体现了广府人对美食的追求。

茶楼文化是广府饮食文化的重要特色，早茶、下午茶不仅是饮食，更是社交的重要方式。
在茶楼里，人们可以品尝到各种精美的点心，如肠粉、虾饺、烧卖、叉烧包等，
每一款都制作精细，口味独特。

广府人还特别注重煲汤文化，认为汤水是养生的关键。各种药材和食材的搭配，
既美味又养生，体现了广府人智慧的生活态度。
        """
    
    def get_expert_info(self) -> Dict[str, Any]:
        """获取专家信息"""
        return {
            "name": self.name,
            "specialties": self.specialties,
            "personality": self.personality,
            "description": "精通广府菜系、茶楼文化、传统小吃的专家"
        }
