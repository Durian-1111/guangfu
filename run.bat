@echo off
chcp 65001 >nul
echo 🎭 广府非遗文化多智能体协同平台
echo ================================================

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)

echo 检查依赖包...
python -c "import fastapi, langchain, langgraph" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖包安装失败
        pause
        exit /b 1
    )
)

echo 创建必要目录...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "data\chroma_db" mkdir data\chroma_db

echo 启动服务...
echo 📍 服务地址: http://localhost:8000
echo 🔧 按 Ctrl+C 停止服务
echo.

python start.py --host 0.0.0.0 --port 8000 --reload

pause
