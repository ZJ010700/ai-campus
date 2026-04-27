"""
AI+Campus 后端应用入口。

FastAPI 应用初始化、中间件配置、生命周期管理。
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine
from app.core.redis import redis_client
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """应用生命周期管理：启动和关闭时的资源初始化与清理。"""
    logger.info(f"🚀 {settings.APP_NAME} 正在启动...")
    logger.info(f"   环境: {settings.APP_ENV}")
    logger.info(f"   调试模式: {settings.DEBUG}")

    try:
        await redis_client.init()
        logger.info("   Redis 连接成功")
    except Exception as e:
        logger.warning(f"   Redis 连接失败: {e}")

    if settings.is_development:
        try:
            async with engine.begin() as conn:
                from app.core.database import Base
                await conn.run_sync(Base.metadata.create_all)
            logger.info("   数据库表初始化完成")
        except Exception as e:
            logger.warning(f"   数据库表初始化失败: {e}")

    logger.info(f"✅ {settings.APP_NAME} 启动完成，监听 {settings.HOST}:{settings.PORT}")

    yield

    logger.info(f"⏳ {settings.APP_NAME} 正在关闭...")

    try:
        await redis_client.close()
        logger.info("   Redis 连接已关闭")
    except Exception as e:
        logger.warning(f"   关闭 Redis 失败: {e}")

    try:
        await engine.dispose()
        logger.info("   数据库引擎已关闭")
    except Exception as e:
        logger.warning(f"   关闭数据库引擎失败: {e}")

    logger.info(f"👋 {settings.APP_NAME} 已关闭")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI+Campus 智慧校园助手后端 API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    logger.warning(f"请求参数验证失败: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": "请求参数验证失败", "detail": errors},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": "服务器内部错误，请稍后重试"},
    )


from app.api.v1.router import api_router

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["系统"])
async def health_check() -> dict:
    return {"status": "healthy", "app": settings.APP_NAME, "version": "1.0.0"}


@app.get("/", tags=["系统"])
async def root() -> dict:
    return {"app": settings.APP_NAME, "version": "1.0.0", "docs": "/docs", "health": "/health"}
