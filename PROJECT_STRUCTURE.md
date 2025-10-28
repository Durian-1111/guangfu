# 项目结构说明

## 广府非遗文化多智能体协同平台

```
agent_system/
├── 📁 agents/                    # 智能体模块
│   ├── __init__.py               # 模块初始化
│   ├── cantonese_opera_expert.py # 粤剧专家智能体
│   ├── architecture_expert.py    # 建筑专家智能体
│   ├── culinary_expert.py       # 美食专家智能体
│   ├── festival_expert.py       # 节庆专家智能体
│   └── collaboration_manager.py # 协同管理器
├── 📁 core/                      # 核心模块
│   ├── __init__.py               # 模块初始化
│   ├── conversation_manager.py   # 对话管理器
│   └── knowledge_base.py         # 知识库管理器
├── 📁 templates/                 # 前端模板
│   ├── index.html               # 主页
│   ├── agents.html              # 专家智能体页面
│   └── collaboration.html       # 协同讨论页面
├── 📁 static/                    # 静态文件
│   ├── 📁 css/
│   │   └── main.css             # 主样式文件
│   └── 📁 js/
│       ├── agents.js            # 专家页面脚本
│       └── collaboration.js     # 协同讨论脚本
├── 📁 data/                      # 数据目录
│   └── 📁 chroma_db/            # 向量数据库
├── 📁 logs/                      # 日志目录
├── app.py                       # 主应用文件
├── config.py                    # 配置文件
├── start.py                     # 启动脚本
├── requirements.txt             # 依赖包列表
├── run.bat                      # Windows启动脚本
├── run.sh                       # Linux/Mac启动脚本
├── README.md                    # 项目说明
└── PROJECT_STRUCTURE.md         # 项目结构说明
```

## 系统架构

### 1. 智能体层 (Agents Layer)
- **粤剧专家**: 专门处理粤剧相关的文化问题
- **建筑专家**: 负责广府建筑、骑楼文化等
- **美食专家**: 处理岭南美食、茶楼文化等
- **节庆专家**: 管理传统节庆、民俗活动等
- **协同管理器**: 协调多个智能体的协同工作

### 2. 核心服务层 (Core Services)
- **对话管理器**: 管理用户对话历史和会话状态
- **知识库管理器**: 管理广府文化知识库和向量检索
- **配置管理**: 统一管理应用配置

### 3. 接口层 (API Layer)
- **FastAPI应用**: 提供RESTful API和WebSocket接口
- **路由管理**: 处理HTTP请求和WebSocket连接
- **静态文件服务**: 提供前端资源

### 4. 前端层 (Frontend Layer)
- **主页**: 展示平台特色和功能介绍
- **专家页面**: 与单个专家智能体对话
- **协同页面**: 多智能体协同讨论界面

## 技术特点

### 🤖 多智能体协同
- 基于LangGraph的工作流管理
- 智能体间的协作和知识融合
- 动态专家选择和问题分配

### 💬 实时对话
- WebSocket实时通信
- 智能对话状态管理
- 多模态交互支持

### 🧠 知识管理
- 向量数据库存储文化知识
- 智能知识检索和推荐
- 知识融合和总结

### 🎨 用户界面
- 响应式设计，支持多设备
- 直观的专家选择和对话界面
- 实时协同讨论展示

## 部署说明

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 OpenAI API Key

# 启动服务
python start.py --reload
```

### 生产环境
```bash
# 使用 uvicorn 启动
uvicorn app:app --host 0.0.0.0 --port 8000

# 或使用 Docker
docker build -t guangfu-heritage-platform .
docker run -p 8000:8000 guangfu-heritage-platform
```

## 扩展指南

### 添加新专家
1. 在 `agents/` 目录创建新的专家类
2. 实现专业知识和对话逻辑
3. 在 `collaboration_manager.py` 中注册
4. 更新前端界面

### 扩展知识库
1. 在 `core/knowledge_base.py` 中添加知识
2. 使用向量数据库存储
3. 实现智能检索算法

### 自定义工作流
1. 修改 `collaboration_manager.py` 中的工作流
2. 调整智能体协作逻辑
3. 优化知识融合策略

---

**广府非遗文化多智能体协同平台** - 传承文化，智能对话

