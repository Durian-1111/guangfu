# 新功能开发指南

## 概述
本文档描述已实现和待实现的新功能，所有功能都确保不影响原有系统运行。

---

## ✅ 已实现的功能

### 1. 新增专家智能体

#### 茶文化专家（已实现）
- **文件**: `agent_system/agents/tea_culture_expert.py`
- **功能**: 茶艺茶道、茶叶品种、茶具鉴赏、饮茶习俗
- **特点**: 温和儒雅，注重茶文化细节

#### 手工艺专家（已实现）
- **文件**: `agent_system/agents/craft_expert.py`
- **功能**: 广绣、广彩、雕刻、传统技艺
- **特点**: 匠心独具，精益求精

---

## 🔨 待实现的功能

### 2. 新增专家智能体

#### 诗词文学专家（待实现）
**创建文件**: `agent_system/agents/literature_expert.py`

```python
"""
诗词文学专家智能体
专门负责广府诗词文学相关的文化介绍和问答
"""

from typing import Dict, Any
from core.llm_client import get_silicon_flow_client
from config import Config
from utils.text_formatter import format_agent_response

class LiteratureExpert:
    def __init__(self):
        self.name = "诗词文学专家"
        self.specialties = ["古典诗词", "岭南文学", "广府诗词", "文学鉴赏", "文化传承"]
        self.personality = "博学文雅，对广府诗词文学有深厚造诣，善于从文学美学角度解读诗词精髓"
        
        # 系统提示词模板
        self.system_prompt = """你是广府文化中的诗词文学专家，名叫文师傅...
        精通广府诗词、岭南文学、古典诗词鉴赏、文学传承等"""

    # 实现与其他专家相同的方法：
    # - interact_with_other_experts
    # - interact_with_other_experts_stream
    # - process_query_stream
    # - process_query
    # - _retrieve_knowledge
    # - _get_default_response
    # - get_expert_info
```

**集成步骤**:
1. 在 `app.py` 导入: `from agents.literature_expert import LiteratureExpert`
2. 初始化: `literature_expert = LiteratureExpert()`
3. 添加到专家映射和API路由

---

#### 中医药专家（待实现）
**创建文件**: `agent_system/agents/tcm_expert.py`

```python
"""
中医药专家智能体
专门负责中医药相关的文化介绍和问答
"""

class TCMExpert:
    def __init__(self):
        self.name = "中医药专家"
        self.specialties = ["中医理论", "中药方剂", "养生保健", "食疗文化", "针灸推拿"]
        self.personality = "博学严谨，对中医药文化有深入研究，善于从养生保健角度提供建议"
        
        # 系统提示词
        self.system_prompt = """你是广府文化中的中医药专家，名叫老中医师傅...
        精通中医理论、中药方剂、养生保健、食疗文化、针灸推拿等"""

    # 实现标准方法...
```

---

### 3. 文化知识图谱功能

**目标**: 可视化广府文化的传承脉络和知识关联

**实现方案**:
1. **后端接口** (`app.py` 添加路由):
```python
@app.get("/api/knowledge_graph")
async def get_knowledge_graph():
    """获取文化知识图谱数据"""
    return {
        "nodes": [
            {"id": "cantonese_opera", "label": "粤剧", "type": "culture"},
            {"id": "architecture", "label": "建筑", "type": "culture"},
            # ... 更多节点
        ],
        "edges": [
            {"source": "cantonese_opera", "target": "architecture", "relation": "相关"},
            # ... 更多关系
        ]
    }
```

2. **前端展示** (`static/js/knowledge_graph.js`):
- 使用 D3.js 或 vis.js 绘制图谱
- 支持交互：点击节点查看详情
- 支持搜索和过滤

3. **知识库** (`data/knowledge_base/`):
- 构建 JSON 格式的知识关系数据
- 定期更新文化传承脉络

---

### 4. 学习路径推荐功能

**目标**: 根据用户兴趣推荐个性化学习路径

**实现方案**:
1. **后端接口** (`app.py`):
```python
@app.post("/api/learning_path/recommend")
async def recommend_learning_path(request: Request):
    """推荐学习路径"""
    data = await request.json()
    interests = data.get("interests", [])
    
    # 根据兴趣推荐学习路径
    paths = {
        "入门": ["广府文化概述", "基础概念"],
        "进阶": ["专家对话", "深入学习"],
        "高级": ["协同讨论", "专业知识"]
    }
    return {"paths": paths}
```

2. **前端页面** (`templates/learning_path.html`):
- 展示学习路径
- 支持进度跟踪

---

### 5. 语音交互功能

**目标**: 支持语音输入和语音输出

**实现方案**:
1. **前端录音** (`static/js/voice_interaction.js`):
```javascript
// 使用 Web Speech API
const recognition = new webkitSpeechRecognition();
recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    // 发送到后端处理
};
```

2. **后端语音处理** (`app.py`):
```python
@app.post("/api/voice/process")
async def process_voice(request: Request):
    """处理语音输入"""
    # 转换语音为文本
    # 调用专家智能体
    # 返回文本回复
    pass

@app.get("/api/voice/synthesize")
async def synthesize_voice(text: str):
    """文本转语音"""
    # 使用 TTS 服务
    pass
```

---

### 6. 文化日历功能

**目标**: 展示广府传统节日和重要文化日期

**实现方案**:
1. **后端接口** (`app.py`):
```python
@app.get("/api/cultural_calendar/{year}/{month}")
async def get_cultural_calendar(year: int, month: int):
    """获取文化日历"""
    calendar_data = {
        "2024-01-01": {"festival": "元旦", "culture": "传统节庆"},
        "2024-02-10": {"festival": "春节", "culture": "最重要的传统节日"},
        # ... 更多日期
    }
    return {"dates": calendar_data}
```

2. **前端展示** (`templates/calendar.html`):
- 日历视图
- 点击查看详情
- 关联专家智能体

---

### 7. 改进多轮对话与上下文

**目标**: 更好的上下文管理和对话连贯性

**改进方案**:
1. **增强对话历史** (`core/conversation_manager.py`):
```python
class ConversationManager:
    def __init__(self):
        self.history = []
        self.max_history_length = 50  # 增加历史长度
        
    async def add_message(self, role, content, metadata=None):
        """添加消息，支持元数据"""
        self.history.append({
            "role": role,
            "content": content,
            "metadata": metadata,
            "timestamp": time.time()
        })
        
    def get_relevant_context(self, query, limit=10):
        """获取相关上下文"""
        # 使用向量检索或关键词匹配
        pass
```

2. **对话状态管理**:
- 跟踪对话主题
- 识别用户意图
- 自动切换专家

---

### 8. 多媒体支持

**目标**: 支持图片、音频、视频的展示和处理

**实现方案**:
1. **图片上传** (`app.py`):
```python
@app.post("/api/upload/image")
async def upload_image(file: UploadFile):
    """上传图片"""
    # 保存图片
    # 使用图像识别API分析
    # 返回描述文本
    pass
```

2. **音频支持**:
- 使用 Web Audio API 录制
- 支持音频文件上传
- 提取音频特征

3. **视频支持**:
- 使用 HTML5 video
- 支持视频播放
- 字幕显示

---

### 9. 个性化推荐功能

**目标**: 根据用户行为和兴趣推荐内容

**实现方案**:
1. **用户画像**:
```python
class UserProfile:
    def __init__(self):
        self.interests = []  # 用户兴趣
        self.history = []     # 对话历史
        self.preferences = {}  # 偏好设置
        
    def update_profile(self, interaction):
        """更新用户画像"""
        # 分析交互数据
        # 更新兴趣标签
        pass
```

2. **推荐算法**:
- 基于内容的推荐
- 协同过滤
- 混合推荐

---

## 📋 实现优先级

### 高优先级（核心功能）
1. ✅ 茶文化专家
2. ✅ 手工艺专家  
3. ⭐ 诗词文学专家
4. ⭐ 中医药专家

### 中优先级（功能增强）
5. 文化知识图谱
6. 学习路径推荐
7. 改进多轮对话

### 低优先级（高级功能）
8. 语音交互
9. 文化日历
10. 多媒体支持
11. 个性化推荐

---

## 🛠️ 开发建议

### 保持原有功能
- ✅ 所有新功能都通过新文件和新路由实现
- ✅ 不修改原有的核心逻辑
- ✅ 使用接口扩展而非替换

### 代码规范
- 遵循现有代码风格
- 添加适当的注释
- 错误处理和日志记录

### 测试建议
1. 单元测试每个新功能
2. 集成测试确保不影响原有功能
3. 性能测试优化响应速度

---

## 📝 更新记录

- 2024-01-XX: 创建文档
- 2024-01-XX: 实现茶文化专家 ✅
- 2024-01-XX: 实现手工艺专家 ✅

