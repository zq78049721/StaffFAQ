"""
检索器模块
负责从向量存储中检索相关文档
"""

from typing import List, Dict
from core.vector_store import VectorStore


class Retriever:
    """文档检索器"""
    
    def __init__(self, vector_store: VectorStore, top_k: int = 3):
        """
        初始化检索器
        
        Args:
            vector_store: 向量存储对象
            top_k: 返回的最相关文档数量
        """
        self.vector_store = vector_store
        self.top_k = top_k
    
    def search(self, query: str, category: str = None) -> List[Dict]:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            category: 分类标签（可选），如果提供则只检索该类别
            
        Returns:
            相关文档列表，包含内容和相似度分数
        """
        store = self.vector_store.get_vector_store()
        
        # 构建过滤条件
        where_filter = None
        if category and category != 'general':
            where_filter = {"category": category}
        
        # 相似度搜索
        results = store.similarity_search_with_score(
            query=query,
            k=self.top_k,
            filter=where_filter
        )
        
        # 格式化结果
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'content': doc.page_content,
                'source': doc.metadata.get('source', 'unknown'),
                'category': doc.metadata.get('category', 'general'),
                'score': score
            })
        
        return formatted_results
    
    def format_context(self, results: List[Dict]) -> str:
        """
        将检索结果格式化为上下文字符串
        
        Args:
            results: 检索结果列表
            
        Returns:
            格式化的上下文字符串
        """
        if not results:
            return "无相关文档"
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"【文档片段 {i}】（来源：{result['source']}）\n"
                f"{result['content']}\n"
            )
        
        return "\n".join(context_parts)
