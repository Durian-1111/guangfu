"""
广府非遗文化多智能体协同平台
基于 LangChain 和 LangGraph 构建
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
import json
import asyncio
from typing import List, Dict, Any
import logging

from agents.cantonese_opera_expert import CantoneseOperaExpert
from agents.architecture_expert import ArchitectureExpert
from agents.culinary_expert import CulinaryExpert
from agents.festival_expert import FestivalExpert
from agents.tea_culture_expert import TeaCultureExpert
from agents.craft_expert import CraftExpert
from agents.literature_expert import LiteratureExpert
from agents.tcm_expert import TCMExpert
from agents.collaboration_manager import CollaborationManager
from agents.guangfu_ambassador import GuangfuAmbassador
from core.conversation_manager import ConversationManager
from core.knowledge_base import KnowledgeBase

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="广府非遗文化多智能体协同平台",
    description="基于LangGraph的广府非遗文化专家智能体协同系统",
    version="1.0.0"
)

# 静态文件和模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 初始化智能体
cantonese_opera_expert = CantoneseOperaExpert()
architecture_expert = ArchitectureExpert()
culinary_expert = CulinaryExpert()
festival_expert = FestivalExpert()
tea_culture_expert = TeaCultureExpert()
craft_expert = CraftExpert()
literature_expert = LiteratureExpert()
tcm_expert = TCMExpert()
collaboration_manager = CollaborationManager()
guangfu_ambassador = GuangfuAmbassador()
conversation_manager = ConversationManager()
knowledge_base = KnowledgeBase()

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """关于页面"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/collaboration", response_class=HTMLResponse)
async def collaboration_page(request: Request):
    """协同讨论页面"""
    return templates.TemplateResponse("collaboration.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """聊天页面"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/knowledge-graph", response_class=HTMLResponse)
async def knowledge_graph_page(request: Request):
    """文化知识图谱页面"""
    return templates.TemplateResponse("knowledge_graph.html", {"request": request})

@app.get("/learning-path", response_class=HTMLResponse)
async def learning_path_page(request: Request):
    """学习路径推荐页面"""
    return templates.TemplateResponse("learning_path.html", {"request": request})

@app.get("/voice-chat", response_class=HTMLResponse)
async def voice_chat_page(request: Request):
    """语音交互页面"""
    return templates.TemplateResponse("voice_chat.html", {"request": request})

@app.get("/cultural-calendar", response_class=HTMLResponse)
async def cultural_calendar_page(request: Request):
    """文化日历页面"""
    return templates.TemplateResponse("cultural_calendar.html", {"request": request})

@app.get("/features", response_class=HTMLResponse)
async def features_page(request: Request):
    """功能中心页面"""
    return templates.TemplateResponse("features.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接处理"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 处理不同类型的消息
            if message_data["type"] == "chat":
                response = await handle_chat_message(message_data)
                await manager.send_personal_message(
                    json.dumps(response, ensure_ascii=False), 
                    websocket
                )
            elif message_data["type"] == "collaboration":
                response = await handle_collaboration_message(message_data)
                await manager.send_personal_message(
                    json.dumps(response, ensure_ascii=False), 
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def handle_chat_message_stream(message_data: Dict[str, Any]):
    """处理流式聊天消息"""
    user_input = message_data["message"]
    agent_type = message_data.get("agent_id", message_data.get("agent_type", "cantonese_opera_critic"))
    
    # 根据智能体类型选择专家（聊天页面只调用单个专家，不使用协同管理器）
    if agent_type == "cantonese_opera_critic":
        async for chunk in cantonese_opera_expert.process_query_stream(user_input):
            yield chunk
    elif agent_type == "architecture_expert":
        async for chunk in architecture_expert.process_query_stream(user_input):
            yield chunk
    elif agent_type == "culinary_expert":
        async for chunk in culinary_expert.process_query_stream(user_input):
            yield chunk
    elif agent_type == "festival_expert":
        async for chunk in festival_expert.process_query_stream(user_input):
            yield chunk
    elif agent_type == "tea_culture_expert":
        async for chunk in tea_culture_expert.process_query_stream(user_input):
            yield chunk
    elif agent_type == "craft_expert":
        async for chunk in craft_expert.process_query_stream(user_input):
            yield chunk
    elif agent_type == "literature_expert":
        async for chunk in literature_expert.process_query_stream(user_input):
            yield chunk
    elif agent_type == "tcm_expert":
        async for chunk in tcm_expert.process_query_stream(user_input):
            yield chunk
    else:
        # 默认使用粤剧专家（聊天页面不使用协同管理器）
        async for chunk in cantonese_opera_expert.process_query_stream(user_input):
            yield chunk

async def handle_chat_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """处理聊天消息"""
    user_input = message_data["message"]
    agent_type = message_data.get("agent_id", message_data.get("agent_type", "cantonese_opera_critic"))
    
    # 根据智能体类型选择专家（聊天页面只调用单个专家，不使用协同管理器）
    if agent_type == "cantonese_opera_critic":
        response = await cantonese_opera_expert.process_query(user_input)
    elif agent_type == "architecture_expert":
        response = await architecture_expert.process_query(user_input)
    elif agent_type == "culinary_expert":
        response = await culinary_expert.process_query(user_input)
    elif agent_type == "festival_expert":
        response = await festival_expert.process_query(user_input)
    elif agent_type == "tea_culture_expert":
        response = await tea_culture_expert.process_query(user_input)
    elif agent_type == "craft_expert":
        response = await craft_expert.process_query(user_input)
    elif agent_type == "literature_expert":
        response = await literature_expert.process_query(user_input)
    elif agent_type == "tcm_expert":
        response = await tcm_expert.process_query(user_input)
    else:
        # 默认使用粤剧专家（聊天页面不使用协同管理器）
        response = await cantonese_opera_expert.process_query(user_input)
    
    return {
        "type": "response",
        "content": response,
        "agent": agent_type,
        "timestamp": asyncio.get_event_loop().time()
    }

async def handle_collaboration_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """处理协同讨论消息"""
    user_input = message_data["message"]
    
    # 启动多智能体协同讨论
    collaboration_result = await collaboration_manager.start_collaboration(user_input)
    
    return {
        "type": "collaboration_response",
        "content": collaboration_result,
        "participants": ["粤剧专家", "建筑专家", "美食专家", "节庆专家"],
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/api/conversations")
async def get_conversations(user_id: str):
    """获取用户对话历史"""
    try:
        # 从会话管理器获取对话历史
        conversations = await conversation_manager.get_user_conversations(user_id)
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"获取对话历史失败: {e}")
        return {"conversations": []}

@app.get("/api/agents")
async def get_agents():
    """获取所有智能体信息"""
    return {
        "agents": [
            {"id": "cantonese_opera", "name": "粤剧专家", "description": "精通粤剧历史、表演艺术、唱腔特点"},
            {"id": "architecture", "name": "广府建筑专家", "description": "了解广府传统建筑、骑楼文化、岭南园林"},
            {"id": "culinary", "name": "岭南美食专家", "description": "熟悉广府菜系、茶楼文化、传统小吃"},
            {"id": "festival", "name": "节庆文化专家", "description": "掌握广府传统节庆、民俗活动、文化仪式"},
            {"id": "tea_culture", "name": "茶文化专家", "description": "精通茶艺茶道、茶叶品种、茶具鉴赏、饮茶习俗"},
            {"id": "craft", "name": "传统手工艺专家", "description": "精通广绣、广彩、雕刻等传统技艺"},
            {"id": "literature", "name": "诗词文学专家", "description": "精通古典诗词、岭南文学、文学鉴赏"},
            {"id": "tcm", "name": "中医药专家", "description": "精通中医理论、养生保健、食疗文化"}
        ]
    }

@app.post("/api/chat")
async def chat_api(request: Request):
    """聊天API接口"""
    data = await request.json()
    response = await handle_chat_message(data)
    return response



@app.post("/api/chat/stream")
async def chat_stream_api(request: Request):
    """流式聊天API接口"""
    data = await request.json()
    
    async def generate_stream():
        async for chunk in handle_chat_message_stream(data):
            yield f"data: {json.dumps({'content': chunk, 'type': 'chunk'}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/plain; charset=utf-8"
        }
    )

@app.post("/api/collaboration/stream")
async def collaboration_stream_api(request: Request):
    """协作讨论流式API接口 - 重新设计为协同讨论模式"""
    data = await request.json()
    message = data.get("message", "")
    
    async def generate_stream():
        try:
            # 第一步：广府文化助手先回应并主持讨论
            yield f"data: {json.dumps({'type': 'expert_start', 'expert': '广府文化助手'}, ensure_ascii=False)}\n\n"
            
            async for chunk in guangfu_ambassador.initial_response_stream(message):
                if chunk and chunk.strip():
                    yield f"data: {json.dumps({'content': chunk, 'type': 'chunk', 'expert': '广府文化助手'}, ensure_ascii=False)}\n\n"
            
            yield f"data: {json.dumps({'type': 'expert_done', 'expert': '广府文化助手'}, ensure_ascii=False)}\n\n"
            
            # 第二步：分析问题，确定需要邀请的专家
            relevant_experts = guangfu_ambassador.analyze_query_for_experts(message)
            
            # 专家名称映射
            expert_mapping = {
                'cantonese_opera': ('粤剧专家', cantonese_opera_expert),
                'architecture': ('建筑专家', architecture_expert),
                'culinary': ('美食专家', culinary_expert),
                'festival': ('节庆专家', festival_expert),
                'tea_culture': ('茶文化专家', tea_culture_expert),
                'craft': ('传统手工艺专家', craft_expert),
                'literature': ('诗词文学专家', literature_expert),
                'tcm': ('中医药专家', tcm_expert)
            }
            
            # 第三步：依次邀请相关专家回复
            expert_responses = {}
            for expert_key in relevant_experts:
                if expert_key in expert_mapping:
                    expert_name, expert_agent = expert_mapping[expert_key]
                    
                    # 添加一个短暂的间隔，模拟真实讨论
                    await asyncio.sleep(1)
                    
                    yield f"data: {json.dumps({'type': 'expert_start', 'expert': expert_name}, ensure_ascii=False)}\n\n"
                    
                    # 收集专家回复内容用于后续总结
                    response_parts = []
                    async for chunk in expert_agent.process_query_stream(message):
                        if chunk and chunk.strip():
                            response_parts.append(chunk)
                            yield f"data: {json.dumps({'content': chunk, 'type': 'chunk', 'expert': expert_name}, ensure_ascii=False)}\n\n"
                    
                    expert_responses[expert_name] = ''.join(response_parts)
                    yield f"data: {json.dumps({'type': 'expert_done', 'expert': expert_name}, ensure_ascii=False)}\n\n"
            
            # 第四步：如果有多个专家参与，广府文化助手进行智能总结
            if len(relevant_experts) > 1:
                await asyncio.sleep(1)
                yield f"data: {json.dumps({'type': 'expert_start', 'expert': '广府文化助手', 'is_summary': True}, ensure_ascii=False)}\n\n"
                
                # 构建专家讨论内容
                discussion_content = ""
                for expert_name, response in expert_responses.items():
                    discussion_content += f"\n\n**{expert_name}**：\n{response}"
                
                # 调用广府文化助手生成智能总结
                try:
                    summary = await guangfu_ambassador.generate_intelligent_summary(
                        prompt="请为这次专家讨论生成深度总结",
                        user_message=message,
                        discussion_content=discussion_content
                    )
                    
                    # 流式输出智能总结
                    for char in summary:
                        yield f"data: {json.dumps({'content': char, 'type': 'chunk', 'expert': '广府文化助手'}, ensure_ascii=False)}\n\n"
                        await asyncio.sleep(0.02)
                        
                except Exception as e:
                    logger.error(f"智能总结生成失败: {e}")
                    # 降级到简单总结
                    fallback_summary = f"刚才各位专家就「{message}」这个问题进行了精彩的讨论，让我来为大家做个总结。\n\n"
                    fallback_summary += "\n\n".join([f"**{name}**：{resp[:100]}..." for name, resp in expert_responses.items()])
                    for char in fallback_summary:
                        yield f"data: {json.dumps({'content': char, 'type': 'chunk', 'expert': '广府文化助手'}, ensure_ascii=False)}\n\n"
                        await asyncio.sleep(0.02)
                
                yield f"data: {json.dumps({'type': 'expert_done', 'expert': '广府文化助手'}, ensure_ascii=False)}\n\n"
            
            yield f"data: {json.dumps({'type': 'discussion_complete'}, ensure_ascii=False)}\n\n"
            
        except Exception as e:
            logger.error(f"Collaboration stream error: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'message': '抱歉，讨论过程中出现了问题'}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/plain; charset=utf-8"
        }
    )

@app.post("/api/collaboration/summary")
async def collaboration_summary_api(request: Request):
    """协作讨论智能总结API接口"""
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        user_message = data.get("user_message", "")
        discussion_content = data.get("discussion_content", [])
        
        # 使用广府文化助手生成智能总结
        summary = await guangfu_ambassador.generate_intelligent_summary(
            user_message, discussion_content, prompt
        )
        
        return {"summary": summary, "status": "success"}
        
    except Exception as e:
        logger.error(f"Collaboration summary error: {str(e)}")
        return {"error": "生成总结失败", "status": "error"}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    
    uvicorn.run(app, host="0.0.0.0", port=args.port)
