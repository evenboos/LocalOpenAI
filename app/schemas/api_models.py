from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any
from enum import Enum

# 定义模型角色枚举
class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

# 聊天消息模型
class ChatMessage(BaseModel):
    role: Role
    content: str
    name: Optional[str] = None

# 聊天完成请求模型
class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    max_tokens: Optional[int] = 2048
    stream: Optional[bool] = False
    n: Optional[int] = 1

# 聊天完成选择模型
class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = "stop"

# 使用量模型
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

# 聊天完成响应模型
class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage

# 文本完成请求模型
class CompletionRequest(BaseModel):
    model: str
    prompt: str
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    max_tokens: Optional[int] = 2048
    stream: Optional[bool] = False
    n: Optional[int] = 1

# 文本完成选择模型
class CompletionChoice(BaseModel):
    text: str
    index: int
    logprobs: Optional[Any] = None
    finish_reason: Optional[str] = "stop"

# 文本完成响应模型
class CompletionResponse(BaseModel):
    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: Usage

# 模型列表响应
class ModelData(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str

# 模型列表响应
class ModelListResponse(BaseModel):
    object: str = "list"
    data: List[ModelData]

# 错误响应模型
class ErrorResponse(BaseModel):
    error: Dict[str, Any]