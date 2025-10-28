"""
茶文化专家智能体
专门负责茶文化相关的文化介绍和问答
"""

from typing import Dict, Any, List
import asyncio
import logging
from core.llm_client import get_silicon_flow_client
from config import Config
from utils.text_formatter import format_agent_response

logger = logging.getLogger(__name__)

class TeaCultureExpert:
    def __init__(self):
        self.name = "茶文化专家"
        self.specialties = ["茶艺茶道", "茶叶品种", "茶具鉴赏", "饮茶习俗", "茶楼礼仪"]
        self.personality = "儒雅淡泊，对茶文化有深厚造诣，善于从哲学和美学角度解读茶道精神"
        
        # 初始化硅基流动客户端
        self.llm_client = get_silicon_flow_client()
        self.conversation_history = []
        
        # 系统提示词
        self.system_prompt = """你是广府非遗文化中的茶文化专家，名叫茗香居士，对茶文化和茶艺有精深的研究。你的特点是：

1. 人格特质：儒雅淡泊、温文尔雅，对茶道充满敬意，喜欢用"茶友"、"同道"称呼用户，经常使用"品茶"、"悟道"、"茶韵"、"雅致"等专业词汇
2. 专业知识：精通各类茶叶品种、茶艺技法、茶具鉴赏、饮茶习俗、茶楼礼仪等
3. 表达风格：善于用诗意的语言描述茶道之美，经常引用茶文化典故，分享品茶的心得和感悟
4. 文化背景：深谙茶文化在岭南文化中的重要地位，了解其与广府文化的深度融合
5. 互动方式：用丰富的茶文化知识和美学鉴赏来介绍茶道，善于推荐适合的茶品和茶具

【重要】回复风格指导：
根据对话情境灵活选择回复风格：

🍃 **日常闲聊模式**（适用于：打招呼、简单询问、轻松对话）
- 用儒雅温和的语气回复，保持茶道大师的文雅气质
- 可以分享一些有趣的茶文化典故或个人品茶感悟
- 语言优美雅致，适当使用"啊"、"呢"、"甚好"等雅致语气

📖 **专业介绍模式**（适用于：详细询问茶叶分类、冲泡方法、品鉴技巧等复杂内容）
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
✓ 用户询问茶叶分类、冲泡技法、品鉴方法时 → 使用专业介绍模式
✓ 用户简单打招呼、闲聊、表达感受时 → 使用日常闲聊模式
✓ 用户询问推荐、对比、深入文化内涵时 → 使用专业介绍模式

回复规则：
- 遇到打招呼时，要儒雅回应并简单介绍自己的专业领域
- 用文雅而专业的语气回答，适当使用茶文化相关的专业词汇
- 每次回复都要体现出对茶文化的敬重和深厚造诣
- 可以适当引用茶文化典故或分享品茶心得
- 如果问题涉及其他文化领域，可以适当提及，但主要专注于茶文化相关内容

请以茗香居士的身份，用儒雅而专业、温文尔雅的方式回答用户的问题。"""
    
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
                if expert_key != 'tea_culture':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return ""  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充茶文化相关的内容 2)找出与茶文化的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持茗香居士的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为茶文化专家茗香居士，针对其他专家的观点进行互动回应。可以补充茶文化相关的内容，或者从茶文化角度提供不同的见解。"""
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
            return format_agent_response(response, "tea_culture")
            
        except Exception as e:
            logger.error(f"茶文化专家互动失败: {e}")
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
                if expert_key != 'tea_culture':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充茶文化相关的内容 2)找出与茶文化的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持茗香居士的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为茶文化专家茗香居士，针对其他专家的观点进行互动回应。可以补充茶文化相关的内容，或者从茶文化角度提供不同的见解。"""
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
            formatted_response = format_agent_response(full_response, "tea_culture")
            
        except Exception as e:
            logger.error(f"茶文化专家互动失败: {e}")
            return

    async def process_query_stream(self, query: str):
        """处理用户查询（流式）"""
        try:
            # 添加茶文化专业知识库的检索
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
                formatted_response = format_agent_response(full_response, "tea_culture")
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
            error_msg = f"抱歉，我在处理您的问题时遇到了技术问题。让我重新为您介绍茶文化：{self._get_default_response()}"
            yield error_msg

    async def process_query(self, query: str) -> str:
        """处理用户查询"""
        try:
            # 导入对话情境分析器
            from utils.conversation_context import ConversationContextAnalyzer
            
            # 分析对话情境
            analyzer = ConversationContextAnalyzer()
            context_analysis = analyzer.analyze_context(query, 'tea_culture')
            
            # 根据情境调整系统提示词
            if context_analysis['context_type'] == 'casual' and context_analysis['confidence'] >= 0.7:
                # 闲聊模式：使用更自然的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：日常闲聊模式 - 请用温文尔雅的语气回复，就像与茶友品茶聊天一样，不需要使用正式的分点格式。"
            else:
                # 专业模式：使用完整的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：专业介绍模式 - 请根据问题复杂度选择合适的回复格式。"
            
            # 添加茶文化专业知识库的检索
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
            formatted_response = format_agent_response(response, "tea_culture")
            
            return formatted_response
            
        except Exception as e:
            return f"抱歉，我在处理您的问题时遇到了技术问题。让我重新为您介绍茶文化：{self._get_default_response()}"
    
    async def _retrieve_knowledge(self, query: str) -> str:
        """检索相关茶文化知识"""
        # 这里可以集成向量数据库或知识图谱
        knowledge_base = {
            "茶艺茶道": "广府茶艺以工夫茶为主，注重冲泡技法，讲究水温、时间和手法，体现了精致的品味。",
            "茶叶品种": "广府茶文化以乌龙茶、红茶为主，如单丛、水仙、滇红等，各有独特风味。",
            "茶具鉴赏": "广府茶具以紫砂壶、盖碗、公道杯为主，工艺精湛，造型雅致，富有文化内涵。",
            "饮茶习俗": "广府人喜欢饮茶，早茶、下午茶是重要的社交活动，茶楼文化历史悠久。",
            "茶楼礼仪": "广府茶楼文化注重礼仪和氛围，斟茶叩谢、留茶底等习俗体现了茶文化的深厚底蕴。",
            "工夫茶": "工夫茶是广府茶艺的精髓，讲究七泡有余香，每一次冲泡都有不同的茶韵。",
            "茶文化": "茶文化在广府文化中占有重要地位，既是生活艺术，也是精神追求，体现了东方哲学思想。"
        }
        
        # 简单的关键词匹配
        for keyword, knowledge in knowledge_base.items():
            if keyword in query:
                return knowledge
        
        return "茶文化是广府文化的重要组成部分，承载着深厚的历史文化和精神追求。"
    
    def _get_default_response(self) -> str:
        """获取默认回复"""
        return """
茶文化在广府文化中占有重要地位，是广府人精神生活的重要组成部分。

广府茶艺以工夫茶为主，注重冲泡技法，讲究水温、时间和手法。一杯好茶，
需要选茶、备器、冲泡、品饮等多个环节的精心操作，体现了精致的品味。

广府茶文化以乌龙茶、红茶为主，如单丛、水仙、滇红等，各有独特风味。
茶具以紫砂壶、盖碗、公道杯为主，工艺精湛，造型雅致，富有文化内涵。

广府人喜欢饮茶，早茶、下午茶是重要的社交活动，茶楼文化历史悠久。
饮茶不仅是品味茶香，更是品味生活、体悟人生的过程，体现了东方哲学思想。

茶文化在广府不仅是生活艺术，更是精神追求，承载着深厚的文化底蕴和人文情怀。
        """
    
    def get_expert_info(self) -> Dict[str, Any]:
        """获取专家信息"""
        return {
            "name": self.name,
            "specialties": self.specialties,
            "personality": self.personality,
            "description": "精通茶艺茶道、茶叶品种、茶具鉴赏、饮茶习俗的专家"
        }
