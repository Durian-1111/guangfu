"""
硅基流动API客户端
用于与硅基流动的大语言模型API进行交互
"""

import requests
import json
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SiliconFlowClient:
    """硅基流动API客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.siliconflow.cn/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.chat_url = f"{base_url}/chat/completions"
        
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "Qwen/QwQ-32B",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        stream: bool = False
    ):
        """发送聊天完成请求"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.chat_url, 
                    json=payload, 
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        if stream:
                            # 流式响应处理
                            buffer = ""
                            async for chunk in response.content.iter_chunked(1024):
                                buffer += chunk.decode('utf-8')
                                lines = buffer.split('\n')
                                buffer = lines[-1]  # 保留最后一行（可能不完整）
                                
                                for line in lines[:-1]:
                                    line = line.strip()
                                    if line.startswith('data: '):
                                        data = line[6:]  # 移除 'data: ' 前缀
                                        if data == '[DONE]':
                                            return
                                        try:
                                            chunk_data = json.loads(data)
                                            if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                                delta = chunk_data['choices'][0].get('delta', {})
                                                if 'content' in delta and delta['content'] is not None:
                                                    yield delta['content']
                                        except json.JSONDecodeError:
                                            continue
                        else:
                            # 非流式响应处理
                            result = await response.json()
                            yield result["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        logger.error(f"API请求失败: {response.status}, {error_text}")
                        if stream:
                            yield "抱歉，AI服务暂时不可用，请稍后再试。"
                        else:
                            yield "抱歉，AI服务暂时不可用，请稍后再试。"
                        
        except asyncio.TimeoutError:
            logger.error("API请求超时")
            if stream:
                yield "抱歉，请求超时，请稍后再试。"
            else:
                yield "抱歉，请求超时，请稍后再试。"
        except Exception as e:
            logger.error(f"API请求异常: {str(e)}")
            if stream:
                yield "抱歉，服务出现异常，请稍后再试。"
            else:
                yield "抱歉，服务出现异常，请稍后再试。"
    
    def chat_completion_sync(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "Qwen/QwQ-32B",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """同步版本的聊天完成请求"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.chat_url, 
                json=payload, 
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"API请求失败: {response.status_code}, {response.text}")
                return "抱歉，AI服务暂时不可用，请稍后再试。"
                
        except requests.exceptions.Timeout:
            logger.error("API请求超时")
            return "抱歉，请求超时，请稍后再试。"
        except Exception as e:
            logger.error(f"API请求异常: {str(e)}")
            return "抱歉，服务出现异常，请稍后再试。"
    
    async def stream_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "Qwen/QwQ-32B",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """流式聊天完成请求"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.chat_url, 
                    json=payload, 
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                line = line.decode('utf-8')
                                if line.startswith('data: '):
                                    data = line[6:].strip()
                                    if data == '[DONE]':
                                        break
                                    try:
                                        chunk = json.loads(data)
                                        if 'choices' in chunk and len(chunk['choices']) > 0:
                                            delta = chunk['choices'][0].get('delta', {})
                                            if 'content' in delta:
                                                yield delta['content']
                                    except json.JSONDecodeError:
                                        continue
                    else:
                        error_text = await response.text()
                        logger.error(f"流式API请求失败: {response.status}, {error_text}")
                        yield "抱歉，AI服务暂时不可用，请稍后再试。"
                        
        except Exception as e:
            logger.error(f"流式API请求异常: {str(e)}")
            yield "抱歉，服务出现异常，请稍后再试。"

# 全局客户端实例
_silicon_flow_client = None

def get_silicon_flow_client() -> SiliconFlowClient:
    """获取硅基流动客户端实例"""
    global _silicon_flow_client
    if _silicon_flow_client is None:
        from config import Config
        _silicon_flow_client = SiliconFlowClient(
            api_key=Config.SILICON_FLOW_API_KEY,
            base_url=Config.SILICON_FLOW_BASE_URL
        )
    return _silicon_flow_client

