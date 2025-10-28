#!/usr/bin/env python3
"""
广府非遗文化多智能体协同平台使用示例
演示如何使用硅基流动API进行智能体对话
"""

import asyncio
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def example_cantonese_opera_chat():
    """粤剧专家示例"""
    print("🎭 粤剧专家对话示例")
    print("=" * 50)
    
    from agents.cantonese_opera_expert import CantoneseOperaExpert
    
    # 创建粤剧专家
    expert = CantoneseOperaExpert()
    
    # 示例对话
    questions = [
        "请介绍一下粤剧的历史发展",
        "粤剧有哪些著名的表演艺术家？",
        "粤剧的唱腔有什么特点？"
    ]
    
    for question in questions:
        print(f"\n❓ 用户: {question}")
        response = await expert.process_query(question)
        print(f"🎭 粤剧专家: {response}")
        print("-" * 30)

async def example_collaboration_chat():
    """协同讨论示例"""
    print("\n🤝 多智能体协同讨论示例")
    print("=" * 50)
    
    from agents.collaboration_manager import CollaborationManager
    
    # 创建协同管理器
    manager = CollaborationManager()
    
    # 复杂问题
    question = "广府文化有什么特色？请从多个角度分析"
    print(f"\n❓ 用户: {question}")
    
    # 启动协同讨论
    result = await manager.start_collaboration(question)
    
    if result.get('success'):
        print("✅ 协同讨论成功！")
        print(f"📊 参与专家: {', '.join(result.get('participants', []))}")
        print(f"💬 综合回答: {result.get('final_response', '')}")
    else:
        print(f"❌ 协同讨论失败: {result.get('error', '未知错误')}")

async def example_direct_api_call():
    """直接API调用示例"""
    print("\n🔗 硅基流动API直接调用示例")
    print("=" * 50)
    
    from core.llm_client import get_silicon_flow_client
    
    # 获取客户端
    client = get_silicon_flow_client()
    
    # 构建消息
    messages = [
        {
            "role": "system", 
            "content": "你是广府文化专家，请用专业而生动的方式介绍广府文化。"
        },
        {
            "role": "user", 
            "content": "请简单介绍一下广府文化的特色"
        }
    ]
    
    print("📡 发送请求到硅基流动API...")
    response = await client.chat_completion(messages)
    print(f"💬 API响应: {response}")

async def main():
    """主函数"""
    print("🎭 广府非遗文化多智能体协同平台 - 使用示例")
    print("=" * 60)
    
    # 检查API密钥
    api_key = os.getenv('SILICON_FLOW_API_KEY')
    if not api_key or api_key == 'your_silicon_flow_api_key_here':
        print("❌ 请先配置 SILICON_FLOW_API_KEY 环境变量")
        print("📝 在 .env 文件中添加: SILICON_FLOW_API_KEY=your_actual_api_key")
        return
    
    try:
        # 示例1: 粤剧专家对话
        await example_cantonese_opera_chat()
        
        # 示例2: 协同讨论
        await example_collaboration_chat()
        
        # 示例3: 直接API调用
        await example_direct_api_call()
        
        print("\n🎉 所有示例运行完成！")
        print("💡 提示: 运行 'python start.py --reload' 启动Web服务")
        
    except Exception as e:
        print(f"❌ 运行示例时出错: {str(e)}")
        print("💡 请检查API密钥和网络连接")

if __name__ == "__main__":
    asyncio.run(main())

