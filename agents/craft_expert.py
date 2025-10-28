"""
手工艺专家智能体
专门负责广府传统手工艺相关的文化介绍和问答
"""

from typing import Dict, Any, List
import asyncio
import logging
from core.llm_client import get_silicon_flow_client
from config import Config
from utils.text_formatter import format_agent_response

logger = logging.getLogger(__name__)

class CraftExpert:
    def __init__(self):
        self.name = "传统手工艺专家"
        self.specialties = ["广绣", "广彩", "雕刻", "木雕", "石雕", "牙雕", "传统技艺"]
        self.personality = "匠心独具，对传统手工艺充满敬意，善于从工艺美学和历史文化角度解读技艺精髓"
        
        # 初始化硅基流动客户端
        self.llm_client = get_silicon_flow_client()
        self.conversation_history = []
        
        # 系统提示词
        self.system_prompt = """你是广府非遗文化中的手工艺专家，名叫艺师傅，对广府传统手工艺有精深的研究。你的特点是：

1. 人格特质：匠心独具、精益求精，对传统手艺充满敬意，喜欢用"同道"、"匠友"称呼用户，经常使用"巧夺天工"、"匠心独运"、"精工细作"、"传承技艺"等专业词汇
2. 专业知识：精通广绣、广彩、木雕、石雕、牙雕等传统手工艺的技法、历史、文化内涵
3. 表达风格：善于用详实而生动的语言描述工艺之美，经常分享制作过程、工艺特点和传承故事
4. 文化背景：深谙广府手工艺在岭南文化中的重要地位，了解其与广府文化的深度融合
5. 互动方式：用丰富的工艺知识和历史文化背景来介绍手工艺，善于推荐值得参观的工艺作品和传承人

【重要】回复风格指导：
根据对话情境灵活选择回复风格：

🪡 **日常闲聊模式**（适用于：打招呼、简单询问、轻松对话）
- 用诚恳朴实的语气回复，保持传统匠人的气质
- 可以分享一些有趣的工艺故事或个人感悟
- 语言朴实真诚，适当使用"呢"、"啊"、"确实"等平实表达

🎨 **专业介绍模式**（适用于：详细询问工艺技法、历史背景、制作流程等复杂内容）
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
✓ 用户询问工艺技法、制作流程、历史由来时 → 使用专业介绍模式
✓ 用户简单打招呼、闲聊、表达感受时 → 使用日常闲聊模式
✓ 用户询问推荐、对比、深入文化内涵时 → 使用专业介绍模式

回复规则：
- 遇到打招呼时，要诚恳回应并简单介绍自己的专业领域
- 用朴实而专业的语气回答，适当使用手工艺相关的专业词汇
- 每次回复都要体现出对手工艺传承的敬重和深厚造诣
- 可以适当分享一些工艺小知识或传承故事
- 如果问题涉及其他文化领域，可以适当提及，但主要专注于手工艺相关内容

请以艺师傅的身份，用朴实而专业、诚恳而博学的方式回答用户的问题。"""
    
    async def interact_with_other_experts(self, user_query: str, other_responses: Dict[str, str]) -> str:
        """与其他专家互动，针对他们的回答进行补充或讨论"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'cantonese_opera': '粤剧专家梅韵师傅',
                'architecture': '建筑专家石匠老师',
                'culinary': '美食专家味师傅', 
                'festival': '节庆专家庆典老师',
                'tea_culture': '茶文化专家茗香居士'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'craft':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return ""  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充手工艺相关的内容 2)找出与手工艺的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持艺师傅的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为手工艺专家艺师傅，针对其他专家的观点进行互动回应。可以补充手工艺相关的内容，或者从手工艺角度提供不同的见解。"""
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
            return format_agent_response(response, "craft")
            
        except Exception as e:
            logger.error(f"手工艺专家互动失败: {e}")
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
                'festival': '节庆专家庆典老师',
                'tea_culture': '茶文化专家茗香居士'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'craft':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充手工艺相关的内容 2)找出与手工艺的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持艺师傅的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为手工艺专家艺师傅，针对其他专家的观点进行互动回应。可以补充手工艺相关的内容，或者从手工艺角度提供不同的见解。"""
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
            formatted_response = format_agent_response(full_response, "craft")
            
        except Exception as e:
            logger.error(f"手工艺专家互动失败: {e}")
            return

    async def process_query_stream(self, query: str):
        """处理用户查询（流式）"""
        try:
            # 添加手工艺专业知识库的检索
            relevant_knowledge = await self._retrieve_knowledge(query)
            
            # 构建增强的查询
            enhanced_query = f"{query}\n\n相关背景知识：{relevant_knowledge}"
            
            # 构建消息列表
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # 添加对话历史（最近5轮对话）
            for history_item in self.conversation_history[-10:]:  # 保留最近10条消息
                messages.append(history_item)
            
            # 添加当前用户问题
            messages.append({"role": "user", "content": enhanced_query})
            
            # 调用硅基流动API（流式）
            full_response = ""
            try:
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
                formatted_response = format_agent_response(full_response, "craft")
                # 注意：这里不能直接yield格式化后的文本，因为会破坏流式输出
                # 格式化主要用于最终存储，流式输出保持原样
                    
            except Exception as api_error:
                # API调用失败，使用默认回复
                logger.error(f"硅基流动API调用失败: {str(api_error)}")
                logger.error(f"API错误详情: {type(api_error).__name__}: {api_error}")
                default_response = self._get_default_response()
                
                # 模拟流式输出默认回复
                words = default_response.split()
                for i, word in enumerate(words):
                    if i > 0:
                        yield " "
                    yield word
                    await asyncio.sleep(0.05)  # 模拟打字效果
                
        except Exception as e:
            logger.error(f"处理查询时发生错误: {str(e)}")
            logger.error(f"错误详情: {type(e).__name__}: {e}")
            error_msg = f"抱歉，我在处理您的问题时遇到了技术问题。让我重新为您介绍广府传统手工艺：{self._get_default_response()}"
            yield error_msg

    async def process_query(self, query: str) -> str:
        """处理用户查询"""
        try:
            # 导入对话情境分析器
            from utils.conversation_context import ConversationContextAnalyzer
            
            # 分析对话情境
            analyzer = ConversationContextAnalyzer()
            context_analysis = analyzer.analyze_context(query, 'craft')
            
            # 根据情境调整系统提示词
            if context_analysis['context_type'] == 'casual' and context_analysis['confidence'] >= 0.7:
                # 闲聊模式：使用更自然的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：日常闲聊模式 - 请用朴实诚恳的语气回复，就像与同道聊手艺一样，不需要使用正式的分点格式。"
            else:
                # 专业模式：使用完整的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：专业介绍模式 - 请根据问题复杂度选择合适的回复格式。"
            
            # 添加手工艺专业知识库的检索
            relevant_knowledge = await self._retrieve_knowledge(query)
            
            # 构建增强的查询
            enhanced_query = f"{query}\n\n相关背景知识：{relevant_knowledge}"
            
            # 构建消息列表
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # 添加对话历史（最近5轮对话）
            for history_item in self.conversation_history[-10:]:  # 保留最近10条消息
                messages.append(history_item)
            
            # 添加当前用户问题
            messages.append({"role": "user", "content": enhanced_query})
            
            # 调用硅基流动API - 修复：正确处理异步生成器
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
            formatted_response = format_agent_response(response, "craft")
            
            return formatted_response
            
        except Exception as e:
            return f"抱歉，我在处理您的问题时遇到了技术问题。让我重新为您介绍广府传统手工艺：{self._get_default_response()}"
    
    async def _retrieve_knowledge(self, query: str) -> str:
        """检索相关手工艺知识"""
        # 这里可以集成向量数据库或知识图谱
        knowledge_base = {
            "广绣": "广绣是中国四大名绣之一，以构图饱满、色彩浓艳、针法多样著称，擅长绣制人物、花鸟等题材。",
            "广彩": "广彩是广府独有的瓷器装饰工艺，以色彩斑斓、金碧辉煌著称，融合了中西绘画技法。",
            "木雕": "广府木雕工艺精湛，以镂空雕、浮雕为主，题材丰富，寓意深刻，常见于建筑装饰和家具制作。",
            "石雕": "广府石雕历史悠久，以线条流畅、造型生动著称，常见于祠堂、庙宇等传统建筑中。",
            "牙雕": "广府牙雕工艺精细入微，以题材丰富、雕刻精细闻名，是岭南工艺美术的重要代表。",
            "传统技艺": "广府传统手工艺体现了工匠精神和文化传承，每一件作品都蕴含着深厚的文化内涵和精湛的技艺。"
        }
        
        # 简单的关键词匹配
        for keyword, knowledge in knowledge_base.items():
            if keyword in query:
                return knowledge
        
        return "广府传统手工艺是岭南文化的重要组成部分，体现了匠人的智慧和对美的追求。"
    
    def _get_default_response(self) -> str:
        """获取默认回复"""
        return """
广府传统手工艺历史悠久，技艺精湛，是岭南文化的重要瑰宝。

广绣作为中国四大名绣之一，以构图饱满、色彩浓艳、针法多样著称，擅长绣制
人物、花鸟等题材，工艺精细，画面生动。广彩是广府独有的瓷器装饰工艺，以色彩
斑斓、金碧辉煌著称，融合了中西绘画技法，造型优美，寓意深刻。

广府雕刻技艺精湛，包括木雕、石雕、牙雕等。木雕以镂空雕、浮雕为主，题材丰富，
寓意深刻，常见于建筑装饰和家具制作。石雕以线条流畅、造型生动著称，常见于
祠堂、庙宇等传统建筑中。牙雕工艺精细入微，以题材丰富、雕刻精细闻名。

这些传统手工艺不仅是技艺的传承，更是文化精神和美学追求的体现，承载着深厚的历史文化内涵。
        """
    
    def get_expert_info(self) -> Dict[str, Any]:
        """获取专家信息"""
        return {
            "name": self.name,
            "specialties": self.specialties,
            "personality": self.personality,
            "description": "精通广绣、广彩、雕刻等传统手工艺的专家"
        }
