"""
RAG 检索增强生成模块。

使用 ChromaDB 实现向量检索，为 AI 回答提供校园知识库支持。
"""
from typing import List, Optional

from app.utils.logger import logger


class RAGRetriever:
    """RAG 检索器。"""

    def __init__(self):
        self.collection = None
        self._initialized = False

    def _init_chroma(self) -> bool:
        """
        初始化 ChromaDB 连接。

        Returns:
            是否初始化成功
        """
        if self._initialized:
            return True

        try:
            import chromadb
            from app.core.config import settings

            client = chromadb.HttpClient(
                host=settings.CHROMADB_HOST,
                port=settings.CHROMADB_PORT,
            )
            self.collection = client.get_or_create_collection(
                name="campus_knowledge",
                metadata={"description": "校园知识库"},
            )
            self._initialized = True
            logger.info("ChromaDB 连接成功")
            return True
        except Exception as e:
            logger.warning(f"ChromaDB 连接失败: {e}，将使用模拟数据")
            self._initialized = False
            return False

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[dict] = None,
    ) -> List[dict]:
        """
        检索相关文档。

        Args:
            query: 查询文本
            top_k: 返回最相关的 k 个文档
            filter_dict: 元数据过滤条件

        Returns:
            相关文档列表
        """
        if not self._init_chroma():
            return self._get_mock_results(query, top_k)

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filter_dict,
            )

            documents = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    distance = results["distances"][0][i] if results["distances"] else 0
                    documents.append({
                        "content": doc,
                        "metadata": metadata,
                        "score": 1 - distance,  # 转换为相似度分数
                    })

            return documents
        except Exception as e:
            logger.error(f"RAG 检索失败: {e}")
            return self._get_mock_results(query, top_k)

    async def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
    ) -> bool:
        """
        添加文档到知识库。

        Args:
            documents: 文档内容列表
            metadatas: 元数据列表
            ids: 文档ID列表

        Returns:
            是否添加成功
        """
        if not self._init_chroma():
            logger.warning("ChromaDB 未连接，无法添加文档")
            return False

        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
            )
            logger.info(f"成功添加 {len(documents)} 个文档到知识库")
            return True
        except Exception as e:
            logger.error(f"添加文档失败: {e}")
            return False

    def _get_mock_results(self, query: str, top_k: int) -> List[dict]:
        """
        获取模拟检索结果（当 ChromaDB 不可用时使用）。

        Args:
            query: 查询文本
            top_k: 返回数量

        Returns:
            模拟的检索结果
        """
        mock_knowledge = [
            {
                "content": "学校图书馆开放时间为周一至周日 7:00-22:30，考试周延长至23:00。借阅规则：本科生最多借10本，借期30天，可续借1次。",
                "metadata": {"source": "图书馆", "category": "daily"},
                "score": 0.85,
            },
            {
                "content": "校园网络使用指南：连接校园WiFi（Campus-WiFi），使用学号和密码登录。每个学生每月免费流量50GB，超出后限速。",
                "metadata": {"source": "信息中心", "category": "campus"},
                "score": 0.80,
            },
            {
                "content": "选课系统开放时间：每学期第16周开始预选，第17周公布结果，第18周补退选。每人每学期最多选25学分。",
                "metadata": {"source": "教务处", "category": "academic"},
                "score": 0.78,
            },
            {
                "content": "心理咨询中心位于学生活动中心3楼，提供免费心理咨询服务。预约电话：010-12345678，服务时间：周一至周五 8:30-17:00。",
                "metadata": {"source": "学生处", "category": "mental_health"},
                "score": 0.75,
            },
            {
                "content": "校园报修流程：1. 通过AI助手或后勤服务平台提交报修申请 2. 后勤部门接收并安排维修 3. 维修完成后反馈结果。紧急报修电话：010-87654321。",
                "metadata": {"source": "后勤处", "category": "daily"},
                "score": 0.72,
            },
        ]

        # 简单的关键词匹配排序
        query_lower = query.lower()
        scored_results = []
        for item in mock_knowledge:
            content_lower = item["content"].lower()
            # 计算匹配度
            match_count = sum(1 for char in query_lower if char in content_lower)
            adjusted_score = item["score"] + match_count * 0.01
            scored_results.append({**item, "score": min(adjusted_score, 1.0)})

        # 按分数排序
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]


# 全局 RAG 检索器实例
rag_retriever = RAGRetriever()
