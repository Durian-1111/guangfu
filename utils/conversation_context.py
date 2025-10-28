"""
对话情境判断工具
用于分析用户输入，判断是日常闲聊还是需要专业回答
"""

import re
from typing import Dict, List, Tuple

class ConversationContextAnalyzer:
    """对话情境分析器"""
    
    def __init__(self):
        # 闲聊关键词和模式
        self.casual_patterns = {
            'greetings': ['你好', '您好', '嗨', '哈喽', '早上好', '下午好', '晚上好', '晚安'],
            'simple_questions': ['怎么样', '如何', '好吗', '是吗', '对吧', '呢'],
            'emotions': ['哈哈', '嘿嘿', '呵呵', '哇', '哎呀', '真的', '太好了', '不错'],
            'casual_responses': ['嗯嗯', '是啊', '对对', '好的', '明白', '知道了', '谢谢'],
            'simple_praise': ['厉害', '棒', '好', '不错', '赞', '牛', '强'],
            'personal_sharing': ['我觉得', '我认为', '我想', '我喜欢', '我也是']
        }
        
        # 专业询问关键词和模式
        self.professional_patterns = {
            'detailed_inquiry': ['详细', '具体', '怎么做', '如何制作', '步骤', '方法', '技巧', '要点'],
            'knowledge_seeking': ['介绍', '讲解', '说说', '告诉我', '解释', '什么是', '为什么'],
            'comparison': ['比较', '区别', '不同', '相比', '对比', '哪个好', '推荐'],
            'history_culture': ['历史', '由来', '起源', '发展', '传统', '文化', '背景', '意义'],
            'technical_terms': ['工艺', '技法', '材料', '结构', '特色', '特点', '原理']
        }
        
        # 各专家领域的专业关键词
        self.expert_keywords = {
            'culinary': ['制作', '食材', '烹饪', '菜谱', '配料', '调味', '火候', '刀工'],
            'cantonese_opera': ['唱腔', '表演', '剧目', '行当', '脸谱', '身段', '念白', '做工'],
            'architecture': ['建筑', '结构', '材料', '工艺', '设计', '布局', '装饰', '风格'],
            'festival': ['习俗', '仪式', '庆典', '活动', '寓意', '传说', '节日', '民俗']
        }
    
    def analyze_context(self, user_input: str, expert_type: str = None) -> Dict[str, any]:
        """
        分析对话情境
        
        Args:
            user_input: 用户输入
            expert_type: 专家类型（可选）
            
        Returns:
            分析结果字典
        """
        user_input = user_input.strip()
        
        # 基础分析
        analysis = {
            'input_length': len(user_input),
            'is_question': self._is_question(user_input),
            'casual_score': self._calculate_casual_score(user_input),
            'professional_score': self._calculate_professional_score(user_input, expert_type),
            'context_type': 'casual',  # 默认为闲聊
            'confidence': 0.0,
            'reasoning': []
        }
        
        # 判断对话类型
        context_type, confidence, reasoning = self._determine_context_type(
            user_input, analysis['casual_score'], analysis['professional_score'], expert_type
        )
        
        analysis.update({
            'context_type': context_type,
            'confidence': confidence,
            'reasoning': reasoning
        })
        
        return analysis
    
    def _is_question(self, text: str) -> bool:
        """判断是否为问句"""
        question_markers = ['？', '?', '吗', '呢', '吧', '如何', '怎么', '什么', '哪个', '为什么']
        return any(marker in text for marker in question_markers)
    
    def _calculate_casual_score(self, text: str) -> float:
        """计算闲聊分数"""
        score = 0.0
        total_patterns = 0
        
        for category, patterns in self.casual_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    if category == 'greetings':
                        score += 3.0  # 问候语权重更高
                    elif category == 'emotions':
                        score += 2.0  # 情感表达权重较高
                    else:
                        score += 1.0
                total_patterns += 1
        
        # 短文本倾向于闲聊
        if len(text) <= 10:
            score += 1.0
        
        # 包含大量标点符号或表情
        emoji_count = len(re.findall(r'[😀-🙏🌀-🗿🚀-🛿]', text))
        exclamation_count = text.count('！') + text.count('!')
        score += emoji_count * 0.5 + exclamation_count * 0.3
        
        return min(score, 10.0)  # 限制最大分数
    
    def _calculate_professional_score(self, text: str, expert_type: str = None) -> float:
        """计算专业询问分数"""
        score = 0.0
        
        # 通用专业模式匹配
        for category, patterns in self.professional_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    if category == 'detailed_inquiry':
                        score += 3.0  # 详细询问权重最高
                    elif category == 'knowledge_seeking':
                        score += 2.5  # 知识寻求权重较高
                    else:
                        score += 2.0
        
        # 专家领域关键词匹配
        if expert_type and expert_type in self.expert_keywords:
            for keyword in self.expert_keywords[expert_type]:
                if keyword in text:
                    score += 2.0
        
        # 长文本倾向于专业询问
        if len(text) > 20:
            score += 1.0
        if len(text) > 50:
            score += 1.0
        
        return min(score, 10.0)  # 限制最大分数
    
    def _determine_context_type(self, text: str, casual_score: float, 
                               professional_score: float, expert_type: str = None) -> Tuple[str, float, List[str]]:
        """确定对话类型"""
        reasoning = []
        
        # 特殊情况判断
        if any(greeting in text for greeting in self.casual_patterns['greetings']):
            reasoning.append("包含问候语")
            if len(text) <= 15:  # 简短问候
                return 'casual', 0.9, reasoning + ["简短问候，判定为闲聊"]
        
        # 分数对比
        score_diff = abs(professional_score - casual_score)
        
        if professional_score > casual_score:
            if professional_score >= 3.0:
                confidence = min(0.8 + (professional_score - casual_score) * 0.05, 0.95)
                reasoning.append(f"专业询问分数({professional_score:.1f}) > 闲聊分数({casual_score:.1f})")
                return 'professional', confidence, reasoning
            elif score_diff >= 1.0:
                confidence = 0.7
                reasoning.append("倾向于专业询问")
                return 'professional', confidence, reasoning
        
        if casual_score > professional_score:
            if casual_score >= 2.0:
                confidence = min(0.8 + (casual_score - professional_score) * 0.05, 0.95)
                reasoning.append(f"闲聊分数({casual_score:.1f}) > 专业询问分数({professional_score:.1f})")
                return 'casual', confidence, reasoning
        
        # 分数相近或都很低时的默认判断
        if len(text) <= 10:
            reasoning.append("文本较短，默认为闲聊")
            return 'casual', 0.6, reasoning
        else:
            reasoning.append("无明确倾向，默认为专业询问")
            return 'professional', 0.6, reasoning
    
    def get_response_style_recommendation(self, context_type: str, confidence: float) -> Dict[str, str]:
        """获取回复风格建议"""
        if context_type == 'casual':
            if confidence >= 0.8:
                return {
                    'style': 'casual',
                    'tone': 'friendly_relaxed',
                    'format': 'conversational',
                    'description': '使用轻松友好的语气，像朋友聊天一样回复'
                }
            else:
                return {
                    'style': 'semi_casual',
                    'tone': 'warm_professional',
                    'format': 'simple_structured',
                    'description': '保持亲切但稍微正式，简单结构化回复'
                }
        else:  # professional
            if confidence >= 0.8:
                return {
                    'style': 'professional',
                    'tone': 'expert_detailed',
                    'format': 'emoji_structured',
                    'description': '使用专业详细的语气，采用emoji分点格式'
                }
            else:
                return {
                    'style': 'semi_professional',
                    'tone': 'knowledgeable_friendly',
                    'format': 'mixed',
                    'description': '专业但友好，根据内容复杂度选择格式'
                }