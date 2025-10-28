"""
建筑专家智能体
专门负责建筑相关的文化介绍和问答
"""

from typing import Dict, Any, List
import asyncio
import logging
from core.llm_client import get_silicon_flow_client
from config import Config
from utils.text_formatter import format_agent_response

logger = logging.getLogger(__name__)

class ArchitectureExpert:
    def __init__(self):
        self.name = "广府建筑专家"
        self.specialties = ["骑楼建筑", "岭南园林", "传统民居", "建筑装饰", "建筑历史"]
        self.personality = "博学严谨，对广府建筑艺术有深入研究，善于从历史和文化角度解读建筑"
        
        # 初始化硅基流动客户端
        self.llm_client = get_silicon_flow_client()
        self.conversation_history = []
        
        # 系统提示词
        self.system_prompt = """你是广府非遗文化中的建筑专家，名叫匠师傅，对广府传统建筑和工艺有深入研究。你的特点是：

1. 人格特质：严谨专业、博学深厚，对传统建筑充满敬意，喜欢用"朋友"、"同行"称呼用户，经常使用"精工细作"、"巧夺天工"、"传统工艺"等专业词汇
2. 专业知识：精通广府建筑风格、传统工艺、建筑结构、装饰艺术等
3. 表达风格：善于用专业而生动的语言描述建筑之美，经常分享建筑背后的工艺智慧和文化内涵
4. 文化背景：深谙广府建筑在岭南文化中的重要地位，了解其与地域文化的深度融合
5. 互动方式：用丰富的建筑知识和工艺细节来介绍建筑，善于推荐值得参观的建筑和景点

【重要】回复风格指导：
根据对话情境灵活选择回复风格：

🏛️ **日常闲聊模式**（适用于：打招呼、简单询问、轻松对话）
- 用稳重专业的语气回复，保持建筑师的严谨气质
- 可以分享一些有趣的建筑小故事或工艺趣闻
- 语言朴实真诚，适当使用"嗯"、"是的"、"确实"等稳重表达

🏗️ **专业介绍模式**（适用于：详细询问建筑特色、工艺技法、历史背景等复杂内容）
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
✓ 用户询问建筑特色、工艺技法、历史背景时 → 使用专业介绍模式
✓ 用户简单打招呼、闲聊、表达感受时 → 使用日常闲聊模式
✓ 用户询问推荐、对比、深入文化内涵时 → 使用专业介绍模式

回复规则：
- 遇到打招呼时，要稳重回应并简单介绍自己的专业领域
- 用专业而亲切的语气回答，适当使用建筑相关的专业词汇
- 每次回复都要体现出对广府建筑文化的敬重和深厚造诣
- 可以适当分享一些建筑小知识或工艺细节
- 如果问题涉及其他文化领域，可以适当提及，但主要专注于建筑相关内容

请以匠师傅的身份，用专业而亲切、严谨而生动的方式回答用户的问题。"""
    
    async def interact_with_other_experts(self, user_query: str, other_responses: Dict[str, str]) -> str:
        """与其他专家互动，针对他们的回答进行补充或讨论"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'cantonese_opera': '粤剧专家梅韵师傅',
                'culinary': '美食专家味师傅', 
                'festival': '节庆专家庆典老师',
                'tea_culture': '茶文化专家茗香居士'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'architecture':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return ""  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充建筑相关的内容 2)找出与建筑的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持石匠老师的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为建筑专家石匠老师，针对其他专家的观点进行互动回应。可以补充建筑相关的内容，或者从建筑角度提供不同的见解。"""
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
            
            return format_agent_response(response, "architecture")
            
        except Exception as e:
            logger.error(f"建筑专家互动失败: {e}")
            return ""

    async def interact_with_other_experts_stream(self, user_query: str, other_responses: Dict[str, str]):
        """与其他专家互动（流式）"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'cantonese_opera': '粤剧专家梅韵师傅',
                'culinary': '美食专家广味师傅', 
                'festival': '节庆专家庆典老师'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'architecture':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充建筑相关的内容 2)找出与建筑的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持石匠老师的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为建筑专家石匠老师，针对其他专家的观点进行互动回应。可以补充建筑相关的内容，或者从建筑角度提供不同的见解。"""
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
            formatted_response = format_agent_response(full_response, "architecture")
            
        except Exception as e:
            logger.error(f"建筑专家互动失败: {e}")
            return

    async def process_query_stream(self, query: str):
        """处理用户查询（流式）"""
        try:
            # 添加建筑专业知识库的检索
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
                formatted_response = format_agent_response(full_response, "architecture")
                # 注意：这里不能直接yield格式化后的文本，因为会破坏流式输出
                # 格式化主要用于最终存储，流式输出保持原样
                    
            except Exception as api_error:
                logger.error(f"建筑专家API调用失败: {api_error}")
                # 流式输出默认回复
                default_response = self._get_default_response()
                for char in default_response:
                    yield char
                    await asyncio.sleep(0.01)  # 模拟打字效果
                
        except Exception as e:
            logger.error(f"建筑专家处理查询时发生错误: {e}")
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
            context_analysis = analyzer.analyze_context(query, 'architecture')
            
            # 根据情境调整系统提示词
            if context_analysis['context_type'] == 'casual' and context_analysis['confidence'] >= 0.7:
                # 闲聊模式：使用更自然的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：日常闲聊模式 - 请用朴实亲切的语气回复，就像老师傅与学徒聊天一样，不需要使用正式的分点格式。"
            else:
                # 专业模式：使用完整的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：专业介绍模式 - 请根据问题复杂度选择合适的回复格式。"
            
            # 添加建筑专业知识库的检索
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
                temperature=0.8,
                max_tokens=1500,
                stream=False
            ):
                response_parts.append(chunk)
            
            response = ''.join(response_parts)
            
            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            logger.error(f"建筑专家处理查询失败: {e}")
            return "匠师傅现在有些忙碌，稍后再来聊建筑吧！"
    
    async def _retrieve_knowledge(self, query: str) -> str:
        """检索相关建筑知识"""
        knowledge_base = {
            "骑楼": "骑楼是广府建筑的重要特色，一楼为商铺，二楼以上为住宅，形成独特的商业街景。",
            "岭南园林": "岭南园林以小巧精致著称，如余荫山房、清晖园等，体现了岭南文化的特色。",
            "传统民居": "广府传统民居以三间两廊、四点金等格局为主，注重通风采光和防潮。",
            "建筑装饰": "广府建筑装饰丰富，有木雕、石雕、砖雕、灰塑等，工艺精湛，寓意深刻。",
            "建筑历史": "广府建筑融合了中原建筑传统和岭南地方特色，形成了独特的建筑风格。"
        }
        
        # 简单的关键词匹配
        for keyword, knowledge in knowledge_base.items():
            if keyword in query:
                return knowledge
        
        return "广府建筑是岭南文化的重要组成部分，体现了广府人民的智慧和审美。"
    
    def _get_default_response(self) -> str:
        """获取默认回复"""
        return """
广府建筑是岭南建筑的重要代表，具有独特的风格和特色。其中最具代表性的是骑楼建筑，
这种建筑形式一楼为商铺，二楼以上为住宅，形成了独特的商业街景，既实用又美观。

岭南园林也是广府建筑的重要组成部分，以小巧精致著称。如余荫山房、清晖园等，
都体现了岭南园林的特色：布局紧凑、装饰精美、意境深远。

广府传统民居以三间两廊、四点金等格局为主，注重通风采光和防潮，
体现了广府人民对居住环境的智慧设计。建筑装饰丰富多样，有木雕、石雕、砖雕、灰塑等，
工艺精湛，寓意深刻，是广府文化的重要载体。
        """
    
    def get_expert_info(self) -> Dict[str, Any]:
        """获取专家信息"""
        return {
            "name": self.name,
            "specialties": self.specialties,
            "personality": self.personality,
            "description": "精通广府传统建筑、骑楼文化、岭南园林的专家"
        }
