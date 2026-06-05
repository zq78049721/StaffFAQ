"""
检查向量库内容
使用 ChromaDB 官方 API
"""

import chromadb
from chromadb.config import Settings

# 初始化客户端
client = chromadb.PersistentClient(path="chroma_db")

# 列出所有集合
collections = client.list_collections()
print(f"集合数量：{len(collections)}")

for col in collections:
    print(f"\n集合名称：{col.name}")
    print(f"文档数量：{col.count()}")
    
    # 获取前 5 条文档
    results = col.peek(5)
    
    print(f"\n前 5 条文档：")
    print("=" * 80)
    
    for i in range(min(5, len(results['documents']))):
        print(f"\n文档 {i+1}:")
        print(f"  内容：{results['documents'][i][:100]}...")
        print(f"  元数据：{results['metadatas'][i]}")
    
    # 检查是否有 category 字段
    all_docs = col.get()
    has_category = any('category' in (meta or {}) for meta in all_docs['metadatas'])
    
    print(f"\n{'=' * 80}")
    print(f"是否包含 category 字段：{has_category}")
    
    if not has_category:
        print("\n❌ 问题确认：文档没有 category 标签！")
        print("这就是为什么按分类检索找不到内容的原因。")
    else:
        print("\n✅ 文档已包含 category 标签")
        # 统计各类别数量
        from collections import Counter
        categories = [meta.get('category', 'unknown') for meta in all_docs['metadatas'] if meta]
        print(f"\n类别分布：")
        for cat, count in Counter(categories).most_common():
            print(f"  - {cat}: {count} 条")
