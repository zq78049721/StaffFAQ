"""
测试问题分类器
"""

from core.question_classifier import QuestionClassifier

def test_classifier():
    """测试分类器"""
    
    classifier = QuestionClassifier()
    
    # 测试问题列表
    test_questions = [
        ("我工作了 10 年，年假有多少天？", "annual_leave"),
        ("加班费怎么算？", "overtime"),
        ("女职工产假多少天？", "maternity"),
        ("试用期工资怎么发？", "probation"),
        ("今天迟到了会被扣钱吗？", "attendance"),
        ("交通补贴有多少？", "salary"),
        ("我想请病假需要什么手续？", "leave"),
        ("离职补偿金怎么算？", "termination"),
        ("公司交五险一金吗？", "insurance"),
        ("公司年终奖什么时候发？", "general"),  # 可能匹配到 salary
    ]
    
    print("=" * 80)
    print("问题分类器测试")
    print("=" * 80)
    
    correct = 0
    total = len(test_questions)
    
    for question, expected_category in test_questions:
        result = classifier.classify_with_confidence(question)
        actual_category = result['category']
        
        is_correct = actual_category == expected_category
        if is_correct:
            correct += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"\n{status} 问题：{question}")
        print(f"   期望分类：{expected_category}")
        print(f"   实际分类：{actual_category}")
        print(f"   置信度：{result['confidence']}")
        print(f"   匹配关键词：{result['matched_keywords']}")
    
    print(f"\n{'='*80}")
    print(f"测试结果：{correct}/{total} 正确（准确率：{correct/total*100:.1f}%）")
    print(f"{'='*80}")

if __name__ == "__main__":
    test_classifier()
