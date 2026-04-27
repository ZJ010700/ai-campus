"""
日志配置模块。

使用 loguru 配置结构化日志输出。
"""
import sys

from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    """配置日志系统。"""
    # 移除默认处理器
    logger.remove()

    # 控制台输出
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # 文件输出（按日期轮转）
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        level=settings.LOG_LEVEL,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        ),
        encoding="utf-8",
    )

    # 错误日志单独存储
    logger.add(
        "logs/error_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        level="ERROR",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}\n{exception}"
        ),
        encoding="utf-8",
    )


# 初始化日志
setup_logging()
