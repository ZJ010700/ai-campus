"""
AI 模块公共接口。
导出 AI 引擎、Agent 调度器、RAG 检索器等核心组件。
"""
from app.ai.agents import AgentDispatcher
from app.ai.engine import AIEngine
from app.ai.rag import RAGRetriever, rag_retriever
from app.ai.tools import TOOL_REGISTRY, execute_tool

__all__ = [
    "AIEngine",
    "AgentDispatcher",
    "RAGRetriever",
    "rag_retriever",
    "TOOL_REGISTRY",
    "execute_tool",
]
