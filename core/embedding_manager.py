"""
嵌入模型管理器
负责加载和管理文本嵌入模型（将文本转换为向量）

职责：
- 加载嵌入模型（本地或远程）
- 提供文本向量化接口
- 支持模型切换和替换
"""

import os
from typing import List, Union


class EmbeddingManager:
    """嵌入模型管理器 - 专注于文本向量化"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):
        """
        初始化嵌入模型
        
        Args:
            model_name: 模型名称或本地路径
            device: 运行设备（cpu/cuda）
        """
        self.model_name = model_name
        self.device = device
        self.embeddings = None
        
        # 加载模型
        self._load_model()
    
    def _load_model(self):
        """加载嵌入模型"""
        from langchain_huggingface import HuggingFaceEmbeddings
        
        print("正在加载嵌入模型...")
        
        # 设置镜像加速下载
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
        
        # 优先使用本地模型（如果存在）
        local_model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "models", 
            self.model_name
        )
        
        if os.path.exists(local_model_path):
            print(f"  ✅ 检测到本地模型：{local_model_path}")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=local_model_path,
                model_kwargs={'device': self.device}
            )
            print("  ✅ 本地嵌入模型加载成功")
        else:
            print(f"  📥 正在从网络下载模型：{self.model_name}")
            try:
                self.embeddings = HuggingFaceEmbeddings(
                    model_name=f"sentence-transformers/{self.model_name}",
                    model_kwargs={'device': self.device}
                )
                print("  ✅ 嵌入模型下载成功")
            except Exception as e:
                print(f"  ⚠️ 模型下载失败：{str(e)}")
                print("  🔄 尝试使用备用模型...")
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="shibing624/paraphrase-multilingual-MiniLM-L12-v2",
                    model_kwargs={'device': self.device}
                )
                print("  ✅ 备用嵌入模型加载成功")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        将多个文档转换为向量
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表（每个向量是一个浮点数数组）
        """
        if not self.embeddings:
            raise Exception("嵌入模型未加载")
        
        return self.embeddings.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """
        将单个查询文本转换为向量
        
        Args:
            text: 查询文本
            
        Returns:
            向量（浮点数数组）
        """
        if not self.embeddings:
            raise Exception("嵌入模型未加载")
        
        return self.embeddings.embed_query(text)
    
    def get_dimension(self) -> int:
        """
        获取向量维度
        
        Returns:
            向量维度（如 384、768、1536 等）
        """
        if not self.embeddings:
            raise Exception("嵌入模型未加载")
        
        # 通过测试文本获取维度
        test_vector = self.embed_query("test")
        return len(test_vector)
    
    def get_model_info(self) -> dict:
        """
        获取模型信息
        
        Returns:
            包含模型信息的字典
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "dimension": self.get_dimension(),
            "type": "HuggingFace Embeddings"
        }
