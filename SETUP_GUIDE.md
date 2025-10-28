# 硅基流动API接入指南

## 配置步骤

### 1. 获取硅基流动API密钥
1. 访问 [硅基流动官网](https://siliconflow.cn/)
2. 注册账号并获取API密钥
3. 记录您的API密钥

### 2. 配置环境变量
创建 `.env` 文件并添加以下配置：

```bash
# 硅基流动API配置
SILICON_FLOW_API_KEY=your_silicon_flow_api_key_here
SILICON_FLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICON_FLOW_MODEL=Qwen/QwQ-32B

# 其他配置
DATABASE_URL=sqlite:///./agent_system.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 启动服务
```bash
# Windows
run.bat

# Linux/Mac
./run.sh

# 或手动启动
python start.py --reload
```

## API接入说明

### 智能体API调用流程
1. **用户提问** → 前端发送WebSocket消息
2. **智能体处理** → 调用硅基流动API
3. **知识检索** → 从本地知识库获取相关信息
4. **消息构建** → 构建包含系统提示词、历史对话、用户问题的消息
5. **API调用** → 发送到硅基流动API
6. **响应处理** → 处理API响应并返回给用户

### 硅基流动API特点
- **模型**: Qwen/QwQ-32B (通义千问大模型)
- **支持**: 中文对话、文化知识问答
- **优势**: 成本低、响应快、中文理解好

### 智能体配置
每个智能体都有：
- **系统提示词**: 定义专家身份和专业领域
- **对话历史**: 保持上下文连贯性
- **知识库**: 广府文化专业知识
- **个性化**: 不同的表达风格和专业知识

## 测试API连接

### 简单测试脚本
```python
import asyncio
from core.llm_client import get_silicon_flow_client

async def test_api():
    client = get_silicon_flow_client()
    
    messages = [
        {"role": "system", "content": "你是粤剧专家"},
        {"role": "user", "content": "请介绍一下粤剧的历史"}
    ]
    
    response = await client.chat_completion(messages)
    print(response)

# 运行测试
asyncio.run(test_api())
```

### 检查配置
```bash
python start.py --check
```

## 故障排除

### 常见问题
1. **API密钥错误**: 检查 `.env` 文件中的 `SILICON_FLOW_API_KEY`
2. **网络连接**: 确保能访问 `api.siliconflow.cn`
3. **依赖缺失**: 运行 `pip install -r requirements.txt`
4. **端口占用**: 修改 `PORT` 配置或停止占用端口的程序

### 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误信息
python start.py --reload 2>&1 | tee debug.log
```

## 性能优化

### API调用优化
- 使用异步调用避免阻塞
- 设置合理的超时时间
- 实现请求重试机制
- 缓存常用知识

### 智能体优化
- 限制对话历史长度
- 优化提示词结构
- 实现知识库检索
- 添加错误处理

## 扩展功能

### 添加新模型
在 `config.py` 中添加新模型配置：
```python
SILICON_FLOW_MODEL_ALT=Qwen/QwQ-14B
```

### 自定义智能体
1. 创建新的专家类
2. 设置系统提示词
3. 实现专业知识库
4. 注册到协同管理器

### 流式响应
使用 `stream_chat_completion` 方法实现实时响应：
```python
async for chunk in client.stream_chat_completion(messages):
    print(chunk, end='', flush=True)
```

---

**硅基流动API接入完成！** 🎉
现在您的广府非遗文化多智能体协同平台已经成功接入硅基流动API，可以开始使用了！

