"""
文档处理模块
负责加载、切分 TXT 文档
"""

import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentProcessor:
    """文档处理器 - 专注于 TXT 文件"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        初始化文档处理器
        
        Args:
            chunk_size: 每个文本块的大小
            chunk_overlap: 文本块之间的重叠大小
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " "]
        )
    
    def load_txt_file(self, file_path: str) -> Document:
        """
        加载单个 TXT 文件
        
        Args:
            file_path: TXT 文件路径
            
        Returns:
            Document 对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return Document(
            page_content=content,
            metadata={"source": os.path.basename(file_path)}
        )
    
    def load_directory(self, directory: str) -> List[Document]:
        """
        加载目录下所有 TXT 文件
        
        Args:
            directory: 目录路径
            
        Returns:
            Document 列表
        """
        documents = []
        
        if not os.path.exists(directory):
            print(f"警告：目录不存在 - {directory}")
            return documents
        
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory, filename)
                try:
                    doc = self.load_txt_file(file_path)
                    documents.append(doc)
                    print(f"✓ 加载：{filename}")
                except Exception as e:
                    print(f"✗ 加载失败 {filename}: {str(e)}")
        
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        切分文档
        
        Args:
            documents: 文档列表
            
        Returns:
            切分后的文档列表
        """
        return self.text_splitter.split_documents(documents)
    
    def process_directory(self, directory: str) -> List[Document]:
        """
        处理整个目录：加载 + 切分
        
        Args:
            directory: 目录路径
            
        Returns:
            切分后的文档列表
        """
        print(f"\n开始处理目录：{directory}")
        print("=" * 50)
        
        # 加载文档
        documents = self.load_directory(directory)
        
        if not documents:
            print("未找到任何 TXT 文件")
            return []
        
        print(f"\n共加载 {len(documents)} 个文件")
        
        # 切分文档
        print("正在切分文档...")
        splits = self.split_documents(documents)
        print(f"切分为 {len(splits)} 个文本块")
        print("=" * 50)
        
        return splits
