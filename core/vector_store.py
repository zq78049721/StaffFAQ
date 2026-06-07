"""
向量存储模块
负责文档的向量存储和检索（ChromaDB 管理）

职责：
- 创建和管理 ChromaDB 向量数据库
- 存储文档向量和元数据
- 提供向量库加载接口

注意：嵌入模型由 EmbeddingManager 统一管理
"""

import os
import warnings
from typing import List, Optional
from langchain_core.documents import Document
from langchain_chroma import Chroma
from core.embedding_manager import EmbeddingManager

# 忽略警告信息
warnings.filterwarnings('ignore')


class VectorStore:
    """向量存储管理器"""
    
    def __init__(self, persist_directory: str = "chroma_db", embedding_manager: Optional[EmbeddingManager] = None):
        """
        初始化向量存储
        
        Args:
            persist_directory: 持久化目录
            embedding_manager: 嵌入模型管理器（可选，如果不提供则自动创建）
        """
        self.persist_directory = persist_directory
        
        # 使用传入的嵌入模型管理器，或创建默认的
        if embedding_manager:
            self.embedding_manager = embedding_manager
        else:
            self.embedding_manager = EmbeddingManager(
                model_name="all-MiniLM-L6-v2",
                device="cpu"
            )
        
        self.vector_store = None
    
    def create_from_documents(self, documents: List[Document]):
        """
        从文档创建向量存储（覆盖旧数据）
        
        Args:
            documents: 文档列表
        """
        print("\n正在创建向量存储...")
        
        # 如果目录已存在，先删除（覆盖旧数据）
        if os.path.exists(self.persist_directory):
            try:
                import shutil
                shutil.rmtree(self.persist_directory)
                print("  已删除旧向量库")
            except Exception as e:
                print(f"  ⚠️ 无法删除旧向量库：{str(e)}")
                print("  将尝试直接覆盖...")
        
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_manager.embeddings,
            persist_directory=self.persist_directory
        )
        # Chroma.from_documents() 已自动持久化，无需手动调用 persist()
        print(f"✓ 向量存储已保存至：{self.persist_directory}")
    
    def load_existing(self) -> bool:
        """
        加载已有的向量存储
        
        Returns:
            是否加载成功
        """
        if os.path.exists(self.persist_directory):
            print(f"\n加载已有向量存储：{self.persist_directory}")
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_manager.embeddings
            )
            return True
        return False
    
    def get_vector_store(self):
        """
        获取向量存储对象
        
        Returns:
            Chroma 向量存储对象
        """
        if not self.vector_store:
            if not self.load_existing():
                raise Exception("向量存储不存在，请先处理文档")
        return self.vector_store
    
    def clear(self):
        """清空向量存储"""
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
            print(f"✓ 已清空向量存储：{self.persist_directory}")
        self.vector_store = None
