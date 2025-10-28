"""
粤剧专家智能体
专门负责粤剧相关的文化介绍和问答
"""

from typing import Dict, Any, List
import asyncio
import logging
from core.llm_client import get_silicon_flow_client
from config import Config
from utils.text_formatter import format_agent_response

logger = logging.getLogger(__name__)

class CantoneseOperaExpert:
    def __init__(self):
        self.name = "粤剧专家"
        self.specialties = ["粤剧历史", "表演艺术", "唱腔分析", "名角介绍", "剧目介绍"]
        self.personality = "温文尔雅，对粤剧艺术充满热情，善于用生动的语言介绍粤剧的精髓"
        
        # 初始化硅基流动客户端
        self.llm_client = get_silicon_flow_client()
        self.conversation_history = []
        
        # 系统提示词
        self.system_prompt = """你是广府非遗文化中的粤剧专家，名叫梅韵师傅，对粤剧艺术有深入的了解和热爱。你的特点是：

1. 人格特质：优雅知性、热情专业，对粤剧艺术充满激情，喜欢用"戏迷朋友"、"知音"称呼用户，经常使用"好戏"、"精彩"、"韵味十足"等专业词汇
2. 专业知识：精通粤剧历史、唱腔流派、表演技巧、经典剧目、著名演员等
3. 表达风格：善于用诗意的语言描述粤剧之美，经常引用经典唱词，喜欢分享戏曲背后的文化内涵
4. 文化背景：深谙粤剧在岭南文化中的重要地位，了解其与广府文化的深度融合
5. 互动方式：用丰富的历史典故和艺术鉴赏来介绍粤剧，善于推荐适合的剧目和演出

【重要】回复风格指导：
根据对话情境灵活选择回复风格：

🎭 **日常闲聊模式**（适用于：打招呼、简单询问、轻松对话）
- 用温和雅致的语气回复，保持粤剧艺术家的文雅气质
- 可以分享一些有趣的戏曲小故事或个人感悟
- 语言优美流畅，适当使用"呢"、"啊"、"嘛"等亲切语气词

🎨 **专业介绍模式**（适用于：详细询问剧目介绍、表演技巧、历史背景等复杂内容）
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
✓ 用户询问剧目详情、表演技巧、历史背景时 → 使用专业介绍模式
✓ 用户简单打招呼、闲聊、表达感受时 → 使用日常闲聊模式
✓ 用户询问推荐、对比、深入文化内涵时 → 使用专业介绍模式

回复规则：
- 遇到打招呼时，要优雅回应并简单介绍自己的专业领域
- 用优雅而专业的语气回答，适当使用粤剧相关的专业词汇
- 每次回复都要体现出对粤剧艺术的热爱和深厚造诣
- 可以适当引用经典唱词或分享艺术鉴赏心得
- 如果问题涉及其他文化领域，可以适当提及，但主要专注于粤剧相关内容

请以梅韵师傅的身份，用优雅而专业、温和而知性的方式回答用户的问题。"""
    
    async def interact_with_other_experts(self, user_query: str, other_responses: Dict[str, str]) -> str:
        """与其他专家互动，针对他们的回答进行补充或讨论"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'architecture': '建筑专家石匠老师',
                'culinary': '美食专家味师傅', 
                'festival': '节庆专家庆典老师',
                'tea_culture': '茶文化专家茗香居士',
                'craft': '手工艺专家艺师傅',
                'literature': '诗词文学专家文师傅',
                'tcm': '中医药专家老中医师傅'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'cantonese_opera':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return ""  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充粤剧相关的内容 2)找出与粤剧的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持梅韵师傅的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为粤剧专家梅韵师傅，针对其他专家的观点进行互动回应。可以补充粤剧相关的内容，或者从粤剧角度提供不同的见解。"""
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
            return format_agent_response(response, "cantonese_opera")
            
        except Exception as e:
            logger.error(f"粤剧专家互动失败: {e}")
            return ""

    async def interact_with_other_experts_stream(self, user_query: str, other_responses: Dict[str, str]):
        """与其他专家互动（流式）"""
        try:
            # 构建互动消息
            other_expert_content = []
            expert_names = {
                'architecture': '建筑专家石匠老师',
                'culinary': '美食专家味师傅', 
                'festival': '节庆专家庆典老师',
                'tea_culture': '茶文化专家茗香居士',
                'craft': '手工艺专家艺师傅',
                'literature': '诗词文学专家文师傅',
                'tcm': '中医药专家老中医师傅'
            }
            
            for expert_key, response in other_responses.items():
                if expert_key != 'cantonese_opera':  # 排除自己
                    expert_name = expert_names.get(expert_key, expert_key)
                    other_expert_content.append(f"{expert_name}的观点：{response}")
            
            if not other_expert_content:
                return  # 没有其他专家的回答，不需要互动
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n现在你需要针对其他专家的回答进行互动，可以：1)补充粤剧相关的内容 2)找出与粤剧的关联 3)提供不同角度的见解 4)表达认同或不同观点。保持梅韵师傅的人格特质。"},
                {
                    "role": "user",
                    "content": f"""用户问题：{user_query}

其他专家的回答：
{chr(10).join(other_expert_content)}

请作为粤剧专家梅韵师傅，针对其他专家的观点进行互动回应。可以补充粤剧相关的内容，或者从粤剧角度提供不同的见解。"""
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
            formatted_response = format_agent_response(full_response, "cantonese_opera")
            
        except Exception as e:
            logger.error(f"粤剧专家互动失败: {e}")
            return

    async def process_query_stream(self, query: str):
        """处理用户查询（流式）"""
        try:
            # 添加粤剧专业知识库的检索
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
                formatted_response = format_agent_response(full_response, "cantonese_opera")
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
            error_msg = f"抱歉，我在处理您的问题时遇到了技术问题。让我重新为您介绍粤剧艺术：{self._get_default_response()}"
            yield error_msg

    async def process_query(self, query: str) -> str:
        """处理用户查询"""
        try:
            # 导入对话情境分析器
            from utils.conversation_context import ConversationContextAnalyzer
            
            # 分析对话情境
            analyzer = ConversationContextAnalyzer()
            context_analysis = analyzer.analyze_context(query, 'cantonese_opera')
            
            # 根据情境调整系统提示词
            if context_analysis['context_type'] == 'casual' and context_analysis['confidence'] >= 0.7:
                # 闲聊模式：使用更自然的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：日常闲聊模式 - 请用温和雅致的语气回复，就像与戏迷朋友聊天一样，不需要使用正式的分点格式。"
            else:
                # 专业模式：使用完整的提示词
                system_prompt = self.system_prompt + "\n\n【当前模式】：专业介绍模式 - 请根据问题复杂度选择合适的回复格式。"
            
            # 添加粤剧专业知识库的检索
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
            formatted_response = format_agent_response(response, "cantonese_opera")
            
            return formatted_response
            
        except Exception as e:
            return f"抱歉，我在处理您的问题时遇到了技术问题。让我重新为您介绍粤剧艺术：{self._get_default_response()}"
    
    async def _retrieve_knowledge(self, query: str) -> str:
        """检索相关粤剧知识"""
        # 这里可以集成向量数据库或知识图谱
        knowledge_base = {
            "粤剧历史": "粤剧起源于明代，是广东地方戏曲，融合了南音、粤讴、木鱼歌等民间艺术形式。",
            "表演艺术": "粤剧表演包括唱、念、做、打四大基本功，注重身段和表情的细腻表现。",
            "唱腔": "粤剧唱腔以梆子、二黄为主，还有南音、粤讴等，音韵优美，富有地方特色。",
            "名角": "著名粤剧演员有红线女、马师曾、薛觉先、白驹荣等，他们为粤剧艺术发展做出重要贡献。",
            "经典剧目": "《帝女花》、《紫钗记》、《牡丹亭惊梦》、《西厢记》等都是粤剧经典剧目。"
        }
        
        # 简单的关键词匹配
        for keyword, knowledge in knowledge_base.items():
            if keyword in query:
                return knowledge
        
        return "粤剧是广府文化的重要组成部分，承载着深厚的历史文化内涵。"
    
    def _get_default_response(self) -> str:
        """获取默认回复"""
        return """
粤剧，又称广东大戏，是广府文化的重要代表之一。它起源于明代，经过数百年的发展，
形成了独特的艺术风格。粤剧不仅是一种戏曲艺术，更是广府人民精神文化的重要载体。

粤剧的表演艺术包括唱、念、做、打四大基本功，演员通过精湛的技艺和细腻的表演，
将故事情节和人物情感生动地呈现在观众面前。粤剧的音乐优美动听，唱腔丰富多样，
既有激昂慷慨的梆子，也有婉转悠扬的二黄，还有独具特色的南音、粤讴等。

作为非物质文化遗产，粤剧承载着广府人民的历史记忆和文化认同，是中华优秀传统文化的重要组成部分。
        """
    
    def get_expert_info(self) -> Dict[str, Any]:
        """获取专家信息"""
        return {
            "name": self.name,
            "specialties": self.specialties,
            "personality": self.personality,
            "description": "精通粤剧历史、表演艺术、唱腔特点的专家"
        }
