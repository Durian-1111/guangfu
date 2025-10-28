# 广府非遗文化多智能体协同平台

基于 LangChain 和 LangGraph 构建的广府非遗文化多智能体协同系统，提供专业的文化介绍和协同讨论服务。

## 功能特色

### 🎭 专家智能体
- **粤剧专家**：精通粤剧历史、表演艺术、唱腔特点
- **建筑专家**：了解广府传统建筑、骑楼文化、岭南园林
- **美食专家**：熟悉广府菜系、茶楼文化、传统小吃
- **节庆专家**：掌握广府传统节庆、民俗活动、文化仪式

### 🤝 多智能体协同
- 基于 LangGraph 的智能体协同工作流
- 多专家协同讨论和知识融合
- 智能问题分析和专家选择
- 综合文化解读和总结

### 💬 实时对话
- WebSocket 实时通信
- 智能对话管理
- 对话历史记录
- 多模态交互支持

## 技术架构

### 核心技术栈
- **后端框架**：FastAPI
- **AI框架**：LangChain + LangGraph
- **大语言模型**：硅基流动 (Qwen/QwQ-32B)
- **数据库**：SQLite + Redis
- **向量数据库**：ChromaDB
- **前端**：Bootstrap 5 + JavaScript
- **通信**：WebSocket

### 系统架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端界面      │    │   FastAPI服务   │    │   智能体系统    │
│                 │◄──►│                 │◄──►│                 │
│  - 专家展示     │    │  - 路由管理     │    │  - 粤剧专家     │
│  - 协同讨论     │    │  - WebSocket    │    │  - 建筑专家     │
│  - 实时聊天     │    │  - API接口      │    │  - 美食专家     │
└─────────────────┘    └─────────────────┘    │  - 节庆专家     │
                                           │  - 协同管理器   │
┌─────────────────┐    ┌─────────────────┐    └─────────────────┘
│   知识库        │    │   对话管理      │
│                 │    │                 │
│  - 文化知识     │    │  - 对话历史     │
│  - 向量检索     │    │  - 会话管理     │
│  - 知识融合     │    │  - 状态跟踪     │
└─────────────────┘    └─────────────────┘
```

## 快速开始

### 环境要求
- Python 3.8+
- 硅基流动API密钥
- Node.js 16+ (可选，用于前端开发)
- Redis (可选，用于缓存)

### 获取硅基流动API密钥
1. 访问 [硅基流动官网](https://siliconflow.cn/)
2. 注册账号并获取API密钥
3. 记录您的API密钥

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境变量
```bash
# 创建配置文件
touch .env

# 编辑配置文件，设置您的硅基流动 API Key
SILICON_FLOW_API_KEY=your_silicon_flow_api_key_here
SILICON_FLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICON_FLOW_MODEL=Qwen/QwQ-32B
```

### 测试API连接
```bash
# 测试硅基流动API连接
python start.py --test

# 或直接运行测试脚本
python test_api.py
```

### 启动服务
```bash
# 启动应用
python start.py --reload

# 或使用 uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 访问应用
打开浏览器访问：http://localhost:8000

## 使用指南

### 1. 专家智能体对话
- 访问 `/agents` 页面
- 选择感兴趣的专家智能体
- 开始专业对话

### 2. 多智能体协同讨论
- 访问 `/collaboration` 页面
- 提出复杂问题
- 观看多位专家协同讨论

### 3. API 接口
- `GET /api/agents` - 获取所有智能体信息
- `WebSocket /ws` - 实时对话接口

## 项目结构

```
agent_system/
├── agents/                 # 智能体模块
│   ├── cantonese_opera_expert.py
│   ├── architecture_expert.py
│   ├── culinary_expert.py
│   ├── festival_expert.py
│   └── collaboration_manager.py
├── core/                  # 核心模块
│   ├── conversation_manager.py
│   └── knowledge_base.py
├── templates/             # 前端模板
│   ├── index.html
│   ├── agents.html
│   └── collaboration.html
├── static/                # 静态文件
│   ├── css/
│   └── js/
├── app.py                 # 主应用
├── config.py             # 配置文件
├── requirements.txt      # 依赖包
└── README.md            # 项目说明
```

## 开发指南

### 添加新的专家智能体
1. 在 `agents/` 目录下创建新的专家类
2. 继承基础智能体接口
3. 实现专业知识和对话逻辑
4. 在 `collaboration_manager.py` 中注册新专家

### 扩展知识库
1. 在 `core/knowledge_base.py` 中添加文化知识
2. 使用向量数据库存储和检索
3. 实现知识融合算法

### 自定义协同工作流
1. 修改 `collaboration_manager.py` 中的工作流定义
2. 调整智能体间的协作逻辑
3. 优化知识融合策略

## 部署说明

### Docker 部署
```bash
# 构建镜像
docker build -t guangfu-heritage-platform .

# 运行容器
docker run -p 8000:8000 guangfu-heritage-platform
```

### 生产环境配置
- 使用 PostgreSQL 替代 SQLite
- 配置 Redis 集群
- 设置负载均衡
- 启用 HTTPS

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目 Issues
- 邮箱：your-email@example.com

---

**广府非遗文化多智能体协同平台** - 传承文化，智能对话
