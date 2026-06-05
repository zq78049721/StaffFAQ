"""
查看 ChromaDB 向量库内容
以可读文字方式展示
"""

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

def view_chroma_db():
    """查看向量库内容"""
    
    persist_directory = "chroma_db"
    
    if not os.path.exists(persist_directory):
        print("❌ 向量库不存在，请先运行系统初始化文档")
        return
    
    print("=" * 80)
    print("ChromaDB 向量库内容查看器")
    print("=" * 80)
    
    # 加载嵌入模型
    print("\n正在加载嵌入模型...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # 加载向量库
    print("正在加载向量库...")
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    # 获取集合
    collection = db._collection
    
    # 获取所有文档
    results = collection.get()
    
    print(f"\n📊 统计信息：")
    print(f"   - 文档总数：{len(results['ids'])}")
    print(f"   - 向量维度：{len(results['embeddings'][0]) if results['embeddings'] else 0}")
    
    print(f"\n📄 文档内容（前 10 条）：")
    print("=" * 80)
    
    for i, (doc_id, document, metadata) in enumerate(
        zip(results['ids'][:10], results['documents'][:10], results['metadatas'][:10])
    ):
        print(f"\n【文档 {i+1}】")
        print(f"ID: {doc_id}")
        print(f"来源: {metadata.get('source', 'unknown')}")
        print(f"内容预览: {document[:200]}...")
        print("-" * 80)
    
    print(f"\n✅ 显示完成！")
    print(f" 提示：如需查看特定类别，可添加过滤条件")

if __name__ == "__main__":
    view_chroma_db()
