"""
文档处理模块
负责加载、切分 TXT 文档，并自动添加分类标签
"""

import os
import re
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentProcessor:
    """文档处理器 - 专注于 TXT 文件，自动分类"""
    
    # 分类关键词映射（用于自动打标签）
    CATEGORY_KEYWORDS = {
        'overtime': ['加班', '延时工作', '超时工作', '1.5 倍', '2 倍', '3 倍'],
        'annual_leave': ['年假', '年休假', '带薪休假', '年休假'],
        'maternity': ['产假', '生育', '哺乳', '陪产', '怀孕', '流产'],
        'probation': ['试用期', '转正', '试用期考核'],
        'attendance': ['考勤', '迟到', '早退', '旷工', '打卡'],
        'salary': ['工资', '薪酬', '奖金', '补贴', '年终奖'],
        'leave': ['请假', '事假', '病假', '婚假', '丧假'],
        'termination': ['离职', '辞职', '辞退', '解除合同', '补偿金'],
        'insurance': ['社保', '公积金', '五险一金'],
    }
    
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
    
    def _detect_categories(self, content: str) -> List[str]:
        """
        根据内容自动检测类别
        
        Args:
            content: 文档内容
            
        Returns:
            类别标签列表
        """
        categories = set()
        content_lower = content.lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    categories.add(category)
                    break
        
        # 如果没有匹配到任何类别，标记为 general
        if not categories:
            categories.add('general')
        
        return list(categories)
    
    def load_txt_file(self, file_path: str) -> List[Document]:
        """
        加载单个 TXT 文件，并自动分类
        
        Args:
            file_path: TXT 文件路径
            
        Returns:
            Document 对象列表（一个文件可能对应多个类别）
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检测类别
        categories = self._detect_categories(content)
        
        print(f"  📄 {os.path.basename(file_path)} → 类别：{categories}")
        
        # 为每个类别创建一个 Document
        documents = []
        for category in categories:
            doc = Document(
                page_content=content,
                metadata={
                    "source": os.path.basename(file_path),
                    "category": category
                }
            )
            documents.append(doc)
        
        return documents
    
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
                    # load_txt_file 现在返回 List[Document]
                    file_docs = self.load_txt_file(file_path)
                    documents.extend(file_docs)
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
