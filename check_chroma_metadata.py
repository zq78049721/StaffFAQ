"""
检查向量库中的文档元数据
"""

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 加载向量库
print("正在加载向量库...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

collection = db._collection

print(f"\n总文档数：{collection.count()}")

# 获取所有文档
docs = collection.get()

print(f"\n前 10 条文档的元数据：")
print("=" * 80)

for i, metadata in enumerate(docs['metadatas'][:10]):
    print(f"\n文档 {i+1}:")
    print(f"  内容预览：{docs['documents'][i][:100]}...")
    print(f"  元数据：{metadata}")

# 检查是否有 category 字段
has_category = any('category' in meta for meta in docs['metadatas'])
print(f"\n{'=' * 80}")
print(f"是否包含 category 字段：{has_category}")

if not has_category:
    print("\n❌ 问题确认：文档没有 category 标签！")
    print("这就是为什么按分类检索找不到内容的原因。")
else:
    print("\n✅ 文档已包含 category 标签")
