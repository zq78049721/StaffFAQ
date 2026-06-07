"""
测试按类别加载提示词
"""

from core.prompt_manager import PromptManager

def test_category_prompts():
    """测试类别专属提示词"""
    
    print("=" * 80)
    print("测试按类别加载提示词")
    print("=" * 80)
    
    # 初始化提示词管理器
    prompt_manager = PromptManager(module_name="hr")
    
    # 列出所有可用的提示词
    print(f"\n可用的提示词版本：{prompt_manager.list_versions()}")
    
    # 测试不同类别的提示词
    test_cases = [
        {
            "category": "annual_leave",
            "question": "工作满 10 年年假多少天？",
            "context": "职工累计工作已满 1 年不满 10 年的，年休假 5 天；已满 10 年不满 20 年的，年休假 10 天。"
        },
        {
            "category": "overtime",
            "question": "加班费怎么算？",
            "context": "工作日加班支付 1.5 倍工资，周末加班支付 2 倍工资，法定节假日加班支付 3 倍工资。"
        },
        {
            "category": "maternity",
            "question": "产假多少天？",
            "context": "女职工生育享受 98 天产假，其中产前可以休假 15 天。"
        },
        {
            "category": None,  # 通用问题，使用默认提示词
            "question": "公司有哪些福利？",
            "context": "公司提供五险一金、年终奖、带薪年假等福利。"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"测试 {i}: {case['category'] or '通用'}")
        print(f"{'=' * 80}")
        
        prompt = prompt_manager.build_prompt(
            version="free",
            question=case["question"],
            context=case["context"],
            category=case["category"]
        )
        
        print(f"\n生成的提示词（前 500 字符）：")
        print(prompt[:500])
        print("...")
    
    print("\n" + "=" * 80)
    print("✅ 测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    test_category_prompts()
