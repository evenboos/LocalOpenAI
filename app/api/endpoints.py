import time
import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from app.core.security import get_api_key
from app.schemas.api_models import (
    ChatCompletionRequest, 
    ChatCompletionResponse, 
    ChatCompletionChoice, 
    ChatMessage,
    CompletionRequest,
    CompletionResponse,
    CompletionChoice,
    Usage,
    Role,
    ModelListResponse,
    ModelData,
    ErrorResponse
)
from app.models.model_loader import model_loader
from app.core.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由
router = APIRouter()

# 简单的token计数函数（实际应用中可能需要更复杂的实现）
def count_tokens(text):
    # 简单估算：每4个字符约为1个token
    return len(text) // 4

@router.post("/v1/chat/completions", response_model=ChatCompletionResponse, responses={403: {"model": ErrorResponse}})
async def create_chat_completion(request: ChatCompletionRequest, api_key: str = Depends(get_api_key)):
    """
    创建聊天完成 - 兼容OpenAI的chat/completions接口
    """
    try:
        # 构建提示
        prompt = ""
        for message in request.messages:
            if message.role == Role.SYSTEM:
                prompt += f"System: {message.content}\n"
            elif message.role == Role.USER:
                prompt += f"User: {message.content}\n"
            elif message.role == Role.ASSISTANT:
                prompt += f"Assistant: {message.content}\n"
        
        prompt += "Assistant: "
        
        # 生成回复
        response_text = model_loader.generate_text(
            prompt=prompt,
            max_length=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        
        # 检查是否有错误
        if isinstance(response_text, dict) and "error" in response_text:
            raise HTTPException(status_code=500, detail=response_text["error"])
        
        # 计算token
        prompt_tokens = count_tokens(prompt)
        completion_tokens = count_tokens(response_text)
        total_tokens = prompt_tokens + completion_tokens
        
        # 构建响应
        return ChatCompletionResponse(
            id=f"chatcmpl-{str(uuid.uuid4())}",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=ChatMessage(
                        role=Role.ASSISTANT,
                        content=response_text
                    ),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens
            )
        )
    except Exception as e:
        logger.error(f"聊天完成请求处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

@router.post("/v1/completions", response_model=CompletionResponse, responses={403: {"model": ErrorResponse}})
async def create_completion(request: CompletionRequest, api_key: str = Depends(get_api_key)):
    """
    创建文本完成 - 兼容OpenAI的completions接口
    """
    try:
        # 生成回复
        response_text = model_loader.generate_text(
            prompt=request.prompt,
            max_length=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        
        # 检查是否有错误
        if isinstance(response_text, dict) and "error" in response_text:
            raise HTTPException(status_code=500, detail=response_text["error"])
        
        # 计算token
        prompt_tokens = count_tokens(request.prompt)
        completion_tokens = count_tokens(response_text)
        total_tokens = prompt_tokens + completion_tokens
        
        # 构建响应
        return CompletionResponse(
            id=f"cmpl-{str(uuid.uuid4())}",
            created=int(time.time()),
            model=request.model,
            choices=[
                CompletionChoice(
                    text=response_text,
                    index=0,
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens
            )
        )
    except Exception as e:
        logger.error(f"文本完成请求处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

@router.get("/v1/models", response_model=ModelListResponse, responses={403: {"model": ErrorResponse}})
async def list_models(api_key: str = Depends(get_api_key)):
    """
    列出可用模型 - 兼容OpenAI的models接口
    """
    try:
        # 创建模型数据
        model_data = ModelData(
            id=settings.MODEL_NAME,
            created=int(time.time()),
            owned_by="local"
        )
        
        # 构建响应
        return ModelListResponse(
            data=[model_data]
        )
    except Exception as e:
        logger.error(f"获取模型列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")