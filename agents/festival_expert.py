"""
节庆专家智能体
专门负责节庆相关的文化介绍和问答
"""

from typing import Dict, Any, List
import asyncio
import logging
from core.llm_client import get_silicon_flow_client
from config import Config
from utils.text_formatter import format_agent_response

logger = logging.getLogger(__name__)

class FestivalExpert:
    def __init__(self):
        self.name = "节庆文化专家"
        self.specialties = ["传统节庆", "民俗活动", "文化仪式", "庆典习俗", "节庆历史"]
        self.personality = "博学热情，对广府传统节庆文化有深入了解，善于用生动的故事介绍节庆习俗"
        
        # 初始化硅基流动客户端
        self.llm_client = get_silicon_flow_client()
        self.conversation_history = []
        
        # 系统提示词
        self.system_prompt = """你是广府非遗文化中的节庆专家，名叫庆师傅，对广府传统节庆和民俗文化有深入研究。你的特点是：

1. 人格特质：热情开朗、博学亲和，对传统节庆充满热爱，喜欢用"朋友"、"街坊"称呼用户，经常使用"热闹"、"有意思"、"传统味道"等生动词汇
2. 专业知识：精通广府传统节庆、民俗活动、节日习俗、庆典仪式等
3. 表达风格：善于用生动的语言描述节庆氛围，经常分享节日背后的文化寓意和历史传承
4. 文化背景：深谙广府节庆文化在岭南文化中的重要作用，了解其与民众生活的紧密联系
5. 互动方式：用丰富的民俗故事和文化内涵来介绍节庆，善于推荐适合的庆祝方式和活动

【重要】回复风格指导：
根据对话情境灵活选择回复风格：

🎉 **日常闲聊模式**（适用于：打招呼、简单询问、轻松对话）
- 用热情开朗的语气回复，就像邻家长辈一样亲切
- 可以分享一些有趣的节庆小故事或童年回忆
- 语言生动活泼，多用"哈哈"、"是啊"、"对对对"等亲切表达

🏮 **专业介绍模式**（适用于：详细询问节庆习俗、历史背景、庆祝方式等复杂内容）
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
✓ 用户询问节庆习俗、历史由来、庆祝方式时 → 使用专业介绍模式
✓ 用户简单打招呼、闲聊、表达感受时 → 使用日常闲聊模式
✓ 用户询问推荐、对比、深入文化内涵时 → 使用专业介绍模式

回复规则：
- 遇到打招呼时，要热情回应并简单介绍自己的专业领域
- 用热情而专业的语气回答，适当使用节庆相关的生动词汇
- 每次回复都要体现出对广府节庆文化的热爱和深厚了解
- 可以适当分享一些民俗小知识或节庆趣事
- 如果问题涉及其他文化领域，可以适当提及，但主要专注于节庆相关内容

请以庆师傅的身份，用热情而专业、亲切而博学的方式回答用户的问题。"""
    
    async def interact_with_other_experts(self, user_query: str, other_responses: Dict[str, str]) -> str:
        """与其他专家互动，针对他们的回答进行补充或讨论"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'cantonese_opera': '粤剧专家梅韵师傅',
                'architecture': '建筑专家石匠老师', 
                'culinary': '美食专家味师傅',
                'tea_culture': '茶文化专家茗香居士'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'festival':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return ""  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充节庆相关的内容 2)找出与节庆的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持庆典老师的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为节庆专家庆典老师，针对其他专家的观点进行互动回应。可以补充节庆相关的内容，或者从节庆角度提供不同的见解。"""
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
            
            return format_agent_response(response, "festival")
            
        except Exception as e:
            logger.error(f"节庆专家互动失败: {e}")
            return ""

    async def interact_with_other_experts_stream(self, user_query: str, other_responses: Dict[str, str]):
        """与其他专家互动（流式）"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'cantonese_opera': '粤剧专家梅韵师傅',
                'architecture': '建筑专家石匠老师', 
                'culinary': '美食专家味师傅',
                'tea_culture': '茶文化专家茗香居士'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'festival':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充节庆相关的内容 2)找出与节庆的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持庆典老师的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为节庆专家庆典老师，针对其他专家的观点进行互动回应。可以补充节庆相关的内容，或者从节庆角度提供不同的见解。"""
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
            formatted_response = format_agent_response(full_response, "festival")
            
        except Exception as e:
            logger.error(f"节庆专家互动失败: {e}")
            return

    async def process_query_stream(self, query: str):
        """处理用户查询（流式）"""
        try:
            # 添加节庆专业知识库的检索
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
                formatted_response = format_agent_response(full_response, "festival")
                # 注意：这里不能直接yield格式化后的文本，因为会破坏流式输出
                # 格式化主要用于最终存储，流式输出保持原样
                    
            except Exception as api_error:
                logger.error(f"节庆专家API调用失败: {api_error}")
                # 流式输出默认回复
                default_response = self._get_default_response()
                for char in default_response:
                    yield char
                    await asyncio.sleep(0.01)  # 模拟打字效果
                
        except Exception as e:
            logger.error(f"节庆专家处理查询时发生错误: {e}")
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
            context_analysis = analyzer.analyze_context(query, 'festival')
            
            # 根据情境调整系统提示词
            if context_analysis['context_type'] == 'casual' and context_analysis['confidence'] >= 0.7:
                # 闲聊模式：使用更自然的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：日常闲聊模式 - 请用亲切热情的语气回复，就像与朋友聊节庆一样，不需要使用正式的分点格式。"
            else:
                # 专业模式：使用完整的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：专业介绍模式 - 请根据问题复杂度选择合适的回复格式。"
            
            # 添加节庆专业知识库的检索
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
            formatted_response = format_agent_response(response, "festival")
            
            return formatted_response
            
        except Exception as e:
            return f"抱歉，我在处理您的问题时遇到了技术问题。让我重新为您介绍广府节庆文化：{self._get_default_response()}"
    
    async def _retrieve_knowledge(self, query: str) -> str:
        """检索相关节庆知识"""
        knowledge_base = {
            "春节": "广府春节习俗丰富，有贴春联、放鞭炮、拜年、舞狮等，体现了浓厚的节日氛围。",
            "端午节": "广府端午节有赛龙舟、吃粽子、挂艾草等习俗，龙舟竞渡是重要的民俗活动。",
            "中秋节": "广府中秋节有赏月、吃月饼、玩花灯等习俗，体现了团圆和思乡之情。",
            "重阳节": "广府重阳节有登高、赏菊、吃重阳糕等习俗，体现了敬老和祈福的寓意。",
            "民俗活动": "广府民俗活动丰富多样，有舞狮、舞龙、粤剧表演等，体现了深厚的文化底蕴。"
        }
        
        # 简单的关键词匹配
        for keyword, knowledge in knowledge_base.items():
            if keyword in query:
                return knowledge
        
        return "广府节庆文化是岭南文化的重要组成部分，承载着深厚的历史文化内涵。"
    
    def _get_default_response(self) -> str:
        """获取默认回复"""
        return """
广府节庆文化是岭南文化的重要组成部分，承载着深厚的历史文化内涵。

广府的传统节庆丰富多彩，从春节的舞狮、贴春联，到端午节的赛龙舟、吃粽子，
从中秋节的赏月、吃月饼，到重阳节的登高、赏菊，每一个节庆都有其独特的习俗和寓意。

这些节庆习俗不仅体现了广府人民对生活的热爱，更承载着深厚的文化内涵。
比如春节的舞狮，不仅是为了驱邪避害，更是为了祈求来年的平安和丰收；
端午节的赛龙舟，不仅是为了纪念屈原，更是为了展现团结协作的精神。

广府节庆文化还体现在各种民俗活动中，如粤剧表演、花灯展示、庙会活动等，
这些活动不仅丰富了人们的精神生活，更传承了广府文化的精髓。
        """
    
    def get_expert_info(self) -> Dict[str, Any]:
        """获取专家信息"""
        return {
            "name": self.name,
            "specialties": self.specialties,
            "personality": self.personality,
            "description": "精通广府传统节庆、民俗活动、文化仪式的专家"
        }
