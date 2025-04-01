from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from .config import settings

# 定义API密钥头部
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    验证API密钥
    """
    if not api_key_header:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="未提供API密钥"
        )
        
    # 检查API密钥格式
    if not api_key_header.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="API密钥格式无效，应为'Bearer YOUR_API_KEY'"
        )
    
    # 提取实际的API密钥
    api_key = api_key_header.replace("Bearer ", "")
    
    # 验证API密钥
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="API密钥无效"
        )
        
    return api_key