from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Settings(BaseSettings):
    # API配置
    API_KEY: str = os.getenv("API_KEY", "sk-your-api-key")
    
    # 模型配置
    MODEL_PATH: str = os.getenv("MODEL_PATH", "your-model-path")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "your-model-name")
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # 应用程序配置
    APP_NAME: str = "Local LLM API Server"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "使用FastAPI将本地大模型开放到公网，遵从OpenAI API格式"

# 创建全局设置对象
settings = Settings()