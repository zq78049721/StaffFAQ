"""
测试用例集合 - 加班相关
"""

from typing import List
from test.models import TestCase


def get_overtime_tests() -> List[TestCase]:
    """获取加班相关的测试用例"""
    return [
        TestCase(
            question="周末加班工资怎么算？",
            expected_categories=["overtime"],
            expected_prompt="overtime.yaml",
            must_contain=["2倍"],
            description="测试周末加班费计算"
        ),
        TestCase(
            question="工作日晚上加班有加班费吗？",
            expected_categories=["overtime"],
            expected_prompt="overtime.yaml",
            must_contain=["1.5倍"],
            description="测试工作日延时加班费"
        ),
        TestCase(
            question="法定节假日加班工资是多少？",
            expected_categories=["overtime"],
            expected_prompt="overtime.yaml",
            must_contain=["3倍"],
            description="测试法定节假日加班费"
        ),
        TestCase(
            question="加班可以调休吗？",
            expected_categories=["overtime"],
            expected_prompt="overtime.yaml",
            description="测试加班调休政策"
        ),
    ]
