#!/bin/bash

echo "🎭 广府非遗文化多智能体协同平台"
echo "================================================"

# 检查Python环境
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi

# 检查依赖包
echo "检查依赖包..."
python3 -c "import fastapi, langchain, langgraph" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  正在安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖包安装失败"
        exit 1
    fi
fi

# 创建必要目录
echo "创建必要目录..."
mkdir -p logs
mkdir -p data/chroma_db

# 启动服务
echo "启动服务..."
echo "📍 服务地址: http://localhost:8000"
echo "🔧 按 Ctrl+C 停止服务"
echo ""

python3 start.py --host 0.0.0.0 --port 8000 --reload
