"""
测试数据模型
TestCase 和 TestResult 类定义
"""

from typing import Dict, List, Optional


class TestCase:
    """测试用例"""
    
    def __init__(self, 
                 question: str,
                 expected_categories: List[str],
                 expected_prompt: Optional[str] = None,
                 must_contain: Optional[List[str]] = None,
                 must_not_contain: Optional[List[str]] = None,
                 description: str = ""):
        """
        初始化测试用例
        
        Args:
            question: 用户问题
            expected_categories: 期望的分类结果列表
            expected_prompt: 期望加载的提示词文件名（如 "annual_leave.yaml"）
            must_contain: 回答中必须包含的关键词列表
            must_not_contain: 回答中不能包含的关键词列表
            description: 测试用例描述
        """
        self.question = question
        self.expected_categories = expected_categories
        self.expected_prompt = expected_prompt
        self.must_contain = must_contain or []
        self.must_not_contain = must_not_contain or []
        self.description = description
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "question": self.question,
            "expected_categories": self.expected_categories,
            "expected_prompt": self.expected_prompt,
            "must_contain": self.must_contain,
            "must_not_contain": self.must_not_contain,
            "description": self.description
        }


class TestResult:
    """测试结果"""
    
    def __init__(self, test_case: TestCase):
        self.test_case = test_case
        self.actual_categories = []
        self.actual_prompt = ""
        self.actual_answer = ""
        self.passed_checks = []
        self.failed_checks = []
        self.is_passed = False
        self.duration = 0.0
        self.error = ""
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "question": self.test_case.question,
            "description": self.test_case.description,
            "expected_categories": self.test_case.expected_categories,
            "actual_categories": self.actual_categories,
            "expected_prompt": self.test_case.expected_prompt,
            "actual_prompt": self.actual_prompt,
            "must_contain": self.test_case.must_contain,
            "must_not_contain": self.test_case.must_not_contain,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "is_passed": self.is_passed,
            "duration": round(self.duration, 2),
            "error": self.error,
            "answer_preview": self.actual_answer[:200] if self.actual_answer else ""
        }
