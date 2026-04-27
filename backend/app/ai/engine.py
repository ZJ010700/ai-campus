"""
AI 引擎核心模块。
基于 LangChain + 通义千问 (DashScope) 实现 LLM 对话、RAG 检索增强生成和流式响应。
"""
from typing import AsyncGenerator, List, Optional

from app.ai.agents import AgentDispatcher
from app.ai.prompts import MAIN_ROUTER_PROMPT
from app.ai.rag import rag_retriever
from app.ai.tools import TOOL_DESCRIPTIONS, execute_tool
from app.core.config import settings
from app.utils.logger import logger


class AIEngine:
    """AI 引擎核心类。"""

    def __init__(self):
        self._llm = None
        self._dispatcher = AgentDispatcher()

    def _get_llm(self):
        if self._llm is not None:
            return self._llm
        try:
            from langchain_openai import ChatOpenAI
            self._llm = ChatOpenAI(
                model=settings.DASHSCOPE_MODEL,
                api_key=settings.DASHSCOPE_API_KEY,
                base_url=settings.DASHSCOPE_BASE_URL,
                temperature=0.7,
                max_tokens=2048,
                streaming=True,
            )
            logger.info(f"LLM 初始化成功: {settings.DASHSCOPE_MODEL}")
            return self._llm
        except Exception as e:
            logger.error(f"LLM 初始化失败: {e}")
            return None

    def _build_messages(self, message, module_type, chat_history=None, context=None):
        messages = []
        system_prompt = MAIN_ROUTER_PROMPT
        if context:
            system_prompt += f"\n\n## 参考知识\n{context}"
        if module_type and module_type != "campus":
            system_prompt += f"\n\n## 当前模块\n用户当前处于【{module_type}】模块，请优先使用该模块的专业能力。"
        messages.append({"role": "system", "content": system_prompt})
        if chat_history:
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": message})
        return messages

    async def _retrieve_context(self, message, module_type):
        try:
            filter_dict = None
            if module_type and module_type != "campus":
                filter_dict = {"category": module_type}
            documents = await rag_retriever.retrieve(query=message, top_k=5, filter_dict=filter_dict)
            if documents:
                context_parts = []
                for doc in documents:
                    source = doc.get("metadata", {}).get("source", "未知来源")
                    context_parts.append(f"[{source}] {doc['content']}")
                return "\n".join(context_parts)
        except Exception as e:
            logger.warning(f"RAG 检索失败: {e}")
        return ""

    async def _call_llm(self, messages):
        llm = self._get_llm()
        if llm is None:
            return self._get_fallback_response()
        try:
            from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
            lc_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    lc_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    lc_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    lc_messages.append(AIMessage(content=msg["content"]))
            response = await llm.ainvoke(lc_messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            return self._get_fallback_response()

    async def chat(self, message, module_type="campus", chat_history=None):
        routing_result = await self._dispatcher.route(message, module_type)
        tool_context = ""
        if routing_result.get("tool_calls"):
            for tool_call in routing_result["tool_calls"]:
                tool_name = tool_call["name"]
                tool_args = tool_call.get("args", {})
                logger.info(f"调用工具: {tool_name}({tool_args})")
                tool_result = await execute_tool(tool_name, **tool_args)
                tool_context += f"\n工具 {tool_name} 返回结果：{tool_result}"
        rag_context = await self._retrieve_context(message, module_type)
        combined_context = ""
        if tool_context:
            combined_context += tool_context
        if rag_context:
            combined_context += f"\n{rag_context}"
        agent_prompt = routing_result.get("prompt_enhancement", "")
        messages = self._build_messages(message=message, module_type=module_type, chat_history=chat_history, context=combined_context or None)
        if agent_prompt:
            messages[-1]["content"] = f"{agent_prompt}\n\n用户消息：{message}"
        response = await self._call_llm(messages)
        return response

    async def chat_stream(self, message, module_type="campus", chat_history=None):
        routing_result = await self._dispatcher.route(message, module_type)
        tool_context = ""
        if routing_result.get("tool_calls"):
            for tool_call in routing_result["tool_calls"]:
                tool_name = tool_call["name"]
                tool_args = tool_call.get("args", {})
                logger.info(f"调用工具: {tool_name}({tool_args})")
                tool_result = await execute_tool(tool_name, **tool_args)
                tool_context += f"\n工具 {tool_name} 返回结果：{tool_result}"
        rag_context = await self._retrieve_context(message, module_type)
        combined_context = ""
        if tool_context:
            combined_context += tool_context
        if rag_context:
            combined_context += f"\n{rag_context}"
        agent_prompt = routing_result.get("prompt_enhancement", "")
        messages = self._build_messages(message=message, module_type=module_type, chat_history=chat_history, context=combined_context or None)
        if agent_prompt:
            messages[-1]["content"] = f"{agent_prompt}\n\n用户消息：{message}"
        llm = self._get_llm()
        if llm is None:
            yield self._get_fallback_response()
            return
        try:
            from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
            lc_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    lc_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    lc_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    lc_messages.append(AIMessage(content=msg["content"]))
            async for chunk in llm.astream(lc_messages):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            logger.error(f"LLM 流式调用失败: {e}")
            yield self._get_fallback_response()

    def _get_fallback_response(self):
        return "抱歉，AI 服务暂时不可用，请稍后再试。如果问题持续存在，请联系管理员。"
