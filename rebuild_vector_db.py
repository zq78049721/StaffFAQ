"""
重新处理文档并录入向量库
添加分类标签
"""

from core.document_processor import DocumentProcessor
from core.vector_store import VectorStore
from core.embedding_manager import EmbeddingManager
import os
import shutil

def rebuild_vector_db():
    """重建向量库"""
    
    print("=" * 80)
    print("重新处理文档并录入向量库")
    print("=" * 80)
    
    # 1. 检查并处理旧的向量库
    if os.path.exists("chroma_db"):
        print("\n⚠️ 检测到旧向量库，将直接覆盖")
        print("（如果报错，请先停止服务器再重试）")
    
    # 2. 初始化嵌入模型管理器
    print("\n正在初始化嵌入模型...")
    embedding_manager = EmbeddingManager(
        model_name="all-MiniLM-L6-v2",
        device="cpu"
    )
    
    # 3. 初始化文档处理器
    print("\n正在初始化文档处理器...")
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    
    # 4. 处理 data/hr 目录（公司政策）
    print("\n" + "=" * 80)
    print("处理公司政策文档：data/hr/")
    print("=" * 80)
    hr_docs = processor.process_directory("data/hr")
    print(f"✅ 公司政策文档处理完成，共 {len(hr_docs)} 个文本块")
    
    # 5. 处理 data/legal 目录（劳动法）
    print("\n" + "=" * 80)
    print("处理劳动法文档：data/legal/")
    print("=" * 80)
    if os.path.exists("data/legal"):
        legal_docs = processor.process_directory("data/legal")
        print(f"✅ 劳动法文档处理完成，共 {len(legal_docs)} 个文本块")
        all_docs = hr_docs + legal_docs
    else:
        print("⚠️ 未找到 data/legal 目录，只处理公司政策文档")
        all_docs = hr_docs
    
    # 6. 创建向量库
    print("\n" + "=" * 80)
    print("创建向量库...")
    print("=" * 80)
    vector_store = VectorStore(persist_directory="chroma_db")
    vector_store.create_from_documents(all_docs)
    
    print("\n" + "=" * 80)
    print("✅ 向量库重建完成！")
    print("=" * 80)
    print(f"\n总文档数：{len(all_docs)}")
    print("向量库位置：chroma_db/")
    print("\n现在可以重启服务器测试问答功能了！")

if __name__ == "__main__":
    rebuild_vector_db()
