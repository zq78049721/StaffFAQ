"""
LLM 客户端模块
支持云端模型（DeepSeek、智谱AI）和本地模型（Ollama）
"""

import os
from typing import Optional, Generator
try:
    from openai import OpenAI
except ImportError:
    pass


class LLMClient:
    """LLM 客户端 - 支持 DeepSeek、智谱AI 和 Ollama"""
    
    def __init__(self, provider: str = "ollama", api_key: Optional[str] = None, model: str = "qwen2.5:1.5b"):
        """
        初始化 LLM 客户端
        
        Args:
            provider: 提供商（"deepseek"、"zhipu" 或 "ollama"）
            api_key: API 密钥（云端模型需要）
            model: 模型名称
        """
        self.provider = provider
        self.model = model
        
        if provider == "deepseek":
            self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
            if not self.api_key:
                raise ValueError("未找到 API Key，请在 .env 文件中设置 DEEPSEEK_API_KEY")
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.deepseek.com"
                )
            except NameError:
                raise ImportError("请安装 openai 库: pip install openai")
            
        elif provider == "zhipu":
            self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
            if not self.api_key:
                raise ValueError("未找到 API Key，请在 .env 文件中设置 ZHIPU_API_KEY")
            try:
                from zhipuai import ZhipuAI
                self.client = ZhipuAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("请安装 zhipuai 库: pip install zhipuai")
            
        elif provider == "ollama":
            try:
                self.client = OpenAI(
                    base_url="http://localhost:11434/v1",
                    api_key="ollama"  # Ollama 不需要真实的 API Key
                )
            except NameError:
                raise ImportError("请安装 openai 库: pip install openai")
        else:
            raise ValueError(f"不支持的提供商: {provider}，请使用 'deepseek'、'zhipu' 或 'ollama'")
    
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """
        生成回答
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            
        Returns:
            生成的文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ LLM 调用失败：{str(e)}"
    
    def generate_stream(self, prompt: str, temperature: float = 0.7) -> Generator[str, None, None]:
        """
        流式生成回答
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            
        Yields:
            生成的文本片段
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"❌ LLM 调用失败：{str(e)}"
