"""
配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    
    # 硅基流动配置
    SILICON_FLOW_API_KEY = os.getenv('SILICON_FLOW_API_KEY', 'sk-kdbwcxieklfjsmvwbogngriafpwaaigrsxpekmumgaabzbzx')
    SILICON_FLOW_BASE_URL = os.getenv('SILICON_FLOW_BASE_URL', 'https://api.siliconflow.cn/v1')
    SILICON_FLOW_MODEL = os.getenv('SILICON_FLOW_MODEL', 'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B')
    
    # 数据库配置
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./agent_system.db')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # 应用配置
    APP_NAME = os.getenv('APP_NAME', '广府非遗文化多智能体协同平台')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    
    # 向量数据库配置
    CHROMA_PERSIST_DIRECTORY = os.getenv('CHROMA_PERSIST_DIRECTORY', './data/chroma_db')
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/app.log')
    
    # 智能体配置
    AGENT_TEMPERATURE = 0.7
    MAX_TOKENS = 2000
    
    # WebSocket配置
    WS_HEARTBEAT_INTERVAL = 30
    WS_MAX_CONNECTIONS = 100
