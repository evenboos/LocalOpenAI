import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    # 启动FastAPI应用
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,  # 开发模式下启用热重载
        log_level="info"
    )