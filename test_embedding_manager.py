"""
测试嵌入模型管理器
验证向量化的功能和维度
"""

from core.embedding_manager import EmbeddingManager

def test_embedding_manager():
    """测试嵌入模型管理器"""
    
    print("=" * 80)
    print("嵌入模型管理器测试")
    print("=" * 80)
    
    # 1. 初始化嵌入模型管理器
    print("\n【步骤 1】初始化嵌入模型管理器...")
    embedding_manager = EmbeddingManager(
        model_name="all-MiniLM-L6-v2",
        device="cpu"
    )
    
    # 2. 获取模型信息
    print("\n【步骤 2】获取模型信息...")
    model_info = embedding_manager.get_model_info()
    print(f"  模型名称: {model_info['model_name']}")
    print(f"  运行设备: {model_info['device']}")
    print(f"  向量维度: {model_info['dimension']}")
    print(f"  模型类型: {model_info['type']}")
    
    # 3. 测试单个文本向量化
    print("\n【步骤 3】测试单个文本向量化...")
    test_text = "工作满 10 年年假多少天？"
    vector = embedding_manager.embed_query(test_text)
    print(f"  原文: {test_text}")
    print(f"  向量长度: {len(vector)}")
    print(f"  向量前 5 维: {vector[:5]}")
    
    # 4. 测试多个文档向量化
    print("\n【步骤 4】测试多个文档向量化...")
    test_texts = [
        "年假规定：工作满 1 年可享受 5 天年假",
        "加班费计算：工作日加班 1.5 倍工资",
        "产假规定：女职工享受 98 天产假"
    ]
    vectors = embedding_manager.embed_documents(test_texts)
    print(f"  文档数量: {len(test_texts)}")
    print(f"  向量数量: {len(vectors)}")
    for i, (text, vec) in enumerate(zip(test_texts, vectors), 1):
        print(f"  文档 {i}: {text[:30]}... -> 维度 {len(vec)}")
    
    # 5. 计算相似度
    print("\n【步骤 5】测试语义相似度...")
    import numpy as np
    
    text1 = "工作满 10 年年假多少天？"
    text2 = "工作 10 年了，可以休几天年假？"
    text3 = "加班费怎么算？"
    
    vec1 = embedding_manager.embed_query(text1)
    vec2 = embedding_manager.embed_query(text2)
    vec3 = embedding_manager.embed_query(text3)
    
    def cosine_similarity(v1, v2):
        v1 = np.array(v1)
        v2 = np.array(v2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    sim_12 = cosine_similarity(vec1, vec2)
    sim_13 = cosine_similarity(vec1, vec3)
    
    print(f"  问题 1: {text1}")
    print(f"  问题 2: {text2}")
    print(f"  相似度: {sim_12:.4f} (应该很高，因为是同义问题)")
    print()
    print(f"  问题 1: {text1}")
    print(f"  问题 3: {text3}")
    print(f"  相似度: {sim_13:.4f} (应该较低，因为是不同主题)")
    
    print("\n" + "=" * 80)
    print("✅ 测试完成！")
    print("=" * 80)
    
    print("\n📊 总结：")
    print(f"- 模型加载成功: ✅")
    print(f"- 向量维度: {model_info['dimension']} 维")
    print(f"- 同义问题相似度: {sim_12:.4f}")
    print(f"- 异义问题相似度: {sim_13:.4f}")
    
    if sim_12 > 0.8 and sim_13 < 0.5:
        print("- 语义理解能力: ✅ 优秀")
    else:
        print("- 语义理解能力: ⚠️ 需要优化")


if __name__ == "__main__":
    test_embedding_manager()
