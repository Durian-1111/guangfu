#!/usr/bin/env python3
"""
硅基流动API测试脚本
用于测试API连接和智能体功能
"""

import asyncio
import os
from dotenv import load_dotenv
from core.llm_client import SiliconFlowClient
from agents.cantonese_opera_expert import CantoneseOperaExpert

# 加载环境变量
load_dotenv()

async def test_silicon_flow_api():
    """测试硅基流动API连接"""
    print("🧪 测试硅基流动API连接...")
    
    # 获取API密钥
    api_key = os.getenv('SILICON_FLOW_API_KEY')
    if not api_key or api_key == 'your_silicon_flow_api_key_here':
        print("❌ 请配置 SILICON_FLOW_API_KEY 环境变量")
        return False
    
    try:
        # 创建客户端
        client = SiliconFlowClient(api_key)
        
        # 测试简单对话
        messages = [
            {"role": "system", "content": "你是一个友好的AI助手"},
            {"role": "user", "content": "你好，请简单介绍一下自己"}
        ]
        
        print("📡 发送测试请求...")
        response_text = ""
        async for chunk in client.chat_completion(messages):
            response_text += chunk
        
        print("✅ API连接成功！")
        print(f"📝 响应内容: {response_text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ API连接失败: {str(e)}")
        return False

async def test_cantonese_opera_expert():
    """测试粤剧专家智能体"""
    print("\n🎭 测试粤剧专家智能体...")
    
    try:
        # 创建粤剧专家
        expert = CantoneseOperaExpert()
        
        # 测试问题
        test_questions = [
            "请介绍一下粤剧的历史",
            "粤剧有哪些经典剧目？",
            "粤剧的表演艺术有什么特点？"
        ]
        
        for question in test_questions:
            print(f"\n❓ 问题: {question}")
            response = await expert.process_query(question)
            print(f"💬 回答: {response[:200]}...")
            
        print("\n✅ 粤剧专家测试成功！")
        return True
        
    except Exception as e:
        print(f"❌ 粤剧专家测试失败: {str(e)}")
        return False

async def test_collaboration():
    """测试协同讨论功能"""
    print("\n🤝 测试协同讨论功能...")
    
    try:
        from agents.collaboration_manager import CollaborationManager
        
        # 创建协同管理器
        manager = CollaborationManager()
        
        # 测试协同问题
        question = "广府文化有什么特色？"
        print(f"❓ 协同问题: {question}")
        
        result = await manager.start_collaboration(question)
        
        if result.get('success'):
            print("✅ 协同讨论测试成功！")
            print(f"📊 参与专家: {result.get('participants', [])}")
            print(f"💬 综合回答: {result.get('final_response', '')[:200]}...")
            return True
        else:
            print(f"❌ 协同讨论失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 协同讨论测试失败: {str(e)}")
        return False

async def main():
    """主测试函数"""
    print("🎭 广府非遗文化多智能体协同平台 - API测试")
    print("=" * 60)
    
    # 测试API连接
    api_ok = await test_silicon_flow_api()
    
    if not api_ok:
        print("\n❌ API连接失败，请检查配置")
        return
    
    # 测试智能体
    expert_ok = await test_cantonese_opera_expert()
    
    # 测试协同功能
    collaboration_ok = await test_collaboration()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print(f"🔗 API连接: {'✅ 成功' if api_ok else '❌ 失败'}")
    print(f"🎭 智能体: {'✅ 成功' if expert_ok else '❌ 失败'}")
    print(f"🤝 协同讨论: {'✅ 成功' if collaboration_ok else '❌ 失败'}")
    
    if api_ok and expert_ok and collaboration_ok:
        print("\n🎉 所有测试通过！系统可以正常使用！")
        print("🚀 运行 'python start.py' 启动服务")
    else:
        print("\n⚠️  部分测试失败，请检查配置和网络连接")

if __name__ == "__main__":
    asyncio.run(main())
