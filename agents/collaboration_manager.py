"""
多智能体协同管理器
基于LangGraph实现智能体之间的协同讨论和知识融合
"""

# 暂时注释掉LangGraph，使用简化的协同逻辑
# from langgraph.graph import StateGraph, END
from typing import Dict, List, Any, TypedDict
import asyncio
import json
from core.llm_client import get_silicon_flow_client
from config import Config

class CollaborationState(TypedDict):
    """协同状态定义"""
    user_query: str
    expert_responses: Dict[str, str]
    collaboration_summary: str
    final_response: str
    current_expert: str

class CollaborationManager:
    def __init__(self):
        self.name = "协同讨论管理器"
        self.experts = {}
        self.llm_client = get_silicon_flow_client()
        
        # 初始化专家智能体
        from .cantonese_opera_expert import CantoneseOperaExpert
        from .architecture_expert import ArchitectureExpert
        from .culinary_expert import CulinaryExpert
        from .festival_expert import FestivalExpert
        from .guangfu_ambassador import GuangfuAmbassador
        
        self.experts = {
            "cantonese_opera": CantoneseOperaExpert(),
            "architecture": ArchitectureExpert(),
            "culinary": CulinaryExpert(),
            "festival": FestivalExpert()
        }
        
        # 初始化广府文化助手
        self.ambassador = GuangfuAmbassador()
        
        # 构建协同工作流
        self.workflow = self._build_collaboration_workflow()
    
    def _build_collaboration_workflow(self):
        """构建协同工作流（简化版本）"""
        # 暂时返回None，使用简化的协同逻辑
        return None
    
    async def start_collaboration(self, user_query: str) -> Dict[str, Any]:
        """启动多智能体协同讨论（新的有序流程）"""
        try:
            # 第一步：广府文化助手欢迎并初步回应
            ambassador_initial = await self.ambassador.initial_response(user_query)
            
            # 第二步：大使分析并选择相关专家
            selected_experts = self.ambassador.analyze_query_for_experts(user_query)
            
            # 第三步：收集专家回应
            expert_responses = {}
            for expert_name in selected_experts:
                if expert_name in self.experts:
                    try:
                        response = await self.experts[expert_name].process_query(user_query)
                        expert_responses[expert_name] = response
                    except Exception as e:
                        expert_responses[expert_name] = f"{expert_name}暂时无法回应：{str(e)}"
            
            # 第四步：专家互动（如果有多个专家参与）
            expert_interactions = {}
            if len(expert_responses) > 1:
                for expert_name in selected_experts:
                    if expert_name in self.experts and hasattr(self.experts[expert_name], 'interact_with_other_experts'):
                        try:
                            interaction = await self.experts[expert_name].interact_with_other_experts(
                                user_query, expert_responses
                            )
                            if interaction:  # 只保存非空的互动回应
                                expert_interactions[expert_name] = interaction
                        except Exception as e:
                            pass  # 互动失败不影响主流程
            
            # 第五步：大使总结
            final_summary = await self.ambassador.summarize_expert_responses(
                user_query, expert_responses, expert_interactions
            )
            
            return {
                "success": True,
                "user_query": user_query,
                "ambassador_initial": ambassador_initial,
                "selected_experts": selected_experts,
                "expert_responses": expert_responses,
                "expert_interactions": expert_interactions,
                "final_summary": final_summary,
                "participants": ["ambassador"] + selected_experts
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_response": "抱歉，协同讨论过程中出现了技术问题，让我为您提供基础回答。"
            }
    
    async def _analyze_query(self, state: CollaborationState) -> CollaborationState:
        """分析用户查询"""
        query = state["user_query"]
        
        # 简单的查询分析
        analysis = {
            "cultural_domains": [],
            "complexity": "medium",
            "requires_collaboration": True
        }
        
        # 根据关键词判断涉及的文化领域
        if any(keyword in query for keyword in ["粤剧", "戏曲", "表演", "唱腔"]):
            analysis["cultural_domains"].append("cantonese_opera")
        
        if any(keyword in query for keyword in ["建筑", "骑楼", "园林", "民居"]):
            analysis["cultural_domains"].append("architecture")
        
        if any(keyword in query for keyword in ["美食", "菜系", "茶楼", "小吃"]):
            analysis["cultural_domains"].append("culinary")
        
        if any(keyword in query for keyword in ["节庆", "民俗", "传统", "庆典"]):
            analysis["cultural_domains"].append("festival")
        
        # 如果没有明确领域，则涉及所有领域
        if not analysis["cultural_domains"]:
            analysis["cultural_domains"] = ["cantonese_opera", "architecture", "culinary", "festival"]
        
        state["analysis"] = analysis
        return state
    
    async def _cantonese_opera_response(self, state: CollaborationState) -> CollaborationState:
        """粤剧专家回应"""
        try:
            response = await self.experts["cantonese_opera"].process_query(state["user_query"])
            state["expert_responses"]["cantonese_opera"] = response
            state["current_expert"] = "cantonese_opera"
        except Exception as e:
            state["expert_responses"]["cantonese_opera"] = f"粤剧专家暂时无法回应：{str(e)}"
        
        return state
    
    async def _architecture_response(self, state: CollaborationState) -> CollaborationState:
        """建筑专家回应"""
        try:
            response = await self.experts["architecture"].process_query(state["user_query"])
            state["expert_responses"]["architecture"] = response
            state["current_expert"] = "architecture"
        except Exception as e:
            state["expert_responses"]["architecture"] = f"建筑专家暂时无法回应：{str(e)}"
        
        return state
    
    async def _culinary_response(self, state: CollaborationState) -> CollaborationState:
        """美食专家回应"""
        try:
            response = await self.experts["culinary"].process_query(state["user_query"])
            state["expert_responses"]["culinary"] = response
            state["current_expert"] = "culinary"
        except Exception as e:
            state["expert_responses"]["culinary"] = f"美食专家暂时无法回应：{str(e)}"
        
        return state
    
    async def _festival_response(self, state: CollaborationState) -> CollaborationState:
        """节庆专家回应"""
        try:
            response = await self.experts["festival"].process_query(state["user_query"])
            state["expert_responses"]["festival"] = response
            state["current_expert"] = "festival"
        except Exception as e:
            state["expert_responses"]["festival"] = f"节庆专家暂时无法回应：{str(e)}"
        
        return state
    
    async def _synthesize_responses(self, state: CollaborationState) -> CollaborationState:
        """综合各专家回应"""
        expert_responses = state["expert_responses"]
        
        # 构建综合摘要
        summary_parts = []
        for expert, response in expert_responses.items():
            expert_name = {
                "cantonese_opera": "粤剧专家",
                "architecture": "建筑专家", 
                "culinary": "美食专家",
                "festival": "节庆专家"
            }.get(expert, expert)
            
            summary_parts.append(f"{expert_name}：{response[:200]}...")
        
        state["collaboration_summary"] = "\n\n".join(summary_parts)
        return state
    
    async def _generate_final_response(self, state: CollaborationState) -> CollaborationState:
        """生成最终回应"""
        try:
            # 构建综合消息
            messages = [
                {
                    "role": "system", 
                    "content": "你是广府非遗文化多智能体协同系统的综合分析师，负责整合各专家的观点，生成全面、连贯的文化解读。"
                },
                {
                    "role": "user",
                    "content": f"""基于以下专家回应，为用户问题生成一个综合性的回答：

用户问题：{state['user_query']}

专家回应：
{state['collaboration_summary']}

请生成一个综合性的回答，整合各专家的观点，形成一个完整、连贯的回应。"""
                }
            ]
            
            # 调用硅基流动API - 修复：正确处理异步生成器
            response_parts = []
            async for chunk in self.llm_client.chat_completion(
                messages=messages,
                model=Config.SILICON_FLOW_MODEL,
                temperature=0.7,
                max_tokens=2000
            ):
                response_parts.append(chunk)
            
            final_response = ''.join(response_parts)
            
            state["final_response"] = final_response
            
        except Exception as e:
            state["final_response"] = f"抱歉，在生成最终回应时遇到了技术问题。各专家回应如下：\n\n{state['collaboration_summary']}"
        
        return state
    
    async def _generate_simple_synthesis(self, user_query: str, expert_responses: Dict[str, str]) -> str:
        """生成简化的综合回应"""
        try:
            # 构建综合消息
            messages = [
                {
                    "role": "system", 
                    "content": "你是广府非遗文化多智能体协同系统的综合分析师，负责整合各专家的观点，生成全面、连贯的文化解读。"
                },
                {
                    "role": "user",
                    "content": f"""基于以下专家回应，为用户问题生成一个综合性的回答：

用户问题：{user_query}

专家回应：
{json.dumps(expert_responses, ensure_ascii=False, indent=2)}

请生成一个综合性的回答，整合各专家的观点，形成一个完整、连贯的回应。"""
                }
            ]
            
            # 调用硅基流动API - 修复：正确处理异步生成器
            response_parts = []
            async for chunk in self.llm_client.chat_completion(
                messages=messages,
                model=Config.SILICON_FLOW_MODEL,
                temperature=0.7,
                max_tokens=2000
            ):
                response_parts.append(chunk)
            
            final_response = ''.join(response_parts)
            
            return final_response
            
        except Exception as e:
            # 如果综合失败，返回简单的专家回应汇总
            summary_parts = []
            for expert_name, response in expert_responses.items():
                expert_display_name = {
                    'cantonese_opera': '粤剧专家',
                    'architecture': '建筑专家',
                    'culinary': '美食专家',
                    'festival': '节庆专家'
                }.get(expert_name, expert_name)
                summary_parts.append(f"{expert_display_name}：{response[:200]}...")
            
            return f"综合各专家观点：\n\n" + "\n\n".join(summary_parts)
    
    async def process_query_stream(self, query: str):
        """处理单个查询（流式版本）- 新的有序流程"""
        try:
            # 第一步：广府文化助手欢迎并初步回应
            yield "🎭 **广府文化助手**：\n"
            async for chunk in self.ambassador.initial_response_stream(query):
                yield chunk
            yield "\n\n"
            
            # 第二步：大使分析并选择相关专家
            selected_experts = self.ambassador.analyze_query_for_experts(query)
            
            # 第三步：收集专家回应
            expert_responses = {}
            for expert_name in selected_experts:
                if expert_name in self.experts:
                    expert_display_name = {
                        'cantonese_opera': '🎭 **粤剧专家梅韵师傅**',
                        'architecture': '🏛️ **建筑专家石匠老师**',
                        'culinary': '🍜 **美食专家味师傅**',
                        'festival': '🎊 **节庆专家庆典老师**'
                    }.get(expert_name, expert_name)
                    
                    yield f"{expert_display_name}：\n"
                    
                    try:
                        full_response = ""
                        async for chunk in self.experts[expert_name].process_query_stream(query):
                            if chunk is not None:  # 确保chunk不为None
                                full_response += chunk
                                yield chunk
                        expert_responses[expert_name] = full_response
                        yield "\n\n"
                    except Exception as e:
                        error_msg = f"{expert_name}暂时无法回应：{str(e)}"
                        expert_responses[expert_name] = error_msg
                        yield error_msg + "\n\n"
            
            # 第四步：专家互动（如果有多个专家参与）
            if len(expert_responses) > 1:
                yield "💬 **专家互动讨论**：\n\n"
                
                for expert_name in selected_experts:
                    if expert_name in self.experts and hasattr(self.experts[expert_name], 'interact_with_other_experts_stream'):
                        expert_display_name = {
                            'cantonese_opera': '🎭 **梅韵师傅补充**',
                            'architecture': '🏛️ **石匠老师补充**',
                            'culinary': '🍜 **味师傅补充**',
                            'festival': '🎊 **庆典老师补充**'
                        }.get(expert_name, expert_name)
                        
                        try:
                            has_interaction = False
                            yield f"{expert_display_name}：\n"
                            async for chunk in self.experts[expert_name].interact_with_other_experts_stream(
                                query, expert_responses
                            ):
                                if chunk:  # 只输出非空内容
                                    has_interaction = True
                                    yield chunk
                            
                            if has_interaction:
                                yield "\n\n"
                            else:
                                # 如果没有互动内容，回退一行
                                yield "\n"
                        except Exception as e:
                            pass  # 互动失败不影响主流程
            
            # 第五步：文化助手总结
            yield "🎯 **广府文化助手总结**：\n"
            async for chunk in self.ambassador.summarize_expert_responses_stream(
                query, expert_responses, {}
            ):
                yield chunk
                
        except Exception as e:
            yield f"抱歉，处理您的问题时遇到了技术问题：{str(e)}"

    async def process_query(self, query: str) -> str:
        """处理单个查询（简化版本）"""
        try:
            # 简单的查询处理
            if "协同" in query or "讨论" in query:
                return await self.start_collaboration(query)
            else:
                # 选择最相关的专家
                relevant_expert = self._select_relevant_expert(query)
                return await self.experts[relevant_expert].process_query(query)
        except Exception as e:
            return f"抱歉，处理您的问题时遇到了技术问题：{str(e)}"
    
    def _select_relevant_expert(self, query: str) -> str:
        """选择最相关的专家"""
        # 简单的关键词匹配
        if any(keyword in query for keyword in ["粤剧", "戏曲", "表演"]):
            return "cantonese_opera"
        elif any(keyword in query for keyword in ["建筑", "骑楼", "园林"]):
            return "architecture"
        elif any(keyword in query for keyword in ["美食", "菜系", "茶楼"]):
            return "culinary"
        elif any(keyword in query for keyword in ["节庆", "民俗", "传统"]):
            return "festival"
        else:
            return "cantonese_opera"  # 默认选择粤剧专家
