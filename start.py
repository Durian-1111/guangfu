#!/usr/bin/env python3
"""
广府非遗文化多智能体协同平台启动脚本
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    try:
        import fastapi
        import langchain
        import langgraph
        print("✅ 核心依赖包已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_config():
    """检查配置文件"""
    config_file = Path(".env")
    if not config_file.exists():
        print("⚠️  配置文件 .env 不存在")
        print("请复制 .env.example 到 .env 并配置您的 OpenAI API Key")
        return False
    
    # 检查硅基流动 API Key
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'your_silicon_flow_api_key_here' in content:
            print("⚠️  请配置您的硅基流动 API Key")
            return False
    
    print("✅ 配置文件检查通过")
    return True

def create_directories():
    """创建必要的目录"""
    directories = ['logs', 'data', 'data/chroma_db']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ 目录结构创建完成")

def start_server(host="0.0.0.0", port=8000, reload=False):
    """启动服务器"""
    print(f"🚀 启动广府非遗文化多智能体协同平台...")
    print(f"📍 服务地址: http://{host}:{port}")
    print(f"🔧 调试模式: {'开启' if reload else '关闭'}")
    
    cmd = [
        "uvicorn", 
        "app:app", 
        "--host", host, 
        "--port", str(port)
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="广府非遗文化多智能体协同平台")
    parser.add_argument("--host", default="0.0.0.0", help="服务器地址")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口")
    parser.add_argument("--reload", action="store_true", help="启用热重载")
    parser.add_argument("--check", action="store_true", help="仅检查环境")
    parser.add_argument("--test", action="store_true", help="测试API连接")
    
    args = parser.parse_args()
    
    print("🎭 广府非遗文化多智能体协同平台")
    print("=" * 50)
    
    # 检查环境
    if not check_dependencies():
        sys.exit(1)
    
    if not check_config():
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    if args.check:
        print("✅ 环境检查完成")
        return
    
    if args.test:
        print("🧪 运行API测试...")
        import subprocess
        try:
            subprocess.run([sys.executable, "test_api.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ API测试失败")
            sys.exit(1)
        return
    
    # 启动服务
    start_server(args.host, args.port, args.reload)

if __name__ == "__main__":
    main()
