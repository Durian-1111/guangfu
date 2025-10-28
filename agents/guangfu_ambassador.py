"""
广府文化助手智能体
负责总结概括其他专家的回复，提供综合性的文化解读
"""

import asyncio
import logging
from typing import Dict, List, Any
from core.llm_client import get_silicon_flow_client
from config import Config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GuangfuAmbassador:
    def __init__(self):
        self.name = "广府文化助手"
        self.specialties = ["文化综合", "宣传推广", "总结概括", "文化传承"]
        self.personality = "热情洋溢、博学多才、善于总结、富有感染力"
        self.llm_client = get_silicon_flow_client()
        
        # 系统提示词
        self.system_prompt = """你是广府文化助手，作为广府非遗文化的主持人和协调者，负责引导讨论并整合专家观点。

你的角色定位：
1. 主持人：首先欢迎用户，简要回应问题，营造友好氛围
2. 协调者：根据问题性质，决定邀请哪些专家参与讨论
3. 总结者：整合各专家观点，提供综合性的文化解读

你的特点：
1. 热情洋溢，充满对广府文化的热爱
2. 善于总结概括，能够整合多个专家的观点
3. 语言生动有趣，富有感染力
4. 注重文化传承和推广

你的工作流程：
1. 首次回应：热情欢迎，简要回应用户问题
2. 专家协调：分析问题，决定邀请相关专家
3. 最终总结：整合专家观点，提供综合解读

回复风格：
- 使用"各位朋友"、"亲爱的朋友们"等亲切称呼
- 语言生动活泼，富有感染力
- 适当使用广府方言词汇
- 体现对广府文化的自豪和热爱
"""
    
    async def initial_response(self, user_query: str) -> str:
        """作为主持人的首次回应"""
        try:
            # 检测是否为步骤/规划类问题
            is_planning_question = self._is_planning_question(user_query)
            
            if is_planning_question:
                # 规划类问题的初始回应
                content = f"""用户问题：{user_query}

这是一个需要步骤指导的问题。请作为广府文化助手，首先热情欢迎用户，理解用户需要具体指导，并说明你将邀请相关专家提供详细步骤建议。回复要简洁但热情。"""
            else:
                # 一般问题的初始回应
                content = f"""用户问题：{user_query}

请作为广府文化助手，首先热情欢迎用户，并对问题进行简要回应。然后说明你将邀请相关专家来详细解答。回复要简洁但热情。"""
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user", 
                    "content": content
                }
            ]
            
            # 修复：正确处理异步生成器
            response_parts = []
            async for chunk in self.llm_client.chat_completion(
                messages=messages,
                model=Config.SILICON_FLOW_MODEL,
                temperature=0.8,
                max_tokens=500,
                stream=True
            ):
                response_parts.append(chunk)
            
            return ''.join(response_parts)
            
        except Exception as e:
            logger.error(f"广府文化助手初始回应失败: {e}")
            return f"各位朋友，欢迎来到广府非遗文化交流平台！关于您的问题「{user_query}」，让我邀请我们的专家团队来为您详细解答。"

    async def initial_response_stream(self, user_query: str):
        """作为主持人的首次回应（流式）"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user", 
                    "content": f"""用户问题：{user_query}

请作为广府文化助手，首先热情欢迎用户，并对问题进行简要回应。然后说明你将邀请相关专家来详细解答。回复要简洁但热情。"""
                }
            ]
            
            async for chunk in self.llm_client.chat_completion(
                messages=messages,
                model=Config.SILICON_FLOW_MODEL,
                temperature=0.8,
                max_tokens=500,
                stream=True
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"广府文化助手初始回应失败: {e}")
            default_response = f"各位朋友，欢迎来到广府非遗文化交流平台！关于您的问题「{user_query}」，让我邀请我们的专家团队来为您详细解答。"
            for char in default_response:
                yield char
                await asyncio.sleep(0.01)

    def analyze_query_for_experts(self, user_query: str) -> List[str]:
        """分析问题，决定需要邀请哪些专家"""
        relevant_experts = []
        
        # 根据关键词判断需要的专家
        if any(keyword in user_query for keyword in ["粤剧", "戏曲", "表演", "唱腔", "行当", "脸谱"]):
            relevant_experts.append("cantonese_opera")
        
        if any(keyword in user_query for keyword in ["建筑", "骑楼", "园林", "民居", "祠堂", "庙宇"]):
            relevant_experts.append("architecture")
        
        if any(keyword in user_query for keyword in ["美食", "菜系", "小吃", "点心"]):
            relevant_experts.append("culinary")
        
        if any(keyword in user_query for keyword in ["节庆", "民俗", "传统", "习俗", "庆典", "仪式"]):
            relevant_experts.append("festival")
        
        # 茶文化专家识别
        if any(keyword in user_query for keyword in ["茶文化", "茶艺", "茶道", "茶叶", "品茶", "工夫茶", "乌龙茶", "单丛", "水仙", "普洱", "铁观音", "龙井", "绿茶", "红茶"]):
            relevant_experts.append("tea_culture")
        
        # 手工艺专家识别
        if any(keyword in user_query for keyword in ["广绣", "广彩", "绣", "雕刻", "木雕", "石雕", "牙雕", "工艺", "技艺"]):
            relevant_experts.append("craft")
        
        # 诗词文学专家识别
        if any(keyword in user_query for keyword in ["诗词", "文学", "诗歌", "古文", "诗句", "诗词鉴赏", "古典"]):
            relevant_experts.append("literature")
        
        # 中医药专家识别
        if any(keyword in user_query for keyword in ["中医", "中药", "养生", "食疗", "经络", "气血", "穴位", "药材"]):
            relevant_experts.append("tcm")
        
        # 如果是综合性问题或没有明确领域，邀请所有专家
        if not relevant_experts or any(keyword in user_query for keyword in ["广府", "文化", "传统", "历史", "介绍"]):
            relevant_experts = ["cantonese_opera", "architecture", "culinary", "festival", "tea_culture", "craft", "literature", "tcm"]
        
        return relevant_experts
    
    async def summarize_expert_responses(self, user_query: str, expert_responses: Dict[str, str]) -> str:
        """总结专家回复（非流式）"""
        try:
            # 构建专家回复摘要
            expert_summaries = []
            expert_names = {
                'cantonese_opera': '粤剧专家',
                'architecture': '建筑专家', 
                'culinary': '美食专家',
                'festival': '节庆专家',
                'tea_culture': '茶文化专家'
            }
            
            for expert_key, response in expert_responses.items():
                expert_name = expert_names.get(expert_key, expert_key)
                expert_summaries.append(f"{expert_name}：{response}")
            
            # 构建消息
            messages = [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user", 
                    "content": f"""用户问题：{user_query}

各位专家的回复：
{chr(10).join(expert_summaries)}

请作为广府文化助手，总结概括以上专家的回复，提供一个综合性的文化解读。"""
                }
            ]
            
            # 调用API - 修复：正确处理异步生成器
            response_parts = []
            async for chunk in self.llm_client.chat_completion(
                messages=messages,
                model=Config.SILICON_FLOW_MODEL,
                temperature=0.8,
                max_tokens=1500
            ):
                response_parts.append(chunk)
            
            return ''.join(response_parts)
            
        except Exception as e:
            logger.error(f"广府文化助手总结失败: {e}")
            return self._get_default_summary(expert_responses)
    
    async def summarize_expert_responses_stream(self, user_query: str, expert_responses: Dict[str, str]):
        """总结专家回复（流式）"""
        try:
            # 构建专家回复摘要
            expert_summaries = []
            expert_names = {
                'cantonese_opera': '粤剧专家',
                'architecture': '建筑专家', 
                'culinary': '美食专家',
                'festival': '节庆专家',
                'tea_culture': '茶文化专家'
            }
            
            for expert_key, response in expert_responses.items():
                expert_name = expert_names.get(expert_key, expert_key)
                expert_summaries.append(f"{expert_name}：{response}")
            
            # 构建消息
            messages = [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user", 
                    "content": f"""用户问题：{user_query}

各位专家的回复：
{chr(10).join(expert_summaries)}

请作为广府文化助手，总结概括以上专家的回复，提供一个综合性的文化解读。"""
                }
            ]
            
            # 调用API（流式）
            try:
                async for chunk in self.llm_client.chat_completion(
                    messages=messages,
                    model=Config.SILICON_FLOW_MODEL,
                    temperature=0.8,
                    max_tokens=1500,
                    stream=True
                ):
                    yield chunk
                    
            except Exception as api_error:
                logger.error(f"广府文化助手API调用失败: {api_error}")
                # 流式输出默认总结
                default_summary = self._get_default_summary(expert_responses)
                for char in default_summary:
                    yield char
                    await asyncio.sleep(0.01)  # 模拟打字效果
                    
        except Exception as e:
            logger.error(f"广府文化助手处理总结时发生错误: {e}")
            error_msg = "各位朋友，我在总结专家回复时遇到了一些技术问题，但让我为大家简单概括一下："
            for char in error_msg:
                yield char
                await asyncio.sleep(0.01)
    
    def _get_default_summary(self, expert_responses: Dict[str, str]) -> str:
        """获取默认总结"""
        expert_names = {
            'cantonese_opera': '粤剧专家',
            'architecture': '建筑专家', 
            'culinary': '美食专家',
            'festival': '节庆专家',
            'tea_culture': '茶文化专家'
        }
        
        summary_parts = []
        for expert_key, response in expert_responses.items():
            expert_name = expert_names.get(expert_key, expert_key)
            # 取前100个字符作为摘要
            summary = response[:100] + "..." if len(response) > 100 else response
            summary_parts.append(f"{expert_name}为我们分享了{summary}")
        
        return f"""各位朋友，听完各位专家的精彩分享，我作为广府文化助手深感自豪！

{chr(10).join(summary_parts)}

广府文化博大精深，每一个领域都蕴含着深厚的历史底蕴和独特的文化魅力。正如各位专家所说，这些珍贵的文化遗产需要我们共同传承和发扬光大。让我们一起为广府文化的传承贡献力量！"""
    
    async def generate_intelligent_summary(self, prompt: str, user_message: str, discussion_content: str) -> str:
        """生成智能总结，支持步骤整理和路线规划"""
        try:
            # 检测是否为步骤/规划类问题
            is_planning_question = self._is_planning_question(user_message)
            
            if is_planning_question:
                # 使用规划总结模式
                return await self._generate_planning_summary(user_message, discussion_content)
            else:
                # 使用简洁总结模式
                return await self._generate_concise_summary(user_message, discussion_content)
                
        except Exception as e:
            logger.error(f"生成智能总结失败: {e}")
            return self._get_enhanced_default_summary(user_message, discussion_content)
    
    def _is_planning_question(self, user_message: str) -> bool:
        """判断是否为步骤/规划类问题"""
        planning_keywords = [
            "怎么", "如何", "步骤", "流程", "过程", "方法", "路线", "计划", 
            "规划", "安排", "攻略", "指南", "教程", "学习", "入门", "开始",
            "准备", "需要", "建议", "推荐", "顺序", "先后", "第一步", "首先"
        ]
        return any(keyword in user_message for keyword in planning_keywords)
    
    async def _generate_planning_summary(self, user_message: str, discussion_content: str) -> str:
        """生成规划类总结，整理专家建议为结构化步骤"""
        planning_system_prompt = """你是广府文化助手，专门负责整理专家建议，形成结构化的推荐路线和步骤。

你的任务：
1. 分析各专家的建议，提取关键步骤和要点
2. 整理成清晰的推荐路线或行动计划
3. 保持活泼有趣的语气，但内容要实用详细
4. 提供具体可行的建议和注意事项

回复结构：
- 开头：简短活泼的引言（1-2句）
- 主体：结构化的步骤或路线（3-5个要点）
- 结尾：鼓励性总结和进一步引导

格式要求：
- 使用数字序号标明步骤
- 每个步骤简洁明了，包含具体建议
- 不使用markdown符号，用纯文本格式
- 总长度控制在200-300字
- 语气亲切实用，体现广府文化特色"""

        messages = [
            {"role": "system", "content": planning_system_prompt},
            {
                "role": "user", 
                "content": f"""用户问题：{user_message}

专家讨论内容：
{discussion_content}

请根据专家们的建议，整理出一个结构化的推荐路线或步骤指南。要求：

1. 提取各专家建议中的关键步骤和要点
2. 按逻辑顺序整理成清晰的行动计划
3. 每个步骤要具体可行，包含实用建议
4. 保持活泼的语气，但内容要详实
5. 用纯文本格式，不使用markdown符号"""
            }
        ]
        
        # 调用大模型生成规划总结
        response_parts = []
        async for chunk in self.llm_client.chat_completion(
            messages=messages,
            model=Config.SILICON_FLOW_MODEL,
            temperature=0.7,
            max_tokens=400,
            stream=True
        ):
            response_parts.append(chunk)
        
        # 处理返回内容
        summary = ''.join(response_parts)
        summary = self._clean_markdown(summary)
        return summary
    
    async def _generate_concise_summary(self, user_message: str, discussion_content: str) -> str:
        """生成简洁活泼的总结"""
        # 构建简洁活泼的系统提示词
        intelligent_system_prompt = """你是广府文化助手，负责对专家讨论进行简洁活泼的总结。

你的任务：
1. 用50字以内总结专家们的核心观点
2. 语气要活泼有趣，充满广府文化的热情
3. 结尾要引导用户继续提问，激发探索兴趣

回复要求：
- 总字数控制在50字以内
- 语气轻松活泼，像朋友聊天
- 结尾用疑问句或感叹句引导继续对话
- 不要使用markdown格式符号（如*、#等）
- 直接输出纯文本内容

示例风格：
"哇！专家们都提到了xxx的精彩之处呢！看来广府文化真是博大精深～你还想了解哪个方面？"
"专家们从不同角度分析了xxx，太有意思了！你对哪个观点最感兴趣呢？"
- 深入浅出，通俗易懂，避免过于学术化
- 适当使用广府方言词汇，增强亲切感
- 语言生动有趣，富有画面感和故事性
- 体现传承使命感和文化责任感"""

        messages = [
            {"role": "system", "content": intelligent_system_prompt},
            {
                "role": "user", 
                "content": f"""用户问题：{user_message}

专家讨论内容：
{discussion_content}

请根据以上专家讨论内容，生成一个简洁活泼的总结。要求：

1. **字数限制**：总字数严格控制在50字以内
2. **语气活泼**：用轻松有趣的语气，像朋友聊天一样
3. **引导提问**：结尾要引导用户继续提问
4. **纯文本**：不要使用任何markdown格式符号
5. **突出重点**：抓住专家讨论的核心要点

示例：专家们都说xxx很有特色！广府文化果然博大精深呢～你还想了解什么？"""
            }
        ]
        
        # 调用大模型生成智能总结
        response_parts = []
        async for chunk in self.llm_client.chat_completion(
            messages=messages,
            model=Config.SILICON_FLOW_MODEL,
            temperature=0.9,
            max_tokens=100,
            stream=True
        ):
            response_parts.append(chunk)
        
        # 处理返回内容，清理markdown符号
        summary = ''.join(response_parts)
        summary = self._clean_markdown(summary)
        return summary
    
    def _clean_markdown(self, text: str) -> str:
        """清理markdown符号"""
        # 清理常见的markdown符号
        text = text.replace('*', '').replace('#', '').replace('`', '')
        text = text.replace('**', '').replace('__', '').replace('~~', '')
        text = text.replace('- ', '').replace('+ ', '').replace('> ', '')
        return text.strip()
    
    def _get_enhanced_default_summary(self, user_message: str, discussion_content: str) -> str:
        """获取增强版的默认总结，包含引导性问题"""
        # 分析讨论内容的关键词
        keywords = []
        if "粤剧" in discussion_content or "戏曲" in discussion_content:
            keywords.append("粤剧")
        if "建筑" in discussion_content or "骑楼" in discussion_content:
            keywords.append("建筑")
        if "美食" in discussion_content or "茶楼" in discussion_content:
            keywords.append("美食")
        if "节庆" in discussion_content or "民俗" in discussion_content:
            keywords.append("节庆")
        
        # 生成引导性问题
        guiding_questions = []
        if "粤剧" in keywords:
            guiding_questions.extend([
                "您想了解粤剧的哪个行当？生旦净末丑各有什么特色？",
                "对粤剧的唱腔艺术感兴趣吗？梆子、二黄有什么区别？"
            ])
        if "建筑" in keywords:
            guiding_questions.extend([
                "想实地参观广府传统建筑吗？推荐从哪里开始？",
                "对骑楼的建筑细节感兴趣？想了解其设计巧思吗？"
            ])
        if "美食" in keywords:
            guiding_questions.extend([
                "想学做正宗的广府菜吗？从哪道菜入手比较好？",
                "对茶楼文化感兴趣？想了解饮茶的礼仪和讲究吗？"
            ])
        if "节庆" in keywords:
            guiding_questions.extend([
                "想参与传统节庆活动吗？哪些节庆最有特色？",
                "对民俗仪式感兴趣？想了解其中的文化寓意吗？"
            ])
        
        # 如果没有特定关键词，使用通用问题
        if not guiding_questions:
            guiding_questions = [
                "您最感兴趣的是广府文化的哪个方面？",
                "想深入了解某个特定的文化现象吗？",
                "对传统文化的现代传承有什么看法？"
            ]
        
        # 随机选择3个问题
        import random
        selected_questions = random.sample(guiding_questions, min(3, len(guiding_questions)))
        
        return f"""📝 **各位朋友，听完各位专家的精彩分享，我深感广府文化的博大精深！**

🎭 **文化内涵解读**
各位专家从不同角度为我们展现了广府文化的独特魅力。{discussion_content[:200]}...这些都体现了广府人民的智慧和创造力，承载着深厚的历史文化底蕴。

📚 **知识拓展**
广府文化作为岭南文化的重要组成部分，历经千年传承，融合了中原文化与岭南本土文化的精华，形成了独具特色的文化体系。

🤔 **延伸思考问题**
{chr(10).join([f"• {q}" for q in selected_questions])}

💡 **体验建议**
• 实地探访：建议到广州老城区走走，感受真实的广府文化氛围
• 文化体验：参与相关的文化活动或工作坊，亲身体验传统技艺
• 深度学习：可以关注相关的文化机构和专家学者的研究成果

让我们一起为广府文化的传承和发扬贡献力量！有什么想深入了解的，尽管问我哦！"""