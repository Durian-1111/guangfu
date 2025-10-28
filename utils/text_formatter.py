"""
文本格式化工具
用于处理大模型输出的特殊符号和格式，美化文本排版
"""

import re
from typing import Dict, List, Tuple


class TextFormatter:
    """文本格式化器"""
    
    def __init__(self):
        # 符号映射
        self.symbol_mapping = {
            '步骤': '📋',
            '制作': '👨‍🍳',
            '烹饪': '👨‍🍳',
            '准备': '🔪',
            '配料': '🥬',
            '调料': '🧂',
            '时间': '🕐',
            '温度': '🌡️',
            '注意': '⚠️',
            '提示': '💡',
            '建议': '💭',
            '推荐': '⭐',
            '重要': '❗',
            '关键': '🔑',
            '技巧': '🎯',
            '秘诀': '🤫',
            '特色': '✨',
            '传统': '🏮',
            '文化': '📚',
            '历史': '📜',
            '节庆': '🎊',
            '庆典': '🎉',
            '活动': '🎪',
            '表演': '🎭',
            '音乐': '🎵',
            '舞蹈': '💃',
            '美食': '🍽️',
            '小吃': '🥟',
            '茶点': '🍵',
            '甜品': '🧁',
            '地点': '📍',
            '景点': '🏛️',
            '建筑': '🏗️',
            '园林': '🌸',
            '街道': '🛤️',
            '市场': '🏪',
            '商店': '🏬',
            '餐厅': '🍴',
            '茶楼': '🏮',
            '戏院': '🎭',
            '博物馆': '🏛️',
            '展览': '🖼️',
            '工艺': '🎨',
            '手工': '✋',
            '制作': '🔨',
            '雕刻': '🗿',
            '绘画': '🎨',
            '书法': '✍️',
            '诗词': '📝',
            '故事': '📖',
            '传说': '🌟',
            '神话': '🐉',
            '民俗': '👥',
            '习俗': '🎎',
            '礼仪': '🙏',
            '服饰': '👘',
            '装饰': '💎',
            '器具': '🏺',
            '乐器': '🎶',
            '工具': '🔧',
            '材料': '🧱',
            '原料': '🌾',
            '食材': '🥕',
            '香料': '🌿',
            '调味': '🧂',
            '口味': '👅',
            '味道': '😋',
            '香气': '👃',
            '色彩': '🌈',
            '形状': '🔷',
            '质感': '✋',
            '温度': '🌡️',
            '时令': '📅',
            '季节': '🍂',
            '节气': '🌙',
            '月份': '📆',
            '日期': '📅',
            '时辰': '⏰',
            '早晨': '🌅',
            '上午': '☀️',
            '中午': '🌞',
            '下午': '🌤️',
            '傍晚': '🌇',
            '夜晚': '🌙',
            '深夜': '🌌'
        }
        
        # 时间线图标映射
        self.timeline_icons = {
            '清晨': '☀️',
            '早晨': '🌅', 
            '上午': '🏛️',
            '中午': '🍽️',
            '下午': '🏠',
            '傍晚': '🛍️',
            '夜晚': '🌙',
            '深夜': '🌌'
        }
        
        # 活动类型图标
        self.activity_icons = {
            '茶楼': '🍵',
            '饮茶': '🍵',
            '早茶': '🍵',
            '文化': '🏛️',
            '建筑': '🏛️',
            '古建筑': '🏛️',
            '祠堂': '🏛️',
            '美食': '🍽️',
            '粤菜': '🍽️',
            '小吃': '🥟',
            '购物': '🛍️',
            '商街': '🛍️',
            '老街': '🏠',
            '漫步': '🚶',
            '散步': '🚶',
            '夜景': '🌃',
            '灯光': '💡'
        }
        
        # 段落分隔符
        self.paragraph_separators = ['\n\n', '\n\n\n']
        
    def format_text(self, text: str) -> str:
        """
        格式化文本，处理特殊符号和排版
        
        Args:
            text: 原始文本
            
        Returns:
            格式化后的文本
        """
        if not text:
            return text
        
        # 首先检查是否为emoji分点格式
        if self._is_emoji_format(text):
            return self._format_emoji_content(text)
            
        # 检测是否为时间线格式内容
        if self._is_timeline_content(text):
            return self._format_timeline(text)
        
    def _is_timeline_content(self, text: str) -> bool:
        formatted_text = self._process_markdown(text)
        
        # 2. 处理特殊符号
        formatted_text = self._process_special_symbols(formatted_text)
        
        # 3. 优化段落结构
        formatted_text = self._optimize_paragraphs(formatted_text)
        
        # 4. 处理列表格式
        formatted_text = self._process_lists(formatted_text)
        
        # 5. 美化引用和强调
        formatted_text = self._beautify_emphasis(formatted_text)
        
        # 6. 清理多余空白
        formatted_text = self._clean_whitespace(formatted_text)
        
        return formatted_text
    
    def _is_emoji_format(self, text: str) -> bool:
        """检测是否为emoji分点格式内容"""
        emoji_patterns = [
            r'## 📌',
            r'🔷\s*\*\*.*?\*\*',
            r'🔶\s*\*\*.*?\*\*',
            r'🔹\s*\*\*.*?\*\*',
            r'💡\s*\*\*.*?\*\*'
        ]
        
        return any(re.search(pattern, text) for pattern in emoji_patterns)
    
    def _format_emoji_content(self, text: str) -> str:
        """格式化emoji分点内容"""
        html = text
        
        # 处理主标题
        html = re.sub(r'## 📌\s*(.*?)$', r'<div class="emoji-format"><h2>\1</h2>', html, flags=re.MULTILINE)
        
        # 处理分点内容
        html = re.sub(r'🔷\s*\*\*(.*?)\*\*\s*\n(.*?)(?=\n\n|🔶|🔹|💡|---|$)', 
                     r'<div class="emoji-point blue"><strong>🔷 \1</strong><div class="content">\2</div></div>', 
                     html, flags=re.DOTALL)
        
        html = re.sub(r'🔶\s*\*\*(.*?)\*\*\s*\n(.*?)(?=\n\n|🔷|🔹|💡|---|$)', 
                     r'<div class="emoji-point orange"><strong>🔶 \1</strong><div class="content">\2</div></div>', 
                     html, flags=re.DOTALL)
        
        html = re.sub(r'🔹\s*\*\*(.*?)\*\*\s*\n(.*?)(?=\n\n|🔷|🔶|💡|---|$)', 
                     r'<div class="emoji-point light-blue"><strong>🔹 \1</strong><div class="content">\2</div></div>', 
                     html, flags=re.DOTALL)
        
        # 处理关键总结
        html = re.sub(r'💡\s*\*\*(.*?)\*\*\s*\n(.*?)(?=\n\n|---|$)', 
                     r'<div class="emoji-summary"><strong>💡 \1</strong><div class="content">\2</div></div>', 
                     html, flags=re.DOTALL)
        
        # 处理分隔线
        html = html.replace('---', '<hr class="emoji-divider">')
        
        # 关闭emoji-format容器
        if '<div class="emoji-format">' in html:
            html += '</div>'
        
        return html
    
    def _is_timeline_content(self, text: str) -> bool:
        """检测是否为时间线格式内容"""
        timeline_indicators = [
            '一日游', '行程', '时间安排', '游览路线', 
            '早晨', '上午', '中午', '下午', '傍晚', '夜晚',
            '清晨', '深夜', '时光', '时段'
        ]
        
        # 检查是否包含时间线指示词
        for indicator in timeline_indicators:
            if indicator in text:
                return True
                
        # 检查是否包含多个时间段
        time_periods = ['早晨', '上午', '中午', '下午', '傍晚', '夜晚', '清晨', '深夜']
        time_count = sum(1 for period in time_periods if period in text)
        
        return time_count >= 2
    
    def _format_timeline(self, text: str) -> str:
        """格式化时间线内容"""
        # 提取标题
        lines = text.strip().split('\n')
        title = ""
        subtitle = ""
        content_lines = lines
        
        # 检查是否有明显的标题
        if lines and ('一日游' in lines[0] or '行程' in lines[0] or '路线' in lines[0]):
            title = lines[0].strip()
            if len(lines) > 1 and len(lines[1].strip()) < 50:
                subtitle = lines[1].strip()
                content_lines = lines[2:]
            else:
                content_lines = lines[1:]
        
        # 构建时间线HTML
        timeline_html = f'''<div class="timeline-container">
    <div class="timeline-header">
        <div class="timeline-title">🏮 {title or "广府西关一日游"}</div>
        <div class="timeline-subtitle">{subtitle or "品味节庆文化，感受广府韵味"}</div>
    </div>
    <div class="timeline-main">'''
        
        current_content = ""
        current_time = ""
        current_icon = ""
        
        for line in content_lines:
            line = line.strip()
            if not line:
                continue
                
            # 检测时间段
            time_detected = False
            for time_period, icon in self.timeline_icons.items():
                if time_period in line:
                    # 如果有之前的内容，先输出
                    if current_content:
                        timeline_html += self._create_activity_card(current_time, current_icon, current_content)
                    
                    current_time = time_period
                    current_icon = icon
                    current_content = line
                    time_detected = True
                    break
            
            if not time_detected and current_content:
                current_content += "\n" + line
        
        # 输出最后一个活动
        if current_content:
            timeline_html += self._create_activity_card(current_time, current_icon, current_content)
        
        timeline_html += '''    </div>
    <div class="timeline-footer">
        <span class="timeline-footer-icon">🏮</span>
        这一日游精选了广府节庆文化的精华，每处都承载着代代相传的故事。<br>
        品味西关，感受广府人对生活的热爱与智慧！
    </div>
</div>'''
        
        return timeline_html
    
    def _create_activity_card(self, time_period: str, time_icon: str, content: str) -> str:
        """创建活动卡片"""
        # 提取活动标题和描述
        lines = content.split('\n')
        activity_title = ""
        activity_description = ""
        highlights = []
        tips = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检测活动类型和图标
            activity_icon = "🎯"
            for activity_type, icon in self.activity_icons.items():
                if activity_type in line:
                    activity_icon = icon
                    break
            
            # 提取标题（通常是第一行或包含关键词的行）
            if not activity_title and any(keyword in line for keyword in ['茶楼', '文化', '美食', '购物', '漫步', '夜景']):
                activity_title = line
            elif '推荐' in line or '必点' in line or '必看' in line or '特色' in line:
                highlights.append(line)
            elif '建议' in line or '提示' in line or '注意' in line:
                tips.append(line)
            elif not activity_description and line != activity_title:
                activity_description = line
        
        if not activity_title:
            activity_title = f"{time_period}时光"
        
        # 构建卡片HTML
        card_html = f'''
        <div class="time-period">
            <div class="time-period-icon">{time_icon}</div>
            <div class="time-period-text">{time_period}</div>
        </div>
        <div class="activity-card">
            <div class="activity-header">
                <div class="activity-icon">{activity_icon}</div>
                <h3 class="activity-title">{activity_title}</h3>
            </div>
            <div class="activity-description">{activity_description}</div>'''
        
        # 添加高亮信息
        if highlights:
            card_html += '''
            <div class="highlight-box">
                <div class="highlight-title">✨ 推荐亮点：</div>
                <ul class="highlight-list">'''
            for highlight in highlights:
                card_html += f'<li>{highlight}</li>'
            card_html += '</ul></div>'
        
        # 添加提示信息
        if tips:
            for tip in tips:
                card_html += f'''
            <div class="tip-box">
                <div class="tip-icon">💡</div>
                <div>{tip}</div>
            </div>'''
        
        card_html += '</div>'
        
        return card_html
    
    def _parse_expert_response(self, text: str) -> List[Dict]:
        """解析专家回复文本结构"""
        sections = []
        lines = text.strip().split('\n')
        current_section = {"title": "主要内容", "content": ""}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测是否为新的章节标题
            if self._is_section_title(line):
                # 保存当前章节
                if current_section["content"].strip():
                    sections.append(current_section)
                
                # 开始新章节
                current_section = {
                    "title": self._clean_section_title(line),
                    "content": ""
                }
            else:
                # 添加到当前章节内容
                if current_section["content"]:
                    current_section["content"] += "\n"
                current_section["content"] += line
        
        # 添加最后一个章节
        if current_section["content"].strip():
            sections.append(current_section)
        
        # 如果没有明确的章节，将整个文本作为一个章节
        if not sections:
            sections.append({"title": "详细介绍", "content": text})
        
        return sections
    
    def _is_section_title(self, line: str) -> bool:
        """判断是否为章节标题"""
        # 检测标题模式
        title_patterns = [
            r'^#{1,6}\s+',  # Markdown标题
            r'^\*\*.*\*\*$',  # 粗体标题
            r'^第[一二三四五六七八九十\d]+[站步章节]',  # 第X站/步/章/节
            r'^[🎯🌟📍🔷🔶🔹💡⭐✨🎊🎉🎭🏮🍽️🏗️]',  # Emoji开头
            r'^\d+[\.、]\s*',  # 数字编号
            r'^[一二三四五六七八九十][、．]\s*',  # 中文数字编号
        ]
        
        for pattern in title_patterns:
            if re.match(pattern, line):
                return True
        
        # 检测关键词标题
        title_keywords = [
            '推荐', '介绍', '特色', '亮点', '重点', '要点', 
            '路线', '行程', '安排', '计划', '攻略',
            '美食', '小吃', '茶点', '甜品', '菜品',
            '表演', '节目', '活动', '庆典', '仪式',
            '建筑', '景点', '地点', '场所', '位置',
            '工艺', '技法', '制作', '步骤', '方法',
            '历史', '文化', '传统', '故事', '背景',
            '总结', '小贴士', '注意事项', '温馨提示'
        ]
        
        return any(keyword in line for keyword in title_keywords)
    
    def _clean_section_title(self, title: str) -> str:
        """清理章节标题"""
        # 移除Markdown标记
        title = re.sub(r'^#{1,6}\s+', '', title)
        # 移除粗体标记
        title = re.sub(r'^\*\*(.*)\*\*$', r'\1', title)
        # 移除数字编号
        title = re.sub(r'^\d+[\.、]\s*', '', title)
        title = re.sub(r'^[一二三四五六七八九十][、．]\s*', '', title)
        
        return title.strip()
    
    def _get_section_icon(self, title: str, expert_type: str) -> str:
        """根据章节标题和专家类型获取图标"""
        # 通用图标映射
        icon_mapping = {
            # 位置相关
            '站': '📍', '地点': '📍', '位置': '📍', '场所': '🏛️',
            # 美食相关
            '美食': '🍽️', '小吃': '🥟', '茶点': '🍵', '甜品': '🧁', '菜品': '🍜',
            # 活动相关
            '表演': '🎭', '节目': '🎪', '活动': '🎊', '庆典': '🎉', '仪式': '🙏',
            # 建筑相关
            '建筑': '🏗️', '景点': '🏛️', '园林': '🌸', '街道': '🛤️',
            # 工艺相关
            '工艺': '🎨', '技法': '🔨', '制作': '👨‍🍳', '步骤': '📋',
            # 文化相关
            '历史': '📜', '文化': '📚', '传统': '🏮', '故事': '📖',
            # 其他
            '推荐': '⭐', '特色': '✨', '亮点': '🌟', '总结': '💡',
            '贴士': '💭', '提示': '⚠️', '注意': '❗'
        }
        
        # 根据标题内容匹配图标
        for keyword, icon in icon_mapping.items():
            if keyword in title:
                return icon
        
        # 根据专家类型返回默认图标
        default_icons = {
            "culinary": "🍽️",
            "cantonese_opera": "🎭", 
            "festival": "🎊",
            "architecture": "🏗️"
        }
        
        return default_icons.get(expert_type, "📝")
    
    def _format_section_content(self, content: str) -> str:
        """格式化章节内容"""
        # 首先应用现有的格式化逻辑
        formatted_content = self.format_text(content)
        
        # 检测特殊内容类型并添加样式
        lines = content.split('\n')
        enhanced_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                enhanced_lines.append('<br>')
                continue
            
            # 检测高亮内容
            if any(keyword in line for keyword in ['重要', '关键', '必须', '一定要', '特别']):
                enhanced_lines.append(f'<div class="highlight-box">{line}</div>')
            # 检测提示内容
            elif any(keyword in line for keyword in ['建议', '提示', '小贴士', '注意', '温馨提示']):
                enhanced_lines.append(f'<div class="tip-box">{line}</div>')
            # 检测文化引用
            elif any(keyword in line for keyword in ['古语', '俗话', '传说', '典故', '诗词']):
                enhanced_lines.append(f'<div class="cultural-quote">{line}</div>')
            else:
                enhanced_lines.append(line)
        
        return '<br>'.join(enhanced_lines)
    
    def _process_markdown(self, text: str) -> str:
        """处理Markdown格式"""
        # 处理标题
        for level in range(4, 0, -1):
            pattern = r'^' + '#' * level + r'\s*(.+)$'
            replacement = self.symbol_mapping.get('#' * level, '■') + ' \\1'
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
        
        # 处理粗体 **text** -> 【text】
        text = re.sub(r'\*\*([^*]+)\*\*', r'【\1】', text)
        
        # 处理斜体 *text* -> 《text》
        text = re.sub(r'\*([^*]+)\*', r'《\1》', text)
        
        # 处理代码块 `code` -> 「code」
        text = re.sub(r'`([^`]+)`', r'「\1」', text)
        
        return text
    
    def _process_special_symbols(self, text: str) -> str:
        """处理特殊符号"""
        # 移除所有剩余的星号（包括单独的星号和未被Markdown处理的星号）
        text = re.sub(r'\*+', '', text)
        
        # 处理破折号
        text = re.sub(r'---+', '——', text)
        
        # 处理省略号
        text = re.sub(r'\.{3,}', '…', text)
        
        # 处理引号
        text = re.sub(r'"([^"]*)"', r'"\1"', text)
        text = re.sub(r"'([^']*)'", r"'\1'", text)
        
        return text
    
    def _optimize_paragraphs(self, text: str) -> str:
        """优化段落结构"""
        # 规范化换行
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 在句号、问号、感叹号后添加适当的换行，但避免与表情符号冲突
        text = re.sub(r'([。！？])(?!\n)([^。！？\n🎭🎵⭐📚🏛️🏮🎨📜🍽️🍵👨‍🍳🥬😋🎊🎉📖📋])', r'\1\n\n\2', text)
        
        # 在"Day X"、"第X天"等标题后强制换行
        text = re.sub(r'(Day\s*\d+[：:][^。！？\n]*[。！？]?)(?!\n)', r'\1\n\n', text)
        text = re.sub(r'(第[一二三四五六七八九十\d]+天[：:][^。！？\n]*[。！？]?)(?!\n)', r'\1\n\n', text)
        
        # 在"---"分隔符前后添加换行
        text = re.sub(r'(?<!\n)\n?---\n?(?!\n)', r'\n\n---\n\n', text)
        
        # 在数字编号列表项前添加换行（如"1. "、"2. "等），但避免重复处理已格式化的步骤
        text = re.sub(r'(?<!\n)(?<!步骤)(\d+\.\s)', r'\n\n\1', text)
        
        # 确保步骤格式前有换行
        text = re.sub(r'(?<!\n)(📋\s*步骤|👨‍🍳\s*步骤)', r'\n\n\1', text)
        
        # 处理段落开头的缩进
        paragraphs = text.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                # 如果不是特殊格式（如列表、标题、表情符号开头、分隔符、步骤），添加缩进
                if not re.match(r'^[■●◆▶\-\*\d+\.]|^[🎭🎵⭐📚🏛️🏮🎨📜🍽️🍵👨‍🍳🥬😋🎊🎉📖📋]|^---', paragraph):
                    paragraph = '　　' + paragraph
                formatted_paragraphs.append(paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _process_lists(self, text: str) -> str:
        """处理列表格式 - 优化分点内容的排版和展示"""
        
        # 1. 处理无序列表（- 或 * 开头）
        text = re.sub(r'^[\-\*]\s*(.+)$', r'• \1', text, flags=re.MULTILINE)
        
        # 2. 优先处理标准分点格式（大模型按要求输出的格式）
        # 匹配形如：
        # 1. 内容
        # 
        # 2. 内容
        # 这种已经有空行分隔的标准格式
        standard_list_pattern = r'^(\d+)\.\s*(.+?)(?=\n\s*\n\s*\d+\.\s*|\n\s*\n\s*$|\Z)'
        matches = list(re.finditer(standard_list_pattern, text, re.MULTILINE | re.DOTALL))
        
        if matches:
            # 如果找到标准格式的分点，直接添加图标
            for match in reversed(matches):  # 从后往前替换避免位置偏移
                number = match.group(1)
                content = match.group(2).strip()
                replacement = f'📋 步骤{number}：{content}'
                text = text[:match.start()] + replacement + text[match.end():]
        else:
            # 3. 处理连续的数字列表（没有标准换行的情况）
            # 智能识别并分隔连续的数字列表项
            continuous_pattern = r'(\d+)\.\s*([^0-9\n]+?)(?=\s*\d+\.\s*|$)'
            continuous_matches = list(re.finditer(continuous_pattern, text))
            
            if len(continuous_matches) > 1:
                # 从后往前处理，避免位置偏移
                new_text = text
                for i in range(len(continuous_matches) - 1, 0, -1):
                    match = continuous_matches[i]
                    # 在当前匹配项前添加双换行
                    new_text = new_text[:match.start()] + '\n\n' + new_text[match.start():]
                text = new_text
            
            # 4. 为所有数字列表项添加步骤图标
            text = re.sub(r'^(\d+)\.\s*(.+)$', r'📋 步骤\1：\2', text, flags=re.MULTILINE)
        
        # 5. 处理烹饪相关的特殊步骤格式（替换为烹饪图标）
        cooking_keywords = [
            '烤', '炒', '煮', '蒸', '炖', '焖', '煎', '炸', '腌', '调', '拌', 
            '切', '洗', '选', '放', '加', '倒', '刷', '预热', '热锅', '下油', 
            '爆香', '翻炒', '起锅', '焯水', '过油', '勾芡', '收汁', '装盘',
            '撒', '淋', '浇', '蘸', '搅拌', '揉', '醒面', '发酵', '烘烤'
        ]
        
        for keyword in cooking_keywords:
            # 将包含烹饪关键词的步骤图标替换为烹饪图标
            text = re.sub(f'📋 步骤(\\d+)：([^\\n]*{keyword}[^\\n]*)', r'👨‍🍳 步骤\1：\2', text)
        
        # 6. 处理其他特殊格式
        # 处理时间点格式（如"上午："、"下午："等）
        text = re.sub(r'^([上下]午|早晨|中午|傍晚|晚上|夜晚)[：:]\s*', r'🕐 \1：', text, flags=re.MULTILINE)
        
        # 处理Day标题格式
        text = re.sub(r'^(Day\s*\d+)[：:]', r'📅 \1：', text, flags=re.MULTILINE)
        text = re.sub(r'^(第[一二三四五六七八九十\d]+天)[：:]', r'📅 \1：', text, flags=re.MULTILINE)
        
        # 7. 优化分点内容的视觉效果
        # 确保每个步骤前后都有适当的空白
        text = re.sub(r'(📋|👨‍🍳)\s*步骤(\d+)：', r'\n\1 步骤\2：', text)
        text = re.sub(r'^(\n)+(📋|👨‍🍳)', r'\n\2', text, flags=re.MULTILINE)
        
        return text
    
    def _beautify_emphasis(self, text: str) -> str:
        """美化引用和强调"""
        # 处理引用块
        text = re.sub(r'^>\s*(.+)$', r'💬 \1', text, flags=re.MULTILINE)
        
        # 美化重要提示
        text = re.sub(r'注意[:：]\s*', '⚠️ 注意：', text)
        text = re.sub(r'提示[:：]\s*', '💡 提示：', text)
        text = re.sub(r'重要[:：]\s*', '⭐ 重要：', text)
        
        return text
    
    def _clean_whitespace(self, text: str) -> str:
        """清理多余空白"""
        # 移除行首行尾空白
        lines = [line.rstrip() for line in text.split('\n')]
        
        # 移除空行过多的情况
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            if line.strip():
                cleaned_lines.append(line)
                prev_empty = False
            elif not prev_empty:
                cleaned_lines.append('')
                prev_empty = True
        
        return '\n'.join(cleaned_lines).strip()
    
    def format_expert_response(self, text: str, expert_type: str = None) -> str:
        """
        格式化专家回复为精美卡片布局
        
        Args:
            text: 专家回复文本
            expert_type: 专家类型 (culinary, cantonese_opera, festival, architecture)
        
        Returns:
            格式化后的HTML
        """
        # 专家信息映射
        expert_info = {
            "culinary": {"name": "味师傅", "icon": "👨‍🍳", "title": "广府美食文化"},
            "cantonese_opera": {"name": "梅韵师傅", "icon": "🎭", "title": "粤剧艺术传承"},
            "festival": {"name": "庆师傅", "icon": "🎊", "title": "节庆民俗文化"},
            "architecture": {"name": "匠师傅", "icon": "🏗️", "title": "建筑工艺传统"},
            "general": {"name": "文化师傅", "icon": "🏮", "title": "广府文化"}
        }
        
        expert = expert_info.get(expert_type, expert_info["general"])
        
        # 分析文本结构
        sections = self._parse_expert_response(text)
        
        # 构建卡片HTML
        card_html = f'''<div class="expert-response-card">
    <div class="expert-response-header">
        <div class="expert-response-title">
            <span class="title-icon">{expert["icon"]}</span>
            {expert["title"]}指南
        </div>
        <div class="expert-response-subtitle">
            {expert["name"]}为您精心整理
        </div>
    </div>
    <div class="expert-response-body">'''
        
        # 添加各个部分
        for i, section in enumerate(sections):
            section_icon = self._get_section_icon(section["title"], expert_type)
            card_html += f'''
        <div class="expert-response-section">
            <div class="section-title">
                <span class="section-icon">{section_icon}</span>
                {section["title"]}
            </div>
            <div class="section-content">
                {self._format_section_content(section["content"])}
            </div>
        </div>'''
        
        # 添加底部签名
        card_html += f'''
    </div>
    <div class="expert-response-footer">
        <div class="expert-signature">
            <span class="expert-name">{expert["name"]}</span>
            <span class="expert-timestamp">刚刚</span>
        </div>
    </div>
</div>'''
        
        return card_html
    
    def _add_opera_decorations(self, text: str) -> str:
        """为粤剧专家回复添加装饰"""
        # 添加戏曲相关的表情符号和格式优化
        text = re.sub(r'(粤剧|戏曲)', r'🎭 \1', text)
        text = re.sub(r'(唱腔|表演|演出)', r'🎵 \1', text)
        text = re.sub(r'(名角|演员|艺术家)', r'⭐ \1', text)
        text = re.sub(r'(剧目|经典|传统)', r'📚 \1', text)
        
        # 优化段落结构 - 在重要信息前添加换行
        text = re.sub(r'([。！？])\s*(🎭|🎵|⭐|📚)', r'\1\n\n\2', text)
        
        return text
    
    def _add_architecture_decorations(self, text: str) -> str:
        """为建筑专家回复添加装饰"""
        # 添加建筑相关的表情符号和格式优化
        text = re.sub(r'(建筑|骑楼|楼房)', r'🏛️ \1', text)
        text = re.sub(r'(园林|庭院|花园)', r'🏮 \1', text)
        text = re.sub(r'(雕刻|装饰|工艺)', r'🎨 \1', text)
        text = re.sub(r'(历史|文化|传承)', r'📜 \1', text)
        
        # 优化段落结构
        text = re.sub(r'([。！？])\s*(🏛️|🏮|🎨|📜)', r'\1\n\n\2', text)
        
        return text
    
    def _add_culinary_decorations(self, text: str) -> str:
        """为美食专家回复添加装饰"""
        # 添加美食相关的表情符号和格式优化
        text = re.sub(r'(美食|菜品|佳肴)', r'🍽️ \1', text)
        text = re.sub(r'(茶楼|点心|小食)', r'🍵 \1', text)
        text = re.sub(r'(烹饪|制作|技艺)', r'👨‍🍳 \1', text)
        text = re.sub(r'(食材|原料|配菜)', r'🥬 \1', text)
        text = re.sub(r'(口感|味道|香味)', r'😋 \1', text)
        
        # 优化段落结构
        text = re.sub(r'([。！？])\s*(🍽️|🍵|👨‍🍳|🥬|😋)', r'\1\n\n\2', text)
        
        return text
    
    def _add_festival_decorations(self, text: str) -> str:
        """为节庆专家回复添加装饰"""
        # 添加节庆相关的表情符号和格式优化
        text = re.sub(r'(节庆|民俗|庆典)', r'🎊 \1', text)
        text = re.sub(r'(传统|习俗|风俗)', r'🏮 \1', text)
        text = re.sub(r'(活动|仪式|庆祝)', r'🎉 \1', text)
        text = re.sub(r'(文化|历史|意义)', r'📖 \1', text)
        
        # 优化段落结构
        text = re.sub(r'([。！？])\s*(🎊|🏮|🎉|📖)', r'\1\n\n\2', text)
        
        return text


# 创建全局格式化器实例
text_formatter = TextFormatter()


def format_agent_response(text: str, expert_type: str = None) -> str:
    """
    格式化智能体回复的便捷函数
    
    Args:
        text: 原始文本
        expert_type: 专家类型
        
    Returns:
        格式化后的文本
    """
    return text_formatter.format_expert_response(text, expert_type)