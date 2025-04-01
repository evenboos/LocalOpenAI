from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

from app.api.endpoints import router as api_router
from app.core.config import settings
from app.models.model_loader import model_loader

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加请求处理中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 添加全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": {"message": f"服务器内部错误: {str(exc)}", "type": "server_error"}},
    )

# 包含API路由
app.include_router(api_router, prefix="")

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}

# 预加载模型
@app.on_event("startup")
async def startup_event():
    logger.info("服务启动中，预加载模型...")
    model_loader.load_model()

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("服务关闭中...")