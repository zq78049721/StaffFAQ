"""
测试 LLM 多标签分类器
"""

from core.question_classifier import QuestionClassifier
from core.llm_client import LLMClient
import os
from dotenv import load_dotenv

# 加载 .env 配置
load_dotenv()

def test_multi_label_classifier():
    """测试多标签分类器"""
    
    # 初始化 LLM 客户端
    provider = os.getenv("LLM_PROVIDER", "ollama")
    model = os.getenv("LLM_MODEL", "qwen2.5:1.5b")
    
    print(f"正在初始化 LLM 客户端（{provider}/{model}）...")
    try:
        llm_client = LLMClient(provider=provider, model=model)
    except Exception as e:
        print(f"❌ LLM 客户端初始化失败：{str(e)}")
        print("提示：请检查 .env 文件中的 API Key 配置")
        return
    
    # 初始化分类器
    classifier = QuestionClassifier(llm_client=llm_client)
    
    # 测试问题列表
    test_questions = [
        # 单标签问题
        ("我工作了 10 年，年假有多少天？", ["annual_leave"]),
        ("加班费怎么算？", ["overtime"]),
        ("女职工产假多少天？", ["maternity"]),
        
        # 多标签问题（重点测试）
        ("我的年假还剩下 3 天，我暂时不想用年假，我是否可以申请事假进行休息？", ["annual_leave", "leave"]),
        ("试用期加班有加班费吗？", ["probation", "overtime"]),
        ("怀孕后请病假，工资怎么算？", ["maternity", "leave", "salary"]),
        ("离职时年假没休完能折算成工资吗？", ["termination", "annual_leave", "salary"]),
        ("迟到扣工资合理吗？", ["attendance", "salary"]),
        
        # 复杂场景
        ("我怀孕 3 个月了，公司能辞退我吗？辞退的话有补偿吗？", ["maternity", "termination"]),
        ("试用期生病了能请病假吗？病假工资怎么算？", ["probation", "leave", "salary"]),
    ]
    
    print("\n" + "=" * 80)
    print("LLM 多标签分类器测试")
    print("=" * 80)
    
    correct_count = 0
    total_count = len(test_questions)
    
    for question, expected_categories in test_questions:
        print(f"\n【问题】{question}")
        print(f"【预期类别】{expected_categories}")
        
        # 调用分类器
        result_categories = classifier.classify(question, use_llm=True)
        
        print(f"【识别结果】{result_categories}")
        
        # 检查是否正确（允许部分匹配）
        matched = set(result_categories) & set(expected_categories)
        if matched:
            correct_count += 1
            print(f"【测试结果】✅ 正确（匹配到：{list(matched)}）")
        else:
            print(f"【测试结果】❌ 未匹配")
        
        print("-" * 80)
    
    # 统计结果
    print("\n" + "=" * 80)
    print(f"测试完成！准确率：{correct_count}/{total_count} ({correct_count/total_count*100:.1f}%)")
    print("=" * 80)

if __name__ == "__main__":
    test_multi_label_classifier()
