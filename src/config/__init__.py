"""
配置管理模块
处理环境变量和密钥加载
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """配置类 - 从环境变量加载密钥"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # 加载 .env.local (不会提交到git的密钥文件)
        env_path = Path(__file__).parent.parent / ".env.local"
        load_dotenv(env_path)
        
        self._initialized = True
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """OpenAI API Key"""
        return os.getenv("OPENAI_API_KEY")
    
    @property
    def anthropic_api_key(self) -> Optional[str]:
        """Anthropic API Key"""
        return os.getenv("ANTHROPIC_API_KEY")
    
    @property
    def minimax_api_key(self) -> Optional[str]:
        """MiniMax API Key"""
        return os.getenv("MINIMAX_API_KEY")
    
    @property
    def default_provider(self) -> str:
        """默认AI提供商"""
        return os.getenv("AI_PROVIDER", "openai")
    
    @property
    def model_name(self) -> str:
        """默认模型"""
        return os.getenv("MODEL_NAME", "gpt-4")
    
    @property
    def max_tokens(self) -> int:
        """最大token数"""
        return int(os.getenv("MAX_TOKENS", "4000"))
    
    @property
    def temperature(self) -> float:
        """温度参数"""
        return float(os.getenv("TEMPERATURE", "0.7"))


# 全局配置实例
config = Config()
