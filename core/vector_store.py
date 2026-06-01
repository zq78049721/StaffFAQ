"""
向量存储模块
负责文档的向量化和存储
"""

import os
import warnings
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# 忽略警告信息
warnings.filterwarnings('ignore')


class VectorStore:
    """向量存储管理器"""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        初始化向量存储
        
        Args:
            persist_directory: 持久化目录
        """
        self.persist_directory = persist_directory
        
        # 使用 Ollama 的嵌入模型（不需要从 Hugging Face 下载）
        print("正在加载嵌入模型...")
        self.embeddings = OllamaEmbeddings(
            model="qwen2.5:1.5b",
            base_url="http://localhost:11434"
        )
        print(" 嵌入模型加载成功")
        
        self.vector_store = None
    
    def create_from_documents(self, documents: List[Document]):
        """
        从文档创建向量存储
        
        Args:
            documents: 文档列表
        """
        print("\n正在创建向量存储...")
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
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
                embedding_function=self.embeddings
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
